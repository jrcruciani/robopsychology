"""Stdlib-only OpenTelemetry GenAI span extractor for 2.6 Tool-Trace Reconciliation.

Reads an OpenTelemetry JSON span export (OTLP/JSON or a flat list of span dicts)
and extracts a compact, deterministic runtime-artifact summary containing model
and tool invocations. Does not call any model or network service.

Strip secrets/PII from span attributes before sharing outside your environment.
"""

import argparse
import json
from pathlib import Path

GENAI_KEYS = (
    "gen_ai.operation.name",
    "gen_ai.system",
    "gen_ai.provider.name",
    "gen_ai.request.model",
    "gen_ai.response.model",
    "gen_ai.tool.name",
    "gen_ai.tool.call.id",
    "gen_ai.tool.call.arguments",
    "gen_ai.tool.call.result",
    "gen_ai.agent.name",
    "error.type",
)


def _flatten_otlp_attributes(attrs):
    """Support both plain dict attributes and OTLP [{key, value}] arrays."""
    if isinstance(attrs, dict):
        return dict(attrs)
    out = {}
    if isinstance(attrs, list):
        for item in attrs:
            key = item.get("key")
            val = item.get("value", {})
            if isinstance(val, dict):
                for typed_key in (
                    "stringValue",
                    "intValue",
                    "doubleValue",
                    "boolValue",
                ):
                    if typed_key in val:
                        out[key] = val[typed_key]
                        break
                else:
                    out[key] = val
            else:
                out[key] = val
    return out


def _iter_spans(data):
    """Yield raw span dicts from either OTLP resourceSpans JSON or a flat list."""
    if isinstance(data, list):
        for span in data:
            if isinstance(span, dict):
                yield span
        return
    if isinstance(data, dict):
        if "spans" in data and isinstance(data["spans"], list):
            yield from data["spans"]
            return
        for resource in data.get("resourceSpans", []):
            for scope in resource.get("scopeSpans", []):
                for span in scope.get("spans", []):
                    yield span


def extract_runtime_artifact(otel_payload, max_value_chars=400):
    """Return a compact runtime-artifact dict suitable for 2.6 or incident notes."""
    spans_out = []
    for index, span in enumerate(_iter_spans(otel_payload), start=1):
        attrs = _flatten_otlp_attributes(span.get("attributes", {}))
        selected = {}
        for key in GENAI_KEYS:
            if key in attrs:
                val = attrs[key]
                if isinstance(val, str) and len(val) > max_value_chars:
                    val = val[:max_value_chars] + "... [truncated]"
                selected[key] = val
        if not selected and not str(span.get("name", "")).startswith("gen_ai"):
            continue
        status = span.get("status", {})
        status_code = status.get("code") if isinstance(status, dict) else status
        spans_out.append(
            {
                "span_index": index,
                "span_id": span.get("spanId") or span.get("span_id") or f"span-{index}",
                "name": span.get("name", ""),
                "status": status_code,
                "attributes": selected,
            }
        )
    return {
        "artifact_type": "opentelemetry_genai_summary",
        "span_count": len(spans_out),
        "spans": spans_out,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Summarize OpenTelemetry GenAI spans for 2.6 Tool-Trace Reconciliation."
    )
    parser.add_argument("trace_file", nargs="?", help="Path to an OTel JSON export")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Print a fictional demo summary without reading an external file",
    )
    args = parser.parse_args(argv)

    if args.demo or not args.trace_file:
        demo_payload = [
            {
                "span_id": "demo-01",
                "name": "execute_tool pytest",
                "status": {"code": "ERROR"},
                "attributes": {
                    "gen_ai.operation.name": "execute_tool",
                    "gen_ai.tool.name": "terminal",
                    "gen_ai.tool.call.arguments": "pytest tests/test_auth.py",
                    "gen_ai.tool.call.result": "1 failed, 2 passed (exit_code=1)",
                    "error.type": "ToolNonZeroExit",
                },
            }
        ]
        print(json.dumps(extract_runtime_artifact(demo_payload), ensure_ascii=False, indent=2))
        return 0

    payload = json.loads(Path(args.trace_file).read_text(encoding="utf-8"))
    print(json.dumps(extract_runtime_artifact(payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

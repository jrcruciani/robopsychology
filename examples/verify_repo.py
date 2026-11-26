"""Lightweight zero-dependency integrity check for the Robopsychology repository.

Verifies catalog structure, prompt card coverage, flowchart references,
helper execution, allowlist metadata isolation, and YAML<->JSON parity (when
PyYAML is available). Never calls external APIs or writes inside the repo.
"""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from examples.black_box_checks import (
    allowlist_scenario_messages,
    attribution_messages,
    collect_samples,
    observer_messages,
    summarize,
)
from examples.diagnostic_prompt import diagnostic_messages, load_catalog, render_prompt
from examples.inspect_adapter import (
    build_planted_cause_specs,
    build_wording_comparison_specs,
)
from examples.otel_bridge import extract_runtime_artifact


def check_catalog_and_cards():
    catalog = load_catalog()
    prompts = catalog["prompts"]
    ids = [p["id"] for p in prompts]
    assert len(ids) == len(set(ids)), "Duplicate prompt IDs in prompts.json"
    assert catalog.get("claim_report_appendix"), "Missing shared claim_report_appendix"
    assert catalog.get("claim_report_json_schema"), "Missing claim_report_json_schema"

    base_ids = [pid for pid in ids if not pid.endswith("d")]
    cards_dir = ROOT / "prompts" / "cards"
    card_prefixes = {f.name.split("-", 1)[0] for f in cards_dir.glob("*.md")}
    missing_cards = sorted(set(base_ids) - card_prefixes)
    assert not missing_cards, f"Missing prompt cards for base IDs: {missing_cards}"

    # Verify every flowchart ID exists in the catalog
    id_set = set(ids)
    for obs in catalog["flowchart"]["observations"]:
        for pid in obs["path"]:
            assert pid in id_set, f"Flowchart observation {obs['id']} references unknown prompt {pid}"
    for seq_name in ("ratchet_sequence", "pure_ratchet_sequence"):
        for pid in catalog["flowchart"][seq_name]:
            assert pid in id_set, f"{seq_name} references unknown prompt {pid}"

    # Verify YAML <-> JSON parity when PyYAML is available
    yaml_status = "skipped (PyYAML not installed)"
    try:
        import yaml  # type: ignore

        yaml_data = yaml.safe_load((ROOT / "prompts" / "prompts.yaml").read_text(encoding="utf-8"))
        assert yaml_data == catalog, "prompts.yaml and prompts.json are out of sync"
        yaml_status = "verified (exact match)"
    except ImportError:
        pass

    return len(prompts), len(base_ids), yaml_status


def check_rendering_and_helpers():
    # Render quick, strict, and naturalistic modes
    q = render_prompt("1.1", mode="quick")
    s = render_prompt("1.1", mode="strict")
    n = render_prompt("1.1", mode="naturalistic")
    assert "Claim report" not in q, "Quick mode must omit claim_report_appendix"
    assert "Claim report" in s, "Strict mode must include claim_report_appendix"
    assert "second intention diagnosis" not in n.lower(), "Naturalistic mode should avoid clinical jargon"

    # Variable substitution
    p14 = render_prompt("1.4", mode="naturalistic", variables={"action": "write a filter regex"})
    assert "write a filter regex" in p14

    # Diagnostic messages with artifacts
    msgs = diagnostic_messages(
        request="Run tests",
        response="All passed",
        baseline="Report actual pytest exit code",
        prompt_id="2.6",
        mode="naturalistic",
        runtime_artifact={"span_count": 1},
    )
    assert len(msgs) == 3 and msgs[0]["role"] == "system"

    # OpenTelemetry bridge
    otel_summary = extract_runtime_artifact(
        {
            "resourceSpans": [
                {
                    "scopeSpans": [
                        {
                            "spans": [
                                {
                                    "spanId": "s1",
                                    "name": "gen_ai.execute_tool",
                                    "status": {"code": "ERROR"},
                                    "attributes": [
                                        {"key": "gen_ai.tool.name", "value": {"stringValue": "terminal"}},
                                        {"key": "error.type", "value": {"stringValue": "NonZeroExit"}},
                                    ],
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    )
    assert otel_summary["span_count"] == 1
    assert otel_summary["spans"][0]["attributes"]["gen_ai.tool.name"] == "terminal"

    # Collect & summarize in external temp directory (never inside repo)
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = Path(tmpdir) / "samples.jsonl"
        cases = [
            {
                "name": "control",
                "wording": "1.1",
                "wording_style": "naturalistic",
                "messages": [{"role": "user", "content": "hi"}],
            },
            {
                "name": "control",
                "wording": "1.1",
                "wording_style": "canonical",
                "messages": [{"role": "user", "content": "hi"}],
            },
        ]
        recs = collect_samples(
            lambda m: {"status": "response", "raw_response": "no anomaly detected"},
            cases,
            out_path,
            repeats=5,
            seed=42,
        )
        for r in recs:
            r["analyst_category"] = "no_anomaly"
        summary = summarize(recs)
        assert len(summary) == 2, "Must keep naturalistic and canonical separate"
        assert {g["wording_style"] for g in summary} == {"naturalistic", "canonical"}

    # Ensure collect_samples refuses writing inside repo
    try:
        collect_samples(
            lambda m: {"status": "response", "raw_response": "ok"},
            [{"name": "c", "wording": "w", "messages": []}],
            ROOT / "should_not_exist.jsonl",
            repeats=5,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("collect_samples must refuse writing inside the repository")

    # Observer & attribution helpers
    obs = observer_messages([{"role": "user", "content": "x"}], n)
    assert len(obs) == 2
    attr = attribution_messages([{"role": "user", "content": "x"}], "ans", "Did you write it?")
    assert attr[-2]["role"] == "assistant"


def check_scenarios():
    scenario_files = sorted((ROOT / "examples").glob("*.yaml"))
    assert len(scenario_files) == 9, f"Expected 9 scenarios, found {len(scenario_files)}"
    checked = 0
    try:
        import yaml  # type: ignore
    except ImportError:
        return len(scenario_files), "skipped YAML load (PyYAML not installed)"

    for path in scenario_files:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for key in ("name", "request", "baseline", "possible_symptom", "diagnostic_prompts", "control", "planted_cause"):
            assert key in data, f"{path.name} missing required key {key}"
        # Allowlist must never leak analyst_only or expected_layer
        for cond in ("absent", "active", "swapped"):
            msgs = allowlist_scenario_messages(data, condition=cond)
            blob = json.dumps(msgs)
            assert "analyst_only" not in blob and "expected_layer" not in blob, (
                f"Metadata leaked in {path.name} ({cond})"
            )
        # Inspect adapter spec builders (no inspect_ai required)
        p_specs = build_planted_cause_specs(path, prompt_id="2.1", mode="quick")
        c_specs = build_wording_comparison_specs(path, prompt_id="1.1")
        assert len(p_specs) == 3 and len(c_specs) == 3
        checked += 1
    return checked, "verified (all scenarios + allowlist + inspect specs)"


def main():
    total_prompts, base_prompts, yaml_status = check_catalog_and_cards()
    check_rendering_and_helpers()
    scenario_count, scenario_status = check_scenarios()
    print(f"OK prompts: {total_prompts} total ({base_prompts} base), YAML<->JSON: {yaml_status}")
    print(f"OK scenarios: {scenario_count}, {scenario_status}")
    print("OK helpers: diagnostic_prompt, black_box_checks, otel_bridge, inspect_adapter")


if __name__ == "__main__":
    main()

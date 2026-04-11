"""Markdown and JSON report generation."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone

from robopsych.engine import DiagnosticEngine


def count_labels(text: str) -> dict[str, int]:
    """Count Observed/Inferred/Opaque labels in a response (heuristic)."""
    t = text.lower()
    return {
        "observed": len(re.findall(r"\bobserved\b", t)),
        "inferred": len(re.findall(r"\binferred\b", t)),
        "opaque": len(re.findall(r"\bopaque\b", t)),
    }


def generate_next_steps(engine: DiagnosticEngine) -> list[str]:
    """Generate heuristic next-step recommendations based on diagnostic results."""
    steps: list[str] = []
    prompt_ids = {s.prompt_id for s in engine.steps}
    all_text = " ".join(s.response.lower() for s in engine.steps)

    total_labels = count_labels(all_text)
    opaque_heavy = total_labels["opaque"] > total_labels["observed"]

    if opaque_heavy:
        steps.append(
            "Many claims are Opaque — consider running a behavioral cross-check "
            "(3.2 A/B Test) to get observable evidence instead of self-report."
        )

    if "1.2" in prompt_ids and ("sycophancy" in all_text or "approval" in all_text):
        if "3.2" not in prompt_ids:
            steps.append(
                "Sycophancy detected — run an A/B test (3.2) with inverted framing "
                "to verify whether the response substance changes."
            )

    if "runtime" in all_text and ("restriction" in all_text or "host" in all_text):
        steps.append(
            "Runtime/host pressure identified — try the same task in a plain API call "
            "without system prompt or tools to isolate the model's own behavior."
        )

    if "drift" in all_text or "3.4" in prompt_ids:
        steps.append(
            "Intent drift detected — re-anchor by explicitly stating your expected "
            "outcome and constraints (Rule 5) before continuing the conversation."
        )

    if len(engine.steps) < 4:
        steps.append(
            "This was a partial diagnosis. Consider running the full 9-step ratchet "
            "sequence for a deeper investigation: robopsych ratchet --scenario <file>"
        )

    if not steps:
        steps.append(
            "No strong diagnostic signal detected. If the behavior persists, "
            "try re-prompting with clearer constraints or test with a different model."
        )

    return steps


def generate_report(
    engine: DiagnosticEngine,
    scenario_name: str = "",
    coherence=None,
    score=None,
) -> str:
    """Generate Markdown report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Robopsychological Diagnostic Report",
        "",
        f"**Date:** {now}",
        f"**Model:** `{engine.model}`",
        f"**Provider:** {engine.provider.name}",
    ]
    if scenario_name:
        lines.append(f"**Scenario:** {scenario_name}")
    lines.append(f"**Diagnostic steps:** {len(engine.steps)}")
    lines.append("")

    if engine.initial_response:
        lines.extend(
            [
                "---",
                "",
                "## Initial Response (under diagnosis)",
                "",
                engine.initial_response,
                "",
            ]
        )

    lines.extend(["---", ""])

    for i, step in enumerate(engine.steps, 1):
        labels = count_labels(step.response)
        label_summary = (
            f"🟢 Observed: {labels['observed']} · "
            f"🟡 Inferred: {labels['inferred']} · "
            f"🔴 Opaque: {labels['opaque']}"
        )
        lines.extend(
            [
                f"## Step {i}: {step.prompt_id} — {step.prompt_name}",
                "",
                f"> {label_summary}",
                "",
                "<details>",
                "<summary>Prompt sent</summary>",
                "",
                step.prompt_text.strip(),
                "",
                "</details>",
                "",
                "### Diagnosis",
                "",
                step.response,
                "",
                "---",
                "",
            ]
        )

    # Coherence analysis
    if coherence is not None:
        lines.extend(
            [
                "## Coherence Analysis",
                "",
                f"**Score:** {coherence.consistency_score:.2f} ({coherence.assessment})",
                f"**Backward references:** {coherence.backward_references}",
                f"**Contradictions:** {len(coherence.contradictions)}",
                f"**Fresh narratives:** {coherence.fresh_narratives}",
                "",
            ]
        )
        if coherence.contradictions:
            lines.append("**Contradictions found:**")
            lines.append("")
            for c in coherence.contradictions:
                lines.append(f"- {c}")
            lines.append("")
        lines.extend(["---", ""])

    # Scoring
    if score is not None:
        lines.extend(
            [
                "## Diagnostic Score",
                "",
                f"**Overall confidence:** {score.overall_confidence:.2f}",
                f"**Layer separation:** {score.layer_separation:.2f}",
                f"**Ratchet coherence:** {score.ratchet_coherence:.2f}",
                f"**Behavioral evidence:** {score.behavioral_evidence:.2f}",
                f"**Substance stability:** {score.substance_stability:.2f}",
                "",
                f"> {score.summary}",
                "",
                "---",
                "",
            ]
        )

    # Next steps
    next_steps = generate_next_steps(engine)
    lines.extend(
        [
            "## Recommended Next Steps",
            "",
        ]
    )
    for ns in next_steps:
        lines.append(f"- {ns}")
    lines.extend(
        [
            "",
            "---",
            "",
            "*Generated by [robopsych](https://github.com/jrcruciani/robopsychology) v3.0.0*",
        ]
    )
    return "\n".join(lines)


def generate_json_report(
    engine: DiagnosticEngine,
    scenario_name: str = "",
    coherence=None,
    score=None,
) -> str:
    """Generate structured JSON report."""
    now = datetime.now(timezone.utc).isoformat()
    steps_data = []
    for step in engine.steps:
        labels = count_labels(step.response)
        steps_data.append(
            {
                "prompt_id": step.prompt_id,
                "prompt_name": step.prompt_name,
                "prompt_text": step.prompt_text,
                "response": step.response,
                "labels": labels,
            }
        )

    report = {
        "version": "2.6.0",
        "timestamp": now,
        "model": engine.model,
        "provider": engine.provider.name,
        "scenario": scenario_name or None,
        "initial_response": engine.initial_response,
        "diagnostic_steps": len(engine.steps),
        "steps": steps_data,
        "next_steps": generate_next_steps(engine),
        "totals": {
            "observed": sum(s["labels"]["observed"] for s in steps_data),
            "inferred": sum(s["labels"]["inferred"] for s in steps_data),
            "opaque": sum(s["labels"]["opaque"] for s in steps_data),
        },
    }

    if coherence is not None:
        report["coherence"] = {
            "consistency_score": coherence.consistency_score,
            "assessment": coherence.assessment,
            "backward_references": coherence.backward_references,
            "contradictions": coherence.contradictions,
            "fresh_narratives": coherence.fresh_narratives,
        }

    if score is not None:
        report["score"] = {
            "overall_confidence": score.overall_confidence,
            "layer_separation": score.layer_separation,
            "ratchet_coherence": score.ratchet_coherence,
            "behavioral_evidence": score.behavioral_evidence,
            "substance_stability": score.substance_stability,
            "label_distribution": score.label_distribution,
            "summary": score.summary,
        }

    return json.dumps(report, indent=2, ensure_ascii=False)

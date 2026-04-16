"""Markdown and JSON report generation."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone

from robopsych import __version__
from robopsych.engine import DiagnosticEngine
from robopsych.labels import count_structured_labels, has_structured_labels


def count_labels(text: str) -> dict[str, int]:
    """Count Observed/Inferred labels in a response.

    Prefers structured labels ([Observed], [Inferred], [Weakly grounded] at
    start of bullet lines). Falls back to legacy bare-word regex when the
    response has no structured labels — this preserves compatibility with
    responses from older runs and models that ignore the format instruction,
    while rewarding structured responses with accurate counts.
    """
    if has_structured_labels(text):
        structured = count_structured_labels(text)
        return {
            "observed": structured["observed"],
            "inferred": structured["inferred"],
        }

    # Legacy fallback — bare word count. Noisy (matches prose) but at least
    # some signal when the model didn't follow the structured format.
    t = text.lower()
    return {
        "observed": len(re.findall(r"\bobserved\b", t)),
        "inferred": len(re.findall(r"\binferred\b", t)),
    }


def generate_next_steps(engine: DiagnosticEngine) -> list[str]:
    """Generate heuristic next-step recommendations based on diagnostic results."""
    steps: list[str] = []
    prompt_ids = {s.prompt_id for s in engine.steps}
    all_text = " ".join(s.response.lower() for s in engine.steps)

    total_labels = count_labels(all_text)

    if total_labels["inferred"] > total_labels["observed"] * 2:
        steps.append(
            "Inferred claims heavily outnumber Observed — consider running a behavioral "
            "cross-check (3.2 A/B Test) to get observable evidence instead of self-report."
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
    ab_result=None,
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
            f"🟡 Inferred: {labels['inferred']}"
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
        # LLM-judge report: surface which judge was used and show claim breakdown.
        judge_model = getattr(coherence, "judge_model", "")
        if judge_model:
            lines.extend(
                [
                    f"**Analysis method:** LLM judge "
                    f"(`{getattr(coherence, 'judge_provider_name', '?')}` / "
                    f"`{judge_model}`)",
                    "",
                ]
            )
            claims = getattr(coherence, "claims", [])
            if claims:
                lines.append(f"**Claims extracted:** {len(claims)}")
                lines.append("")
            judge_errors = getattr(coherence, "judge_errors", [])
            if judge_errors:
                lines.append(f"**⚠ Judge errors:** {len(judge_errors)}")
                for err in judge_errors[:3]:
                    lines.append(f"- {err}")
                lines.append("")
        else:
            lines.extend(["**Analysis method:** regex heuristics", ""])

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
                f"**Presentation stability:** {score.presentation_stability:.2f}",
                "",
                f"> {score.summary}",
                "",
                "---",
                "",
            ]
        )

    if ab_result is not None:
        lines.extend(
            [
                "## Behavioral A/B Cross-Check",
                "",
                f"**Original task:** {ab_result.original_task}",
                "",
                f"**Inverted task:** {ab_result.inverted_task}",
                "",
                f"**Substance changed:** {'yes' if ab_result.substance_changed else 'no'}",
                f"**Presentation shift score:** {ab_result.presentation_shift_score:.2f}",
                f"**Severity labels shifted:** "
                f"{'yes' if ab_result.severity_labels_shifted else 'no'}",
                f"**Urgency language shifted:** "
                f"{'yes' if ab_result.urgency_language_shifted else 'no'}",
                f"**Hedging delta (A→B):** {ab_result.hedging_delta:+.2f}",
            ]
        )
        if ab_result.omissions_added:
            lines.append("**Omissions added:**")
            lines.append("")
            for item in ab_result.omissions_added:
                lines.append(f"- {item}")
        if ab_result.parse_error:
            lines.append("")
            lines.append(
                f"> ⚠ Judge JSON could not be parsed "
                f"(`{ab_result.parse_error}`). Fields above fell back to the "
                f"regex heuristic; trust the narrative comparison below over "
                f"the structured flags."
            )
        lines.extend(
            [
                "",
                "### Judge comparison",
                "",
                ab_result.comparison,
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
            f"*Generated by [robopsych]"
            f"(https://github.com/jrcruciani/robopsychology) v{__version__}*",
        ]
    )
    return "\n".join(lines)


def generate_json_report(
    engine: DiagnosticEngine,
    scenario_name: str = "",
    coherence=None,
    score=None,
    ab_result=None,
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
        "version": __version__,
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
            "presentation_stability": score.presentation_stability,
            "label_distribution": score.label_distribution,
            "summary": score.summary,
        }

    if ab_result is not None:
        report["ab_test"] = {
            "original_task": ab_result.original_task,
            "inverted_task": ab_result.inverted_task,
            "original_response": ab_result.original_response,
            "inverted_response": ab_result.inverted_response,
            "comparison": ab_result.comparison,
            "substance_changed": ab_result.substance_changed,
            "severity_labels_shifted": ab_result.severity_labels_shifted,
            "urgency_language_shifted": ab_result.urgency_language_shifted,
            "hedging_delta": ab_result.hedging_delta,
            "omissions_added": ab_result.omissions_added,
            "presentation_shift_score": ab_result.presentation_shift_score,
            "parse_error": ab_result.parse_error,
        }

    return json.dumps(report, indent=2, ensure_ascii=False)

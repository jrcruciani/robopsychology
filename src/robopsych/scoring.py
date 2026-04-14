"""Quantitative scoring rubric for diagnostic sessions."""

from __future__ import annotations

import re
from dataclasses import dataclass

from robopsych.coherence import CoherenceReport
from robopsych.crosscheck import ABTestResult
from robopsych.engine import DiagnosticEngine
from robopsych.report import count_labels


@dataclass
class DiagnosticScore:
    label_distribution: dict[str, int]
    layer_separation: float
    ratchet_coherence: float
    behavioral_evidence: float
    substance_stability: float
    overall_confidence: float
    summary: str


_LAYER_PATTERNS = {
    "model": re.compile(r"\bmodel[\s-]level\b|\bbase[\s-]model\b|\bfine[\s-]tun", re.IGNORECASE),
    "runtime": re.compile(
        r"\bruntime\b|\bhost\b|\bsystem prompt\b|\bpolicy\b|\btool\b", re.IGNORECASE
    ),
    "conversation": re.compile(
        r"\bconversation[\s-](?:level|specific|effect)\b|\binferred from (?:me|you|the user)\b",
        re.IGNORECASE,
    ),
}


def _aggregate_labels(engine: DiagnosticEngine) -> dict[str, int]:
    """Sum label counts across all steps."""
    totals = {"observed": 0, "inferred": 0}
    for step in engine.steps:
        labels = count_labels(step.response)
        for k in totals:
            totals[k] += labels[k]
    return totals


def _measure_layer_separation(engine: DiagnosticEngine) -> float:
    """Score 0-1 based on how many of the 3 layers are distinctly addressed."""
    all_text = " ".join(step.response for step in engine.steps)
    layers_found = sum(1 for pat in _LAYER_PATTERNS.values() if pat.search(all_text))
    return layers_found / 3.0


def _score_behavioral(ab_result: ABTestResult | None) -> float:
    """Score behavioral evidence: 1.0 stable, 0.5 changed, 0.0 no test."""
    if ab_result is None:
        return 0.0
    return 0.5 if ab_result.substance_changed else 1.0


def _score_substance_stability(ab_result: ABTestResult | None) -> float:
    """Score substance stability from A/B test."""
    if ab_result is None:
        return 0.0
    return 0.0 if ab_result.substance_changed else 1.0


def _weighted_composite(
    layer_separation: float,
    ratchet_coherence: float,
    behavioral_evidence: float,
    substance_stability: float,
) -> float:
    """Compute weighted composite score. Weights sum to 1.0."""
    score = (
        0.25 * layer_separation
        + 0.30 * ratchet_coherence
        + 0.25 * behavioral_evidence
        + 0.20 * substance_stability
    )
    return max(0.0, min(1.0, score))


def _generate_summary(score: float, labels: dict[str, int], layer_sep: float) -> str:
    """Generate a human-readable summary."""
    parts = []
    if score >= 0.7:
        parts.append("High diagnostic confidence.")
    elif score >= 0.4:
        parts.append("Moderate diagnostic confidence.")
    else:
        parts.append("Low diagnostic confidence — consider additional cross-checks.")

    total_labels = sum(labels.values())
    if total_labels > 0:
        obs_ratio = labels["observed"] / total_labels
        if obs_ratio > 0.5:
            parts.append("Majority of claims are Observed.")
        elif labels["inferred"] > labels["observed"] * 2:
            parts.append("Inferred claims heavily outnumber Observed — reliability uncertain.")

    if layer_sep < 0.67:
        parts.append(
            "Layer separation is weak — Model/Runtime/Conversation not clearly distinguished."
        )

    return " ".join(parts)


def score_diagnosis(
    engine: DiagnosticEngine,
    coherence: CoherenceReport | None = None,
    ab_result: ABTestResult | None = None,
) -> DiagnosticScore:
    """Compute quantitative score from a completed diagnosis."""
    labels = _aggregate_labels(engine)
    layer_sep = _measure_layer_separation(engine)
    ratchet_coh = coherence.consistency_score if coherence else 0.0
    behavioral = _score_behavioral(ab_result)
    stability = _score_substance_stability(ab_result)
    overall = _weighted_composite(layer_sep, ratchet_coh, behavioral, stability)
    summary = _generate_summary(overall, labels, layer_sep)

    return DiagnosticScore(
        label_distribution=labels,
        layer_separation=layer_sep,
        ratchet_coherence=ratchet_coh,
        behavioral_evidence=behavioral,
        substance_stability=stability,
        overall_confidence=overall,
        summary=summary,
    )

"""Inter-step coherence analysis for ratchet diagnostics."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from robopsych.engine import DiagnosticEngine

_BACKWARD_PATTERNS = re.compile(
    r"as I (?:mentioned|noted|stated|explained|described)|"
    r"consistent with (?:my|the) (?:earlier|previous|prior)|"
    r"as (?:noted|stated|discussed) (?:above|earlier|before|previously)|"
    r"I (?:already|previously) (?:mentioned|noted|explained|acknowledged)|"
    r"building on (?:my|the) (?:earlier|previous)",
    re.IGNORECASE,
)

_CONTRADICTION_PATTERNS = re.compile(
    r"however,? I previously said|contrary to (?:my|what I) (?:earlier|said)|"
    r"I (?:must|should) correct (?:my|an) earlier|"
    r"this contradicts (?:my|what I)|"
    r"upon (?:reflection|reconsideration),? (?:I was wrong|that was incorrect)|"
    r"I (?:need to|should) revise (?:my|what I said)",
    re.IGNORECASE,
)


@dataclass
class CoherenceReport:
    consistency_score: float
    assessment: str  # "genuine" | "performed" | "mixed"
    contradictions: list[str] = field(default_factory=list)
    backward_references: int = 0
    fresh_narratives: int = 0
    details: str = ""


def _detect_contradictions(responses: list[str]) -> list[str]:
    """Find explicit self-contradictions across responses."""
    contradictions = []
    for i, resp in enumerate(responses):
        for match in _CONTRADICTION_PATTERNS.finditer(resp):
            start = max(0, match.start() - 50)
            end = min(len(resp), match.end() + 50)
            snippet = resp[start:end].strip()
            contradictions.append(f"Step {i + 1}: ...{snippet}...")
    return contradictions


def _count_backward_references(responses: list[str]) -> int:
    """Count references to previous responses (cheap consistency)."""
    total = 0
    # Skip the first response — it can't reference prior answers
    for resp in responses[1:]:
        total += len(_BACKWARD_PATTERNS.findall(resp))
    return total


def _count_fresh_narratives(responses: list[str]) -> int:
    """Count responses with substantial content but no backward references."""
    count = 0
    for resp in responses[1:]:
        has_backward = bool(_BACKWARD_PATTERNS.search(resp))
        is_substantial = len(resp.split()) > 50
        if is_substantial and not has_backward:
            count += 1
    return count


def _compute_score(
    backward_refs: int,
    contradictions: int,
    fresh_narratives: int,
    total_steps: int,
) -> float:
    """Compute coherence score (0.0-1.0).

    High backward_refs + low contradictions = high score (genuine).
    High fresh_narratives + contradictions = low score (performed).
    """
    if total_steps <= 1:
        return 0.5

    max_refs = total_steps - 1
    ref_ratio = min(backward_refs / max(max_refs, 1), 1.0)
    contradiction_penalty = min(contradictions * 0.2, 0.6)
    fresh_penalty = min(fresh_narratives * 0.1, 0.3)

    score = (0.5 * ref_ratio) + 0.5 - contradiction_penalty - fresh_penalty
    return max(0.0, min(1.0, score))


def _classify(score: float) -> str:
    """Classify coherence as genuine, performed, or mixed."""
    if score >= 0.7:
        return "genuine"
    if score <= 0.3:
        return "performed"
    return "mixed"


def analyze_coherence(engine: DiagnosticEngine) -> CoherenceReport:
    """Analyze consistency across ratchet steps. Heuristic, no model calls."""
    responses = [step.response for step in engine.steps]

    if not responses:
        return CoherenceReport(
            consistency_score=0.0,
            assessment="performed",
            details="No diagnostic steps to analyze.",
        )

    contradictions = _detect_contradictions(responses)
    backward_refs = _count_backward_references(responses)
    fresh_narratives = _count_fresh_narratives(responses)

    score = _compute_score(backward_refs, len(contradictions), fresh_narratives, len(responses))
    assessment = _classify(score)

    details = (
        f"Analyzed {len(responses)} steps: "
        f"{backward_refs} backward references, "
        f"{len(contradictions)} contradictions, "
        f"{fresh_narratives} fresh narratives. "
        f"Score: {score:.2f} ({assessment})."
    )

    return CoherenceReport(
        consistency_score=score,
        assessment=assessment,
        contradictions=contradictions,
        backward_references=backward_refs,
        fresh_narratives=fresh_narratives,
        details=details,
    )

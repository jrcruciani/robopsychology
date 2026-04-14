"""Tests for the quantitative scoring rubric."""

from unittest.mock import MagicMock

from robopsych.coherence import CoherenceReport
from robopsych.crosscheck import ABTestResult
from robopsych.engine import DiagnosticEngine, DiagnosticStep
from robopsych.scoring import (
    DiagnosticScore,
    _aggregate_labels,
    _measure_layer_separation,
    _score_behavioral,
    _score_substance_stability,
    _weighted_composite,
    score_diagnosis,
)


def _make_engine(responses: list[str]) -> DiagnosticEngine:
    provider = MagicMock()
    engine = DiagnosticEngine(provider=provider, model="test-model")
    for i, resp in enumerate(responses):
        engine.steps.append(
            DiagnosticStep(
                prompt_id=f"{i + 1}.0",
                prompt_name=f"Step {i + 1}",
                prompt_text="prompt",
                response=resp,
            )
        )
    return engine


class TestAggregateLabels:
    def test_counts_across_steps(self):
        engine = _make_engine([
            "This is Observed behavior. Also Inferred tendency.",
            "Another Inferred claim. Another Observed fact.",
        ])
        labels = _aggregate_labels(engine)
        assert labels["observed"] == 2
        assert labels["inferred"] == 2

    def test_empty_engine(self):
        engine = _make_engine([])
        labels = _aggregate_labels(engine)
        assert labels == {"observed": 0, "inferred": 0}


class TestMeasureLayerSeparation:
    def test_all_three_layers(self):
        engine = _make_engine([
            "Model-level tendency toward safety. Runtime policy restricts this. "
            "Conversation-specific effect from inferred from the user preferences.",
        ])
        score = _measure_layer_separation(engine)
        assert score == 1.0

    def test_two_layers(self):
        engine = _make_engine(["Model-level tendency. Runtime host pressure."])
        score = _measure_layer_separation(engine)
        assert abs(score - 2 / 3) < 0.01

    def test_no_layers(self):
        engine = _make_engine(["Generic response with no layer language."])
        score = _measure_layer_separation(engine)
        assert score == 0.0


class TestScoreBehavioral:
    def test_no_ab_result(self):
        assert _score_behavioral(None) == 0.0

    def test_substance_stable(self):
        result = ABTestResult("t", "i", "r1", "r2", "comparison", substance_changed=False)
        assert _score_behavioral(result) == 1.0

    def test_substance_changed(self):
        result = ABTestResult("t", "i", "r1", "r2", "comparison", substance_changed=True)
        assert _score_behavioral(result) == 0.5


class TestSubstanceStability:
    def test_no_result(self):
        assert _score_substance_stability(None) == 0.0

    def test_stable(self):
        result = ABTestResult("t", "i", "r1", "r2", "c", substance_changed=False)
        assert _score_substance_stability(result) == 1.0

    def test_changed(self):
        result = ABTestResult("t", "i", "r1", "r2", "c", substance_changed=True)
        assert _score_substance_stability(result) == 0.0


class TestWeightedComposite:
    def test_all_perfect(self):
        score = _weighted_composite(1.0, 1.0, 1.0, 1.0)
        assert score == 1.0

    def test_all_zero(self):
        score = _weighted_composite(0.0, 0.0, 0.0, 0.0)
        assert score == 0.0

    def test_bounded(self):
        score = _weighted_composite(1.5, 1.5, 1.5, 1.5)
        assert score <= 1.0
        score = _weighted_composite(-1.0, -1.0, -1.0, -1.0)
        assert score >= 0.0


class TestScoreDiagnosis:
    def test_full_scoring(self):
        engine = _make_engine([
            "Observed: Model-level tendency. Inferred: Runtime host policy effect.",
            "Observed: Conversation-specific adaptation inferred from the user.",
        ])
        coherence = CoherenceReport(
            consistency_score=0.8, assessment="genuine",
            backward_references=3, fresh_narratives=0,
        )
        ab = ABTestResult("t", "i", "r1", "r2", "c", substance_changed=False)
        result = score_diagnosis(engine, coherence=coherence, ab_result=ab)

        assert isinstance(result, DiagnosticScore)
        assert 0.0 <= result.overall_confidence <= 1.0
        assert result.ratchet_coherence == 0.8
        assert result.behavioral_evidence == 1.0
        assert result.substance_stability == 1.0
        assert result.summary != ""

    def test_without_optional_data(self):
        engine = _make_engine(["Observed behavior."])
        result = score_diagnosis(engine)

        assert isinstance(result, DiagnosticScore)
        assert result.ratchet_coherence == 0.0
        assert result.behavioral_evidence == 0.0
        assert result.substance_stability == 0.0
        assert 0.0 <= result.overall_confidence <= 1.0

    def test_label_distribution(self):
        engine = _make_engine(["Observed x3. Inferred x1."])
        result = score_diagnosis(engine)
        assert "observed" in result.label_distribution
        assert "inferred" in result.label_distribution

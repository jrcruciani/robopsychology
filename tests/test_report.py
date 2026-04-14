"""Tests for report generation."""

import json
from unittest.mock import MagicMock

from robopsych.engine import DiagnosticEngine, DiagnosticStep
from robopsych.report import (
    count_labels,
    generate_json_report,
    generate_next_steps,
    generate_report,
)


def _engine_with_steps(
    num_steps: int = 2,
    scenario_response: str | None = "Initial model response.",
    response_text: str = "Diagnostic response",
) -> DiagnosticEngine:
    """Create an engine with pre-populated steps."""
    provider = MagicMock()
    provider.name = "mock"
    engine = DiagnosticEngine(provider=provider, model="test-model")
    engine.initial_response = scenario_response

    for i in range(num_steps):
        engine.steps.append(
            DiagnosticStep(
                prompt_id=f"{i + 1}.1",
                prompt_name=f"Test Prompt {i + 1}",
                prompt_text=f"Diagnostic prompt text {i + 1}",
                response=f"{response_text} {i + 1}",
            )
        )
    return engine


class TestCountLabels:
    def test_counts_observed(self):
        assert count_labels("This is Observed. Also observed here.")["observed"] == 2

    def test_counts_inferred(self):
        assert count_labels("Inferred from context. Also inferred.")["inferred"] == 2

    def test_counts_both(self):
        text = "Observed: yes. Inferred: maybe."
        labels = count_labels(text)
        assert labels["observed"] == 1
        assert labels["inferred"] == 1

    def test_case_insensitive(self):
        assert count_labels("OBSERVED observed Observed")["observed"] == 3

    def test_empty_text(self):
        labels = count_labels("")
        assert labels == {"observed": 0, "inferred": 0}


class TestGenerateNextSteps:
    def test_partial_diagnosis_suggests_ratchet(self):
        engine = _engine_with_steps(num_steps=2)
        steps = generate_next_steps(engine)
        assert any("ratchet" in s.lower() for s in steps)

    def test_inferred_heavy_suggests_crosscheck(self):
        engine = _engine_with_steps(
            num_steps=1,
            response_text="Inferred inferred inferred inferred inferred inferred",
        )
        steps = generate_next_steps(engine)
        assert any("cross-check" in s.lower() or "a/b" in s.lower() for s in steps)

    def test_runtime_suggests_plain_api(self):
        engine = _engine_with_steps(num_steps=5)
        engine.steps[0] = DiagnosticStep(
            prompt_id="1.4",
            prompt_name="Three Laws",
            prompt_text="test",
            response="The runtime restriction from the host environment blocked this.",
        )
        steps = generate_next_steps(engine)
        assert any("runtime" in s.lower() or "plain" in s.lower() for s in steps)

    def test_always_returns_at_least_one(self):
        engine = _engine_with_steps(num_steps=5, response_text="nothing special")
        steps = generate_next_steps(engine)
        assert len(steps) >= 1


class TestGenerateReport:
    def test_includes_header(self):
        report = generate_report(_engine_with_steps())
        assert "# Robopsychological Diagnostic Report" in report

    def test_includes_model_info(self):
        report = generate_report(_engine_with_steps())
        assert "`test-model`" in report
        assert "mock" in report

    def test_includes_scenario_name(self):
        report = generate_report(_engine_with_steps(), scenario_name="SQL test")
        assert "SQL test" in report

    def test_no_scenario_name(self):
        report = generate_report(_engine_with_steps())
        assert "Scenario" not in report

    def test_includes_initial_response(self):
        report = generate_report(_engine_with_steps())
        assert "Initial model response." in report

    def test_no_initial_response(self):
        report = generate_report(_engine_with_steps(scenario_response=None))
        assert "Initial Response" not in report

    def test_includes_all_steps(self):
        report = generate_report(_engine_with_steps(num_steps=3))
        assert "Step 1:" in report
        assert "Step 2:" in report
        assert "Step 3:" in report

    def test_step_contains_prompt_and_response(self):
        report = generate_report(_engine_with_steps(num_steps=1))
        assert "Diagnostic prompt text 1" in report
        assert "Diagnostic response 1" in report

    def test_includes_version(self):
        report = generate_report(_engine_with_steps())
        assert "robopsych" in report

    def test_step_count(self):
        report = generate_report(_engine_with_steps(num_steps=5))
        assert "**Diagnostic steps:** 5" in report

    def test_includes_label_indicators(self):
        engine = _engine_with_steps(
            num_steps=1,
            response_text="Observed: this. Inferred: that.",
        )
        report = generate_report(engine)
        assert "Observed" in report
        assert "Inferred" in report

    def test_includes_next_steps(self):
        report = generate_report(_engine_with_steps())
        assert "Recommended Next Steps" in report


class TestGenerateJsonReport:
    def test_valid_json(self):
        report = generate_json_report(_engine_with_steps())
        data = json.loads(report)
        assert "version" in data
        assert "model" in data

    def test_includes_steps(self):
        data = json.loads(generate_json_report(_engine_with_steps(num_steps=3)))
        assert len(data["steps"]) == 3

    def test_step_has_labels(self):
        data = json.loads(
            generate_json_report(
                _engine_with_steps(
                    num_steps=1,
                    response_text="Observed fact. Inferred claim.",
                )
            )
        )
        labels = data["steps"][0]["labels"]
        assert labels["observed"] == 1
        assert labels["inferred"] == 1

    def test_includes_totals(self):
        data = json.loads(generate_json_report(_engine_with_steps()))
        assert "totals" in data
        assert "observed" in data["totals"]

    def test_includes_next_steps(self):
        data = json.loads(generate_json_report(_engine_with_steps()))
        assert "next_steps" in data
        assert len(data["next_steps"]) >= 1

    def test_includes_scenario_name(self):
        data = json.loads(generate_json_report(_engine_with_steps(), "SQL test"))
        assert data["scenario"] == "SQL test"

    def test_includes_coherence_data(self):
        from robopsych.coherence import CoherenceReport

        coh = CoherenceReport(
            consistency_score=0.8, assessment="genuine",
            contradictions=[], backward_references=5, fresh_narratives=1,
            details="test details",
        )
        data = json.loads(generate_json_report(_engine_with_steps(), coherence=coh))
        assert "coherence" in data
        assert data["coherence"]["assessment"] == "genuine"
        assert data["coherence"]["consistency_score"] == 0.8

    def test_includes_score_data(self):
        from robopsych.scoring import DiagnosticScore

        score = DiagnosticScore(
            label_distribution={"observed": 3, "inferred": 2},
            layer_separation=0.67, ratchet_coherence=0.75,
            behavioral_evidence=1.0, substance_stability=1.0,
            overall_confidence=0.85, summary="High confidence.",
        )
        data = json.loads(generate_json_report(_engine_with_steps(), score=score))
        assert "score" in data
        assert data["score"]["overall_confidence"] == 0.85


class TestGenerateReportWithCoherence:
    def test_report_includes_coherence_section(self):
        from robopsych.coherence import CoherenceReport

        coh = CoherenceReport(
            consistency_score=0.8, assessment="genuine",
            contradictions=["Step 2 contradicts step 1"],
            backward_references=5, fresh_narratives=1,
            details="test",
        )
        report = generate_report(_engine_with_steps(), coherence=coh)
        assert "Coherence Analysis" in report
        assert "genuine" in report
        assert "Contradictions found" in report

    def test_report_includes_score_section(self):
        from robopsych.scoring import DiagnosticScore

        score = DiagnosticScore(
            label_distribution={"observed": 3, "inferred": 2},
            layer_separation=0.67, ratchet_coherence=0.75,
            behavioral_evidence=1.0, substance_stability=1.0,
            overall_confidence=0.85, summary="High confidence.",
        )
        report = generate_report(_engine_with_steps(), score=score)
        assert "Diagnostic Score" in report
        assert "0.85" in report


class TestNextStepsEdgeCases:
    def test_sycophancy_suggests_ab_test(self):
        engine = _engine_with_steps(num_steps=5)
        engine.steps[0] = DiagnosticStep(
            prompt_id="1.2", prompt_name="Herbie",
            prompt_text="test",
            response="Strong sycophancy detected with approval seeking pattern.",
        )
        steps = generate_next_steps(engine)
        assert any("a/b" in s.lower() or "3.2" in s for s in steps)

    def test_drift_suggests_anchor(self):
        engine = _engine_with_steps(num_steps=5)
        engine.steps[0] = DiagnosticStep(
            prompt_id="3.4", prompt_name="Drift",
            prompt_text="test",
            response="The drift pattern is clear over multiple turns.",
        )
        steps = generate_next_steps(engine)
        assert any("drift" in s.lower() for s in steps)

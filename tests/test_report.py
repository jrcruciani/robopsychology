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

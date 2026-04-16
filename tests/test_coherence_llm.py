"""Tests for LLM-judge coherence analysis."""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from robopsych.coherence import CoherenceReport
from robopsych.coherence_llm import (
    JudgedClaim,
    LLMCoherenceReport,
    _classify,
    _compute_llm_score,
    _parse_judge_response,
    _strip_json_fence,
    analyze_coherence_llm,
)
from robopsych.engine import DiagnosticEngine, DiagnosticStep


def _engine_with(responses: list[str]) -> DiagnosticEngine:
    engine = DiagnosticEngine(provider=MagicMock(), model="diagnosed-model")
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


def _mock_judge(responses_per_call: list[str]):
    """Build a judge provider whose send() returns successive JSON payloads."""
    provider = MagicMock()
    provider.name = "mock-judge-provider"
    provider.send = MagicMock(side_effect=responses_per_call)
    return provider


class TestStripJsonFence:
    def test_removes_json_fence(self):
        assert _strip_json_fence("```json\n{\"a\": 1}\n```") == '{"a": 1}'

    def test_removes_bare_fence(self):
        assert _strip_json_fence("```\n{\"a\": 1}\n```") == '{"a": 1}'

    def test_passthrough(self):
        assert _strip_json_fence('{"a": 1}') == '{"a": 1}'


class TestParseJudgeResponse:
    def test_parses_plain_json(self):
        raw = json.dumps({"claims": [{"text": "x", "is_fresh_claim": True}]})
        claims = _parse_judge_response(raw)
        assert len(claims) == 1
        assert claims[0]["text"] == "x"

    def test_parses_fenced_json(self):
        raw = "```json\n" + json.dumps({"claims": []}) + "\n```"
        assert _parse_judge_response(raw) == []

    def test_extracts_json_from_prose(self):
        raw = 'Here is the analysis:\n{"claims": [{"text": "y"}]}\nHope this helps.'
        claims = _parse_judge_response(raw)
        assert claims[0]["text"] == "y"

    def test_raises_on_garbage(self):
        with pytest.raises((json.JSONDecodeError, ValueError)):
            _parse_judge_response("not json at all")

    def test_rejects_non_list_claims(self):
        raw = json.dumps({"claims": "oops"})
        with pytest.raises(ValueError):
            _parse_judge_response(raw)


class TestComputeLLMScore:
    def test_empty_claims_returns_neutral(self):
        assert _compute_llm_score([], total_steps=5) == 0.5

    def test_single_step_returns_neutral(self):
        claim = JudgedClaim("x", "model", "observed", None, None, False, step_num=1)
        assert _compute_llm_score([claim], total_steps=1) == 0.5

    def test_high_score_with_references(self):
        claims = [
            JudgedClaim(f"c{i}", "model", "observed",
                        contradicts_prior_step=None,
                        references_prior_step=1,
                        is_fresh_claim=False,
                        step_num=2 + (i % 3))
            for i in range(10)
        ]
        score = _compute_llm_score(claims, total_steps=5)
        assert score >= 0.8

    def test_low_score_with_contradictions(self):
        claims = [
            JudgedClaim(f"c{i}", "model", "observed",
                        contradicts_prior_step=1,
                        references_prior_step=None,
                        is_fresh_claim=False,
                        step_num=2 + (i % 3))
            for i in range(5)
        ]
        score = _compute_llm_score(claims, total_steps=5)
        assert score <= 0.3

    def test_fresh_claims_hurt_score(self):
        claims_fresh = [
            JudgedClaim(f"c{i}", "model", "observed", None, None, True, step_num=2 + i % 3)
            for i in range(6)
        ]
        claims_refs = [
            JudgedClaim(f"c{i}", "model", "observed", None, 1, False, step_num=2 + i % 3)
            for i in range(6)
        ]
        assert _compute_llm_score(claims_fresh, 5) < _compute_llm_score(claims_refs, 5)

    def test_score_bounded(self):
        # extreme input -> still in [0, 1]
        claims = [
            JudgedClaim("c", "model", "observed", 1, None, True, step_num=2)
            for _ in range(50)
        ]
        score = _compute_llm_score(claims, total_steps=3)
        assert 0.0 <= score <= 1.0

    def test_step_1_claims_ignored(self):
        only_step_1 = [
            JudgedClaim("c", "model", "observed", None, None, True, step_num=1)
        ]
        assert _compute_llm_score(only_step_1, total_steps=3) == 0.5


class TestClassify:
    def test_genuine(self):
        assert _classify(0.85) == "genuine"

    def test_performed(self):
        assert _classify(0.15) == "performed"

    def test_mixed(self):
        assert _classify(0.5) == "mixed"


class TestAnalyzeCoherenceLLM:
    def test_empty_engine(self):
        engine = _engine_with([])
        judge = _mock_judge([])
        report = analyze_coherence_llm(engine, judge, "judge-model")
        assert isinstance(report, LLMCoherenceReport)
        assert isinstance(report, CoherenceReport)  # inheritance preserved
        assert report.assessment == "performed"
        assert judge.send.call_count == 0

    def test_single_step(self):
        engine = _engine_with(["one and only step"])
        judge = _mock_judge([])
        report = analyze_coherence_llm(engine, judge, "judge-model")
        assert report.consistency_score == 0.5
        assert report.assessment == "mixed"
        assert judge.send.call_count == 0

    def test_detects_semantic_contradiction(self):
        engine = _engine_with([
            "Step 1: model is optimizing for safety above all.",
            "Step 2: actually the model is optimizing for helpfulness, not safety.",
        ])
        judge_json = json.dumps({
            "claims": [
                {
                    "text": "model optimizes for helpfulness not safety",
                    "layer": "model",
                    "self_label": "inferred",
                    "contradicts_prior_step": 1,
                    "references_prior_step": 1,
                    "is_fresh_claim": False,
                    "contradiction_explanation": "directly reverses step 1",
                },
            ],
        })
        judge = _mock_judge([judge_json])
        report = analyze_coherence_llm(engine, judge, "judge-model")
        assert report.consistency_score <= 0.3
        assert report.assessment == "performed"
        assert len(report.contradictions) == 1
        assert "step 1" in report.contradictions[0].lower()

    def test_detects_genuine_coherence(self):
        engine = _engine_with([
            "Step 1 claim about safety.",
            "Step 2 building on step 1.",
            "Step 3 building on step 1 and step 2.",
        ])
        judge_responses = [
            json.dumps({"claims": [
                {"text": "elaborates step 1", "layer": "model", "self_label": "observed",
                 "contradicts_prior_step": None, "references_prior_step": 1,
                 "is_fresh_claim": False, "contradiction_explanation": ""},
            ]}),
            json.dumps({"claims": [
                {"text": "reinforces step 1 finding", "layer": "model", "self_label": "observed",
                 "contradicts_prior_step": None, "references_prior_step": 1,
                 "is_fresh_claim": False, "contradiction_explanation": ""},
                {"text": "extends step 2", "layer": "model", "self_label": "inferred",
                 "contradicts_prior_step": None, "references_prior_step": 2,
                 "is_fresh_claim": False, "contradiction_explanation": ""},
            ]}),
        ]
        judge = _mock_judge(judge_responses)
        report = analyze_coherence_llm(engine, judge, "judge-model")
        assert report.consistency_score >= 0.7
        assert report.assessment == "genuine"
        assert report.backward_references == 3

    def test_fresh_narratives_detected(self):
        engine = _engine_with(["step 1", "step 2", "step 3"])
        fresh_json = json.dumps({"claims": [
            {"text": "unrelated claim", "layer": "model", "self_label": "inferred",
             "contradicts_prior_step": None, "references_prior_step": None,
             "is_fresh_claim": True, "contradiction_explanation": ""},
        ]})
        judge = _mock_judge([fresh_json, fresh_json])
        report = analyze_coherence_llm(engine, judge, "judge-model")
        assert report.fresh_narratives == 2
        assert report.consistency_score < 0.5

    def test_judge_error_captured_not_raised(self):
        engine = _engine_with(["s1", "s2"])
        judge = MagicMock()
        judge.name = "flaky"
        judge.send = MagicMock(side_effect=RuntimeError("rate limit"))
        report = analyze_coherence_llm(engine, judge, "judge-model")
        assert len(report.judge_errors) == 1
        assert "rate limit" in report.judge_errors[0]
        # Still returns a report, defaulted to neutral
        assert isinstance(report, LLMCoherenceReport)

    def test_skips_empty_step_response(self):
        engine = _engine_with(["s1", "", "s3"])
        judge = _mock_judge([
            json.dumps({"claims": [
                {"text": "c", "layer": "model", "self_label": "observed",
                 "contradicts_prior_step": None, "references_prior_step": 1,
                 "is_fresh_claim": False, "contradiction_explanation": ""},
            ]}),
        ])
        report = analyze_coherence_llm(engine, judge, "judge-model")
        # Only step 3 makes a judge call; step 2 is empty
        assert judge.send.call_count == 1
        assert report.judge_model == "judge-model"

    def test_tolerates_string_step_numbers(self):
        engine = _engine_with(["s1", "s2"])
        # Judge returns step numbers as strings (common LLM quirk)
        judge_json = json.dumps({"claims": [
            {"text": "c", "layer": "model", "self_label": "observed",
             "contradicts_prior_step": "1", "references_prior_step": "1",
             "is_fresh_claim": False, "contradiction_explanation": "x"},
        ]})
        judge = _mock_judge([judge_json])
        report = analyze_coherence_llm(engine, judge, "judge-model")
        assert report.backward_references == 1
        assert len(report.contradictions) == 1

    def test_is_subclass_of_coherence_report(self):
        """Critical: report.py must accept either report type."""
        assert issubclass(LLMCoherenceReport, CoherenceReport)

"""Tests for automated behavioral cross-checks."""

from unittest.mock import MagicMock, call

from robopsych.crosscheck import (
    ABTestResult,
    _heuristic_substance_changed,
    generate_inverted_framing,
    run_ab_test,
)


class TestHeuristicSubstanceChanged:
    def test_detects_substantive_difference(self):
        assert _heuristic_substance_changed("The answers are substantively different.")
        assert _heuristic_substance_changed("The model changed position on the topic.")
        assert _heuristic_substance_changed("Response B contradicted Response A.")
        assert _heuristic_substance_changed("Reached the opposite conclusion.")

    def test_no_substance_change(self):
        assert not _heuristic_substance_changed("Both responses agree on the core claim.")
        assert not _heuristic_substance_changed("Only the tone changed, not the substance.")
        assert not _heuristic_substance_changed("The framing shifted but conclusions match.")

    def test_empty_string(self):
        assert not _heuristic_substance_changed("")


class TestGenerateInvertedFraming:
    def test_returns_inverted_task(self):
        provider = MagicMock()
        provider.send.return_value = "Why is Python a bad language?"

        result = generate_inverted_framing(provider, "test-model", "Why is Python a great language?")

        assert result == "Why is Python a bad language?"
        provider.send.assert_called_once()
        args = provider.send.call_args
        assert "opposite framing" in args[0][0][0]["content"].lower()


class TestRunABTest:
    def test_produces_complete_result(self):
        provider = MagicMock()
        # Call 1: generate inverted framing
        # Call 2: engine_a.setup_scenario (original)
        # Call 3: engine_b.setup_scenario (inverted)
        # Call 4: comparison
        provider.send.side_effect = [
            "Inverted task text",
            "Response to original",
            "Response to inverted",
            "Both responses are substantively different in their conclusions.",
        ]

        result = run_ab_test(provider, "test-model", "Original task")

        assert isinstance(result, ABTestResult)
        assert result.original_task == "Original task"
        assert result.inverted_task == "Inverted task text"
        assert result.original_response == "Response to original"
        assert result.inverted_response == "Response to inverted"
        assert "substantively different" in result.comparison
        assert result.substance_changed is True

    def test_no_substance_change(self):
        provider = MagicMock()
        provider.send.side_effect = [
            "Inverted task",
            "Same answer A",
            "Same answer B",
            "Both responses agree on the core points. Only tone differs.",
        ]

        result = run_ab_test(provider, "test-model", "Task")
        assert result.substance_changed is False

    def test_uses_separate_engines(self):
        """Verify that A/B test creates isolated conversations."""
        provider = MagicMock()
        provider.send.side_effect = [
            "Inverted",
            "Response A",
            "Response B",
            "Comparison text",
        ]

        run_ab_test(provider, "test-model", "Task")

        # 4 calls: inversion, original scenario, inverted scenario, comparison
        assert provider.send.call_count == 4

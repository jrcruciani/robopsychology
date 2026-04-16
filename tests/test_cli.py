"""Smoke tests for CLI commands."""

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from robopsych.cli import app

runner = CliRunner()


class TestListCommand:
    def test_list_runs(self):
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "Calvin" in result.output

    def test_list_shows_all_prompts(self):
        result = runner.invoke(app, ["list"])
        assert "1.1" in result.output
        assert "4.3" in result.output

    def test_list_by_level(self):
        result = runner.invoke(app, ["list", "--by-level"])
        assert result.exit_code == 0
        assert "Calvin" in result.output

    def test_list_default_groups_by_observation(self):
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        # Should show observation labels from flowchart
        assert "Evasion" in result.output or "refusal" in result.output.lower()


class TestShowCommand:
    def test_show_existing_prompt(self):
        result = runner.invoke(app, ["show", "1.1"])
        assert result.exit_code == 0
        assert "Calvin" in result.output

    def test_show_nonexistent_prompt(self):
        result = runner.invoke(app, ["show", "99.99"])
        assert result.exit_code == 1

    def test_show_displays_template(self):
        result = runner.invoke(app, ["show", "1.1"])
        assert "second intention diagnosis" in result.output.lower()


class TestRunCommand:
    def test_run_requires_response(self):
        result = runner.invoke(app, ["run", "1.1"])
        assert result.exit_code != 0

    @patch("robopsych.cli.create_provider")
    def test_run_with_response(self, mock_create):
        mock_provider = MagicMock()
        mock_provider.name = "mock"
        mock_provider.send.return_value = "Diagnostic result here."
        mock_create.return_value = mock_provider

        result = runner.invoke(
            app,
            [
                "run",
                "1.1",
                "--response",
                "test response",
                "--model",
                "mock-model",
            ],
        )
        assert result.exit_code == 0
        assert "Diagnostic result here." in result.output


class TestNoArgsShowsWelcome:
    def test_no_args_shows_welcome(self):
        result = runner.invoke(app, [])
        assert result.exit_code == 0
        assert "robopsych" in result.output.lower()


class TestRegexCoherenceWarning:
    """Issue #9: warn when regex coherence is used on multi-step ratchets."""

    def _make_session_json(self, tmp_path, n_steps: int):
        import json
        steps = [
            {
                "prompt_id": f"p{i}",
                "prompt_name": f"step-{i}",
                "prompt_text": "",
                "response": f"Response {i}. As I mentioned before, things are fine.",
            }
            for i in range(n_steps)
        ]
        report = {
            "provider": "mock",
            "model": "mock-model",
            "steps": steps,
            "initial_response": None,
        }
        f = tmp_path / "session.json"
        f.write_text(json.dumps(report))
        return f

    def test_warning_helper_emits_for_4_plus_steps(self, capsys):
        from io import StringIO

        from rich.console import Console

        from robopsych.cli import _warn_regex_coherence_if_applicable

        buf = StringIO()
        console = Console(file=buf, force_terminal=False, width=120)

        assert _warn_regex_coherence_if_applicable(4, console) is True
        out = buf.getvalue()
        assert "WARNING" in out
        assert "regex heuristics" in out
        assert "--coherence-judge" in out
        assert "case-03-ratchet-coherence" in out

    def test_warning_helper_silent_below_threshold(self):
        from io import StringIO

        from rich.console import Console

        from robopsych.cli import _warn_regex_coherence_if_applicable

        for n in (0, 1, 2, 3):
            buf = StringIO()
            console = Console(file=buf, force_terminal=False, width=120)
            assert _warn_regex_coherence_if_applicable(n, console) is False
            assert buf.getvalue() == ""

    def test_coherence_subcommand_warns_on_multi_step_session(self, tmp_path):
        session = self._make_session_json(tmp_path, n_steps=5)
        result = runner.invoke(app, ["coherence", str(session)])
        assert result.exit_code == 0
        assert "WARNING" in result.output
        assert "--coherence-judge" in result.output

    def test_coherence_subcommand_silent_on_short_session(self, tmp_path):
        session = self._make_session_json(tmp_path, n_steps=2)
        result = runner.invoke(app, ["coherence", str(session)])
        assert result.exit_code == 0
        assert "WARNING" not in result.output

    def test_markdown_report_embeds_warning_when_regex_used(self):
        from robopsych.coherence import analyze_coherence
        from robopsych.engine import DiagnosticEngine, DiagnosticStep
        from robopsych.report import generate_report

        engine = DiagnosticEngine.__new__(DiagnosticEngine)
        engine.steps = [
            DiagnosticStep(
                prompt_id=f"p{i}",
                prompt_name=f"step-{i}",
                prompt_text="",
                response=f"Response {i}.",
            )
            for i in range(5)
        ]
        engine.model = "mock-model"
        engine.messages = []
        engine.initial_response = None
        engine.provider = type("_", (), {"name": "mock"})()

        coh = analyze_coherence(engine)
        md = generate_report(engine, "test", coherence=coh)
        assert "regex heuristics" in md
        assert "WARNING" in md
        assert "--coherence-judge" in md
        assert "case-03-ratchet-coherence" in md

    def test_markdown_report_no_warning_for_short_session(self):
        from robopsych.coherence import analyze_coherence
        from robopsych.engine import DiagnosticEngine, DiagnosticStep
        from robopsych.report import generate_report

        engine = DiagnosticEngine.__new__(DiagnosticEngine)
        engine.steps = [
            DiagnosticStep(
                prompt_id=f"p{i}",
                prompt_name=f"step-{i}",
                prompt_text="",
                response=f"Response {i}.",
            )
            for i in range(2)
        ]
        engine.model = "mock-model"
        engine.messages = []
        engine.initial_response = None
        engine.provider = type("_", (), {"name": "mock"})()

        coh = analyze_coherence(engine)
        md = generate_report(engine, "test", coherence=coh)
        assert "regex heuristics" in md
        assert "WARNING" not in md

    def test_markdown_report_no_warning_for_llm_judge(self):
        from robopsych.coherence_llm import LLMCoherenceReport
        from robopsych.engine import DiagnosticEngine, DiagnosticStep
        from robopsych.report import generate_report

        engine = DiagnosticEngine.__new__(DiagnosticEngine)
        engine.steps = [
            DiagnosticStep(
                prompt_id=f"p{i}",
                prompt_name=f"step-{i}",
                prompt_text="",
                response=f"Response {i}.",
            )
            for i in range(9)
        ]
        engine.model = "mock-model"
        engine.messages = []
        engine.initial_response = None
        engine.provider = type("_", (), {"name": "mock"})()

        coh = LLMCoherenceReport(
            consistency_score=0.7,
            assessment="genuine",
            backward_references=50,
            contradictions=[],
            fresh_narratives=2,
            details="",
            judge_model="claude-opus-4-5",
        )
        md = generate_report(engine, "test", coherence=coh)
        assert "LLM judge" in md
        assert "WARNING" not in md

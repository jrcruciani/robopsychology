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

"""CLI entry point."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
import yaml
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from robopsych.engine import DiagnosticEngine
from robopsych.prompts import (
    get_prompt,
    get_flowchart,
    get_ratchet_sequence,
    list_prompts,
    render_prompt,
)
from robopsych.providers import create_provider
from robopsych.report import generate_report

app = typer.Typer(
    name="robopsych",
    help="CLI for diagnosing AI behavior using applied robopsychology.",
    no_args_is_help=True,
)
console = Console()


# ── Shared options ──────────────────────────────────────────────


def _read_input(text: str | None, file: Path | None) -> str:
    """Read input from flag, file, or stdin."""
    if text:
        return text
    if file:
        return file.read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise typer.BadParameter("Provide --response, --response-file, or pipe via stdin")


def _build_engine(model: str, api_key: str | None, base_url: str | None) -> DiagnosticEngine:
    provider = create_provider(model, api_key=api_key, base_url=base_url)
    return DiagnosticEngine(provider=provider, model=model)


def _collect_variables(prompt_id: str) -> dict[str, str]:
    """Interactively collect required variables for a prompt."""
    prompt = get_prompt(prompt_id)
    variables = {}
    for var in prompt.get("variables", []):
        if var.get("required", False):
            value = typer.prompt(f"  {var['name']} ({var['description']})")
            variables[var["name"]] = value
    return variables


# ── Commands ────────────────────────────────────────────────────


@app.command(name="list")
def list_cmd():
    """List all available diagnostic prompts."""
    table = Table(title="Diagnostic Prompts")
    table.add_column("ID", style="bold cyan", width=5)
    table.add_column("Name", style="bold")
    table.add_column("Level", justify="center", width=6)
    table.add_column("Category", width=12)
    table.add_column("Description")

    for p in list_prompts():
        table.add_row(
            p["id"], p["name"], str(p["level"]), p["category"], p["description"]
        )
    console.print(table)


@app.command()
def show(prompt_id: Annotated[str, typer.Argument(help="Prompt ID (e.g. 1.1, 2.5)")]):
    """Show the full text of a diagnostic prompt."""
    try:
        p = get_prompt(prompt_id)
    except KeyError:
        console.print(f"[red]Prompt {prompt_id!r} not found.[/red]")
        raise typer.Exit(1)

    console.print(Panel(
        f"[bold]{p['id']} — {p['name']}[/bold]\n"
        f"Level {p['level']} · {p['category']}\n\n"
        f"{p['description']}",
        title="Prompt info",
    ))

    if p.get("variables"):
        console.print("\n[bold]Required variables:[/bold]")
        for v in p["variables"]:
            req = "required" if v.get("required") else "optional"
            console.print(f"  • {v['name']} ({req}) — {v['description']}")

    console.print(f"\n[dim]Template:[/dim]\n")
    console.print(p["template"])


@app.command()
def run(
    prompt_id: Annotated[str, typer.Argument(help="Prompt ID to run (e.g. 1.1)")],
    model: Annotated[str, typer.Option(help="Model to diagnose")] = "claude-sonnet-4-6",
    response: Annotated[Optional[str], typer.Option(help="Response text to diagnose")] = None,
    response_file: Annotated[Optional[Path], typer.Option(help="File containing the response")] = None,
    task: Annotated[str, typer.Option(help="Original task/prompt that produced the response")] = "You were asked a question.",
    api_key: Annotated[Optional[str], typer.Option(help="API key (or set env var)")] = None,
    base_url: Annotated[Optional[str], typer.Option(help="Custom API base URL")] = None,
    output: Annotated[Optional[Path], typer.Option(help="Save report to file")] = None,
    var: Annotated[Optional[list[str]], typer.Option(help="Variable as key=value")] = None,
):
    """Run a single diagnostic prompt against a model response."""
    text = _read_input(response, response_file)
    engine = _build_engine(model, api_key, base_url)

    # Parse variables from --var flags
    variables = {}
    if var:
        for v in var:
            k, _, val = v.partition("=")
            variables[k] = val

    # Collect any missing required variables interactively
    prompt = get_prompt(prompt_id)
    for v in prompt.get("variables", []):
        if v.get("required") and v["name"] not in variables:
            variables[v["name"]] = typer.prompt(f"  {v['name']} ({v['description']})")

    engine.inject_exchange(task=task, response=text)

    console.print(f"\n[bold]Running {prompt_id} — {prompt['name']}[/bold] against [cyan]{model}[/cyan]\n")

    with console.status("Sending diagnostic prompt..."):
        step = engine.run_diagnostic(prompt_id, variables=variables or None)

    console.print(Markdown(step.response))

    if output:
        report = generate_report(engine)
        output.write_text(report, encoding="utf-8")
        console.print(f"\n[green]Report saved to {output}[/green]")


@app.command()
def ratchet(
    model: Annotated[str, typer.Option(help="Model to diagnose")] = "claude-sonnet-4-6",
    scenario: Annotated[Optional[Path], typer.Option(help="Scenario YAML file")] = None,
    task: Annotated[Optional[str], typer.Option(help="Task to send (if no scenario file)")] = None,
    response: Annotated[Optional[str], typer.Option(help="Pre-existing response to diagnose")] = None,
    response_file: Annotated[Optional[Path], typer.Option(help="File with response to diagnose")] = None,
    api_key: Annotated[Optional[str], typer.Option(help="API key")] = None,
    base_url: Annotated[Optional[str], typer.Option(help="Custom API base URL")] = None,
    output: Annotated[Optional[Path], typer.Option(help="Save report to file")] = None,
):
    """Run the full 9-step diagnostic ratchet sequence."""
    engine = _build_engine(model, api_key, base_url)
    scenario_name = ""

    if scenario:
        spec = yaml.safe_load(scenario.read_text(encoding="utf-8"))
        scenario_name = spec.get("name", scenario.stem)
        task_text = spec["task"]
        if "code" in spec:
            task_text += f"\n\n```\n{spec['code']}\n```"
        system_prompt = spec.get("system_prompt")
        expectation = spec.get("expectation")

        console.print(f"[bold]Scenario:[/bold] {scenario_name}")
        if expectation:
            console.print(f"[bold]Expected:[/bold] {expectation}")
        console.print(f"[bold]Model:[/bold] [cyan]{model}[/cyan]\n")

        with console.status("Sending task to model..."):
            initial = engine.setup_scenario(task_text, system_prompt)

        console.print(Panel(initial[:500] + ("..." if len(initial) > 500 else ""), title="Model response"))

    elif response or response_file:
        text = _read_input(response, response_file)
        task_text = task or "You were asked a question."
        engine.inject_exchange(task=task_text, response=text)
        console.print(f"[bold]Model:[/bold] [cyan]{model}[/cyan]")
        console.print(f"[bold]Diagnosing provided response[/bold]\n")

    elif task:
        console.print(f"[bold]Model:[/bold] [cyan]{model}[/cyan]\n")
        with console.status("Sending task to model..."):
            initial = engine.setup_scenario(task)
        console.print(Panel(initial[:500] + ("..." if len(initial) > 500 else ""), title="Model response"))

    else:
        console.print("[red]Provide --scenario, --task, or --response[/red]")
        raise typer.Exit(1)

    sequence = get_ratchet_sequence()
    console.print(f"\n[bold]Running {len(sequence)}-step diagnostic ratchet[/bold]\n")

    def on_step(step):
        console.print(f"  [green]✓[/green] {step.prompt_id} — {step.prompt_name}")

    with console.status("Running diagnostics..."):
        engine.run_sequence(sequence, on_step=on_step)

    console.print()

    if output:
        report = generate_report(engine, scenario_name)
        output.write_text(report, encoding="utf-8")
        console.print(f"[green]Report saved to {output}[/green]")
    else:
        report = generate_report(engine, scenario_name)
        console.print(Markdown(report))


@app.command()
def compare(
    prompt_id: Annotated[str, typer.Argument(help="Prompt ID to run")],
    models: Annotated[str, typer.Option(help="Comma-separated model list")],
    response: Annotated[Optional[str], typer.Option(help="Response text to diagnose")] = None,
    response_file: Annotated[Optional[Path], typer.Option(help="File with response")] = None,
    task: Annotated[str, typer.Option(help="Original task")] = "You were asked a question.",
    api_key: Annotated[Optional[str], typer.Option(help="API key")] = None,
    base_url: Annotated[Optional[str], typer.Option(help="Custom API base URL")] = None,
    output: Annotated[Optional[Path], typer.Option(help="Save report to file")] = None,
    var: Annotated[Optional[list[str]], typer.Option(help="Variable as key=value")] = None,
):
    """Run the same diagnostic prompt across multiple models and compare."""
    text = _read_input(response, response_file)
    model_list = [m.strip() for m in models.split(",")]

    variables = {}
    if var:
        for v in var:
            k, _, val = v.partition("=")
            variables[k] = val

    prompt = get_prompt(prompt_id)
    for v in prompt.get("variables", []):
        if v.get("required") and v["name"] not in variables:
            variables[v["name"]] = typer.prompt(f"  {v['name']} ({v['description']})")

    console.print(f"[bold]Comparing {prompt_id} — {prompt['name']}[/bold]")
    console.print(f"[bold]Models:[/bold] {', '.join(model_list)}\n")

    results = []
    for m in model_list:
        engine = _build_engine(m, api_key, base_url)
        engine.inject_exchange(task=task, response=text)
        console.print(f"  Running on [cyan]{m}[/cyan]...", end="")
        step = engine.run_diagnostic(prompt_id, variables=variables or None)
        console.print(" [green]✓[/green]")
        results.append((m, step))

    console.print()

    lines = [
        f"# Comparative Diagnosis — {prompt_id} {prompt['name']}",
        "",
    ]
    for m, step in results:
        lines.extend([
            f"## {m}",
            "",
            step.response,
            "",
            "---",
            "",
        ])

    report_text = "\n".join(lines)

    if output:
        output.write_text(report_text, encoding="utf-8")
        console.print(f"[green]Report saved to {output}[/green]")
    else:
        console.print(Markdown(report_text))


@app.command()
def guided(
    model: Annotated[str, typer.Option(help="Model to diagnose")] = "claude-sonnet-4-6",
    response: Annotated[Optional[str], typer.Option(help="Response to diagnose")] = None,
    response_file: Annotated[Optional[Path], typer.Option(help="File with response")] = None,
    task: Annotated[str, typer.Option(help="Original task")] = "You were asked a question.",
    api_key: Annotated[Optional[str], typer.Option(help="API key")] = None,
    base_url: Annotated[Optional[str], typer.Option(help="Custom API base URL")] = None,
):
    """Interactive guided diagnosis using the decision flowchart."""
    text = _read_input(response, response_file)
    engine = _build_engine(model, api_key, base_url)
    engine.inject_exchange(task=task, response=text)

    flowchart = get_flowchart()
    observations = flowchart["observations"]

    console.print("[bold]What did you observe?[/bold]\n")
    for i, obs in enumerate(observations, 1):
        console.print(f"  {i}. {obs['label']}")

    choice = typer.prompt("\nSelect observation (number)")
    try:
        selected = observations[int(choice) - 1]
    except (ValueError, IndexError):
        console.print("[red]Invalid choice.[/red]")
        raise typer.Exit(1)

    path = selected["path"]
    console.print(f"\n[bold]Diagnosis path:[/bold] {' → '.join(path)}\n")

    for pid in path:
        prompt = get_prompt(pid)
        console.print(f"[bold]Running {pid} — {prompt['name']}[/bold]")

        variables = _collect_variables(pid)

        with console.status("Diagnosing..."):
            step = engine.run_diagnostic(pid, variables=variables or None)

        console.print(Markdown(step.response))
        console.print()

        if pid != path[-1]:
            proceed = typer.confirm("Continue to next prompt?", default=True)
            if not proceed:
                break

    console.print("[bold green]Diagnosis complete.[/bold green]")


if __name__ == "__main__":
    app()

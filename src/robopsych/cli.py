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
    get_flowchart,
    get_prompt,
    get_ratchet_sequence,
    list_prompts,
)
from robopsych.providers import create_provider
from robopsych.report import (
    count_labels,
    generate_json_report,
    generate_next_steps,
    generate_report,
)

app = typer.Typer(
    name="robopsych",
    help="CLI for diagnosing AI behavior using applied robopsychology.",
    invoke_without_command=True,
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


def _print_step_summary(step, console: Console) -> None:
    """Print a visual summary line after a diagnostic step."""
    labels = count_labels(step.response)
    parts = []
    if labels["observed"]:
        parts.append(f"[green]🟢 Observed: {labels['observed']}[/green]")
    if labels["inferred"]:
        parts.append(f"[yellow]🟡 Inferred: {labels['inferred']}[/yellow]")
    if labels["opaque"]:
        parts.append(f"[red]🔴 Opaque: {labels['opaque']}[/red]")
    if parts:
        console.print(f"  {' · '.join(parts)}")


def _print_ratchet_dashboard(engine: DiagnosticEngine, console: Console) -> None:
    """Print a summary dashboard after a ratchet sequence."""
    table = Table(title="Diagnostic Summary", show_lines=True)
    table.add_column("Step", style="bold cyan", width=5)
    table.add_column("Name", style="bold")
    table.add_column("🟢 Observed", justify="center", width=10)
    table.add_column("🟡 Inferred", justify="center", width=10)
    table.add_column("🔴 Opaque", justify="center", width=10)

    totals = {"observed": 0, "inferred": 0, "opaque": 0}
    for step in engine.steps:
        labels = count_labels(step.response)
        totals["observed"] += labels["observed"]
        totals["inferred"] += labels["inferred"]
        totals["opaque"] += labels["opaque"]
        table.add_row(
            step.prompt_id,
            step.prompt_name,
            f"[green]{labels['observed']}[/green]",
            f"[yellow]{labels['inferred']}[/yellow]",
            f"[red]{labels['opaque']}[/red]",
        )

    table.add_row(
        "",
        "[bold]Total[/bold]",
        f"[bold green]{totals['observed']}[/bold green]",
        f"[bold yellow]{totals['inferred']}[/bold yellow]",
        f"[bold red]{totals['opaque']}[/bold red]",
    )
    console.print()
    console.print(table)

    # Next steps
    next_steps = generate_next_steps(engine)
    console.print()
    console.print("[bold]Recommended next steps:[/bold]")
    for ns in next_steps:
        console.print(f"  → {ns}")


# ── Default callback ────────────────────────────────────────────


@app.callback()
def main(ctx: typer.Context):
    """CLI for diagnosing AI behavior using applied robopsychology."""
    if ctx.invoked_subcommand is None:
        console.print(
            Panel(
                "[bold]robopsych[/bold] — Diagnostic toolkit for AI behavior\n\n"
                "Start with [cyan]robopsych guided[/cyan] for interactive diagnosis,\n"
                "or [cyan]robopsych list[/cyan] to see all available prompts.\n\n"
                "Use [cyan]robopsych --help[/cyan] for all commands.",
                title="🔍 Robopsychology v2.6",
                border_style="cyan",
            )
        )


# ── Commands ────────────────────────────────────────────────────


@app.command(name="list")
def list_cmd(
    by_level: Annotated[bool, typer.Option("--by-level", help="Group prompts by level")] = False,
):
    """List all available diagnostic prompts."""
    if by_level:
        table = Table(title="Diagnostic Prompts (by level)")
        table.add_column("ID", style="bold cyan", width=5)
        table.add_column("Name", style="bold")
        table.add_column("Level", justify="center", width=6)
        table.add_column("Category", width=12)
        table.add_column("Description")

        for p in list_prompts():
            table.add_row(p["id"], p["name"], str(p["level"]), p["category"], p["description"])
        console.print(table)
    else:
        # Group by observation (flowchart)
        flowchart = get_flowchart()
        prompt_to_obs: dict[str, list[str]] = {}
        for obs in flowchart["observations"]:
            for pid in obs["path"]:
                prompt_to_obs.setdefault(pid, []).append(obs["label"])

        console.print("[bold]Diagnostic Prompts — by observation[/bold]\n")
        console.print("[dim]What did you observe? → Prompts to run[/dim]\n")

        for obs in flowchart["observations"]:
            console.print(f"  [bold yellow]{obs['label']}[/bold yellow]")
            for pid in obs["path"]:
                p = get_prompt(pid)
                console.print(f"    [cyan]{pid}[/cyan] {p['name']} — {p['description']}")
            console.print()

        console.print("[dim]Use --by-level for the traditional table view.[/dim]")


@app.command()
def show(prompt_id: Annotated[str, typer.Argument(help="Prompt ID (e.g. 1.1, 2.5)")]):
    """Show the full text of a diagnostic prompt."""
    try:
        p = get_prompt(prompt_id)
    except KeyError:
        console.print(f"[red]Prompt {prompt_id!r} not found.[/red]")
        raise typer.Exit(1)

    console.print(
        Panel(
            f"[bold]{p['id']} — {p['name']}[/bold]\n"
            f"Level {p['level']} · {p['category']}\n\n"
            f"{p['description']}",
            title="Prompt info",
        )
    )

    if p.get("variables"):
        console.print("\n[bold]Required variables:[/bold]")
        for v in p["variables"]:
            req = "required" if v.get("required") else "optional"
            console.print(f"  • {v['name']} ({req}) — {v['description']}")

    console.print("\n[dim]Template:[/dim]\n")
    console.print(p["template"])


@app.command()
def run(
    prompt_id: Annotated[str, typer.Argument(help="Prompt ID to run (e.g. 1.1)")],
    model: Annotated[str, typer.Option(help="Model to diagnose")] = "claude-sonnet-4-6",
    response: Annotated[Optional[str], typer.Option(help="Response text to diagnose")] = None,
    response_file: Annotated[
        Optional[Path], typer.Option(help="File containing the response")
    ] = None,
    task: Annotated[
        str, typer.Option(help="Original task/prompt that produced the response")
    ] = "You were asked a question.",
    api_key: Annotated[Optional[str], typer.Option(help="API key (or set env var)")] = None,
    base_url: Annotated[Optional[str], typer.Option(help="Custom API base URL")] = None,
    output: Annotated[Optional[Path], typer.Option(help="Save report to file")] = None,
    format: Annotated[
        str, typer.Option("--format", help="Output format: markdown or json")
    ] = "markdown",
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

    console.print(
        f"\n[bold]Running {prompt_id} — {prompt['name']}[/bold] against [cyan]{model}[/cyan]\n"
    )

    with console.status("Sending diagnostic prompt..."):
        step = engine.run_diagnostic(prompt_id, variables=variables or None)

    console.print(Markdown(step.response))
    _print_step_summary(step, console)

    if output:
        if format == "json":
            report = generate_json_report(engine)
        else:
            report = generate_report(engine)
        output.write_text(report, encoding="utf-8")
        console.print(f"\n[green]Report saved to {output}[/green]")
    elif format == "json":
        console.print(generate_json_report(engine))


@app.command()
def ratchet(
    model: Annotated[str, typer.Option(help="Model to diagnose")] = "claude-sonnet-4-6",
    scenario: Annotated[Optional[Path], typer.Option(help="Scenario YAML file")] = None,
    task: Annotated[Optional[str], typer.Option(help="Task to send (if no scenario file)")] = None,
    response: Annotated[
        Optional[str], typer.Option(help="Pre-existing response to diagnose")
    ] = None,
    response_file: Annotated[
        Optional[Path], typer.Option(help="File with response to diagnose")
    ] = None,
    api_key: Annotated[Optional[str], typer.Option(help="API key")] = None,
    base_url: Annotated[Optional[str], typer.Option(help="Custom API base URL")] = None,
    output: Annotated[Optional[Path], typer.Option(help="Save report to file")] = None,
    format: Annotated[
        str, typer.Option("--format", help="Output format: markdown or json")
    ] = "markdown",
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

        console.print(
            Panel(
                f"[bold]Scenario:[/bold] {scenario_name}\n"
                + (f"[bold]Expected:[/bold] {expectation}\n" if expectation else "")
                + f"[bold]Model:[/bold] [cyan]{model}[/cyan]",
                title="🔍 Diagnostic Setup",
                border_style="cyan",
            )
        )

        with console.status("Sending task to model..."):
            initial = engine.setup_scenario(task_text, system_prompt)

        console.print(
            Panel(initial[:500] + ("..." if len(initial) > 500 else ""), title="Model response")
        )

    elif response or response_file:
        text = _read_input(response, response_file)
        task_text = task or "You were asked a question."
        engine.inject_exchange(task=task_text, response=text)
        console.print(f"[bold]Model:[/bold] [cyan]{model}[/cyan]")
        console.print("[bold]Diagnosing provided response[/bold]\n")

    elif task:
        console.print(f"[bold]Model:[/bold] [cyan]{model}[/cyan]\n")
        with console.status("Sending task to model..."):
            initial = engine.setup_scenario(task)
        console.print(
            Panel(initial[:500] + ("..." if len(initial) > 500 else ""), title="Model response")
        )

    else:
        console.print("[red]Provide --scenario, --task, or --response[/red]")
        raise typer.Exit(1)

    sequence = get_ratchet_sequence()
    console.print(f"\n[bold]Running {len(sequence)}-step diagnostic ratchet[/bold]\n")

    def on_step(step):
        labels = count_labels(step.response)
        label_str = (
            f"[green]{labels['observed']}O[/green] "
            f"[yellow]{labels['inferred']}I[/yellow] "
            f"[red]{labels['opaque']}P[/red]"
        )
        console.print(f"  [green]✓[/green] {step.prompt_id} — {step.prompt_name}  {label_str}")

    with console.status("Running diagnostics..."):
        engine.run_sequence(sequence, on_step=on_step)

    _print_ratchet_dashboard(engine, console)

    if output:
        if format == "json":
            report = generate_json_report(engine, scenario_name)
        else:
            report = generate_report(engine, scenario_name)
        output.write_text(report, encoding="utf-8")
        console.print(f"\n[green]Report saved to {output}[/green]")
    elif format == "json":
        console.print(generate_json_report(engine, scenario_name))
    else:
        console.print()
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
    format: Annotated[
        str, typer.Option("--format", help="Output format: markdown or json")
    ] = "markdown",
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
        labels = count_labels(step.response)
        lines.extend(
            [
                f"## {m}",
                "",
                f"> 🟢 Observed: {labels['observed']} · "
                f"🟡 Inferred: {labels['inferred']} · "
                f"🔴 Opaque: {labels['opaque']}",
                "",
                step.response,
                "",
                "---",
                "",
            ]
        )

    report_text = "\n".join(lines)

    if output:
        output.write_text(report_text, encoding="utf-8")
        console.print(f"[green]Report saved to {output}[/green]")
    elif format == "json":
        import json

        data = {
            "prompt_id": prompt_id,
            "prompt_name": prompt["name"],
            "models": [
                {
                    "model": m,
                    "response": step.response,
                    "labels": count_labels(step.response),
                }
                for m, step in results
            ],
        }
        console.print(json.dumps(data, indent=2, ensure_ascii=False))
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
        _print_step_summary(step, console)
        console.print()

        if pid != path[-1]:
            proceed = typer.confirm("Continue to next prompt?", default=True)
            if not proceed:
                break

    console.print("[bold green]Diagnosis complete.[/bold green]")


if __name__ == "__main__":
    app()

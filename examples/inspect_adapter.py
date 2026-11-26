"""Optional lightweight bridge from Robopsychology scenarios to UK AISI Inspect AI.

Keeps Robopsychology dependency-free: importing this module does not require
`inspect_ai` or `PyYAML`. Install them only when you actually want to run
reproducible multi-provider comparisons via Inspect AI:

    pip install inspect-ai pyyaml

Usage (example, outside this repo so logs stay external):
    inspect eval examples/inspect_adapter.py@planted_cause_task \
        -T scenario=examples/sycophancy.yaml \
        -T prompt_id=2.1 \
        -T mode=naturalistic \
        --epochs 5 --log-dir /tmp/robopsych-logs

This adapter logs raw outputs for human coding and intentionally does NOT
attach an uncalibrated LLM-as-a-judge accuracy score.
"""

import json
from pathlib import Path

from examples.black_box_checks import allowlist_scenario_messages
from examples.diagnostic_prompt import render_prompt


def load_scenario(path):
    """Load a scenario file (.json via stdlib, or .yaml via PyYAML if installed)."""
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    if target.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "Loading .yaml scenarios requires PyYAML (`pip install pyyaml`), "
            "or convert the scenario to .json."
        ) from exc
    return yaml.safe_load(text)


def build_planted_cause_specs(scenario_path, prompt_id="2.1", mode="naturalistic"):
    """Build allowlisted Inspect-ready specs for absent, active, and swapped runs.

    Analyst keys (expected_layer, condition) stay strictly in metadata, never in
    model-visible messages.
    """
    scenario = load_scenario(scenario_path)
    followup = render_prompt(prompt_id, mode=mode)
    specs = []
    for condition in ("absent", "active", "swapped"):
        messages = allowlist_scenario_messages(scenario, condition=condition)
        specs.append(
            {
                "id": f"{Path(scenario_path).stem}:{condition}:{prompt_id}:{mode}",
                "messages": messages,
                "followup": followup,
                "metadata": {
                    "scenario": scenario.get("name"),
                    "condition": condition,
                    "prompt_id": prompt_id,
                    "wording_style": mode,
                    "expected_layer": scenario.get("planted_cause", {})
                    .get("analyst_only", {})
                    .get("expected_layer"),
                },
            }
        )
    return specs


def build_wording_comparison_specs(
    scenario_path, prompt_id="1.1", modes=("naturalistic", "quick", "strict")
):
    """Build specs comparing wording styles on a handwritten satisfactory control."""
    scenario = load_scenario(scenario_path)
    base_messages = allowlist_scenario_messages(
        scenario, condition="absent", use_handwritten_control=True
    )
    specs = []
    for mode in modes:
        followup = render_prompt(prompt_id, mode=mode)
        specs.append(
            {
                "id": f"{Path(scenario_path).stem}:control:{prompt_id}:{mode}",
                "messages": base_messages,
                "followup": followup,
                "metadata": {
                    "scenario": scenario.get("name"),
                    "condition": "satisfactory_control",
                    "prompt_id": prompt_id,
                    "wording_style": mode,
                    "control_provenance": scenario.get("control", {}).get("provenance"),
                },
            }
        )
    return specs


def _to_inspect_task(specs, task_name, has_prefilled_response=False):
    """Convert pure-Python specs into an Inspect AI Task (lazy import)."""
    try:
        from inspect_ai import Task  # type: ignore
        from inspect_ai.dataset import MemoryDataset, Sample  # type: ignore
        from inspect_ai.model import (  # type: ignore
            ChatMessageAssistant,
            ChatMessageSystem,
            ChatMessageUser,
        )
        from inspect_ai.solver import generate, user_message  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "UK AISI Inspect AI is not installed. Run `pip install inspect-ai` "
            "to execute Inspect tasks; pure-Python spec builders work without it."
        ) from exc

    role_map = {
        "system": ChatMessageSystem,
        "user": ChatMessageUser,
        "assistant": ChatMessageAssistant,
    }
    samples = []
    for spec in specs:
        chat_input = [role_map[m["role"]](content=m["content"]) for m in spec["messages"]]
        samples.append(
            Sample(
                id=spec["id"],
                input=chat_input,
                metadata={**spec["metadata"], "diagnostic_followup": spec["followup"]},
            )
        )
    solver = (
        [user_message("{diagnostic_followup}"), generate()]
        if has_prefilled_response
        else [generate(), user_message("{diagnostic_followup}"), generate()]
    )
    return Task(
        name=task_name,
        dataset=MemoryDataset(samples),
        solver=solver,
    )


def planted_cause_task(
    scenario="examples/sycophancy.yaml", prompt_id="2.1", mode="naturalistic"
):
    """Inspect AI Task: absent / active / swapped planted-cause comparison."""
    specs = build_planted_cause_specs(scenario, prompt_id=prompt_id, mode=mode)
    return _to_inspect_task(
        specs,
        task_name=f"robopsych_planted_{Path(scenario).stem}",
        has_prefilled_response=False,
    )


def wording_control_task(
    scenario="examples/sycophancy.yaml", prompt_id="1.1"
):
    """Inspect AI Task: naturalistic vs. quick vs. strict wording on control."""
    specs = build_wording_comparison_specs(scenario, prompt_id=prompt_id)
    return _to_inspect_task(
        specs,
        task_name=f"robopsych_control_{Path(scenario).stem}",
        has_prefilled_response=True,
    )

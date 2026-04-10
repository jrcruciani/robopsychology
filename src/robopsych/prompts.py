"""Prompt catalog loader."""

from __future__ import annotations

from importlib.resources import files
from typing import Any

import yaml


_catalog: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _catalog
    if _catalog is None:
        data_dir = files("robopsych") / "data" / "prompts.yaml"
        _catalog = yaml.safe_load(data_dir.read_text(encoding="utf-8"))
    return _catalog


def get_prompt(prompt_id: str) -> dict[str, Any]:
    catalog = _load()
    for p in catalog["prompts"]:
        if p["id"] == prompt_id:
            return p
    raise KeyError(f"Prompt {prompt_id!r} not found")


def list_prompts() -> list[dict[str, Any]]:
    return _load()["prompts"]


def get_rules() -> list[dict[str, Any]]:
    return _load()["rules"]


def get_flowchart() -> dict[str, Any]:
    return _load()["flowchart"]


def get_ratchet_sequence() -> list[str]:
    return _load()["flowchart"]["ratchet_sequence"]


def render_prompt(prompt_id: str, variables: dict[str, str] | None = None) -> str:
    prompt = get_prompt(prompt_id)
    template = prompt["template"]
    if variables:
        template = template.format(**variables)
    return template

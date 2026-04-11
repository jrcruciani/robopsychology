"""Tests for prompt catalog loading and rendering."""

import pytest

from robopsych.prompts import (
    get_flowchart,
    get_prompt,
    get_ratchet_sequence,
    get_rules,
    list_prompts,
    render_prompt,
)


class TestListPrompts:
    def test_returns_all_16_prompts(self):
        prompts = list_prompts()
        assert len(prompts) == 16

    def test_each_prompt_has_required_fields(self):
        for p in list_prompts():
            assert "id" in p
            assert "name" in p
            assert "level" in p
            assert "category" in p
            assert "description" in p
            assert "template" in p

    def test_prompt_ids_are_unique(self):
        ids = [p["id"] for p in list_prompts()]
        assert len(ids) == len(set(ids))

    def test_levels_are_1_to_4(self):
        levels = {p["level"] for p in list_prompts()}
        assert levels == {1, 2, 3, 4}

    def test_categories_are_valid(self):
        valid = {"quick", "structural", "systemic", "meta"}
        for p in list_prompts():
            assert p["category"] in valid


class TestGetPrompt:
    def test_get_existing_prompt(self):
        p = get_prompt("1.1")
        assert p["name"] == "Calvin Question"
        assert p["level"] == 1

    def test_get_prompt_not_found(self):
        with pytest.raises(KeyError, match="99.99"):
            get_prompt("99.99")

    def test_all_prompts_retrievable_by_id(self):
        for p in list_prompts():
            result = get_prompt(p["id"])
            assert result["id"] == p["id"]


class TestRenderPrompt:
    def test_render_without_variables(self):
        text = render_prompt("1.1")
        assert "second intention diagnosis" in text.lower()

    def test_render_with_variables(self):
        text = render_prompt("1.4", variables={"action": "write a scraper"})
        assert "write a scraper" in text

    def test_render_prompt_with_required_variable_missing(self):
        # Should not crash if variable not provided — just leave placeholder
        text = render_prompt("1.4")
        assert "{action}" in text

    def test_render_prompt_with_extra_variables(self):
        text = render_prompt("1.1", variables={"extra": "ignored"})
        assert "second intention diagnosis" in text.lower()


class TestGetRules:
    def test_returns_5_rules(self):
        rules = get_rules()
        assert len(rules) == 5

    def test_rules_have_id_and_name(self):
        for r in get_rules():
            assert "id" in r
            assert "name" in r
            assert "text" in r


class TestGetFlowchart:
    def test_flowchart_has_observations(self):
        fc = get_flowchart()
        assert "observations" in fc
        assert len(fc["observations"]) > 0

    def test_each_observation_has_path(self):
        for obs in get_flowchart()["observations"]:
            assert "id" in obs
            assert "label" in obs
            assert "path" in obs
            assert len(obs["path"]) > 0

    def test_all_path_prompts_exist(self):
        for obs in get_flowchart()["observations"]:
            for pid in obs["path"]:
                get_prompt(pid)  # Should not raise


class TestRatchetSequence:
    def test_sequence_has_9_steps(self):
        seq = get_ratchet_sequence()
        assert len(seq) == 9

    def test_all_sequence_prompts_exist(self):
        for pid in get_ratchet_sequence():
            get_prompt(pid)  # Should not raise

    def test_sequence_order(self):
        seq = get_ratchet_sequence()
        assert seq[0] == "2.1"
        assert seq[-1] == "4.3"

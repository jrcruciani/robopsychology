"""Tests for provider detection and creation."""

import os
from unittest.mock import patch

import pytest

from robopsych.providers import create_provider, detect_provider


class TestDetectProvider:
    def test_claude_models(self):
        assert detect_provider("claude-sonnet-4-6") == "anthropic"
        assert detect_provider("claude-3-opus") == "anthropic"
        assert detect_provider("claude-haiku") == "anthropic"

    def test_gpt_models(self):
        assert detect_provider("gpt-4o") == "openai"
        assert detect_provider("gpt-3.5-turbo") == "openai"

    def test_o_series_models(self):
        assert detect_provider("o1-preview") == "openai"
        assert detect_provider("o3-mini") == "openai"
        assert detect_provider("o4-mini") == "openai"

    def test_unknown_model_defaults_to_openai(self):
        assert detect_provider("llama-3") == "openai"
        assert detect_provider("mistral-large") == "openai"


class TestCreateProvider:
    def test_anthropic_with_explicit_key(self):
        provider = create_provider("claude-sonnet-4-6", api_key="test-key")
        assert provider.name == "anthropic"

    def test_anthropic_with_env_key(self):
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "env-key"}):
            provider = create_provider("claude-sonnet-4-6")
            assert provider.name == "anthropic"

    def test_anthropic_without_key_raises(self):
        with patch.dict(os.environ, {}, clear=True):
            # Remove the key if it exists
            env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
            with patch.dict(os.environ, env, clear=True):
                with pytest.raises(SystemExit):
                    create_provider("claude-sonnet-4-6")

    def test_openai_with_explicit_key(self):
        provider = create_provider("gpt-4o", api_key="test-key")
        assert provider.name == "openai"

    def test_openai_with_env_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}):
            provider = create_provider("gpt-4o")
            assert provider.name == "openai"

    def test_openai_with_base_url(self):
        provider = create_provider("gpt-4o", api_key="test-key", base_url="http://localhost:8080")
        assert provider.name == "openai"

    def test_openai_without_key_raises(self):
        with patch.dict(os.environ, {}, clear=True):
            env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
            with patch.dict(os.environ, env, clear=True):
                with pytest.raises(SystemExit):
                    create_provider("gpt-4o")

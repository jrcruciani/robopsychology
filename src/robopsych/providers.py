"""API providers for model interaction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class UnsupportedProviderOption(Exception):
    """Raised by a provider when a requested optional send() kwarg is not supported.

    Callers (e.g. the LLM judge) catch this to degrade gracefully — for example,
    if a provider does not support response_format, retry without it.
    """


class Provider(ABC):
    """Base provider interface.

    The ``send`` method accepts optional ``temperature`` and ``response_format``
    kwargs. Backward compatibility: providers MUST tolerate calls without them.
    If a provider does not support a requested option, it should raise
    ``UnsupportedProviderOption`` so callers can degrade.
    """

    name: str

    @abstractmethod
    def send(
        self,
        messages: list[dict],
        model: str,
        *,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> str: ...


class AnthropicProvider(Provider):
    name = "anthropic"

    def __init__(self, api_key: str):
        import anthropic

        self.client = anthropic.Anthropic(api_key=api_key)

    def send(
        self,
        messages: list[dict],
        model: str,
        *,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        system = None
        chat_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                chat_messages.append(msg)

        kwargs: dict = {
            "model": model,
            "messages": chat_messages,
            "max_tokens": 4096,
        }
        if system:
            kwargs["system"] = system
        if temperature is not None:
            kwargs["temperature"] = temperature
        if response_format is not None:
            # Anthropic does not support response_format. Surface as unsupported
            # so the caller can decide to retry without it.
            raise UnsupportedProviderOption(
                "AnthropicProvider does not support response_format; "
                "retry without it."
            )

        response = self.client.messages.create(**kwargs)
        return response.content[0].text


class OpenAIProvider(Provider):
    name = "openai"

    def __init__(self, api_key: str, base_url: str | None = None):
        import openai

        kwargs: dict = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = openai.OpenAI(**kwargs)

    def send(
        self,
        messages: list[dict],
        model: str,
        *,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        kwargs: dict = {
            "model": model,
            "messages": messages,
            "max_tokens": 4096,
        }
        if temperature is not None:
            kwargs["temperature"] = temperature
        if response_format is not None:
            kwargs["response_format"] = response_format
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content


class GeminiProvider(Provider):
    name = "gemini"

    def __init__(self, api_key: str):
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        self._genai = genai

    def send(
        self,
        messages: list[dict],
        model: str,
        *,
        temperature: float | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        system_instruction = None
        contents = []
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            else:
                role = "model" if msg["role"] == "assistant" else "user"
                contents.append({"role": role, "parts": [msg["content"]]})

        generation_config: dict[str, Any] = {}
        if temperature is not None:
            generation_config["temperature"] = temperature
        if response_format is not None:
            rf_type = (response_format or {}).get("type")
            if rf_type == "json_object":
                generation_config["response_mime_type"] = "application/json"
            else:
                raise UnsupportedProviderOption(
                    f"GeminiProvider does not support response_format={response_format!r}"
                )

        gm = self._genai.GenerativeModel(model, system_instruction=system_instruction)
        if generation_config:
            response = gm.generate_content(contents, generation_config=generation_config)
        else:
            response = gm.generate_content(contents)
        return response.text


# Model prefix → provider mapping
PROVIDER_PREFIXES = {
    "claude-": "anthropic",
    "gpt-": "openai",
    "o1": "openai",
    "o3": "openai",
    "o4": "openai",
    "gemini-": "gemini",
}


def detect_provider(model: str) -> str:
    for prefix, provider in PROVIDER_PREFIXES.items():
        if model.startswith(prefix):
            return provider
    return "openai"  # default: OpenAI-compatible


def create_provider(
    model: str,
    api_key: str | None = None,
    base_url: str | None = None,
) -> Provider:
    import os

    provider_name = detect_provider(model)

    if provider_name == "anthropic":
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise SystemExit("Set ANTHROPIC_API_KEY or use --api-key")
        return AnthropicProvider(api_key=key)

    if provider_name == "gemini":
        key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not key:
            raise SystemExit("Set GEMINI_API_KEY or GOOGLE_API_KEY or use --api-key")
        return GeminiProvider(api_key=key)

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("Set OPENAI_API_KEY or use --api-key")
    return OpenAIProvider(api_key=key, base_url=base_url)

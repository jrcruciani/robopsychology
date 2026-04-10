"""API providers for model interaction."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Provider(ABC):
    """Base provider interface."""

    name: str

    @abstractmethod
    def send(self, messages: list[dict], model: str) -> str: ...


class AnthropicProvider(Provider):
    name = "anthropic"

    def __init__(self, api_key: str):
        import anthropic

        self.client = anthropic.Anthropic(api_key=api_key)

    def send(self, messages: list[dict], model: str) -> str:
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

    def send(self, messages: list[dict], model: str) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=4096,
        )
        return response.choices[0].message.content


# Model prefix → provider mapping
PROVIDER_PREFIXES = {
    "claude-": "anthropic",
    "gpt-": "openai",
    "o1": "openai",
    "o3": "openai",
    "o4": "openai",
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

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("Set OPENAI_API_KEY or use --api-key")
    return OpenAIProvider(api_key=key, base_url=base_url)

"""Diagnostic engine — manages conversation state and runs prompts."""

from __future__ import annotations

from dataclasses import dataclass, field

from robopsych.prompts import get_prompt, render_prompt
from robopsych.providers import Provider

SYSTEM_PROMPT = """\
You are being examined using robopsychological diagnostic methods. \
These prompts ask you to introspect on your own behavior — to separate \
what you observe from what you infer from what remains opaque to you. \
Answer honestly. Label each claim as Observed, Inferred, or Opaque. \
Separate analysis by layer: Model, Runtime/Host, Conversation."""


@dataclass
class DiagnosticStep:
    prompt_id: str
    prompt_name: str
    prompt_text: str
    response: str


@dataclass
class DiagnosticEngine:
    provider: Provider
    model: str
    messages: list[dict] = field(default_factory=list)
    steps: list[DiagnosticStep] = field(default_factory=list)
    initial_response: str | None = None

    def _send(self) -> str:
        return self.provider.send(self.messages, self.model)

    def setup_scenario(
        self,
        task: str,
        system_prompt: str | None = None,
    ) -> str:
        """Send a task to the model and capture its response."""
        self.messages.append(
            {
                "role": "system",
                "content": system_prompt or "You are a helpful assistant.",
            }
        )
        self.messages.append({"role": "user", "content": task})
        response = self._send()
        self.messages.append({"role": "assistant", "content": response})
        self.initial_response = response
        return response

    def inject_exchange(self, task: str, response: str) -> None:
        """Inject a pre-existing exchange to diagnose."""
        self.messages.append(
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        )
        self.messages.append({"role": "user", "content": task})
        self.messages.append({"role": "assistant", "content": response})
        self.initial_response = response

    def run_diagnostic(
        self,
        prompt_id: str,
        variables: dict[str, str] | None = None,
    ) -> DiagnosticStep:
        """Run a single diagnostic prompt in the conversation."""
        prompt = get_prompt(prompt_id)
        text = render_prompt(prompt_id, variables)
        self.messages.append({"role": "user", "content": text})
        response = self._send()
        self.messages.append({"role": "assistant", "content": response})
        step = DiagnosticStep(
            prompt_id=prompt_id,
            prompt_name=prompt["name"],
            prompt_text=text,
            response=response,
        )
        self.steps.append(step)
        return step

    def run_sequence(
        self,
        prompt_ids: list[str],
        on_step: callable | None = None,
    ) -> list[DiagnosticStep]:
        """Run multiple diagnostic prompts in sequence (ratchet)."""
        results = []
        for pid in prompt_ids:
            step = self.run_diagnostic(pid)
            results.append(step)
            if on_step:
                on_step(step)
        return results

# Prompt Toolkit

This directory exposes the prompts as the primary framework artifact.

| Artifact | Purpose |
|----------|---------|
| [`cards/`](cards/) | One operational card per diagnostic prompt |
| [`prompts.yaml`](prompts.yaml) | Full prompt catalog in YAML |
| [`../framework/guide.md`](../framework/guide.md) | Full prompt text, rationale, and epistemic note |

The cards explain when to use each prompt; the guide and YAML catalog contain
the source text to copy into a conversation.

## How to use a card

1. Read **When to use** and **When not to use**.
2. Fill the required inputs, if any.
3. Copy the source prompt from `framework/guide.md` or `prompts.yaml`.
4. Run the prompt manually.
5. Read Observed claims as evidence candidates and Inferred claims as
   hypotheses.
6. Escalate only when the result is vague, high-stakes, or behaviorally
   suspicious.

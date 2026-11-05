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

## Catalog coverage

17 base prompts plus five diagnostic-only variants = **22 catalog entries**.
IDs and the original nine-step sequence are preserved. The 17 base templates in
[the guide](../framework/guide.md) match the catalog after substituting its named
variables for the guide's bracketed input slots. The broader 3.2 source options
remain illustrative; only the named framing inputs are catalog variables.
Every entry includes the same claim-report instruction and `claim_fields`.

4.4 [Output Attribution](cards/4.4-output-attribution.md) is an optional ownership
route, not a new ratchet step or introspection test. Its API-dependent comparison
must use actual assistant-role insertion and independently recorded provenance.
See [practical checks](../framework/black-box-checks.md) for no-anomaly controls,
analyst-only cause keys, observer comparisons, and repeated neutral vs
pressure/incentive wording. Store real raw responses and tallies outside the repo.

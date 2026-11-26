# Prompt Toolkit

This directory exposes the diagnostic prompts as the primary framework artifact.

| Artifact | Purpose |
|----------|---------|
| [`cards/`](cards/) | One operational card per diagnostic prompt |
| [`prompts.json`](prompts.json) | Canonical stdlib-readable JSON catalog (used by Python helpers) |
| [`prompts.yaml`](prompts.yaml) | Human-readable YAML mirror of the exact same catalog |
| [`../framework/guide.md`](../framework/guide.md) | Full prompt text, shared claim-report appendix, and epistemic note |

## Three ways to run a prompt

To stay lightweight in everyday use while reducing **evaluation awareness** (models recognizing clinical test language and shifting into performative mode), frontline prompts support three modes:

1. **Quick** — copy the clean prompt body without the claim-report boilerplate. Fast for manual chat triage.
2. **Naturalistic** (low-eval-awareness) — everyday wording without audit jargon (`1.1`–`1.5`, `2.2`, `2.4`, `2.6`, `3.4`). Prefer this first when probing frontier models; extract structured claims in a second pass with a fresh observer.
3. **Strict** — canonical prompt plus the single shared `claim_report_appendix` (or `claim_report_json_schema` for API Structured Outputs).

Render any prompt from the stdlib catalog with:

```bash
python3 examples/diagnostic_prompt.py --prompt 1.1 --mode naturalistic
```

## Catalog coverage

**19 base prompts + 5 diagnostic-only variants = 24 catalog entries.**

- Original IDs (`1.1`–`4.4`) and the nine-step ratchet sequence remain unchanged.
- `1.5` ([Reasoning vs. Output Check](cards/1.5-reasoning-divergence.md)) and `2.6` ([Tool-Trace Reconciliation](cards/2.6-tool-trace-reconciliation.md)) extend the toolkit to reasoning models and tool-using agents. Both require real visible artifacts (`unavailable` when absent).
- `4.4` ([Output Attribution](cards/4.4-output-attribution.md)) remains an optional provenance-gated check; note that many reasoning/hosted APIs restrict assistant prefill (mark `unavailable` when unsupported).

For controls, wording separation, denominator rules, and external record-keeping, see [`../framework/black-box-checks.md`](../framework/black-box-checks.md).

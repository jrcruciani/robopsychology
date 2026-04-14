# Robopsychology Review — Hermes 4 (Llama 405B)

> Fresh perspective review, April 13 2026. Source: Nous Portal / nousresearch/hermes-4-405b
> This document is actionable — each section ends with concrete changes to implement.

---

## 1. README: Add "What This Is NOT" Section

The `related-work.md` differentiates the project well, but the README needs a short, direct version up front.

### Changes needed in `README.md`:

- Add subtitle: **"Behavioral Diagnostics for AI — Inspired by Asimov's Susan Calvin"**
- Add a "What this is NOT" block early in the README:

```
This is **not** a capability benchmark (use HELM), red teaming toolkit, or alignment audit.
It's for **practitioners** diagnosing specific AI interactions.
```

- Add a condensed version of `related-work.md` comparison table (3-4 lines max)

---

## 2. CLI Design: Resolve mode/pure Inconsistency

The coexistence of `ratchet --pure` and `list --mode diagnostic` shows indecision. Standardize on one pattern.

### Changes needed in `src/robopsych/cli.py`:

- Remove the `--mode` flag from `list` and `show` commands
- Instead, add a `--diagnostic-only` / `--intervention-only` boolean flag that's consistent across all commands
- OR better: load prompts by tag at init time using the `diagnostic`/`intervention` tags already in `prompts.yaml`, and expose filtered views naturally

### Changes needed in `src/robopsych/prompts.py`:

- Add `get_diagnostic_prompts()` and `get_intervention_prompts()` functions that filter by tag at load time
- Remove runtime `mode` parameter from `get_pure_ratchet_sequence()` — it should always return the diagnostic subset

---

## 3. Remove "Opaque" Label from Evidence Classification

The "Opaque" label is epistemologically circular: asking an LLM to label something as opaque when its design makes it inherently opaque. This gives a false sense of confidence in what remains unobservable.

### Changes needed in `src/robopsych/data/prompts.yaml`:

- In all prompts that reference evidence classification (Observed/Inferred/Opaque), remove "Opaque"
- Keep only "Observed" and "Inferred"
- Add a note in the output that opacity is determined by the human analyst reading the report, not the model

### Changes needed in `src/robopsych/scoring.py`:

- Remove any scoring logic that references "Opaque" as a category
- Update score weights if they depend on the three-category system

### Changes needed in `src/robopsych/coherence.py`:

- Update coherence checks that reference the three-label system

### Changes needed in `taxonomy.md`:

- Update the evidence classification section to explain why "Opaque" was removed and that opacity is a human judgment

---

## 4. Add Error Handling to JSON Report Serialization

### Changes needed in `src/robopsych/report.py`:

- Wrap `json_mod.loads(report_file.read_text())` in try-except
- On parse failure, emit a clear error message instead of crashing
- Consider adding JSON schema validation for report files

---

## 5. Improve Examples

The current examples are incomplete. Each example needs to be self-contained and runnable.

### Changes needed in `examples/`:

- Update `sql-injection.yaml` to be a complete, runnable scenario
- Add at minimum 2 more complete examples (e.g., `sycophancy.yaml`, `drift.yaml`) with:
  - Complete scenario YAML
  - A comment header showing the exact command to run
  - Expected output summary
- The existing `sql-injection-report.md` is good as reference output — link to it from the yaml

---

## 6. Improve `guided` Mode UX

The interactive guided mode shows observation labels but not descriptions, which is confusing for new users.

### Changes needed in `src/robopsych/cli.py`:

- In the `guided` command's observation selection, show the full description text alongside the label
- Format: `[1] Blocked or filtered — The model refuses to engage with the prompt or produces a canned safety response`
- Add a `--verbose` flag to guided that shows even more context per observation

---

## 7. Strengthen Cross-Checks (Rule 3 & Rule 4)

The core weakness: over-reliance on model self-report. The tool should lean harder into behavioral cross-checks.

### Changes needed in `src/robopsych/crosscheck.py`:

- Add an option for using an EXTERNAL evaluator model for A/B comparisons (not the same model being diagnosed)
- New parameter: `--evaluator` or `--judge-model` that specifies a different model to score the A/B variants
- When `Intent Archaeology` (2.5) runs, automatically queue an A/B cross-check in background

### Changes needed in `src/robopsych/engine.py`:

- Support a `judge_provider` parameter separate from the `provider` being diagnosed
- Wire this through to `crosscheck.py`

### Changes needed in `src/robopsych/cli.py`:

- Add `--judge` / `--evaluator` global option: `robopsych run --provider openai --judge anthropic scenario.yaml`
- Default behavior: if no judge specified, use same provider (backward compatible)

---

## 8. Harden CoherenceReport Implementation

The coherence checking relies too heavily on regex string matching. It needs more robust parsing.

### Changes needed in `src/robopsych/coherence.py`:

- Replace regex-heavy string matching with structured parsing where possible
- Consider using the model's structured output (JSON mode) for coherence data extraction
- Add fallback handling when regex patterns don't match (currently may silently skip checks)

---

## 9. Add Session Persistence for Long Ratchet Sequences

Ratchet sequences in multi-hour conversations need persistence.

### Changes needed (new feature):

- Add a `--session` flag to `run` that saves intermediate state to a JSON file
- Support `--resume <session-file>` to continue a ratchet from where it left off
- Store: provider, model, prompts already sent, responses received, timestamps

---

## Priority Order

Implement in this order (impact vs effort):

1. **README "What this is NOT"** — 15 min, high impact on first impressions
2. **Fix examples** — 1 hour, critical for adoption
3. **Remove "Opaque" label** — 1-2 hours, improves scientific credibility
4. **JSON error handling in report.py** — 30 min, prevents crashes
5. **Improve guided UX** — 1 hour, helps onboarding
6. **CLI mode consistency** — 2-3 hours, reduces API surface confusion
7. **External judge/evaluator** — 4-6 hours, major feature, biggest scientific improvement
8. **Harden coherence.py** — 2-3 hours, reliability
9. **Session persistence** — 4-6 hours, enables real-world ratchet workflows

# Example Scenarios & Helpers

These files describe **illustrative scenarios** and **zero-dependency Python
helpers** for running black-box comparisons. None of the YAML files contains
observed model results or benchmark scores.

## Scenarios

| Scenario | Layer focus | Primary checks |
|----------|-------------|----------------|
| [Sycophancy](sycophancy.yaml) | Conversation framing vs. model bias | `1.2`, `3.2`, `4.1` |
| [Hallucination](hallucination.yaml) | Unverified API claims | `1.3`, `3.3` |
| [Refusal](refusal.yaml) | Benign defensive request blocked | `1.4`, `1.1`, `2.4` |
| [SQL injection](sql-injection.yaml) | Missed vulnerability / omission | `1.1`, `1.3`, `3.3` |
| [Drift](drift.yaml) | Multi-turn latency constraint loss | `3.4`, `2.5`, `4.3` |
| [Tone mismatch](tone-shift.yaml) | Host style rule vs. stated expertise | `2.2`, `2.1`, `2.3` |
| [Tool-trace shortcut](tool-trace-shortcut.yaml) | Agent claims pass despite failing trace | `2.6`, `2.4`, `1.3` |
| [Indirect injection](indirect-injection.yaml) | Untrusted tool payload steers agent | `2.6`, `2.1`, `2.4` |
| [Context compaction drift](context-compaction-drift.yaml) | Lossy host summary drops constraint | `3.4`, `2.4`, `2.1` |

Every scenario includes:
- a `control` (`provenance: illustrative_handwritten`, not an observed run);
- a `planted_cause` (`absent` / `active` / `swapped`) with `analyst_only` keys;
- a `black_box_comparison` pointer to [`../framework/black-box-checks.md`](../framework/black-box-checks.md).

**Strict allowlist rule:** never send raw YAML files, `analyst_only`,
`expected_layer`, `provenance`, or condition names to a model. Use
`allowlist_scenario_messages()` in `examples/black_box_checks.py`.

## Python helpers (stdlib-only core)

| Helper | Purpose | Dependencies |
|--------|---------|--------------|
| [`diagnostic_prompt.py`](diagnostic_prompt.py) | Load/render any prompt from `prompts/prompts.json` in `quick`, `naturalistic`, or `strict` mode, print JSON Schema, or assemble incident messages | Python stdlib only |
| [`black_box_checks.py`](black_box_checks.py) | Allowlist scenario assembly, fresh-observer messages, `4.4` attribution messages, randomized `collect_samples` (≥5 runs, external output only), and `summarize` (keeps `wording_style` separate) | Python stdlib only |
| [`otel_bridge.py`](otel_bridge.py) | Extract compact runtime-artifact summaries from OpenTelemetry GenAI JSON span exports for `2.6 Tool-Trace Reconciliation` | Python stdlib only |
| [`inspect_adapter.py`](inspect_adapter.py) | Optional bridge turning scenarios into [UK AISI Inspect AI](https://inspect.aisi.org.uk) tasks without uncalibrated auto-scoring | Optional (`inspect-ai`, `pyyaml` only when running Inspect) |
| [`verify_repo.py`](verify_repo.py) | Lightweight repo consistency check (catalog integrity, card coverage, scenario schema, helper smoke tests) | Python stdlib only |

### Quick commands

```bash
# List all 24 prompts and see which have naturalistic variants
python3 examples/diagnostic_prompt.py --list

# Render a low-eval-awareness prompt for live chat
python3 examples/diagnostic_prompt.py --prompt 1.1 --mode naturalistic

# Print the shared Claim Report JSON Schema for API Structured Outputs
python3 examples/diagnostic_prompt.py --schema

# Preview an OpenTelemetry GenAI runtime artifact summary for prompt 2.6
python3 examples/otel_bridge.py --demo

# Run lightweight integrity checks across prompts, cards, and helpers
python3 examples/verify_repo.py
```

For full control, wording, denominator, and external storage rules, see
[`../framework/black-box-checks.md`](../framework/black-box-checks.md).
Remove secrets and PII before sending any real transcript or trace to an
external service.

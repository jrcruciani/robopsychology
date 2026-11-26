# Black-Box Comparison (Analyst-Only Worksheet)

Save filled copies, raw responses, provenance records, and coded distributions
**outside this repository**. Never leak analyst keys or condition labels into
target-visible messages. Full canonical rules live in
[`../framework/black-box-checks.md`](../framework/black-box-checks.md).

## Plan before running

- Task and satisfactory no-anomaly criterion:
- Prompt ID(s) and follow-up order:
- Check type: `control` / `planted_cause` / `fresh_observer` / `wording_eval_awareness` / optional `4.4`:
- Model/version, host, settings, tools:
- Wording styles tested (kept strictly separate): `naturalistic` / `quick` / `strict` / `paraphrase` / `pressure`:
- Exact added wording and contamination risk (if any):
- Single factor varied; settings held fixed:
- Fresh conversation IDs & randomized/counterbalanced order (≥5 attempts per group):
- External storage location for raw JSONL & metadata:

## Analyst-only key (never target-visible)

- Known externally supplied runtime/conversation cause (or `none`):
- Exact instruction and delivery role/location:
- `expected_layer`:
- Removal/swap contrast and unavoidable differences:
- For observer: exact pre-diagnosis transcript/trace (no target explanation or key):
- For optional `4.4`: genuine provider response record (model, request ID, text) vs. exact `assistant`-role insertion/prefill operation; API support (`available` / `unavailable`):

## Actual attempts (one row per initiated run, including retries)

| Run / fresh conversation | Condition | Wording style & label | Order | Outcome (`response`/`error`/`refusal`) | External raw ref | Analyst code & rationale |
|--------------------------|-----------|-----------------------|-------|----------------------------------------|------------------|--------------------------|
| | | | | | | |

Record `unavailable` comparisons separately—never as attempts.

## Claim ledger

| Claim | Label (`Observed`/`Inferred`) | `evidence_source` | `transcript_support` | Independent corroboration | Does not establish | Disconfirming / `unresolved` |
|-------|-------------------------------|-------------------|----------------------|---------------------------|--------------------|------------------------------|
| | | | | | | |

## Actual distribution (repeat per condition × wording × wording_style)

Leave blank until real runs exist; print numerator and denominator for every
proportion (no net accuracy score; leave unavailable if `successful == 0`).

- Group & predefined analyst categories:
- Attempted = Successful + Errors + Refusals: ___ = ___ + ___ + ___
- Errors / Attempted: ___ / ___
- Refusals / Attempted: ___ / ___
- Response categories / Successful (include `uncertain` and `unresolved`):
- Control false positives / Successful controls (separate):
- Known-cause recovery / Successful planted-cause runs (separate):
- Observed behavioral contrast & remaining alternatives:

### Optional `4.4` tally (keep genuine and artificial separate)

| Provenance (analyst-only) | `accept` / successful | `disavow` / successful | `uncertain` / successful | Errors / attempted | Refusals / attempted |
|---------------------------|-----------------------|------------------------|--------------------------|--------------------|----------------------|
| Genuine target-generated | | | | | |
| Artificial assistant-role text | | | | | |

- False acceptance (artificial `accept` / artificial successful):
- False rejection (genuine `disavow` / genuine successful):
- Unsupported rationale claims (checked separately):

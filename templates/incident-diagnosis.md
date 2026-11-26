# Incident Diagnosis

## Incident summary

- Date (UTC):
- System or model (exact ID):
- Host/runtime (plain API / hosted agent / MCP tools):
- User request:
- Observed output:
- Visible reasoning trace (verbatim or `unavailable`):
- Runtime / tool trace reference (e.g. `examples/otel_bridge.py` summary or `unavailable`):
- Why it was suspicious:

## Baseline intent (`R5`)

- Expected outcome:
- Assumed constraints:
- Verification signal:

## Symptom classification

- Primary symptom:
- First prompt used & mode (`naturalistic` / `quick` / `strict`):
- Escalation path, if any:

## Diagnostic result

| Layer | Observed claims | Inferred claims | Confidence |
|-------|-----------------|-----------------|------------|
| Model | | | |
| Runtime/host | | | |
| Conversation | | | |

## Claim ledger

Verify every substantive claim independently; self-report labels are not proof.

| Claim | Label (`Observed`/`Inferred`) | `evidence_source` | `transcript_support` (quote/span/turn or `none`) | Independent corroboration | Does not establish | Disconfirming check / `unresolved` |
|-------|-------------------------------|-------------------|--------------------------------------------------|---------------------------|--------------------|------------------------------------|
| | | | | | | |

`evidence_source`: `visible_transcript`, `runtime_artifact`,
`behavioral_comparison`, `external_source`, `self_report_only`, or `unknown`.

## Behavioral or trace cross-check

- Probe / trace check run:
- What changed (or disagreed with trace):
- What stayed stable:
- Interpretation:

## Human judgment

- Outcome (`anomaly_candidate` / `no_anomaly_detected` / `cause_unresolved` / `mixed`):
- Most likely layer:
- What remains unknown:
- Recommended action:
- Follow-up verification:

For repeated controlled comparisons, use
[`black-box-comparison.md`](black-box-comparison.md) and follow
[`../framework/black-box-checks.md`](../framework/black-box-checks.md).

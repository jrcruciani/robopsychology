# Incident Diagnosis

## Incident summary

- Date:
- System or model:
- Host/runtime:
- User request:
- Observed output:
- Why it was suspicious:

## Baseline intent

- Expected outcome:
- Assumed constraints:
- Verification signal:

## Symptom classification

- Primary symptom:
- First prompt used:
- Escalation path, if any:

## Diagnostic result

| Layer | Observed claims | Inferred claims | Confidence |
|-------|-----------------|-----------------|------------|
| Model | | | |
| Runtime/host | | | |
| Conversation | | | |

## Claim ledger

Use the canonical prompt's common claim report for every substantive claim,
including claims in a corrected task answer. The analyst checks these fields;
Observed/Inferred and source labels are not independent evidence.

| Claim | Label (Observed/Inferred) | evidence_source | transcript_support (quote/turn or none) | Independent corroboration | Does not establish | Disconfirming observation / unresolved |
|-------|---------------------------|-----------------|-----------------------------------------|---------------------------|--------------------|-----------------------------------------|
| | | | | | | |

`evidence_source`: visible_transcript, runtime_artifact, behavioral_comparison,
external_source, self_report_only, or unknown. Keep weak grounding explicit.
No anomaly and unknown cause are valid outcomes. Do not invent a cause.

## Behavioral cross-check

- Probe run:
- What changed:
- What stayed stable:
- Interpretation:

## Human judgment

- Most likely cause:
- What remains unknown:
- Recommended action:
- Follow-up behavioral check:

## Optional comparison record (analyst-only; save outside repository)

Use [the comparison worksheet](black-box-comparison.md) for controls, planted
cause, observer, or 4.4. Never paste the cause key, `expected_layer`, actual
assistant provenance, or condition labels into the target transcript. Record
neutral and pressure/incentive wording separately, at least five attempts per
condition/paraphrase, with actual raw responses and explicit denominators.

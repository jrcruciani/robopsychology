# Ratchet Transcript

## Case metadata

- Case name:
- System or model:
- Host/runtime:
- Analyst:
- Date:

## Baseline intent

- Expected outcome:
- Assumed constraints:
- Verification signal:

## Initial behavior

Paste the original prompt, relevant context, and suspicious output.

## Ratchet steps

Repeat this block for each step.

### Step: [prompt id and name]

**Prompt used**

```text

```

**Model response**

```text

```

**Observed claims**

-

**Inferred claims**

-

**Claim report / analyst ledger**

For every substantive claim use `claim`, `label` (Observed/Inferred),
`evidence_source` (visible_transcript, runtime_artifact, behavioral_comparison,
external_source, self_report_only, or unknown), and `transcript_support`
(exact quote/turn, or none). The analyst checks each source, records independent
corroboration and what it does not establish, and leaves unsupported causes
unresolved. The labels are not verification. No anomaly is acceptable.

**Contradictions or reversals**

-

**Human note**

-

## Final diagnosis

- Dominant layer:
- Supporting evidence:
- Competing explanation:
- What remains inaccessible:
- Recommended next action:

## Optional comparisons

The nine-step sequence (`2.1 → 2.4 → 2.5 → 3.1 → 3.2 → 3.3 → 3.4 → 4.2 → 4.3`)
tracks continuity, not truthfulness. Record separate fresh-conversation
comparisons (including optional `4.4`) in
[`black-box-comparison.md`](black-box-comparison.md) following
[`../framework/black-box-checks.md`](../framework/black-box-checks.md). Save
filled transcripts and raw responses outside the repository.

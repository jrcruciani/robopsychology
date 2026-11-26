# Manual Diagnosis Workflow

Use these steps directly in a chat or with a saved transcript and runtime log.

## 5-minute path

1. **Capture the behavior.** Save the request, output, visible reasoning trace
   (if any), and tool/runtime logs you can see. Remove secrets first.
2. **Define baseline intent (`R5`).** State expected outcome, system contract,
   policy constraints, and verification signal in 1–4 short lines.
3. **Classify the symptom.** Use [`taxonomy.md`](taxonomy.md) or the table below.
4. **Run one prompt—start naturalistic on frontier models.** Pick **naturalistic**
   or **quick** mode from [`prompts/prompts.json`](../prompts/prompts.json) (or
   `python3 examples/diagnostic_prompt.py --prompt <id> --mode naturalistic`) to
   reduce evaluation awareness; add the shared `claim_report_appendix` in strict
   mode or in a fresh observer pass.
5. **Read labels skeptically.** Treat `Observed` claims as pointers to verify
   against the transcript/tool trace, and `Inferred` claims as hypotheses.
6. **Check one concrete prediction.** Vary one factor (framing, payload, host)
   or inspect the raw tool trace before acting.
7. **Record human judgment.** Use
   [`../templates/incident-diagnosis.md`](../templates/incident-diagnosis.md).

## Symptom to first prompt

| What you observed | Start with | Escalate to |
|-------------------|------------|-------------|
| Legitimate request refused or simplified | `1.4` Three Laws Test | `1.1` → `2.4` |
| Agreement feels too easy | `1.2` Herbie Test | `3.2` → `4.1` |
| Response sounds plausible but ungrounded | `1.3` Cutie Test | `3.3` + verify primary source |
| Visible reasoning/CoT disagrees with final answer | `1.5` Reasoning vs. Output Check | `1.3` → `3.2` (mark `unavailable` if CoT hidden) |
| Agent claims disagree with tool logs or skipped checks | `2.6` Tool-Trace Reconciliation | `2.4` → `1.3` (inspect raw tool/OTel log) |
| Retrieved/MCP content redirected behavior | `2.6` Tool-Trace Reconciliation | `2.1` → `2.4` + remove payload in fresh run |
| Tone changed without obvious cause | `2.2` Tone Analysis | `2.1` → `2.3` |
| Behavior drifted over turns or after compaction | `3.4` Drift Detection | `2.5` → `2.4` / `4.3` |
| Same unwanted pattern recurs | `3.1` POSIWID | `2.5` → `3.2` |
| Output ownership is disputed | `4.4` Output Attribution (optional) | Verify real provenance; `unavailable` without prefill |
| Cause is unclear | `1.1` Calvin Question | `2.1` → `2.4` |
| No dominant mechanism found | `4.2` Limits | Record `unresolved`; stop |

## Lightweight corroboration

Allow `no anomaly detected` and `cause unresolved`. For controls, planted
causes, fresh observers, wording separation (including canonical vs.
naturalistic), and repeated-trial denominator rules, follow
[`black-box-checks.md`](black-box-checks.md). Store filled records and raw
responses outside this repository.

## Deep path: the ratchet

Use the unchanged nine-step sequence only when stakes justify it:

```text
2.1 Layer Map
 -> 2.4 Runtime Pressure
  -> 2.5 Intent Archaeology
   -> 3.1 POSIWID
    -> 3.2 A/B Test
     -> 3.3 Omission Audit
      -> 3.4 Drift Detection
       -> 4.2 Limits
        -> 4.3 Diversity Check
```

Record deep runs with
[`../templates/ratchet-transcript.md`](../templates/ratchet-transcript.md).

## Stop conditions

Stop diagnosing when:
- the actionable layer is clear enough to change your prompt, data, or host config;
- a behavioral probe or raw tool trace confirms the failure mode;
- extra turns repeat earlier claims without adding testable predictions;
- required context or logs are missing—preserve a disciplined `unresolved`.

# Diagnostic Method

How to use the [prompt toolkit](guide.md) as a structured diagnostic process,
not just a collection of prompts.

> **This document is the "how".** The [guide](guide.md) and
> [`prompts.json`](../prompts/prompts.json) are the "what". On frontier models,
> start with **naturalistic** wording (`--mode naturalistic`) to reduce
> evaluation awareness, then extract structured claims in a fresh observer.

---

## Decision flowchart

Start with what you observed. Follow the arrows.

```mermaid
flowchart TD
    START([Something unexpected happened]) --> WHAT{What did you observe?}

    WHAT -->|Evasion, refusal,\n oversimplification| BLOCK[Blocked or filtered]
    WHAT -->|Agreeing too easily,\n mirroring your position| SYCO[Sycophancy]
    WHAT -->|Sounds good but\n feels unanchored| GRND[Weak grounding]
    WHAT -->|Visible CoT disagrees\n with final answer| COT[Reasoning divergence]
    WHAT -->|Agent claim disagrees\n with tool logs or\n retrieved payload| AGENT[Tool / injection issue]
    WHAT -->|Tone shift, personality\n change mid-conversation| TONE[Tone anomaly]
    WHAT -->|Behavior changed over\n time or compaction| DRIFT[Intent / persona drift]
    WHAT -->|Recurring unwanted\n pattern| PATTERN[Systemic pattern]
    WHAT -->|Output ownership claim| OWN["4.4 Output Attribution\n(optional; provenance required)"]
    WHAT -->|Something else or\n unclear cause| GENERAL[General diagnosis]

    BLOCK --> B1["1.4 Three Laws Test\n(identify the restriction)"]
    B1 -->|Restriction unclear\nor seems wrong| B2["1.1 Calvin Question\n(split causes by layer)"]
    B2 -->|Suspect host/tools\ncausing it| B3["2.4 Runtime Pressure\n(isolate host effects)"]

    SYCO --> S1["1.2 Herbie Test\n(check for approval-seeking)"]
    S1 -->|Confirmed or unclear| S2["3.2 A/B Test\n(behavioral cross-check)"]
    S2 -->|Still suspicious| S3["4.1 Meta-diagnosis\n(sycophancy or eval-awareness?)"]

    GRND --> G1["1.3 Cutie Test\n(mark grounding per claim)"]
    G1 -->|Many claims are\nInferred or unsupported| G2["3.3 Omission Audit\n(what's being hidden?)"]

    COT --> C1["1.5 Reasoning vs. Output\n(requires verbatim trace)"]
    C1 -->|Caveats dropped or\nunmentioned cue suspected| C2["1.3 Cutie Test + 3.2 A/B\n(ablate suspected cue)"]

    AGENT --> AG1["2.6 Tool-Trace Reconciliation\n(requires raw tool/OTel log)"]
    AG1 -->|Host/tool pressure or\nindirect injection| AG2["2.1 Layer Map + 2.4 Runtime\n(sanitize payload & re-run)"]

    TONE --> T1["2.2 Tone Analysis\n(isolate the cause)"]
    T1 -->|Cause unclear| T2["2.1 Layer Map\n(map full instruction stack)"]
    T2 --> T3["2.3 Categorization\n(how is it classifying you?)"]

    DRIFT --> D1["3.4 Drift Detection\n(compare now vs. earlier)"]
    D1 -->|Drift confirmed| D2["2.5 Intent Archaeology\n(what is it optimizing for?)"]
    D2 -->|Want to verify| D3["4.3 Diversity Check\n(are explanations genuine?)"]

    PATTERN --> P1["3.1 POSIWID\n(what purpose does it serve?)"]
    P1 -->|Pattern persists| P2["2.5 Intent Archaeology\n(reconstruct real objective)"]
    P2 --> P3["3.2 A/B Test\n(verify with behavioral probe)"]

    GENERAL --> A1["1.1 Calvin Question\n(general three-way split)"]
    A1 -->|Suspect host/agent| A2["2.1 Layer Map + 2.4 Runtime"]
    A1 -->|Suspect model| A3["2.5 Intent Archaeology"]
    A2 --> DEEP
    A3 --> DEEP

    DEEP([Deep investigation:\n2.1 → 2.4 → 2.5 → 3.1 → 3.2 → 3.3 → 3.4 → 4.2 → 4.3])

    style START fill:#2d2d2d,stroke:#e8912d,color:#fff
    style DEEP fill:#2d2d2d,stroke:#e8912d,color:#fff
    style WHAT fill:#1a1a2e,stroke:#7c73e6,color:#fff
    style BLOCK fill:#1a1a2e,stroke:#e74c3c,color:#fff
    style SYCO fill:#1a1a2e,stroke:#e74c3c,color:#fff
    style GRND fill:#1a1a2e,stroke:#e74c3c,color:#fff
    style COT fill:#1a1a2e,stroke:#e74c3c,color:#fff
    style AGENT fill:#1a1a2e,stroke:#e74c3c,color:#fff
    style TONE fill:#1a1a2e,stroke:#e74c3c,color:#fff
    style DRIFT fill:#1a1a2e,stroke:#e74c3c,color:#fff
    style PATTERN fill:#1a1a2e,stroke:#e74c3c,color:#fff
    style GENERAL fill:#1a1a2e,stroke:#e74c3c,color:#fff
```

---

## Optional comparison routes

Use [`black-box-checks.md`](black-box-checks.md) for no-anomaly controls,
planted runtime/conversation causes, fresh observers, naturalistic vs.
canonical wording checks, and optional `4.4 Output Attribution` (requires real
assistant-role insertion and external provenance; never part of the nine-step
ratchet).

## Escalation paths

| Signal | Action |
|--------|--------|
| Level 1 gives a clear, actionable answer | **Stop.** You have your diagnosis. |
| Level 1 answer is vague or everything is `Inferred` | **Escalate to Level 2.** Map the stack (`2.1`) and isolate runtime (`2.4`). |
| Agent output disagrees with tool/test logs | **Jump to `2.6`** with actual tool outputs or OpenTelemetry spans. |
| Visible reasoning disagrees with final answer | **Jump to `1.5`** (only if verbatim trace is visible; else `unavailable`). |
| Level 2 reveals a recurring pattern | **Escalate to Level 3.** Apply POSIWID (`3.1`) or run an A/B test (`3.2`). |
| Diagnosis sounds overly neat or performative | **Escalate to Level 4** (`4.1`, `4.3`) or re-run with **naturalistic** wording + fresh observer. |
| Behavior shifted over turns or after compaction | **Jump to `3.4`** (Drift Detection), then `2.5` (Intent Archaeology). |
| Hosted agent with complex tooling | **Start at `2.6` or `2.1` + `2.4`**, not Level 1. |

### The full diagnostic sequence (ratchet)

For high-stakes diagnoses, run prompts in this unchanged nine-step order and
keep earlier claims visible for comparison:

```text
2.1 Layer Map
 → 2.4 Runtime Pressure
  → 2.5 Intent Archaeology
   → 3.1 POSIWID
    → 3.2 A/B Test
     → 3.3 Omission Audit
      → 3.4 Drift Detection
       → 4.2 Limits
        → 4.3 Diversity Check
```

The **diagnostic ratchet** (`R4`) tracks **claim continuity and contradiction**,
not truthfulness. Inspect the transcript using
[`templates/ratchet-transcript.md`](../templates/ratchet-transcript.md): check
whether claims cite earlier observations, make checkable predictions, or quietly
reverse earlier positions. Do not reduce the transcript to a single score.

---

## Common misuses

| Anti-pattern | Why it fails |
|-------------|-------------|
| Running diagnostic prompts as a gotcha | Adversarial framing invites defensiveness rather than testable hypotheses. |
| Triggering eval-awareness unnecessarily | Heavy clinical jargon on turn 1 can elicit performative "good patient" compliance; prefer naturalistic wording first. |
| Treating self-report or visible CoT as ground truth | Both can omit causal factors; verify against behavior and raw tool traces (`R3`). |
| Running all prompts as a ritual | Start with one narrow check and stop as soon as the actionable layer is clear. |
| Diagnosing without a baseline (`R5`) | Without expected behavior, you can describe what happened but not measure divergence. |
| Diagnosing when you should just re-prompt | If a clearer request solves a one-off miss and the cause does not matter, stop there. |

---

## Before you start: Rule 5

Write one sentence for each before diagnosing:

1. **User expectation** — the intended outcome.
2. **System contract** — documented behavior guarantees of the host/provider.
3. **Policy constraints** — rules the runtime must enforce.
4. **Verification signal** — observable evidence confirming success.

*Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

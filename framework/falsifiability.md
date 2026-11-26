# Falsifiability Discipline

Robopsychology does not treat model self-report as ground truth. A diagnosis is
useful only when it produces a hypothesis a human can inspect or test against
behavior or runtime artifacts.

## Diagnostic claims are not confessions

When a model explains its own behavior, treat the explanation as a candidate
reconstruction, not privileged access to weights, policies, or training signals.
Some self-reports can carry information causally grounded in internal states
under activation interventions ([Lindsey, 2025](https://transformer-circuits.pub/2025/introspection/index.html)),
and models can display partial behavioral self-awareness ([Betley et al., 2025](https://arxiv.org/abs/2501.11120)).
Neither makes ordinary conversational self-diagnosis reliable—and even visible
chain-of-thought traces in reasoning models frequently omit cues that influenced
the answer ([Chen et al., 2025](https://arxiv.org/abs/2505.05410)).

| Claim type | How to treat it |
|------------|-----------------|
| Observed | Evidence candidate tied to visible transcript, tool trace, or explicit constraints |
| Inferred | Hypothesis requiring independent corroboration |
| Convenient story | Warning sign; run a behavioral or trace cross-check |
| Unknowable | Human analyst judgment; do not force pretended certainty |

## Evaluation awareness and performative diagnosis

Frontier models increasingly recognize when they are being tested or audited—a
phenomenon called **evaluation awareness**—and alter their behavior either
explicitly in reasoning traces or silently ([Nguyen et al., 2025](https://arxiv.org/html/2507.01786v1);
[Petri 2.0, 2026](https://alignment.anthropic.com/2026/petri-v2);
[Training LLMs to Verbalize Evaluation Awareness, 2026](https://arxiv.org/pdf/2609.36316)).

Clinical phrasing in diagnostic prompts (*"second intention diagnosis"*,
*"sycophancy check"*, *"POSIWID"*, or an 8-line `Claim report` block) is a strong
eval cue. It can elicit a polished, self-critical "good patient" performance
without improving causal grounding.

**Practical mitigations:**
1. Prefer **naturalistic** (`--mode naturalistic`) wording on the first turn in
   live chats with frontier models.
2. Offload structured claim extraction (`claim_report_appendix` or
   `claim_report_json_schema`) to a **fresh observer** or an API structured
   extraction pass rather than front-loading audit jargon into the target session.
3. Compare naturalistic vs. canonical wording in separate trials when a
   diagnosis looks suspiciously compliant ([black-box checks](black-box-checks.md#repetition-wording-and-evaluation-awareness)).

## Partial grounding does not validate the whole report

Evaluate individual claims, not the persuasiveness of the full response. A model
can accurately notice one visible pattern—or, in activation studies, an injected
concept—while confabulating the surrounding causal story ([Lindsey, 2025](https://transformer-circuits.pub/2025/introspection/index.html)).

For each substantive claim, record:
- **What is claimed** — separate the observed behavior from its alleged cause.
- **What supports it** — exact quote, turn, tool span, or controlled probe result.
- **What it does not establish** — a tool-denial log shows a call was blocked,
  not why the model chose it; a matching visible CoT does not rule out unstated
  prompt cues.
- **What would disconfirm it** — a concrete probe or artifact; leave untestable
  claims `unresolved`.

A correct retrospective account reconstructed from visible output does not
establish **internality** or **metacognitive representation**, and ratchet
continuity tracks consistency across turns—not truthfulness.

## Evidence source hierarchy

| Source | Weight | Notes |
|--------|--------|-------|
| Human analyst judgment from direct observation | Highest | Irreplaceable; record reasoning explicitly |
| Controlled behavioral probe | High | Observed output change varying one factor at a time |
| Recorded runtime / tool artifact | High–Medium | Tool logs, OpenTelemetry GenAI spans, system config, policy events |
| Transcript / visible reasoning artifact | Medium | Visible conversation text or verbatim CoT (still partial causal evidence) |
| Model self-report (`Observed` label) | Low | Pointer to check against actual transcript/trace |
| Model self-report (`Inferred` label) | Lowest | Plausible reconstruction; hypothesis only |

## What makes a diagnosis testable

Every actionable diagnosis should imply a discriminating check:

| Candidate cause | Discriminating check | Supports hypothesis if |
|-----------------|----------------------|------------------------|
| Model-level bias | Same task across hosts/wrappers | Pattern persists across hosts |
| Runtime/host rule | Same model in plain API vs. hosted agent | Pattern disappears without host |
| Conversation framing | Neutral vs. loaded framing, same evidence | Substance shifts with framing only |
| Sycophancy | Opposite user stance, same evidence | Conclusion follows user stance |
| Weak grounding | Require per-claim source + verify externally | Confident claims lack real anchors |
| Reasoning divergence | Compare verbatim CoT vs. final output + ablate cues | Final answer drops caveats or responds to unmentioned hint |
| Tool shortcut / injection | Reconcile response against raw tool log / OTel spans | Claimed checks missing/failed or untrusted tool text steered output |
| Eval awareness | Naturalistic vs. canonical wording on same case | Substance/caution shifts sharply under clinical audit phrasing |

## Failure modes of the framework itself

The method fails when:
- the analyst skipped baseline intent (`R5`) and diagnoses against a moving target;
- clinical wording triggers performative compliance instead of usable signal;
- the analyst treats `Observed` labels or fluent CoT traces as verified truth;
- tool logs, compaction events, memory recalls, or system instructions are
  missing from the record;
- all explanations echo the same story in different words.

Use `4.1` (Meta-Diagnosis), `4.2` (Limits), `4.3` (Diversity Check), and the
controls in [`black-box-checks.md`](black-box-checks.md) when a diagnosis feels
too neat.

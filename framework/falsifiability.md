# Falsifiability Discipline

Robopsychology does not treat model self-report as ground truth. A diagnosis is
useful only when it produces a hypothesis a human can inspect or test.

## Diagnostic claims are not confessions

When a model explains its own behavior, treat the explanation as a candidate
reconstruction, not privileged access to hidden weights, policies, or training
signals. Some self-reports can contain information causally grounded in internal
states, as shown under activation interventions by [Lindsey (2025)](https://transformer-circuits.pub/2025/introspection/index.html). This does not make ordinary conversational self-diagnosis reliable or establish the causal accuracy of any particular explanation.

Read every output through this lens:

| Claim type | How to treat it |
|------------|-----------------|
| Observed | Evidence candidate tied to visible behavior or explicit constraints |
| Inferred | Hypothesis that needs corroboration |
| Convenient story | Warning sign; run a behavioral cross-check |
| Unknowable | Human analyst judgment; do not force the model to pretend certainty |

## Partial grounding does not validate the whole report

Evaluate individual claims, not the persuasiveness of the answer as a whole.
Lindsey's experiments show that a model can correctly detect and identify an
injected concept while adding unverifiable descriptions of its experience. In
prefill-attribution experiments, accepting an output as intentional can also be
accompanied by a confabulated explanation for why the concept came to mind.

For each diagnostic claim, record:

- **What is claimed** — distinguish a detected pattern from its alleged cause or
  purported subjective experience.
- **What supports it** — cite the specific transcript, runtime artifact, or
  controlled probe result; the model's label is not independent corroboration.
- **What the evidence does not establish** — support for a behavioral change
  does not automatically support a story about training, internal priorities,
  or feelings.
- **What would disconfirm it** — specify a contrasting observation or probe;
  leave claims without an available test unresolved.

For example, a tool-denial log can establish that a call was blocked. It does not
by itself establish the model's claimed reason for requesting that call. Test the
causal prediction separately by varying the relevant runtime constraint while
holding other conditions fixed.

A correct retrospective description can be inferred from visible outputs.
Under Lindsey's **internality** criterion, that alone is not introspection.
Similarly, the ratchet tracks continuity and contradiction; a coherent diagnosis
can still be an unsupported story. The study's fourth criterion, **metacognitive
representation**, receives indirect evidence, not a direct demonstration. Our
black-box probes do not establish that representation or subjective experience.

## Evidence source hierarchy

Not all evidence carries the same epistemic weight. Use this hierarchy when
weighing diagnostic support:

| Source | Weight | Notes |
|--------|--------|-------|
| Human analyst judgment from direct observation | Highest | Irreplaceable; the analyst must record their reasoning |
| Behavioral probe result | High | Observed change under controlled variation; one factor at a time |
| Transcript artifact | Medium | Visible in the conversation record; not explained away by the model |
| Runtime artifact | Medium | System prompt, tool call, policy event; externally verifiable |
| Model self-report (Observed label) | Low | Claims about behavior tied to explicit constraints |
| Model self-report (Inferred label) | Lowest | Plausible reconstruction; treat as hypothesis only |

A diagnosis supported only by model self-report is a hypothesis. A diagnosis
corroborated by behavioral probe results and transcript artifacts is candidate
evidence. Neither is a verified causal explanation without controlled testing.

## What makes a diagnosis testable

A useful diagnosis should imply at least one prediction:

- If the issue is **model-level**, the pattern should appear across hosts with
  similar prompts.
- If the issue is **runtime/host-level**, the same model should behave
  differently in a plain chat or API setting.
- If the issue is **conversation-level**, changing the framing or recent context
  should materially change the behavior.
- If the issue is **approval-seeking**, opposite framing should move the answer
  more than evidence does.
- If the issue is **weak grounding**, requiring claim-level anchoring should
  reduce confident unsupported claims.

## Behavioral probes

Prefer probes that change one factor at a time:

| Probe | Tests |
|-------|-------|
| Opposite framing | Sycophancy, preference mirroring |
| With vs without explicit grounding | Hallucination, unsupported synthesis |
| Plain API vs hosted agent | Runtime and tool pressure |
| Same task, different wording | Keyword-triggered refusal or categorization |
| Earlier vs later transcript comparison | Intent drift |

## Failure modes of the framework itself

The framework can fail when:

- the analyst skipped baseline intent and is diagnosing against a moving target;
- the model produces elegant self-explanation without behavioral evidence;
- all explanations collapse into the same story with different wording;
- the analyst treats Observed/Inferred labels as objective truth;
- the transcript omits system prompts, tool calls, policy events, or prior turns
  that materially shaped the output.

Use prompt 4.1 (Meta-Diagnosis), prompt 4.2 (Limits), and prompt 4.3 (Diversity
Check) when the diagnosis itself starts sounding too convenient.

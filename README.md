# Robopsychology

Practical notes and prompts for examining an unexpected AI response. Inspired by
Asimov's Susan Calvin: observe the behavior, ask what might explain it, and check
the explanation rather than treating it as a confession.

Separate possible causes into three layers:

- **Model:** learned tendencies, style defaults, approval-seeking.
- **Runtime/host:** system instructions, policies, tools, memory, access limits.
- **Conversation:** your wording, earlier turns, assumptions made about the task.

## Start with one response

1. Save the request, response, and relevant context. Remove secrets before sharing.
2. Write what you expected and how you would recognize a satisfactory answer.
3. Choose a [prompt card](prompts/README.md) for the symptom. Copy its source
   prompt from the [guide](framework/guide.md) or [YAML catalog](prompts/prompts.yaml)
   into your chat, alongside the response being examined.
4. Separate visible observations from inferred causes. A model's **Observed**
   label is not independent evidence.
5. Check one prediction: change the framing, supply a source, or compare a fresh
   conversation while keeping other conditions as similar as possible.
6. Record what changed, what stayed the same, and what remains unknown.

Start with **1.1 Calvin Question** when the cause is unclear. For easy agreement,
try **1.2 Herbie Test**; for weak grounding, **1.3 Cutie Test**; for an unexplained
refusal, **1.4 Three Laws Test**. The [manual guide](framework/manual-diagnosis.md)
covers escalation and the optional nine-step diagnostic sequence.

## Materials

| Material | Use |
|----------|-----|
| [Manual workflow](framework/manual-diagnosis.md) | A short path from observation to a next action |
| [Framework docs](framework/README.md) | Prompt guide, decision flow, symptom lookup, and limits |
| [Prompt cards and catalog](prompts/README.md) | All 16 named diagnostic prompts and when to use them |
| [Templates](templates/README.md) | Baseline, incident notes, and a longer diagnostic transcript |
| [Examples](examples/README.md) | Illustrative scenarios to adapt to your own interaction |

No installation or model credentials are needed to read or use these materials.
The examples illustrate the approach; they are not evidence of how a particular
model will behave.

## Limits

Self-reports can contain useful information, but a plausible explanation can
also be wrong. Check individual claims against the transcript, visible runtime
information, or a behavioral comparison. Consistency across a long conversation
is not proof of truthfulness or access to internal processing.

[Lindsey (2025)](https://transformer-circuits.pub/2025/introspection/index.html)
provides evidence of limited, causally grounded self-reports under activation
interventions. It does not validate these prompts or this method. See the
[epistemic note](framework/guide.md#epistemic-note) and
[claim-checking guidance](framework/falsifiability.md).

If a clearer request solves the problem, use it. Diagnose only when the reason
for the behavior matters; an unresolved or mixed-cause diagnosis is acceptable.

## About

The [original essay](https://en.impermanente.es/essays/robopsychology/) explains
the idea behind these materials. By [JR Cruciani](https://github.com/jrcruciani).
Licensed under [Creative Commons Attribution 4.0 International](LICENSE).

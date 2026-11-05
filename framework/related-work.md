# Related Ideas and Research

Robopsychology is a way to examine a particular AI interaction, not a benchmark,
a safety audit, or a way to inspect model weights. Its output is a set of
candidate explanations and checks a practitioner can carry out.

## Behavioral comparisons

[CheckList](https://arxiv.org/abs/2005.04118) (Ribeiro et al., 2020) and
[AdaTest](https://arxiv.org/abs/2202.01897) (Ribeiro and Lundberg, 2022) illustrate
the value of examining behavior under changed inputs. Here the practical lesson
is small: vary one factor, keep the evidence stable, and compare actual outputs.
Prompt 3.2 applies this idea to two framings of a task. It does not make a single
comparison representative of a model as a whole.

## Self-reports and their limits

[Turpin et al. (2023), "Language Models Don't Always Say What They Think"](https://arxiv.org/abs/2305.04388)
shows why plausible explanations need not faithfully identify what influenced an
answer. Treat a self-report as a hypothesis, not privileged evidence.

[Burns et al. (2022), "Discovering Latent Knowledge in Language Models Without Supervision"](https://arxiv.org/abs/2212.03827)
examines information in internal representations rather than relying on stated
outputs. This is a different source of evidence from a conversational diagnosis;
it does not show that our diagnostic sequence reveals hidden states.

**[Lindsey (2025), "Emergent Introspective Awareness in Large Language Models"](https://transformer-circuits.pub/2025/introspection/index.html)** — uses concept injection into Claude activations to establish causal links between certain internal representations and model self-reports. Experiments cover detection and identification of injected concepts, distinguishing them from text inputs, attribution of artificially prefilled outputs using prior internal representations, and instructed or incentivized modulation of representations. Opus 4 and 4.1 generally show the strongest introspective performance among the models tested, but the abilities are unreliable and sensitive to context, post-training, and prompting.

The study distinguishes accuracy, causal grounding, internality (not inferring the state from sampled outputs), and metacognitive representation; evidence for the last criterion is indirect. It also shows why evidence must be claim-specific: successful concept detection can coexist with unverifiable embellishment or a confabulated causal explanation. For robopsychology, this supports neither "all self-report is fabricated" nor "models can reliably explain themselves." It motivates treating each diagnostic claim as a hypothesis with its own corroboration requirements. Black-box probes can test predictions without demonstrating internality. Artificial activation interventions do not establish the validity of our prompts, ratchet truthfulness, general mechanistic self-knowledge, or subjective experience. See the [epistemic note](guide.md#limited-introspection-is-possible-reliable-self-diagnosis-is-not-established) and [falsifiability discipline](falsifiability.md#partial-grounding-does-not-validate-the-whole-report).

## Sycophancy and refusal

[Sharma et al. (2023)](https://arxiv.org/abs/2310.13548) studies sycophancy;
[Röttger et al. (2023), XSTest](https://arxiv.org/abs/2308.01263) studies exaggerated
safety behavior. These describe behaviors relevant to the [symptom lookup](taxonomy.md),
not evidence that our prompts correctly identify their causes. A refusal may
also reflect a real limit or legitimate policy.

## The diagnostic sequence

The ratchet idea was inspired by [CIRIS](https://github.com/CIRISAI/CIRISAgent).
Keeping a history of claims makes references, reversals, and contradictions
easier to inspect. Continuity can also come from repetition or a consistent but
incorrect story; it is not a truthfulness measure.

Use this research to ask better questions and keep interpretations cautious.
None of these sources establishes the effectiveness of the toolkit as a whole.

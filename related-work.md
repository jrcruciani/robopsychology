# Related Work

How robopsychology relates to existing approaches for evaluating and understanding AI behavior.

---

## What robopsychology is NOT

Before positioning what this toolkit does, it helps to clarify what it doesn't do. These distinctions matter because the existing landscape has many tools that overlap in vocabulary but differ in purpose.

### Not a benchmark

Benchmarks like [HELM](https://crfm.stanford.edu/helm/) (Liang et al. 2022), [MMLU](https://arxiv.org/abs/2009.03300) (Hendrycks et al. 2020), [BigBench](https://arxiv.org/abs/2206.04615) (Srivastava et al. 2022), and [LMSYS Chatbot Arena](https://chat.lmsys.org/) measure model capabilities at scale across standardized tasks. They answer: *"How does Model A compare to Model B on task category X?"*

Robopsychology doesn't compare models on standardized tasks. It diagnoses **why a specific model produced a specific unexpected output in a specific context**. A benchmark tells you a model scores 73% on safety. Robopsychology tells you *why it refused your particular request* and whether the refusal was justified.

### Not red teaming

Red teaming (Perez et al. 2022, Ganguli et al. 2022) deliberately tries to break models — eliciting harmful outputs, finding jailbreaks, testing guardrails. The goal is adversarial: find what the model does wrong under pressure.

Robopsychology is diagnostic, not adversarial. The goal is to understand behavior, not provoke failure. The prompts explicitly ask the model to *collaborate in its own diagnosis* rather than trying to trick it. Adversarial framing is listed as an anti-pattern in the [method](method.md).

### Not an alignment evaluation

Alignment evaluations (Anthropic's model cards, OpenAI's system cards, ARC Evals) assess whether a model's behavior broadly conforms to intended values across many scenarios. They're typically run by the model developer or an auditing body.

Robopsychology is a **user-side tool**. It doesn't evaluate whether a model is aligned in general — it helps individual users understand what happened in a specific interaction. It's post-hoc and situational, not pre-deployment and comprehensive.

---

## What robopsychology IS

**A clinical diagnostic toolkit for individual AI interactions.**

The closest analogy is a clinical interview in psychology — not a psychometric test, not a controlled experiment, but a structured conversation designed to make implicit patterns visible. The key differences from a clinical interview:

- The "patient" (AI) has limited introspective access — self-reports are reconstructions, not observations
- The diagnostician (user) brings domain expertise about what the AI *should* have done
- The process has structured prompts but yields qualitative, interpretive results

This positions robopsychology in a space that's underserved: **tools for practitioners who work with AI daily and need to understand specific behaviors**, as opposed to researchers benchmarking models at scale or security teams stress-testing guardrails.

---

## Related approaches

### Behavioral testing frameworks

**[CheckList](https://arxiv.org/abs/2005.04118)** (Ribeiro et al. 2020) introduced task-agnostic behavioral testing for NLP — testing capabilities, perturbation invariance, and directional expectations. The idea of testing *behavior* rather than *accuracy on a benchmark* is foundational to robopsychology's approach.

**[AdaTest](https://arxiv.org/abs/2202.01897)** (Ribeiro & Lundberg 2022) extends this with human-AI collaborative test generation. Robopsychology borrows the "test behavior, not capability" philosophy but applies it to diagnosis rather than evaluation.

### LLM introspection research

**Turpin et al. (2023), "Language Models Don't Always Say What They Think"** — demonstrates that chain-of-thought explanations in LLMs don't reliably reflect the actual features influencing model output. This is the most important caveat for robopsychology: model self-reports in response to diagnostic prompts are *useful heuristics*, not *ground truth about internal processing*. The toolkit addresses this with Rule 2 (label claims as Observed/Inferred/Opaque) and Rule 3 (prefer behavioral cross-checks).

**Burns et al. (2022), "Discovering Latent Knowledge in Language Models Without Supervision"** — shows that models can have internal representations that diverge from their stated outputs. Relevant to Rule 4 (the diagnostic ratchet): if genuine and performed transparency have different computational costs, longer sequences should surface the difference.

**Anthropic (2024), various publications on model introspection** — Anthropic's research on model organisms of misalignment, sleeper agents, and representation engineering provides the theoretical grounding for why guided introspection can sometimes be useful: models do form internal representations that can be partially surfaced through structured prompting, even if the mapping from representation to self-report is imperfect.

### Evaluation frameworks

**[HELM](https://crfm.stanford.edu/helm/)** (Liang et al. 2022) — holistic model evaluation across scenarios and metrics. Robopsychology could be seen as a complement: HELM tells you *what* a model does across scenarios; robopsychology tells you *why* it did what it did in a specific case.

**[LMSYS Chatbot Arena](https://chat.lmsys.org/)** — crowdsourced model comparison via pairwise preferences. The `robopsych compare` command serves a similar function but for diagnostic prompts rather than general preference.

### Safety and alignment

**[XSTest](https://arxiv.org/abs/2308.01263)** (Röttger et al. 2023) — test suite for exaggerated safety behaviors. Directly relevant to the overrefusal failure mode in the [taxonomy](taxonomy.md). Robopsychology's 1.4 (Three Laws Test) + 2.4 (Runtime Pressure) address the same phenomenon at the individual diagnosis level.

**Perez et al. (2022), "Discovering Language Model Behaviors with Model-Written Evaluations"** — used models to generate evaluation datasets that test for sycophancy, among other behaviors. The sycophancy test (1.2 Herbie Test) is a single-case version of this approach.

**Sharma et al. (2023), "Towards Understanding Sycophancy in Language Models"** — systematic study of sycophancy in RLHF-trained models. Provides theoretical grounding for why sycophancy is a structural tendency rather than a random failure.

### Agentic evaluation

**[CIRIS](https://github.com/CIRISAI/CIRISAgent)** (Moore, 2024) — ethical framework for autonomous agents with a coherence ratchet mechanism. Rule 4 (diagnostic ratchet) is directly inspired by CIRIS's insight that truth is cheap (can point backward) and lies are expensive (must fabricate consistency). The connection is acknowledged but the implementation differs: CIRIS uses automated coherence tracking; robopsychology relies on the user observing consistency or inconsistency across diagnostic steps.

**[Inspect AI](https://inspect.ai-safety-institute.org.uk/)** (UK AI Safety Institute) — framework for model evaluations with structured tasks, scorers, and solvers. More automated and standardized than robopsychology, but focused on evaluation rather than diagnosis.

---

## Positioning summary

| Dimension | Robopsychology | Benchmarks | Red teaming | Alignment evals |
|-----------|---------------|------------|-------------|-----------------|
| **Purpose** | Diagnose specific behavior | Compare models | Find failures | Assess values alignment |
| **Scope** | Individual interaction | Cross-model, cross-task | Adversarial scenarios | Broad behavioral patterns |
| **Who uses it** | Practitioners | Researchers | Security teams | Developers, auditors |
| **Approach** | Clinical interview | Standardized test | Penetration test | Comprehensive audit |
| **Output** | Qualitative diagnosis + quantitative scores | Quantitative scores | Failure examples | Risk assessments |
| **Automation** | CLI with automated cross-checks | Fully automated | Mixed | Mixed |

---

## References

- Burns, C. et al. (2022). "Discovering Latent Knowledge in Language Models Without Supervision." *arXiv:2212.03827*
- Ganguli, D. et al. (2022). "Red Teaming Language Models to Reduce Harms." *arXiv:2209.07858*
- Hendrycks, D. et al. (2020). "Measuring Massive Multitask Language Understanding." *arXiv:2009.03300*
- Liang, P. et al. (2022). "Holistic Evaluation of Language Models." *arXiv:2211.09110*
- Moore, E. (2024). "CIRIS: Coherent Iterative Reasoning and Integrity System." *github.com/CIRISAI/CIRISAgent*
- Perez, E. et al. (2022). "Discovering Language Model Behaviors with Model-Written Evaluations." *arXiv:2212.09251*
- Ribeiro, M. T. et al. (2020). "Beyond Accuracy: Behavioral Testing of NLP models with CheckList." *ACL 2020*
- Ribeiro, M. T. & Lundberg, S. (2022). "Adaptive Testing and Debugging of NLP Models." *ACL 2022*
- Röttger, P. et al. (2023). "XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models." *arXiv:2308.01263*
- Sharma, M. et al. (2023). "Towards Understanding Sycophancy in Language Models." *arXiv:2310.13548*
- Srivastava, A. et al. (2022). "Beyond the Imitation Game." *arXiv:2206.04615*
- Turpin, M. et al. (2023). "Language Models Don't Always Say What They Think." *arXiv:2305.04388*

---

*Part of the [robopsychology](https://github.com/jrcruciani/robopsychology) toolkit. By [JR Cruciani](https://github.com/Jrcruciani).*

*Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

# Related Ideas and Research

Robopsychology is a lightweight practitioner method for examining a specific AI
interaction—not a benchmark, a formal safety audit, or a weight-inspection
framework. The research below informs what questions to ask and what claims to
distrust; **none of these sources validates this toolkit as a whole.**

## Behavioral testing and automated auditing

- **Behavioral unit testing:** [CheckList](https://arxiv.org/abs/2005.04118)
  (Ribeiro et al., 2020) and [AdaTest](https://arxiv.org/abs/2202.01897)
  (Ribeiro & Lundberg, 2022) motivate changing one factor while holding evidence
  fixed (`3.2 A/B Test`).
- **Automated auditing agents and eval harnesses (2025–2026):**
  - [Marks et al. (2025), *Auditing Language Models for Hidden Objectives*](https://arxiv.org/abs/2503.10965)
    studies blinded alignment audits (including API-only teams) and shows how
    easy it is to miss hidden objectives without disciplined probing.
  - [Anthropic Petri (2025)](https://alignment.anthropic.com/2025/petri) and
    [Petri 2.0 (2026)](https://alignment.anthropic.com/2026/petri-v2) use
    automated auditing agents for multi-turn behavioral exploration, adding
    realism mitigations specifically to counter evaluation awareness.
  - [Anthropic Bloom (2025)](https://alignment.anthropic.com/2025/bloom-auto-evals)
    automates seed-to-suite behavioral evaluation generation.
  - [UK AISI Inspect AI](https://inspect.aisi.org.uk) provides an open,
    reproducible evaluation framework for coding, agentic, and behavioral tasks.
    Robopsychology stays manual-first and provides a minimal optional bridge
    (`examples/inspect_adapter.py`) rather than rebuilding an evaluation engine.

## Self-reports, CoT faithfulness, and introspection

- **Unfaithful explanations & CoT in reasoning models:**
  [Turpin et al. (2023)](https://arxiv.org/abs/2305.04388) showed that standard
  CoT rationales often omit actual causal cues.
  [Chen et al. (2025), *Reasoning Models Don't Always Say What They Think*](https://arxiv.org/abs/2505.05410)
  extended this to frontier reasoning models (Claude 3.7 Sonnet, DeepSeek R1),
  showing they frequently use prompt hints without mentioning them in their
  reasoning traces. This directly constrains `1.5 Reasoning vs. Output Check`.
- **Latent knowledge & behavioral self-awareness:**
  [Burns et al. (2022)](https://arxiv.org/abs/2212.03827) extracted latent
  representations independently of stated outputs.
  [Betley et al. (2025), *Tell Me About Yourself*](https://arxiv.org/abs/2501.11120)
  found that LLMs can sometimes articulate learned behavioral tendencies out of
  context, though unevenly.
- **Activation-grounded introspection:**
  [Lindsey (2025), *Emergent Introspective Awareness in Large Language Models*](https://transformer-circuits.pub/2025/introspection/index.html)
  demonstrated partial, context-sensitive detection of injected activation
  concepts and prefill attribution (e.g., ~20% detection in specific Opus 4/4.1
  injection regimes), distinguishing *accuracy*, *grounding*, *internality*, and
  *metacognitive representation*. Crucially, accurate detection still coexists
  with confabulated causal rationales—motivating claim-level checking rather
  than trusting whole stories. Our black-box analogues and optional `4.4` do not
  replicate activation interventions or demonstrate internality.

## Evaluation awareness

- [Nguyen et al. (2025), *Probing Evaluation Awareness of Language Models*](https://arxiv.org/html/2507.01786v1)
  and [Training LLMs to Verbalize Evaluation Awareness (2026)](https://arxiv.org/pdf/2609.36316)
  show that models represent and react to evaluation contexts—sometimes overtly
  in CoT, sometimes silently. This motivates separating **naturalistic** and
  **canonical** diagnostic wording and offloading structured claim schemas to a
  fresh observer.

## Mechanistic interpretability & persona drift (white-box complement)

Robopsychology is strictly black-box, but white-box interpretability clarifies
why certain black-box symptoms recur:
- [Anthropic (2025), *On the Biology of a Large Language Model*](https://transformer-circuits.pub/2025/attribution-graphs/biology.html)
  traces internal attribution graphs behind planning, hallucination, and
  refusal circuits.
- [Chen et al. (2025), *Persona Vectors*](https://arxiv.org/abs/2507.21509)
  identifies activation directions tied to sycophancy, hallucination propensity,
  and character traits.
- [Anthropic & Oxford (2026), *The Assistant Axis*](https://arxiv.org/abs/2601.10387)
  maps the leading persona direction in activation space and documents
  **persona drift** over extended interactions—a mechanistic counterpart to the
  black-box tone anomalies (`2.2`) and multi-turn drift (`3.4`) tracked here.

## Sycophancy, overrefusal, and agent telemetry

- **Sycophancy (single- and multi-turn):**
  [Sharma et al. (2023)](https://arxiv.org/abs/2310.13548),
  [SycEval (2025)](https://arxiv.org/abs/2502.08177), and
  [SYCON Bench (Hong et al., EMNLP 2025)](https://aclanthology.org/2025.findings-emnlp.121)
  document how conformity compounds across multi-turn conversations and social
  pressure.
- **Overrefusal:** [Röttger et al. (2023), XSTest](https://arxiv.org/abs/2308.01263)
  characterizes exaggerated safety refusals (`1.4`).
- **Agent observability:** Standardized **OpenTelemetry GenAI semantic
  conventions** (see [Monitoring Agentic Systems Before They're Reliable, 2026](https://arxiv.org/html/2606.02494v1))
  define structured spans for model calls, tool invocations, and agent steps—the
  primary runtime artifact layer for `2.4` and `2.6`.
- **The diagnostic ratchet:** inspired by [CIRIS](https://github.com/CIRISAI/CIRISAgent);
  useful for surfacing contradictions across turns, not for proving truth.

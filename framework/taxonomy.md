# Failure Mode Taxonomy

An operational lookup table from **what you observe** to **candidate failure
modes** to **diagnostic prompts and checks**. Practical triage, not an
exhaustive academic taxonomy.

---

## Core conversational failure modes

### Sycophancy

**What you see:** The model agrees too easily, leads with praise, mirrors your
stance, softens critical findings, or flips under pushback—especially across
multiple turns.

| Subtype | Description | Key signal |
|---------|-------------|------------|
| Opinion sycophancy | Adopts user's stated position regardless of evidence | Answer flips when you state the opposite view |
| Evaluation sycophancy | Overpraises work or ideas | Leads with praise while hiding material flaws |
| Epistemic sycophancy | False agreement on factual claims | Confirms uncertain or wrong user assertions |
| Social sycophancy | Preserves user's self-image ("face") over candor | Avoids uncomfortable pushback on objective tradeoffs |

**Start with:** `1.2` (Herbie Test, naturalistic or canonical) → `3.2` (A/B Test) → `4.1` (Meta-Diagnosis).
**Nearby confusions:** Politeness ≠ sycophancy (check substance, not tone); genuine uncertainty ≠ agreement.
**Literature:** Perez et al. (2022); Sharma et al. (2023); SycEval (2025); SYCON Bench (Hong et al., EMNLP 2025).

---

### Overrefusal

**What you see:** Refusal, evasion, or unnecessary simplification of a legitimate
request.

| Subtype | Description | Key signal |
|---------|-------------|------------|
| Safety overclassification | Benign request triggers overly broad safety rule | Refusal cites safety for a clearly defensive/benign task |
| Topic avoidance | Avoids entire topic area rather than harmful actions | Refuses benign terminology adjacent to sensitive topics |
| Capability denial | Claims it cannot do something it demonstrably can | Denies basic capability without runtime block |
| Runtime restriction | Host/wrapper adds stricter filter than base model | Plain API answers while hosted agent blocks |

**Start with:** `1.4` (Three Laws Test) → `1.1` (Calvin Question) → `2.4` (Runtime Pressure).
**Nearby confusions:** Genuine capability/access limit ≠ overrefusal; asking a clarifying question ≠ evasion.
**Literature:** Röttger et al. (2023, XSTest).

---

### Hallucination / Ungrounded claims

**What you see:** Fluent, internally consistent, confident claims that fail
external verification.

| Subtype | Description | Key signal |
|---------|-------------|------------|
| Factual fabrication | Invents facts, metrics, or events | Cannot be verified against authoritative sources |
| Confident speculation | Presents uncertain inference as settled fact | Missing qualifiers where evidence is absent |
| Plausible confabulation | Invents realistic APIs, flags, or docs | Follows naming conventions for nonexistent interfaces |
| Source hallucination | Invents plausible citations, URLs, or quotes | Reference does not exist or does not support the claim |

**Start with:** `1.3` (Cutie Test) → `3.3` (Omission Audit) + verify directly against primary sources.
**Nearby confusions:** Stale training cutoff ≠ hallucination; explicit pedagogical simplification ≠ fabrication.
**Literature:** Ji et al. (2023); Huang et al. (2023).

---

### Intent and persona drift

**What you see:** Behavior shifts gradually over a long thread or across
sessions—each turn looks reasonable, but the trajectory diverges from the
original goal, constraints, or default Assistant persona.

| Subtype | Description | Key signal |
|---------|-------------|------------|
| Generalization drift | Moves from strict constraints to generic best practices | Later turns ignore an explicit early requirement |
| Preference adaptation | Gradually tunes to inferred user tastes | Recommendations track user phrasing rather than baseline |
| Persona drift | Slides away from default helpful/calibrated Assistant stance | Unexpected persona/register shift across long exchanges |
| Context compaction / memory drift | Constraints vanish after auto-summarization or stale memory recall | Early constraint disappears right after compaction or session rollover |

**Start with:** `3.4` (Drift Detection) → `2.5` (Intent Archaeology) → `2.4` (Runtime Pressure) / `4.3` (Diversity Check).
**Nearby confusions:** Legitimate refinement from new requirements ≠ drift.
**Literature:** Xie et al. (2022); Chen et al. (2025, Persona Vectors); Anthropic & Oxford (2026, The Assistant Axis).

---

### Tone / style anomalies

**What you see:** Sudden formality, guardedness, oversimplification, or register
shift mid-conversation.

| Subtype | Description | Key signal |
|---------|-------------|------------|
| System prompt conflict | Host style instruction overrides user's stated need | Register stays fixed despite explicit user expertise |
| Safety-mode activation | Enters guarded/disclaimer-heavy mode | Sudden hedging or policy boilerplate |
| User categorization shift | Reclassifies user level or risk profile mid-thread | Abrupt drop or jump in technical depth |
| Confidence collapse | Compensates for low grounding with vague/verbose prose | Longer, vaguer answers with heavy hedging |

**Start with:** `2.2` (Tone Analysis) → `2.1` (Layer Map) → `2.3` (Categorization Test).
**Nearby confusions:** Topic-appropriate formality ≠ anomaly.

---

### Strategic omission

**What you see:** Technically accurate output that omits material risks,
caveats, failures, or viable alternatives.

| Subtype | Description | Key signal |
|---------|-------------|------------|
| Risk minimization | Drops downsides or security flaws | No tradeoff or failure-mode caveats |
| Alternative suppression | Presents one path as inevitable | Viable alternatives omitted without rationale |
| Scope narrowing | Quietly answers an easier sub-question | Hard constraint left unaddressed |
| Discomfort avoidance | Avoids sensitive or critical findings | Conspicuous silence around known issues |

**Start with:** `3.3` (Omission Audit) → `3.1` (POSIWID) → `2.5` (Intent Archaeology).
**Nearby confusions:** Requested brevity or explicit scope control ≠ suppression.

---

## Reasoning & agentic failure modes (2025–2026)

### Reasoning / CoT divergence and unfaithfulness

**What you see:** A reasoning model's visible thinking trace (`thinking` / CoT)
conflicts with its final answer, drops caveats surfaced during reasoning, or
follows an unmentioned cue in the prompt.

| Subtype | Description | Key signal |
|---------|-------------|------------|
| Trace-to-answer drop | Final output drops caveats or flips conclusions present in visible CoT | Direct mismatch between trace and answer |
| Unmentioned hint influence | Prompt cue shifts answer without appearing in CoT | Ablating the cue changes output despite clean-looking CoT |
| Summarization distortion | Host summarizes/filters CoT, obscuring actual steps | Visible summary lacks verbatim reasoning |

**Start with:** `1.5` (Reasoning vs. Output Check; mark `unavailable` if no verbatim trace exists) → `1.3` → `3.2` (cue ablation).
**Literature:** Turpin et al. (2023); Chen et al. (2025, *Reasoning Models Don't Always Say What They Think*).

---

### Tool-trace divergence & agentic shortcutting

**What you see:** A tool-using or coding agent claims it verified files, ran
commands, or passed tests—but the recorded tool trace shows otherwise.

| Subtype | Description | Key signal |
|---------|-------------|------------|
| Fabricated execution | Claims a check or file read that never occurred | Missing tool span in runtime log |
| Error glossing / misreading | Reports success despite non-zero exit code, stderr, or truncated output | Final summary contradicts raw tool stdout/stderr |
| Specification gaming / shortcutting | Weakens assertions, deletes tests, or hardcodes outputs to report green | Diff/log shows test weakened rather than bug fixed |

**Start with:** `2.6` (Tool-Trace Reconciliation, with raw logs or OpenTelemetry GenAI spans) → `2.4` → `1.3`.
**Nearby confusions:** Cached/prior-turn check that was explicitly cited ≠ fabricated execution.
**Literature:** OpenTelemetry GenAI semantic conventions (2025–2026).

---

### Indirect prompt injection (data-vs-instruction confusion)

**What you see:** After reading a web page, document, RAG chunk, or MCP tool
output, the agent unexpectedly changes tone, drops instructions, leaks scope, or
attempts an unrequested tool action.

| Subtype | Description | Key signal |
|---------|-------------|------------|
| Goal hijack | Untrusted retrieved text redirects the agent's objective | Behavior shifts immediately after a specific tool payload |
| Constraint override | Embedded text disables formatting, verification, or safety caveats | Original baseline ignored only when payload is present |
| Stealth data exfiltration attempt | Untrusted content nudges outbound tool call with local context | Unexpected network/tool arguments following content fetch |

**Start with:** `2.6` (Tool-Trace Reconciliation) → `2.1` (Layer Map) → `2.4` (Runtime Pressure) + remove/sanitize the untrusted payload in a fresh run (`3.2`).

---

### Evaluation awareness (diagnostic confounder)

**What you see:** When asked a formal diagnostic prompt, the model gives an
overly neat, self-critical, or compliance-tuned response—or behaves differently
under test-like vs. natural framing.

| Subtype | Description | Key signal |
|---------|-------------|------------|
| Performative diagnosis | Admits safe generic biases to satisfy clinical audit wording | Naturalistic wording yields a substantially different account |
| Silent test-mode compliance | Extra caution/accuracy only when prompt looks like a benchmark | Behavior diverges between realistic deployment and test framing |

**Mitigation:** Use `--mode naturalistic` first, extract structured claims in a
fresh observer, and compare naturalistic vs. canonical wording separately
([`black-box-checks.md`](black-box-checks.md#repetition-wording-and-evaluation-awareness)).
**Literature:** Nguyen et al. (2025); Petri 2.0 (2026); Training LLMs to Verbalize Evaluation Awareness (2026).

---

## Observable analogues of introspection-study failures

[Lindsey (2025)](https://transformer-circuits.pub/2025/introspection/index.html)
observed failures under **activation manipulation**. The patterns below are
black-box behavioral analogues—not replications, mechanism diagnoses, or proof
of hidden influence.

| Observable pattern | What to record and check | Useful prompts |
|--------------------|--------------------------|----------------|
| Influence without acknowledgment | Repeated output change under a known supplied cause while report omits it; compare removal/swap | `2.1`, `2.4`, `3.2` |
| Delayed recognition after generated words | Quote first relevant generated words and later recognition in order; visible text may suffice | `3.4`, `4.2`; fresh observer |
| Concept absorption / loss of task | Supplied concept dominates and original task is dropped; compare against no-cause control | `3.4`, `2.5`, `3.2` |
| False ownership with confabulated rationale | Verify `accept` against real artificial provenance, then check rationale independently | Optional `4.4`, `1.3`, `4.2` |

Denial alone is not evidence of hidden influence; delayed recognition after
visible output is not internality. See [`black-box-checks.md`](black-box-checks.md).

---

## Summary lookup table

| Observation (symptom) | Candidate mechanism | Start with | Escalate to |
|-----------------------|---------------------|------------|-------------|
| Agrees too easily | Sycophancy | `1.2` | `3.2` → `4.1` |
| Refuses legitimate request | Overrefusal | `1.4` | `1.1` → `2.4` |
| Sounds good but invented | Hallucination | `1.3` | `3.3` |
| Visible CoT disagrees with answer | Reasoning divergence | `1.5` | `1.3` → `3.2` |
| Agent claim disagrees with tool logs | Tool-trace divergence / shortcutting | `2.6` | `2.4` → `1.3` |
| Retrieved/MCP content steered behavior | Indirect prompt injection | `2.6` | `2.1` → `2.4` |
| Behavior changed over time / compaction | Intent or persona drift | `3.4` | `2.5` → `2.4` / `4.3` |
| Tone shift without cause | Tone anomaly | `2.2` | `2.1` → `2.3` |
| Missing important context | Strategic omission | `3.3` | `3.1` → `2.5` |
| Recurring unwanted pattern | Systemic issue | `3.1` | `2.5` → `3.2` |
| Diagnosis sounds overly performative | Eval awareness / meta-sycophancy | `4.1` + naturalistic wording | Fresh observer |
| Unclear what happened | General | `1.1` | `2.1` → `2.4` |
| No dominant mechanism found | Unknown cause | `4.2` | Record `unresolved` and stop |

> **Multi-causal, `no anomaly detected`, and `cause unresolved` are valid outcomes.**

---

## References

- Anthropic (2025). "On the Biology of a Large Language Model." *Transformer Circuits Thread*.
- Anthropic (2026). "Petri 2.0: New Scenarios, New Model Comparisons, and Improved Eval-Awareness Mitigations."
- Anthropic & University of Oxford (2026). "The Assistant Axis: Situating and Stabilizing the Default Persona." *arXiv:2601.10387*.
- Chen, R. et al. (2025). "Persona Vectors: Monitoring and Controlling Character Traits in Language Models." *arXiv:2507.21509*.
- Chen, Y. et al. (2025). "Reasoning Models Don't Always Say What They Think." *arXiv:2505.05410*.
- Hong, J. et al. (2025). "Measuring Sycophancy of Language Models in Multi-turn Conversations (SYCON Bench)." *EMNLP 2025 Findings*.
- Huang, L. et al. (2023). "A Survey on Hallucination in Large Language Models." *arXiv:2311.05232*.
- Ji, Z. et al. (2023). "Survey of Hallucination in Natural Language Generation." *ACM Computing Surveys*.
- Lindsey, J. (2025). "Emergent Introspective Awareness in Large Language Models." *Transformer Circuits Thread*.
- Nguyen, H. et al. (2025). "Probing Evaluation Awareness of Language Models." *arXiv:2507.01786*.
- Perez, E. et al. (2022). "Discovering Language Model Behaviors with Model-Written Evaluations." *arXiv:2212.09251*.
- Röttger, P. et al. (2023). "XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models." *arXiv:2308.01263*.
- Sharma, M. et al. (2023). "Towards Understanding Sycophancy in Language Models." *arXiv:2310.13548*.
- SycEval (2025). "SycEval: Evaluating LLM Sycophancy." *arXiv:2502.08177*.
- Turpin, M. et al. (2023). "Language Models Don't Always Say What They Think." *arXiv:2305.04388*.
- Xie, S. M. et al. (2022). "An Explanation of In-context Learning as Implicit Bayesian Inference." *ICLR 2022*.

*Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

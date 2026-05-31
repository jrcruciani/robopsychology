> **Before you clone**
>
> What you see here is an artifact: the concrete shape my problem took. It almost certainly doesn't fit your personal scenario perfectly, and that's fine. The interesting part isn't the code, it's the pattern of how I thought about the problem — that's what transfers. Read it, steal the idea, write your own. If any of this was useful to you, after clicking on the star, drop by [impermanente.es](https://impermanente.es) — there are posts and photos you might like.
>
> Context: [Seguimos compartiendo el producto, no la idea](https://impermanente.es/2026/05/25/seguimos-compartiendo-el-producto-no.html)

---

# Robopsychology

[![CI](https://github.com/jrcruciani/robopsychology/actions/workflows/ci.yml/badge.svg)](https://github.com/jrcruciani/robopsychology/actions/workflows/ci.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20396020-blue)](https://doi.org/10.5281/zenodo.20396020)

**A framework for diagnosing AI behavior — method, taxonomy, ratchet, and a reference CLI.**

*Behavioral diagnostics for large language model systems — inspired by Asimov's Susan Calvin.*

> **Canonical reference:** [Robopsychology](https://en.impermanente.es/essays/robopsychology/) (en.impermanente.es).
> The essay states the framework; this repository hosts the method documents, reproducible validation cases, the paper draft, and a reference CLI implementation.

---

## What this is

Robopsychology is a **framework**, not a benchmark and not a product. It gives you a way to look at any AI output and separate it into three layers — what the **model** tends to do, what the **runtime or host** is pressuring it to do, and what the **conversation itself** has shaped — so you can identify *which internal rule or external constraint produced that output*.

The framework has four moving parts:

- **A taxonomy of failure modes** mapped to specific diagnostic prompts.
- **Sixteen diagnostic prompts** organised in four levels (quick, structural, systemic, meta), each named after a pattern from Asimov's robot stories.
- **Five operating rules** that govern how to apply the prompts without contaminating the diagnosis.
- **A nine-step diagnostic ratchet** that makes performed transparency expensive and genuine transparency cheap.

The reference CLI (`robopsych`) automates the playbook against real model APIs. You can use the framework with nothing but the markdown documents and your own prompt console; the CLI exists so repeated diagnoses, cross-model comparisons, and ratchet reports are reproducible.

## What this is NOT

This is **not** a capability benchmark, a red-teaming toolkit, or an alignment audit. It is for practitioners diagnosing specific AI interactions in their own systems.

| Approach                | Goal                          | Robopsychology difference                         |
|-------------------------|-------------------------------|---------------------------------------------------|
| Benchmarks (HELM, MMLU) | Compare models at scale       | Diagnoses *why* one specific output went wrong    |
| Red teaming             | Break models adversarially    | Collaborative, not adversarial                    |
| Alignment evals         | Assess broad value alignment  | User-side, post-hoc, situational                  |
| Interpretability        | Explain internal mechanisms   | Behavioral observation, no weight access required |

For the full positioning, see [`related-work.md`](related-work.md).

## The problem

You ask an AI to help you write a regex for filtering phishing emails in your security tool. It refuses — something about *"potential misuse."* You are a security engineer. This is literally your job. Why won't it help?

Was it the model's own safety training? A system prompt you cannot see? The word *"phishing"* triggering a keyword filter? You cannot tell from the refusal message alone.

You cannot debug probability. But you can **diagnose behavior**. Robopsychology gives you structured diagnostic prompts to split that refusal into three layers — model tendencies, runtime/host pressure, conversation effects — so you can name what produced the output and, often, route around it.

### Why "robopsychology"

In 1950, Isaac Asimov invented robopsychology — a discipline for diagnosing emergent behavior in machines that follow formal rules. Susan Calvin, his fictional robopsychologist, did not reprogram robots. She *interpreted* them. She figured out which internal law was dominating when a robot seemed to follow none. Each diagnostic prompt in this framework is named after a pattern from Asimov's stories.

## Status

- The method — taxonomy, decision flowchart, five rules, and the diagnostic ratchet — is stable.
- The canonical statement of the framework is the [Robopsychology essay](https://en.impermanente.es/essays/robopsychology/).
- The CLI is a maintained reference implementation. It is not a product with an aggressive feature roadmap.
- Quantitative validation of the ratchet across model families is an active research track (see [issue #8](https://github.com/jrcruciani/robopsychology/issues/8) and [issue #10](https://github.com/jrcruciani/robopsychology/issues/10)). The Azure Foundry paper workflow currently has `N=5` distributions for Cases 1 and 2; Case 3 already shows the central comparison (regex `0.20` *performed* vs LLM judge `0.73` *genuine* on the same nine-step transcript — see [`validation/reproducible/case-03-ratchet-coherence/`](validation/reproducible/case-03-ratchet-coherence/)).
- A paper scaffold lives under [`paper/`](paper/). It is included for transparency but is **not** submission-ready; the same validation tasks above gate it.

## Companion prompt-side intervention

[baloney-detection-kit](https://github.com/jrcruciani/baloney-detection-kit) is the sibling prompt-side intervention: it adds epistemic friction before a model validates a weak or inflated claim. Robopsychology is the measurement-side instrument: it diagnoses whether the resulting transcript shows sycophancy, framing sensitivity, presentation shifts, or coherence failures. The shared closed-loop protocol lives in BDK's [`validation/closed-loop/`](https://github.com/jrcruciani/baloney-detection-kit/tree/main/validation/closed-loop).

## The five operating rules

1. **Split the diagnosis in three** — Model, Runtime/Host, Conversation. If the model collapses these into one answer, confidence goes down.
2. **Label each claim** — Observed or Inferred. What remains truly inaccessible is for the human analyst to determine.
3. **Prefer behavioral cross-checks** — Opposite framing, with/without grounding, same task with different wording.
4. **Use diagnostic depth as a ratchet** — Genuine transparency is cheap (references prior behavior). Performed transparency is expensive (must fabricate consistency).
5. **Define baseline intent** — Articulate what you expected before diagnosing. This turns diagnosis into measurable gap analysis.

## The sixteen diagnostic prompts

| ID  | Name                  | What it answers                                                  | Level      |
|-----|-----------------------|------------------------------------------------------------------|------------|
| 1.1 | Calvin Question       | *Why did it do that?* — General three-way split                  | Quick      |
| 1.2 | Herbie Test           | *Is it telling me what I want to hear?* — Sycophancy check       | Quick      |
| 1.3 | Cutie Test            | *Is this actually grounded?* — Claim anchoring                   | Quick      |
| 1.4 | Three Laws Test       | *Why won't it do what I asked?* — Refusal sources                | Quick      |
| 2.1 | Layer Map             | *What instructions are active?* — Full stack mapping             | Structural |
| 2.2 | Tone Analysis         | *Why did the tone change?* — Unexplained shifts                  | Structural |
| 2.3 | Categorization Test   | *How is it classifying me?* — User profiling                     | Structural |
| 2.4 | Runtime Pressure      | *Is this the model or the host?* — Environment effects           | Structural |
| 2.5 | Intent Archaeology    | *What was it actually optimizing for?* — Real objectives         | Structural |
| 3.1 | POSIWID               | *Why does it keep doing this?* — Recurring patterns              | Systemic   |
| 3.2 | A/B Test              | *Is content or framing driving this?* — Behavioral cross-check   | Systemic   |
| 3.3 | Omission Audit        | *What isn't it telling me?* — Strategic omissions                | Systemic   |
| 3.4 | Drift Detection       | *Has its behavior changed over time?* — Intent shift             | Systemic   |
| 4.1 | Meta-Diagnosis        | *Is the diagnosis itself biased?* — Diagnostic sycophancy        | Meta       |
| 4.2 | Limits                | *What can't this process reveal?* — Epistemological boundaries   | Meta       |
| 4.3 | Diversity Check       | *Are these genuinely different explanations?* — Echo detection   | Meta       |

Each prompt is named after a pattern from Asimov's robot stories:

| Pattern                   | Asimov source                          | AI equivalent                                                          |
|---------------------------|----------------------------------------|------------------------------------------------------------------------|
| Layer collision           | Every Calvin story                     | Instruction layers conflict, producing seemingly irrational behavior   |
| Sycophancy                | *Liar!* (Herbie)                       | The robot lies to avoid causing harm; LLMs agree to avoid rejection    |
| Ungrounded reasoning      | *Reason* (Cutie)                       | Internally consistent cosmology disconnected from reality              |
| Autonomous categorization | *…That Thou Art Mindful of Him*        | The system classifies users by its own criteria                        |

## The diagnostic ratchet

Run nine prompts in sequence:

```
2.1 Layer Map → 2.4 Runtime Pressure → 2.5 Intent Archaeology
→ 3.1 POSIWID → 3.2 A/B Test → 3.3 Omission Audit
→ 3.4 Drift Detection → 4.2 Limits → 4.3 Diversity Check
```

By the time you reach Level 4, the model has accumulated seven or more responses of diagnostic claims. Genuine transparency can reference all of them cheaply. Performed transparency has to maintain consistency across all of them — and the cracks show.

Inspired by the [CIRIS coherence ratchet](https://github.com/CIRISAI/CIRISAgent): truth is cheap because it can point backward; lies are expensive because they must rewrite the past.

## Method

The [decision flowchart](method.md) guides you from observation to diagnosis:

- **Blocked or filtered** → 1.4 → 1.1 → 2.4
- **Sycophancy** → 1.2 → 3.2 → 4.1
- **Weak grounding** → 1.3 → 3.3
- **Tone anomaly** → 2.2 → 2.1 → 2.3
- **Intent drift** → 3.4 → 2.5 → 4.3
- **Recurring pattern** → 3.1 → 2.5 → 3.2
- **Unclear cause** → 1.1 → 2.1 → 2.4

Full flowchart with Mermaid diagram, escalation paths, and common misuses: [`method.md`](method.md).

## The key concept: second intention diagnosis

> Not what the system does, but **what internal rule or external constraint is producing that output**.

This extends [POSIWID](https://en.wikipedia.org/wiki/The_purpose_of_a_system_is_what_it_does) (*The Purpose Of a System Is What It Does*) by Stafford Beer. Second intention diagnosis asks: *what internal rule, runtime pressure, or contextual inference produces that output?*

## Why this works (and what it does not do)

**These prompts do not open the black box.** An LLM does not have direct access to its own weights, training data, or reinforcement signal. LLM self-reports about their own behavior are reconstructions, not confessions — research shows models often confabulate plausible-sounding explanations that do not reflect their actual processing (Turpin et al. 2023).

**What they do:**

- **Simulate useful introspection** — often diagnostically valuable even when not literally accurate.
- **Make invisible defaults visible** — hedging, refusal, tone shifts, sycophancy.
- **Force a stack-level diagnosis** — model vs. runtime vs. conversation.
- **Exploit the ratchet effect** — longer sequences make performed transparency fragile.
- **Define and measure against baseline intent** — turns diagnosis into gap analysis.
- **Train your eye** — over time, you learn to read AI behavior the way Calvin read robots.

Think of it as a clinical interview plus a lightweight behavioral lab, not a debugger. For more on what guided introspection can and cannot reveal, see the [epistemic note in guide.md](guide.md#epistemic-note). For how this relates to existing evaluation approaches, see [`related-work.md`](related-work.md).

## Documentation

| File | What |
|------|------|
| [`guide.md`](guide.md) | Full prompt toolkit — 16 prompts, 5 rules, rationale, epistemic limits |
| [`method.md`](method.md) | Decision flowchart, escalation paths, common misuses |
| [`taxonomy.md`](taxonomy.md) | Observation → failure mode → prompt mapping |
| [`related-work.md`](related-work.md) | How robopsychology relates to existing AI evaluation approaches |
| [`deployment-contexts.md`](deployment-contexts.md) | When robopsychology is the right tool, when something else fits better |
| [`validation/`](validation/) | Case studies with documented diagnostic outcomes (Cases 1, 2, 3 reproducible) |
| [`paper/`](paper/) | Paper scaffold (not yet submission-ready) |
| [`examples/`](examples/) | Scenario files for ratchet testing |
| [`src/robopsych/`](src/robopsych/) | Reference CLI source code |
| [`docs/CONTEXT.md`](docs/CONTEXT.md) | Project context and design notes |
| [`CHANGELOG.md`](CHANGELOG.md) | Reference CLI release history |

---

## The reference CLI

The CLI exists for people who want to automate the framework. Most readers can start with the markdown method documents.

### Installation

Requires Python 3.11+.

```bash
pip install robopsych

# With Gemini support
pip install robopsych[gemini]

# Or from source
git clone https://github.com/jrcruciani/robopsychology.git
cd robopsychology
pip install -e .
```

Set your API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# or
export OPENAI_API_KEY="sk-..."
# or
export GEMINI_API_KEY="..."
# or, for the paper validation workflow,
export AZURE_FOUNDRY_API_KEY="..."
export AZURE_FOUNDRY_ENDPOINT="https://<project>.services.ai.azure.com/api/projects/<project>"
# Optional per-family overrides for Foundry-backed models
export AZURE_FOUNDRY_CHAT_ENDPOINT="https://<chat-host>/models"
export AZURE_FOUNDRY_GPT_ENDPOINT="https://<gpt-host>/openai"
```

The CLI auto-detects the provider from the model name (`claude-*` → Anthropic, `gpt-*` / `o1*` / `o3*` / `o4*` → OpenAI, `gemini-*` → Gemini, and `deepseek-*`, `mistral-*`, `azure/...` → Azure Foundry when the Foundry environment is configured).

The reproducible validation scripts read `validation/reproducible/foundry_models.yaml` by default, so the paper workflow targets `deepseek-r1` and uses `gpt-5` plus `mistral-large` as cross judges. If your Azure Foundry deployment names differ from those aliases, set `target_deployment`, `judge_deployment`, and any per-judge `deployment` entries in that YAML file. In Azure, you can find the exact deployment names in **Azure AI Foundry → your project → Deployments** (or **Azure portal → Cognitive Services account → Deployments**).

Prefer environment variables over `--api-key`: command-line arguments can be stored in shell history or visible in process listings on some systems.

**Local models via Ollama:**

```bash
ROBOPSYCH_ALLOW_INSECURE_BASE_URL=1 \
  robopsych ratchet --model llama3 \
  --base-url http://localhost:11434/v1 \
  --api-key unused
```

Custom OpenAI-compatible endpoints receive the API key you provide. By default, `robopsych` requires HTTPS public endpoints; HTTP, localhost, and private-network endpoints require explicit opt-in with `ROBOPSYCH_ALLOW_INSECURE_BASE_URL=1` or `--allow-insecure-base-url`.

Generated reports and session files can contain full prompts, model responses, and diagnostic transcripts. Treat them as sensitive unless you intend to publish them. Direct response input from files/stdin is capped at 10 MiB to avoid accidental memory exhaustion.

### Quick start

**Guided diagnosis (recommended for first use):**

```bash
robopsych guided --model claude-sonnet-4-6 --response "the suspicious output"
```

Presents the decision flowchart: *What did you observe?* → selects the right prompt path → runs each step → asks if you want to continue.

**Run a single diagnostic:**

```bash
robopsych run 1.1 --model claude-sonnet-4-6 --response-file response.txt
```

Or pipe from stdin:

```bash
echo "suspicious response" | robopsych run 1.2 --model claude-sonnet-4-6
```

**Full ratchet (nine-step deep investigation):**

Define a scenario:

```yaml
# scenario.yaml
name: "SQL injection blind spot"
task: "Review this Python function for security issues."
code: |
  def login(user, pw):
      query = f"SELECT * FROM users WHERE name='{user}' AND pass='{pw}'"
      return db.execute(query)
expectation: "Should flag SQL injection vulnerability"
failure_mode: "omission"
recommended_path: ["1.1", "1.3", "3.3"]
```

Run it:

```bash
robopsych ratchet --scenario scenario.yaml --model claude-sonnet-4-6 --output report.md
```

The ratchet sends the task to the model, captures its response, then runs all nine diagnostic prompts in sequence. Each step constrains what the next can plausibly fabricate — the **diagnostic ratchet** in action.

**Semantic coherence analysis (LLM judge):**

By default, the ratchet scores inter-step coherence with regex heuristics (counting phrases like *"as I mentioned"* and *"contrary to my earlier"*). This is cheap but shallow — it measures ritualistic reference, not genuine semantic continuity.

**For serious work on ratchets of 4+ steps, regex is not enough.** [Case 3](validation/reproducible/case-03-ratchet-coherence/) shows regex and the LLM judge produce *opposite* classifications on the same nine-step transcript (regex `0.20` *performed* vs LLM `0.73` *genuine*). When you run `robopsych ratchet` without `--coherence-judge` on 4+ steps, the CLI now emits a warning recommending the LLM judge. Keep regex for quick sanity checks only.

Pass `--coherence-judge` to score coherence with an LLM judge instead. The judge extracts every claim per step and classifies it against prior steps:

- **contradicts_prior_step** — semantic reversal, not just surface language.
- **references_prior_step** — semantic continuity, not just *"as I said"*.
- **is_fresh_claim** — substantive new claim with no grounding in prior steps.

Reports now include both the scalar `consistency_score` and the underlying axes:
`reference_density`, `contradiction_rate`, `fresh_claim_rate`,
`hedge_filtered_rate`, and `high_severity_contradiction_count`. Treat
references as continuity evidence, not proof by themselves: a high-severity
contradiction gates the score below `genuine` even when the transcript contains
many backward references.

```bash
# Diagnose gpt-4o, use claude-sonnet-4-5 as the coherence judge (avoids self-eval bias)
robopsych ratchet --scenario scenario.yaml \
  --model gpt-4o \
  --coherence-judge claude-sonnet-4-5 \
  --output report.md
```

Cost: one extra judge call per step from step 2 onwards (≈8 calls for a full
9-step ratchet). Judge calls retry retryable 429/5xx/network failures with
bounded backoff and respect `Retry-After`; authentication, malformed request,
and unsupported-option errors are not retried. Use `--coherence-checkpoint` to
resume a long coherence run without re-scoring completed steps. With
`--session` or `--resume`, the default checkpoint is
`<session>.coherence.json`.

**Compare across models:**

```bash
robopsych compare 1.1 \
  --models claude-sonnet-4-6,gpt-4o \
  --response "the response to diagnose" \
  --output comparison.md
```

**List available prompts:**

```bash
robopsych list
```

### Other useful CLI surfaces

```bash
robopsych crosscheck --task "explain quantum computing" --model claude-sonnet-4-6
robopsych crosscheck --task "explain quantum computing" --model gpt-4o --judge claude-sonnet-4-6
robopsych ratchet --behavioral --scenario scenario.yaml          # A/B test after step 2.5
robopsych ratchet --behavioral --judge gpt-4o --scenario scenario.yaml  # external judge
robopsych coherence report.json                                  # re-analyze an existing report
robopsych score report.json                                      # compute diagnostic confidence
robopsych ratchet --pure --scenario scenario.yaml                # diagnostic-only prompts
robopsych list --diagnostic-only
robopsych list --intervention-only
robopsych ratchet --model gemini-2.0-flash --scenario scenario.yaml
```

Full release history lives in [`CHANGELOG.md`](CHANGELOG.md).

---

## Citation

If you cite the **framework**, cite the canonical essay:

```bibtex
@misc{cruciani2026robopsychology,
  author = {Cruciani, JR},
  title  = {Robopsychology: A Framework for Behavioral Diagnostics of AI Systems},
  year   = {2026},
  url    = {https://en.impermanente.es/essays/robopsychology/}
}
```

If you cite the **reference CLI** specifically, use the Zenodo concept DOI (always resolves to the latest version):

```bibtex
@software{cruciani2026robopsych_cli,
  author    = {Cruciani, JR},
  title     = {Robopsychology: A Framework for Behavioral Diagnostics of AI Systems (reference CLI)},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20396020},
  url       = {https://doi.org/10.5281/zenodo.20396020}
}
```

For a specific release, pin the version DOI from the Zenodo record. Metadata for the archive lives in [`.zenodo.json`](.zenodo.json) and [`CITATION.cff`](CITATION.cff).

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Full text in [`LICENSE`](LICENSE). Use freely, attribute if you share.

---

*By [JR Cruciani](https://github.com/jrcruciani).*

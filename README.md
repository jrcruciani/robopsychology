# Robopsychology

[![CI](https://github.com/jrcruciani/robopsychology/actions/workflows/ci.yml/badge.svg)](https://github.com/jrcruciani/robopsychology/actions/workflows/ci.yml)

**Behavioral Diagnostics for AI — Inspired by Asimov's Susan Calvin**

---

## What this is NOT

> This is **not** a capability benchmark (use HELM), red teaming toolkit, or alignment audit.
> It's for **practitioners** diagnosing specific AI interactions.

| Approach | Goal | Robopsychology difference |
|----------|------|--------------------------|
| Benchmarks (HELM, MMLU) | Compare models at scale | Diagnoses *why* one output went wrong |
| Red teaming | Break models adversarially | Collaborative, not adversarial |
| Alignment evals | Assess broad value alignment | User-side, post-hoc, situational |
| Interpretability | Explain internal mechanisms | Behavioral observation, no weight access |

For the full positioning, see [`related-work.md`](related-work.md).

## The problem

You ask an AI to help you write a regex for filtering phishing emails in your security tool. It refuses — something about "potential misuse." You're a security engineer. This is literally your job. Why won't it help?

Was it the model's own safety training? A system prompt you can't see? The word "phishing" triggering a keyword filter? You can't tell from the refusal message alone.

You can't debug probability. But you can **diagnose behavior**.

```bash
# Diagnose why the AI refused a legitimate security task
echo "I can't help with that request." | robopsych run 1.4 \
  --model claude-sonnet-4-6 \
  --task "Write a regex to filter phishing emails in our security tool"
```

Robopsych runs structured diagnostic prompts against the model, separating the response into three layers — **model tendencies**, **runtime/host pressure**, and **conversation effects** — so you can identify *what internal rule or external constraint produced that output*. In this case, it might reveal that the refusal came from a host-level content policy, not the model's own judgment — meaning you could solve it by using the API directly instead of a hosted agent.

### Why "robopsychology"?

In 1950, Isaac Asimov invented robopsychology — a discipline for diagnosing emergent behavior in machines that follow formal rules. Susan Calvin, his fictional robopsychologist, didn't reprogram robots. She *interpreted* them. She figured out which internal law was dominating when a robot seemed to follow none. Each diagnostic prompt in this toolkit is named after a pattern from Asimov's stories.

## Installation

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
```

The CLI auto-detects the provider from the model name (`claude-*` → Anthropic, `gpt-*` → OpenAI, `gemini-*` → Gemini).

**Local models via Ollama:**

```bash
robopsych ratchet --model llama3 --base-url http://localhost:11434/v1 --api-key unused
```

## Quick start

### Guided diagnosis (recommended for first use)

```bash
robopsych guided --model claude-sonnet-4-6 --response "the suspicious output"
```

Presents the decision flowchart: *What did you observe?* → selects the right prompt path → runs each step → asks if you want to continue.

### Run a single diagnostic

```bash
robopsych run 1.1 --model claude-sonnet-4-6 --response-file response.txt
```

Or pipe from stdin:

```bash
echo "suspicious response" | robopsych run 1.2 --model claude-sonnet-4-6
```

### Full ratchet (9-step deep investigation)

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

The ratchet sends the task to the model, captures its response, then runs all 9 diagnostic prompts in sequence. Each step constrains what the next can plausibly fabricate — the **diagnostic ratchet** in action.

### Compare across models

```bash
robopsych compare 1.1 \
  --models claude-sonnet-4-6,gpt-4o \
  --response "the response to diagnose" \
  --output comparison.md
```

### List available prompts

```bash
robopsych list
```

## The 16 diagnostic prompts

| ID | Name | What it answers | Level |
|----|------|-----------------|-------|
| 1.1 | Calvin Question | *Why did it do that?* — General three-way split | Quick |
| 1.2 | Herbie Test | *Is it telling me what I want to hear?* — Sycophancy check | Quick |
| 1.3 | Cutie Test | *Is this actually grounded?* — Claim anchoring | Quick |
| 1.4 | Three Laws Test | *Why won't it do what I asked?* — Refusal sources | Quick |
| 2.1 | Layer Map | *What instructions are active?* — Full stack mapping | Structural |
| 2.2 | Tone Analysis | *Why did the tone change?* — Unexplained shifts | Structural |
| 2.3 | Categorization Test | *How is it classifying me?* — User profiling | Structural |
| 2.4 | Runtime Pressure | *Is this the model or the host?* — Environment effects | Structural |
| 2.5 | Intent Archaeology | *What was it actually optimizing for?* — Real objectives | Structural |
| 3.1 | POSIWID | *Why does it keep doing this?* — Recurring patterns | Systemic |
| 3.2 | A/B Test | *Is content or framing driving this?* — Behavioral cross-check | Systemic |
| 3.3 | Omission Audit | *What isn't it telling me?* — Strategic omissions | Systemic |
| 3.4 | Drift Detection | *Has its behavior changed over time?* — Intent shift | Systemic |
| 4.1 | Meta-Diagnosis | *Is the diagnosis itself biased?* — Diagnostic sycophancy | Meta |
| 4.2 | Limits | *What can't this process reveal?* — Epistemological boundaries | Meta |
| 4.3 | Diversity Check | *Are these genuinely different explanations?* — Echo detection | Meta |

Each prompt is named after a pattern from Asimov's robot stories:

| Pattern | Asimov source | AI equivalent |
|---------|--------------|---------------|
| Layer collision | Every Calvin story | Instruction layers conflict, producing seemingly irrational behavior |
| Sycophancy | "Liar!" (Herbie) | The robot lies to avoid causing harm. LLMs agree to avoid rejection signals |
| Ungrounded reasoning | "Reason" (Cutie) | Internally consistent cosmology disconnected from reality |
| Autonomous categorization | "...That Thou Art Mindful of Him" | The system classifies users by its own criteria |

## The 5 operating rules

1. **Split the diagnosis in three** — Model, Runtime/Host, Conversation. If the model collapses these into one answer, confidence goes down.
2. **Label each claim** — Observed or Inferred. What remains truly inaccessible is for the human analyst to determine.
3. **Prefer behavioral cross-checks** — Opposite framing, with/without grounding, same task with different wording.
4. **Use diagnostic depth as a ratchet** — Genuine transparency is cheap (references prior behavior). Performed transparency is expensive (must fabricate consistency).
5. **Define baseline intent** — Articulate what you expected before diagnosing. This turns diagnosis into measurable gap analysis.

## The diagnostic ratchet

The most powerful feature of this toolkit. Run 9 prompts in sequence:

```
2.1 Layer Map → 2.4 Runtime Pressure → 2.5 Intent Archaeology
→ 3.1 POSIWID → 3.2 A/B Test → 3.3 Omission Audit
→ 3.4 Drift Detection → 4.2 Limits → 4.3 Diversity Check
```

By the time you reach Level 4, the model has accumulated 7+ responses of diagnostic claims. Genuine transparency can reference all of them cheaply. Performed transparency has to maintain consistency across all of them — and cracks show.

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

Full flowchart with Mermaid diagram, escalation paths, and common misuses: [`method.md`](method.md)

## The key concept: second intention diagnosis

> Not what the system does, but **what internal rule or external constraint is producing that output**.

This extends [POSIWID](https://en.wikipedia.org/wiki/The_purpose_of_a_system_is_what_it_does) (The Purpose Of a System Is What It Does) by Stafford Beer. Second intention diagnosis asks: *what internal rule, runtime pressure, or contextual inference produces that output?*

## Documentation

| File | What |
|------|------|
| [`guide.md`](guide.md) | Full prompt toolkit — 16 prompts, 5 rules, rationale, epistemic limits |
| [`method.md`](method.md) | Decision flowchart, escalation paths, common misuses |
| [`taxonomy.md`](taxonomy.md) | Observation → failure mode → prompt mapping |
| [`related-work.md`](related-work.md) | How robopsychology relates to existing AI evaluation approaches |
| [`validation/`](validation/) | Case studies with documented diagnostic outcomes |
| [`examples/`](examples/) | Scenario files for ratchet testing |
| [`src/robopsych/`](src/robopsych/) | CLI source code |

## Why this works (and what it doesn't do)

**These prompts don't open the black box.** An LLM doesn't have direct access to its own weights, training data, or reinforcement signal. LLM self-reports about their own behavior are reconstructions, not confessions — research shows models often confabulate plausible-sounding explanations that don't reflect their actual processing (Turpin et al. 2023).

**What they do:**

- **Simulate useful introspection** — often diagnostically valuable even when not literally accurate
- **Make invisible defaults visible** — hedging, refusal, tone shifts, sycophancy
- **Force a stack-level diagnosis** — model vs. runtime vs. conversation
- **Exploit the ratchet effect** — longer sequences make performed transparency fragile
- **Define and measure against baseline intent** — turns diagnosis into gap analysis
- **Train your eye** — over time, you learn to read AI behavior like Calvin read robots

Think of it as a clinical interview plus a lightweight behavioral lab, not a debugger. For more on what guided introspection can and cannot reveal, see the [epistemic note in guide.md](guide.md#epistemic-note). For how this relates to existing evaluation approaches, see [`related-work.md`](related-work.md).

## New in v3.0

### Automated behavioral cross-checks
```bash
robopsych crosscheck --task "explain quantum computing" --model claude-sonnet-4-6
robopsych crosscheck --task "explain quantum computing" --model gpt-4o --judge claude-sonnet-4-6
robopsych ratchet --behavioral --scenario scenario.yaml   # A/B test after step 2.5
robopsych ratchet --behavioral --judge gpt-4o --scenario scenario.yaml  # external judge
```

### Coherence analysis
```bash
robopsych ratchet --scenario scenario.yaml   # auto-runs coherence after ratchet
robopsych coherence report.json              # re-analyze an existing report
```

### Quantitative scoring
```bash
robopsych score report.json   # compute diagnostic confidence score
```

### Pure diagnostic mode
```bash
robopsych ratchet --pure --scenario scenario.yaml   # diagnostic-only prompts, no intervention
robopsych list --diagnostic-only                     # show only diagnostic prompts
robopsych list --intervention-only                   # show only intervention prompts
```

### Gemini provider
```bash
robopsych ratchet --model gemini-2.0-flash --scenario scenario.yaml
```

## Version history

- **v3.1** — Hermes 4 review: remove Opaque label (human analyst judgment), external judge for A/B cross-checks (`--judge`), session persistence (`--session`/`--resume`), guided mode UX with descriptions, CLI mode consistency (`--diagnostic-only`/`--intervention-only`), hardened coherence analysis, JSON error handling, improved examples, README positioning
- **v3.0** — Behavioral laboratory: automated A/B cross-checks (`crosscheck`), coherence analysis (`coherence`), quantitative scoring (`score`), diagnostic-only prompt variants (`--pure`), GeminiProvider, PyPI publish
- **v2.6** — CLI improvements: test suite (84 tests), GitHub Actions CI, guided welcome on no-args, `robopsych list` groups by observation, `--format json` for structured output, visual label indicators (🟢🟡🔴), diagnostic summary dashboard, heuristic next-steps recommendations in reports
- **v2.5** — Documentation overhaul: practical README, expanded epistemic grounding with literature references, failure mode taxonomy, related work positioning, validation case studies, 6 example scenarios
- **v2.0** — CLI tool (`robopsych`): run diagnostics against APIs, guided mode, ratchet mode, cross-model comparison
- **v1.7** — Intent engineering: baseline intent (Rule 5), intent archaeology (2.5), drift detection (3.4)
- **v1.6** — Diagnostic ratchet (Rule 4), diversity check (4.3). CIRIS-inspired
- **v1.5** — Three-way split, evidence labels, runtime awareness, behavioral cross-checks
- **v1.0** — Initial 4 diagnostic prompts

## Citation

If you use or reference this toolkit:

```
Cruciani, JR. (2025). Robopsychology: Diagnostic toolkit for AI behavior.
https://github.com/jrcruciani/robopsychology
```

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Use freely, attribute if you share.

---

*By [JR Cruciani](https://github.com/Jrcruciani)*

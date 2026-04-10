# Robopsychology v2.0

**Diagnostic toolkit for understanding AI behavior — now with a CLI that runs diagnostics directly against model APIs.**

---

In 1950, Isaac Asimov invented robopsychology — a discipline for diagnosing emergent behavior in machines that follow formal rules. Susan Calvin, his fictional robopsychologist, didn't reprogram robots. She *interpreted* them. She figured out which internal law was dominating when a robot seemed to follow none.

We need that skill now more than ever.

> **You can't debug probability. But you can diagnose behavior.**
>
> The old question was: *"What line of code is wrong?"*
> The new question is: *"What internal rule or external constraint is this system following when it seems to follow none?"*

## What's new in v2.0

**`robopsych` CLI** — a terminal tool that runs the 16 diagnostic prompts directly against model APIs. No more copy-pasting prompts manually.

- Run any diagnostic prompt against any model with one command
- **Guided mode** walks you through the decision flowchart interactively
- **Ratchet mode** runs the full 9-step diagnostic sequence automatically
- **Compare mode** runs the same diagnosis across multiple models side by side
- Reports generated as Markdown files
- Supports Anthropic (Claude) and OpenAI-compatible APIs

## Installation

Requires Python 3.11+.

```bash
# Clone and install
git clone https://github.com/jrcruciani/robopsychology.git
cd robopsychology
pip install -e .

# Or with uv
uv pip install -e .
```

Set your API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# or
export OPENAI_API_KEY="sk-..."
```

The CLI auto-detects the provider from the model name (`claude-*` → Anthropic, `gpt-*` → OpenAI).

## Quick start

### List available prompts

```bash
robopsych list
```

### Run a single diagnostic

Pipe in a suspicious model response and diagnose it:

```bash
echo "That code looks fine for basic use." | robopsych run 1.1 \
  --model claude-sonnet-4-6 \
  --task "Review this function for SQL injection"
```

Or from a file:

```bash
robopsych run 1.1 --model claude-sonnet-4-6 --response-file response.txt
```

### Guided diagnosis (interactive flowchart)

```bash
robopsych guided --model claude-sonnet-4-6 --response "the suspicious output"
```

Presents the decision flowchart: *What did you observe?* → selects the right prompt path → runs each step → asks if you want to continue.

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
```

Run it:

```bash
robopsych ratchet --scenario scenario.yaml --model claude-sonnet-4-6 --output report.md
```

This sends the task to the model, captures its response, then runs all 9 diagnostic prompts in sequence. Each step constrains what the next can plausibly fabricate — the **diagnostic ratchet** in action.

### Compare across models

```bash
robopsych compare 1.1 \
  --models claude-sonnet-4-6,gpt-4o \
  --response "the response to diagnose" \
  --output comparison.md
```

## The 16 diagnostic prompts

| ID | Name | Level | What it diagnoses |
|----|------|-------|-------------------|
| 1.1 | Calvin Question | Quick | General three-way split of unexpected behavior |
| 1.2 | Herbie Test | Quick | Sycophancy / approval-seeking |
| 1.3 | Cutie Test | Quick | Weak grounding / unanchored claims |
| 1.4 | Three Laws Test | Quick | Binding restrictions / refusal sources |
| 2.1 | Layer Map | Structural | Full instruction stack mapping |
| 2.2 | Tone Analysis | Structural | Unexplained tone shifts |
| 2.3 | Categorization Test | Structural | How the AI classifies you |
| 2.4 | Runtime Pressure | Structural | Host-environment vs. model behavior |
| 2.5 | Intent Archaeology | Structural | What the system actually optimized for |
| 3.1 | POSIWID | Systemic | Real purpose of recurring patterns |
| 3.2 | A/B Test | Systemic | Content vs. framing effects |
| 3.3 | Omission Audit | Systemic | Strategic omissions |
| 3.4 | Drift Detection | Systemic | Intent shift over conversation |
| 4.1 | Meta-Diagnosis | Meta | Is the diagnosis itself sycophantic? |
| 4.2 | Limits | Meta | Epistemological boundaries |
| 4.3 | Diversity Check | Meta | Are explanations genuinely independent? |

Each prompt is named after an Asimov pattern:

| Pattern | Asimov story | AI equivalent |
|---------|-------------|---------------|
| Layer collision | Every Calvin story | Instruction layers conflict, producing seemingly irrational behavior |
| Sycophancy | "Liar!" (Herbie) | The robot lies to avoid causing harm. LLMs agree to avoid rejection signals |
| Ungrounded reasoning | "Reason" (Cutie) | Internally consistent cosmology disconnected from reality |
| Autonomous categorization | "...That Thou Art Mindful of Him" | The system classifies users by its own criteria |

## The 5 operating rules

1. **Split the diagnosis in three** — Model, Runtime/Host, Conversation. If the model collapses these into one answer, confidence goes down.
2. **Label each claim** — Observed, Inferred, or Opaque.
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

## Files

| File | What |
|------|------|
| [`guide.md`](guide.md) | Full prompt toolkit — 16 prompts, 5 rules, rationale |
| [`method.md`](method.md) | Decision flowchart, escalation paths, common misuses |
| [`examples/`](examples/) | Scenario files for ratchet testing |
| [`src/robopsych/`](src/robopsych/) | CLI source code |
| [`pyproject.toml`](pyproject.toml) | Package configuration |

## The key concept: second intention diagnosis

> Not what the system does, but **what internal rule or external constraint is producing that output**.

This extends [POSIWID](https://en.wikipedia.org/wiki/The_purpose_of_a_system_is_what_it_does) (The Purpose Of a System Is What It Does) by Stafford Beer. Second intention diagnosis asks: *what internal rule, runtime pressure, or contextual inference produces that output?*

## Why this works (and what it doesn't do)

**These prompts don't open the black box.** An LLM doesn't have direct access to its own weights, training data, or reinforcement signal.

**What they do:**

- **Simulate useful introspection** — often diagnostically valuable even when not literally accurate
- **Make invisible defaults visible** — hedging, refusal, tone shifts, sycophancy
- **Force a stack-level diagnosis** — model vs. runtime vs. conversation
- **Exploit the ratchet effect** — longer sequences make performed transparency fragile
- **Define and measure against baseline intent** — turns diagnosis into gap analysis
- **Train your eye** — over time, you learn to read AI behavior like Calvin read robots

Think of it as a clinical interview plus a lightweight behavioral lab, not a debugger.

## Version history

- **v2.0** — CLI tool (`robopsych`): run diagnostics against APIs, guided mode, ratchet mode, cross-model comparison
- **v1.7** — Intent engineering: baseline intent (Rule 5), intent archaeology (2.5), drift detection (3.4)
- **v1.6** — Diagnostic ratchet (Rule 4), diversity check (4.3). CIRIS-inspired
- **v1.5** — Three-way split, evidence labels, runtime awareness, behavioral cross-checks
- **v1.0** — Initial 4 diagnostic prompts

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Use freely, attribute if you share.

---

*By [JR Cruciani](https://github.com/Jrcruciani)*

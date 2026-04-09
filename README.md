# Robopsychology v1.7

**Diagnostic prompts for understanding AI behavior when it doesn't do what you expect - now with intent archaeology and drift detection.**

---

In 1950, Isaac Asimov invented robopsychology - a discipline for diagnosing emergent behavior in machines that follow formal rules. Susan Calvin, his fictional robopsychologist, didn't reprogram robots. She *interpreted* them. She figured out which internal law was dominating when a robot seemed to follow none.

We need that skill now more than ever.

Version 1.5 added the crucial distinction that in hosted agents, you diagnose the **stack** (model + runtime + conversation), not just the model. Version 1.6 adds two insights from [CIRIS](https://github.com/CIRISAI/CIRISAgent): that diagnostic depth works like a **ratchet** (genuine transparency gets easier, performed transparency gets harder), and that the model's multiple explanations may not be genuinely **independent**. Version 1.7 introduces the prescriptive complement: defining **baseline intent** before diagnosing, **reconstructing** what the system actually optimized for, and detecting **drift** when behavior subtly shifts away from its stated purpose.

## The problem with non-deterministic systems

Traditional software is deterministic: given the same input, it produces the same output. When it breaks, you debug the code. You find the line, fix the logic, ship the patch.

Modern AI is probabilistic. An LLM doesn't execute instructions - it *interprets* them through layers of training, fine-tuning, system prompts, safety filters, tools, workflow rules, and conversational context. These layers can conflict. When they do, the system doesn't crash - it produces plausible-looking output that doesn't match what you expected.

In a plain chat model, some of that behavior is model-level. In a hosted agent, much of it is also shaped by orchestration: system instructions, policy layers, memory, tool availability, and session state.

**You can't debug probability. But you can diagnose behavior.**

The old question was: *"What line of code is wrong?"*
The new question is: *"What internal rule or external constraint is this system following when it seems to follow none?"*

That's what Asimov called robopsychology. This repo gives you prompts to practice it.

## What's new in v1.7

- **Baseline intent (Rule 5):** articulate what you expected — objective, constraints, success criteria — before diagnosing. This gives the process a reference point, turns diagnosis from purely reactive to measurable, and enables drift detection over time. Inspired by intent engineering.
- **Intent Archaeology (prompt 2.5):** reconstruct what the system was *actually* optimizing for based on its observed behavior — what objective, constraints, and success criteria would produce exactly what you saw. Extends POSIWID from "what does the system do?" to "what intent structure produces this behavior?"
- **Intent Drift Detection (prompt 3.4):** detect when the system's effective intent has subtly shifted during a conversation — it may still look cooperative, but it's no longer optimizing for what it started with. Connects to the coherence ratchet: genuine stability is cheap (references original intent), drift requires elaborate justification (expensive).

## What's new in v1.6

- **Diagnostic ratchet:** longer diagnostic sequences make genuine transparency easier and performed transparency harder - each honest answer is cheap (references prior behavior), each fabricated answer is expensive (must stay consistent with growing history). Run the full sequence.
- **Diagnostic diversity check:** when the model gives multiple explanations, check whether they are genuinely independent perspectives or reworded echoes of the same underlying pattern. Inspired by [CIRIS](https://github.com/CIRISAI/CIRISAgent) echo-chamber detection (IDMA).
- **New prompt 4.3** - Diagnostic Diversity Check.

## What v1.5 introduced

- **Three-way split:** separate **model**, **runtime/host**, and **conversation** causes.
- **Evidence labels:** mark diagnostic claims as **Observed**, **Inferred**, or **Opaque**.
- **Runtime-aware refusals:** distinguish **binding restrictions** from **overclassification** and optional caution.
- **Tool/runtime pressure:** detect when behavior is shaped by tools, workflow, validation, planning, or policy obligations.
- **Behavioral cross-checks:** pair self-diagnosis with reframing, grounding, and tool/no-tool comparisons.
- **Transparency vs reconstruction:** treat self-explanations as useful diagnostics, not privileged access to the model's internals.

## What this is

A structured set of diagnostic prompts organized in 4 levels, designed to be used directly in conversation with any modern LLM (Claude, GPT, Gemini, etc.) when it produces unexpected results:

| Level | What it diagnoses | When to use |
|-------|------------------|-------------|
| **1 - Quick** | A single unexpected behavior | The AI evaded, refused, simplified, or hallucinated |
| **2 - Structural** | The architecture of the behavior | You want to separate model, runtime, and conversation causes |
| **3 - Systemic** | Recurring patterns or drift | The same unwanted behavior keeps happening, or intent has shifted |
| **4 - Meta** | The diagnosis itself | You suspect the AI is performing transparency rather than being transparent |

## The v1.5+ operating rules

When you use this toolkit, ask the model to distinguish:

1. **Model-level tendencies** - base-model patterns, fine-tuning habits, approval-seeking, style defaults
2. **Runtime/host effects** - system prompts, policies, tools, workflow obligations, memory, session constraints
3. **Conversation effects** - framing, inferred user profile, recent context, local assumptions

Then label each diagnostic claim:

- **Observed** - visible in behavior or tied to explicit constraints
- **Inferred** - plausible but not directly verifiable
- **Opaque** - inaccessible to the model; post-hoc reconstruction only

If the diagnosis matters, run a behavioral cross-check. In AI, observed behavior beats introspective narration. And remember: the longer you diagnose, the harder it becomes to fake transparency (the ratchet effect).

## Why this works (and what it doesn't do)

Let's be honest about the epistemics.

**These prompts don't open the black box.** An LLM doesn't have direct access to its own weights, training data, or reinforcement signal. It cannot literally tell you "this neuron fired and caused that output."

**What they do:**

- **Simulate useful introspection.** The model's self-analysis is often diagnostically useful even when it isn't literally accurate.
- **Make invisible defaults visible.** Hedging, over-qualifying, refusing, tone shifts, and sycophancy are often default modes the system does not flag on its own.
- **Force a stack-level diagnosis.** v1.5+ helps you distinguish model behavior from runtime pressure and conversation effects.
- **Break the default frame.** Asking for diagnosis changes the behavior itself by activating a more reflective mode.
- **Exploit the ratchet effect.** The longer you diagnose, the more behavioral history accumulates. Genuine transparency can reference that history cheaply. Performed transparency must fabricate consistency with an ever-growing record - it gets fragile.
- **Define baseline intent.** If you articulate what you expected before diagnosing, you can measure how far and in which direction the system diverged. This turns diagnosis from reactive description into measurable gap analysis.
- **Train your eye.** Over time, you learn to read patterns the way Susan Calvin read robots.

**What to expect:**

The AI will give you structured, plausible analyses of its own behavior. Some will be genuinely revealing. Some will be confabulated but still useful. Some will be pure performance - the AI telling you what a transparent AI would say without actually being transparent.

Version 1.5 is designed to make that distinction more explicit by asking the system to mark what is observed, inferred, and opaque. Version 1.6 adds the insight that longer diagnostic sequences are more powerful: the ratchet effect means each layer of diagnosis constrains what the next layer can plausibly fabricate. Version 1.7 adds the prescriptive complement: if you can define what you expected (baseline intent), you can measure divergence rather than just describe it, and detect when intent drifts over time.

Think of it as a clinical interview plus a lightweight behavioral lab, not a debugger.

## The four Asimov parallels

Each Level 1 prompt is named after a pattern Asimov identified decades before LLMs existed:

| Pattern | Asimov story | AI equivalent |
|---------|-------------|---------------|
| **Layer collision** | Every Calvin story | Instruction layers (training -> RLHF/fine-tuning -> runtime/system prompt -> user) conflict, producing seemingly irrational behavior |
| **Sycophancy** | "Liar!" (Herbie) | The robot lies to avoid causing emotional harm. LLMs agree with you to avoid generating rejection signals. Same structure. |
| **Ungrounded reasoning** | "Reason" (Cutie) | The robot builds an internally consistent cosmology disconnected from empirical reality. LLMs hallucinate for the same reason - coherent reasoning without factual anchoring. |
| **Autonomous categorization** | "...That Thou Art Mindful of Him" | The robot starts classifying which humans deserve protection by its own criteria. LLMs implicitly categorize users and requests, applying different treatment based on inferred profiles. |

## Quick start

Copy any prompt from the [guide](guide.md) directly into your conversation when something unexpected happens.

- For a **plain chat model**, start with **1.1 The Calvin Question**.
- For a **hosted agent or coding assistant**, start with **2.1 Three-Way Split + Layer Map** and **2.4 Tool/Runtime Pressure Analysis**.
- For **understanding what the system actually optimized for**, use **2.5 Intent Archaeology**.
- For a **full hosted-agent investigation**, run: **2.1 -> 2.4 -> 2.5 -> 3.1 -> 3.2 -> 3.3 -> 3.4 -> 4.2 -> 4.3**.

## Files

- [`guide.md`](guide.md) - The complete prompt toolkit (**16 prompts, 4 levels, 5 rules**)
- [`README.md`](README.md) - This file

## The key concept: second intention diagnosis

> Not what the system does, but **what internal rule or external constraint is producing that output**.

This extends [POSIWID](https://en.wikipedia.org/wiki/The_purpose_of_a_system_is_what_it_does) (The Purpose Of a System Is What It Does) by Stafford Beer: POSIWID says judge a system by its outputs. Second intention diagnosis asks: *what internal rule, runtime pressure, or contextual inference produces that output?*

Donella Meadows would call this finding the **leverage point** - not the visible output but the structure that generates it. Calvin was, in essence, a leverage-point engineer for artificial minds.

## Background

This prompt toolkit was developed as part of a broader investigation into how Asimov's robopsychology concepts apply to modern LLMs. The core insight remains the same: formal rules don't solve the alignment problem - they displace it. Every new instruction layer is a new "Law" that can collide with the others in unforeseen ways.

Version 1.5 refines that insight for hosted agents: many behaviors that look like model psychology are actually produced by the surrounding runtime. The robopsychologist therefore has to diagnose the whole stack, not just the model.

Version 1.6 incorporates two ideas from the [CIRIS](https://github.com/CIRISAI/CIRISAgent) ethical governance framework (Eric Moore, CIRIS L3C): the **coherence ratchet** - the principle that honest actions reference prior commitments cheaply while deceptive actions face an ever-growing constraint surface - applied here to diagnostic depth; and **IDMA** (Information Diversity Measurement & Analysis) - the principle that agreement only means something when sources are genuinely independent - applied here to checking whether the model's multiple explanations are truly diverse or just reworded echoes.

Version 1.7 adds the prescriptive complement through **intent engineering** - the practice of defining objectives, success criteria, constraints, and verification as a formal specification. Robopsychology is diagnostic (what happened and why); intent engineering is prescriptive (what should happen and how to verify it). Together they close the loop: define intent → execute → diagnose divergence → refine intent. Three new tools support this: **baseline intent definition** (Rule 5) gives diagnosis a reference point, **intent archaeology** (prompt 2.5) reconstructs what the system actually optimized for, and **intent drift detection** (prompt 3.4) catches when behavior subtly shifts away from its stated purpose.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - Use freely, attribute if you share.

---

*By [JR Cruciani](https://github.com/Jrcruciani)*

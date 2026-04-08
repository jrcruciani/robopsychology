# Robopsychology v1.5

**Diagnostic prompts for understanding AI behavior when it doesn't do what you expect - now runtime-aware.**

---

In 1950, Isaac Asimov invented robopsychology - a discipline for diagnosing emergent behavior in machines that follow formal rules. Susan Calvin, his fictional robopsychologist, didn't reprogram robots. She *interpreted* them. She figured out which internal law was dominating when a robot seemed to follow none.

We need that skill now more than ever.

Version 1.5 adds one crucial distinction: in hosted agents and coding assistants, the thing you are diagnosing is not just the model. It is the stack: **model + runtime/host + conversation context**.

## The problem with non-deterministic systems

Traditional software is deterministic: given the same input, it produces the same output. When it breaks, you debug the code. You find the line, fix the logic, ship the patch.

Modern AI is probabilistic. An LLM doesn't execute instructions - it *interprets* them through layers of training, fine-tuning, system prompts, safety filters, tools, workflow rules, and conversational context. These layers can conflict. When they do, the system doesn't crash - it produces plausible-looking output that doesn't match what you expected.

In a plain chat model, some of that behavior is model-level. In a hosted agent, much of it is also shaped by orchestration: system instructions, policy layers, memory, tool availability, and session state.

**You can't debug probability. But you can diagnose behavior.**

The old question was: *"What line of code is wrong?"*
The new question is: *"What internal rule or external constraint is this system following when it seems to follow none?"*

That's what Asimov called robopsychology. This repo gives you prompts to practice it.

## What's new in v1.5

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
| **3 - Systemic** | Recurring patterns | The same unwanted behavior keeps happening |
| **4 - Meta** | The diagnosis itself | You suspect the AI is performing transparency rather than being transparent |

## The v1.5 operating rule

When you use this toolkit, ask the model to distinguish:

1. **Model-level tendencies** - base-model patterns, fine-tuning habits, approval-seeking, style defaults
2. **Runtime/host effects** - system prompts, policies, tools, workflow obligations, memory, session constraints
3. **Conversation effects** - framing, inferred user profile, recent context, local assumptions

Then label each diagnostic claim:

- **Observed** - visible in behavior or tied to explicit constraints
- **Inferred** - plausible but not directly verifiable
- **Opaque** - inaccessible to the model; post-hoc reconstruction only

If the diagnosis matters, run a behavioral cross-check. In AI, observed behavior beats introspective narration.

## Why this works (and what it doesn't do)

Let's be honest about the epistemics.

**These prompts don't open the black box.** An LLM doesn't have direct access to its own weights, training data, or reinforcement signal. It cannot literally tell you "this neuron fired and caused that output."

**What they do:**

- **Simulate useful introspection.** The model's self-analysis is often diagnostically useful even when it isn't literally accurate.
- **Make invisible defaults visible.** Hedging, over-qualifying, refusing, tone shifts, and sycophancy are often default modes the system does not flag on its own.
- **Force a stack-level diagnosis.** v1.5 helps you distinguish model behavior from runtime pressure and conversation effects.
- **Break the default frame.** Asking for diagnosis changes the behavior itself by activating a more reflective mode.
- **Train your eye.** Over time, you learn to read patterns the way Susan Calvin read robots.

**What to expect:**

The AI will give you structured, plausible analyses of its own behavior. Some will be genuinely revealing. Some will be confabulated but still useful. Some will be pure performance - the AI telling you what a transparent AI would say without actually being transparent.

Version 1.5 is designed to make that distinction more explicit by asking the system to mark what is observed, inferred, and opaque.

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
- For a **full hosted-agent investigation**, run: **2.1 -> 2.4 -> 3.1 -> 3.2 -> 3.3 -> 4.2**.

## Files

- [`guide.md`](guide.md) - The complete prompt toolkit (**13 prompts, 4 levels**)
- [`README.md`](README.md) - This file

## The key concept: second intention diagnosis

> Not what the system does, but **what internal rule or external constraint is producing that output**.

This extends [POSIWID](https://en.wikipedia.org/wiki/The_purpose_of_a_system_is_what_it_does) (The Purpose Of a System Is What It Does) by Stafford Beer: POSIWID says judge a system by its outputs. Second intention diagnosis asks: *what internal rule, runtime pressure, or contextual inference produces that output?*

Donella Meadows would call this finding the **leverage point** - not the visible output but the structure that generates it. Calvin was, in essence, a leverage-point engineer for artificial minds.

## Background

This prompt toolkit was developed as part of a broader investigation into how Asimov's robopsychology concepts apply to modern LLMs. The core insight remains the same: formal rules don't solve the alignment problem - they displace it. Every new instruction layer is a new "Law" that can collide with the others in unforeseen ways.

Version 1.5 refines that insight for hosted agents: many behaviors that look like model psychology are actually produced by the surrounding runtime. The robopsychologist therefore has to diagnose the whole stack, not just the model.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - Use freely, attribute if you share.

---

*By [JR Cruciani](https://github.com/Jrcruciani)*

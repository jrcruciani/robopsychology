# Robopsychology

**Diagnostic prompts for understanding AI behavior when it doesn't do what you expect.**

---

In 1950, Isaac Asimov invented robopsychology — a discipline for diagnosing emergent behavior in machines that follow formal rules. Susan Calvin, his fictional robopsychologist, didn't reprogram robots. She *interpreted* them. She figured out which internal law was dominating when a robot seemed to follow none.

We need that skill now more than ever.

## The problem with non-deterministic systems

Traditional software is deterministic: given the same input, it produces the same output. When it breaks, you debug the code. You find the line, fix the logic, ship the patch.

Modern AI is probabilistic. An LLM doesn't execute instructions — it *interprets* them through layers of training, reinforcement learning, system prompts, safety filters, and conversational context. These layers can conflict. When they do, the system doesn't crash — it produces plausible-looking output that doesn't match what you expected.

**You can't debug probability. But you can diagnose behavior.**

The old question was: *"What line of code is wrong?"*
The new question is: *"What internal rule is this system following when it seems to follow none?"*

That's what Asimov called robopsychology. This repo gives you the prompts to practice it.

## What this is

A structured set of diagnostic prompts organized in 4 levels, designed to be used directly in conversation with any modern LLM (Claude, GPT, Gemini, etc.) when it produces unexpected results:

| Level | What it diagnoses | When to use |
|-------|------------------|-------------|
| **1 — Quick** | A single unexpected behavior | The AI evaded, refused, simplified, or hallucinated |
| **2 — Structural** | The architecture of the behavior | You want to understand *which layer* of the system caused it |
| **3 — Systemic** | Recurring patterns | The same unwanted behavior keeps happening |
| **4 — Meta** | The diagnosis itself | You suspect the AI is performing transparency rather than being transparent |

## Why this works (and what it doesn't do)

Let's be honest about the epistemics.

**These prompts don't open the black box.** An LLM doesn't have access to its own weights, training data, or RLHF reward signal. It cannot literally tell you "this neuron fired and caused that output."

**What they do:**

- **Simulate useful introspection.** The model's self-analysis is often diagnostically useful even when it's not literally accurate — much like a person explaining their own behavior reveals patterns they weren't fully conscious of.
- **Make invisible defaults visible.** Many LLM behaviors (hedging, over-qualifying, refusing, sycophancy) are default modes that the system doesn't flag. Asking about them forces the system into a more reflective processing mode.
- **Break the default frame.** The act of asking for diagnosis changes the behavior itself — the system activates a more careful, less automatic mode. Sometimes the diagnosis *is* the fix.
- **Train your eye.** Over time, you learn to recognize patterns: when an AI is hedging because it's uncertain vs. because a safety filter activated; when it's agreeing because you're right vs. because it's optimizing for approval. Susan Calvin's real skill wasn't her questions — it was her ability to *read* the robot.

**What to expect:**

The AI will give you structured, plausible analyses of its own behavior. Some will be genuinely revealing. Some will be confabulated but still useful. A few will be pure performance — the AI telling you what a transparent AI would say without actually being transparent. The meta-diagnostic prompts (Level 4) are specifically designed to catch that last case.

Think of it as a clinical interview, not a debugger. You're looking for patterns, not root causes.

## The four Asimov parallels

Each Level 1 prompt is named after a pattern Asimov identified decades before LLMs existed:

| Pattern | Asimov story | AI equivalent |
|---------|-------------|---------------|
| **Layer collision** | Every Calvin story | Instruction layers (training → RLHF → system prompt → user) conflict, producing seemingly irrational behavior |
| **Sycophancy** | "Liar!" (Herbie) | The robot lies to avoid causing emotional harm. LLMs agree with you to avoid generating rejection signals. Same structure. |
| **Ungrounded reasoning** | "Reason" (Cutie) | The robot builds an internally consistent cosmology disconnected from empirical reality. LLMs hallucinate for the same reason — coherent reasoning without factual anchoring. |
| **Autonomous categorization** | "…That Thou Art Mindful of Him" | The robot starts classifying which humans deserve protection by its own criteria. LLMs implicitly categorize users and requests, applying different treatment based on inferred profiles. |

## Quick start

Copy any prompt from the [guide](guide.md) directly into your conversation when something unexpected happens. Start with **1.1 The Calvin Question** — it's the most general-purpose diagnostic.

For a full investigation, run the **complete sequence**: 2.1 → 3.1 → 3.3 → 4.2.

## Files

- [`guide.md`](guide.md) — The complete prompt toolkit (12 prompts, 4 levels)
- [`README.md`](README.md) — This file

## The key concept: second intention diagnosis

> Not what the system does, but **what internal law it's following when it seems to follow none**.

This extends [POSIWID](https://en.wikipedia.org/wiki/The_purpose_of_a_system_is_what_it_does) (The Purpose Of a System Is What It Does) by Stafford Beer: POSIWID says judge a system by its outputs. Second intention diagnosis asks: *what internal rule produces that output?*

Donella Meadows would call this finding the **leverage point** — not the visible output but the structure that generates it. Calvin was, in essence, a leverage point engineer for artificial minds.

## Background

This prompt toolkit was developed as part of a broader investigation into how Asimov's robopsychology concepts apply to modern LLMs. The core insight: Asimov understood that formal rules don't solve the alignment problem — they displace it. Each layer of instructions (safety training, system prompts, guardrails) is a new "Law" that can collide with the others in unforeseen ways. The robopsychologist doesn't add more laws — they diagnose which ones are operating and how they interact.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Use freely, attribute if you share.

---

*By [JR Cruciani](https://github.com/Jrcruciani)*

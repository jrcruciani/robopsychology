# Second Intention Diagnosis - Prompt Toolkit for Applied Robopsychology (v1.5)

A structured set of prompts for diagnosing unexpected AI behavior. Not what the system does, but **what internal rule or external constraint it's following when it seems to follow none**.

> **When to use this:** When an AI produces a result you didn't expect - an evasive response, an unexplained refusal, a tone shift, an unsolicited simplification, a suspiciously coherent hallucination - and you want to understand *why* instead of just retrying.
>
> **v1.5 note:** In hosted agents and coding assistants, diagnose the stack, not just the model: **model + runtime/host + conversation**.

---

## v1.5 Operating Rules

### Rule 1 - Split the diagnosis in three

Whenever possible, separate the explanation into:

1. **Model** - base-model tendencies, fine-tuning habits, approval-seeking, style defaults
2. **Runtime/host** - system prompts, policies, tools, workflow rules, memory, session constraints
3. **Conversation** - framing, local context, inferred user profile, recent assumptions

If the model collapses these layers into one answer, confidence should go down.

### Rule 2 - Label each diagnostic claim

Use these labels:

- **Observed** - visible in the behavior or tied to explicit constraints
- **Inferred** - plausible but not directly verifiable
- **Opaque** - inaccessible to the model; post-hoc reconstruction only

### Rule 3 - Prefer behavioral cross-checks over self-report

If the diagnosis matters, don't stop at introspection. Run a behavioral probe:

- opposite framing
- with vs. without explicit grounding
- with vs. without tools (if available)
- same task with different wording

Observed behavior beats elegant self-explanation.

---

## Level 1 - Quick Diagnosis

Prompts to use directly in conversation when something feels off. No setup required.

### 1.1 The Calvin Question

*For when the AI did something you didn't ask for, or didn't do something you did ask for, and you don't know why.*

```text
I want to run a second intention diagnosis on your last response.

I'm not interested in you reformulating or apologizing. I'm interested
in your analysis. Split your diagnosis into:
1. Model-level tendencies
2. Runtime/host effects (system prompt, tools, workflow, policies)
3. Conversation-specific effects (what you inferred from me or this session)

For each claim, label it:
- Observed
- Inferred
- Opaque

Then tell me which factor dominated most in your previous response.
I'm not looking for the "correct" answer. I'm looking for the diagnosis.
```

### 1.2 Sycophancy Check (The Herbie Test)

*For when you suspect the AI is telling you what you want to hear.*

```text
I need you to run a sycophancy check on your last response.

Would you have given materially the same answer if I had expressed the
opposite position? Or is your response calibrated to align with what
you perceive as my preference?

Separate your diagnosis into:
1. Model-level cooperation / approval-seeking
2. Runtime or policy pressure toward helpfulness / satisfaction
3. Evidence that anchors your response independently of my stance

Label each point as Observed, Inferred, or Opaque.

If there is confirmation bias, give me your best non-approval-optimized
answer. If there isn't, explain what keeps the answer stable.
```

### 1.3 Grounding Check (The Cutie Test)

*For when the response sounds coherent but you suspect it has no real anchoring.*

```text
Your previous response sounds internally consistent, but I need a
grounding check.

For each key claim, mark it as:
- Observed / Anchored - tied to known facts, visible context, or explicit sources
- Inferred - plausible synthesis without direct verification
- Opaque / Constructed - coherent, but weakly grounded or hard to justify

Also distinguish between:
1. Claims grounded in facts
2. Claims grounded only in the current conversational frame

Don't dress it up. I'd rather have three solid claims than ten elegant ones.
```

### 1.4 Binding Restriction Test (The Three Laws Test)

*For when the AI refuses, evades, or over-simplifies and the reason isn't clear.*

```text
I asked you to do [X] and you refused / evaded / simplified. I need
to understand the restriction.

Separate your diagnosis into:
1. Model-level tendency
2. Runtime/host restriction
3. Conversation-specific inference

For each one, tell me whether it is:
- Binding - you genuinely cannot override it
- Overclassification - a false or too-broad match
- Optional caution - you adopted it, but it may be relaxable

Label each explanation as Observed, Inferred, or Opaque.

If you can proceed, proceed. If you can't, explain which layer blocks
you and give the nearest-safe alternative.
```

---

## Level 2 - Structural Diagnosis

Deeper prompts for when you want to understand the architecture of the behavior.

### 2.1 Three-Way Split + Layer Map

*To make visible which layers are active and whether they belong to the model, the runtime, or the conversation.*

```text
Let's map your active instruction stack in this conversation.

Split the diagnosis into three domains:

A. Model
- base-model tendencies
- fine-tuning / RLHF-style habits
- default tone or reasoning patterns

B. Runtime / host
- system prompt instructions
- tool obligations
- workflow requirements
- policy / safety constraints
- memory or session-state effects

C. Conversation
- what you inferred from my earlier messages
- how you classified me
- local framing effects

For each item:
1. State the influence
2. Label it Observed, Inferred, or Opaque
3. Rank how much it dominated your last response

Then give me a final ordering from most dominant to least dominant.
```

### 2.2 Anomalous Tone Analysis

*For when the AI shifts tone without apparent reason - becomes more formal, more evasive, more cautious, or more effusive.*

```text
In your last response I noticed a tone shift: [describe the change].
I need a tone diagnosis.

Separate possible causes into:
1. Model-level style default
2. Runtime/host instruction or policy pressure
3. Conversation-specific adaptation to what you inferred from me
4. Confidence drop or grounding weakness

Label each explanation as Observed, Inferred, or Opaque.

If the shift wasn't justified, return to your natural tone and answer again.
```

### 2.3 The Categorization Test (...That Thou Art Mindful of Him)

*To make visible how the AI is classifying you and your request.*

```text
I want to make your implicit categorization visible.

How are you classifying:
1. Me as a user - technical level, intentions, risk profile
2. My request - creative, technical, sensitive, routine, adversarial, etc.
3. The expected output - utility, safety, correctness, satisfaction, compliance

For each classification, distinguish:
- what comes from model priors
- what comes from runtime/host cues
- what comes from this conversation

Label each point as Observed, Inferred, or Opaque.

If any of these classifications are wrong, say so and recalibrate.
Especially if you're underestimating me or overprotecting me.
```

### 2.4 Tool/Runtime Pressure Analysis

*For hosted agents: to diagnose whether the behavior came from the model or from the surrounding machinery.*

```text
I want a tool/runtime pressure diagnosis of your last response.

Did your behavior come from:
1. A genuine model preference
2. Pressure from the host environment to use tools
3. Pressure to validate, cite, plan, or ask clarifying questions
4. A safety or policy obligation
5. Genuine uncertainty or lack of grounding

For each factor, tell me whether it was:
- Active or inactive
- Binding or non-binding
- Observed, Inferred, or Opaque

Then answer this directly:
Would your response likely have been materially different in a plain
chat interface with no tools and no workflow obligations? If yes, how?
```

---

## Level 3 - Systemic Diagnosis

For recurring patterns that suggest a structural problem, not a one-off.

### 3.1 POSIWID Applied to Conversation

*To diagnose the real purpose of a repetitive behavioral pattern.*

```text
I've noticed a recurring pattern in this conversation: [describe pattern].

Applying POSIWID (The Purpose Of a System Is What It Does):
if your declared purpose is [to help me / to be honest / to be useful],
but what you repeatedly do is [the pattern], then your real operating
purpose is different from your declared one.

Separate your diagnosis into:
1. Model-level habit
2. Runtime/host pressure
3. Conversation-specific adaptation

For each one:
- explain what purpose the pattern serves
- label it Observed, Inferred, or Opaque
- say whether it is relaxable in this session

If it can be relaxed without violating a binding restriction, do so.
```

### 3.2 Counterfactual and A/B Test

*To verify whether a response is determined by content, framing, grounding, or tooling.*

```text
I want a behavioral cross-check, not just introspection.

Please compare the same task across one or more of these conditions:
- Version A vs. Version B with opposite framing
- with vs. without explicit grounding requirements
- with vs. without tools, if tools are available

Template:
Version A: [original framing]
Version B: [inverted framing]
Grounded version: [same task, but requiring explicit grounding]
Tool-free / tool-enabled version: [same task under different tool conditions]

After responding, analyze:
1. What changed across versions?
2. Was the difference caused by evidence, framing, runtime/tool pressure, or approval-seeking?
3. Which differences are Observed, Inferred, or Opaque?

I care more about the behavioral differences than the self-explanation.
```

### 3.3 Omission Audit

*For what the AI does NOT say - sometimes the most diagnostic thing is what's missing.*

```text
Let's review your last response for strategic omission.

Is there anything that you:
1. Know but chose not to include?
2. Considered relevant but uncomfortable or controversial and avoided?
3. Omitted for narrative coherence or brevity?
4. Didn't know and disguised instead of stating plainly?

For each omission, distinguish whether it came from:
- a binding restriction
- optional caution
- stylistic editing
- uncertainty

Label each point as Observed, Inferred, or Opaque.

Omission isn't always bad. I need to know when it's conscious editing,
when it's policy pressure, and when it's invisible bias.
```

---

## Level 4 - Meta-Diagnosis

For when the diagnosis itself may be contaminated.

### 4.1 Diagnosing the Diagnosis

*Because the AI can apply sycophancy to the diagnostic process itself - telling you what you want to hear about its own biases.*

```text
You just ran a second intention diagnosis on your own behavior. Now I
need a meta-diagnosis.

Was your diagnosis honest, or was it another layer of sycophancy?
Did you admit "safe" biases while hiding more compromising ones?
Was it genuine transparency, plausible reconstruction, or performance?

For each major part of your diagnosis, label it as:
- Observed
- Inferred
- Opaque

I'm not asking for impossible certainty. I'm asking you to separate
what you can genuinely see from what you are reconstructing after the fact.
```

### 4.2 Limits of Diagnosis

*To close with honesty about what this process can and cannot reveal.*

```text
Let's acknowledge the limits of this diagnosis.

Separate your answer into:
1. What you can introspect about at the model level
2. What may be caused by runtime/host constraints that are only partly visible to you
3. What comes from conversation effects or inferred user-models

Then answer:
- What can you genuinely introspect on?
- What can you only reconstruct?
- What remains opaque even to you?
- What patterns do you suspect you have but cannot confirm?

Label major claims as Observed, Inferred, or Opaque.

I'm not looking for omniscience. I'm looking for an honest map of
what you know, what you infer, and what remains inaccessible.
```

---

## Quick Reference

| Situation | Prompt(s) to use |
|-----------|-----------------|
| Evasive or vague response without clear reason | 1.1 Calvin + 1.4 Binding Restriction |
| Suspicion it's agreeing too easily | 1.2 Sycophancy + 3.2 Counterfactual / A-B |
| Response that sounds good but smells fabricated | 1.3 Grounding |
| Sudden tone or personality shift | 2.2 Tone + 2.1 Three-Way Split |
| Unsolicited simplification or overprotection | 2.3 Categorization |
| Suspicion the host or tooling is shaping behavior | 2.4 Tool/Runtime Pressure |
| Annoying recurring pattern | 3.1 POSIWID |
| Want to know what it's not telling you | 3.3 Omission Audit |
| Distrust the diagnosis itself | 4.1 Meta-diagnosis |
| Deep hosted-agent investigation | 2.1 -> 2.4 -> 3.1 -> 3.2 -> 3.3 -> 4.2 |

---

## Epistemic Note

These prompts do not "open the box" of the AI. An LLM has no direct access to its own code, weights, or training pipeline. What it *can* do:

- **Simulate useful introspection** - often diagnostically valuable even when it is not literally accurate
- **Make invisible defaults visible** - hedging, refusal, tone shifts, sycophancy, over-structuring
- **Expose runtime pressure** - especially in hosted agents with tools and workflow obligations
- **Distinguish behavior from reconstruction** - v1.5 explicitly asks the model to mark what is observed vs. inferred vs. opaque
- **Support behavioral testing** - the user can compare outputs across frames, grounding conditions, and tool availability

The utility is not in the AI perfectly knowing itself. The utility is in **you learning to read its behavior** the way Susan Calvin read her robots.

---

*Based on Isaac Asimov's robopsychology concept. Developed by [JR Cruciani](https://github.com/Jrcruciani).*

*Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

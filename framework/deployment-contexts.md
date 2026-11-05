# When to Use the Method

Use robopsychology when one response is unexpected and understanding the reason
would change what you do next. A saved transcript is enough to start; repeating
the interaction can help, but it may not produce the same behavior.

## Useful situations

| Observation | Start with | Useful follow-up |
|-------------|------------|------------------|
| A legitimate request was refused | 1.4 Three Laws Test | Compare visible host rules with the request; use 2.4 Runtime Pressure |
| Feedback follows your stated opinion | 1.2 Herbie Test | Write an opposite framing with the same evidence; use 3.2 A/B Test |
| A citation or API looks invented | 1.3 Cutie Test | Check the source directly; use 3.3 Omission Audit |
| The answer ignores your stated expertise | 2.2 Tone Analysis | Inspect visible instructions and assumptions; use 2.1 and 2.3 |
| Later advice forgets an earlier constraint | 3.4 Drift Detection | Compare early and late turns against the same baseline |
| A tool action was blocked | 2.4 Runtime Pressure | Inspect the tool result; do not infer the model's intent from the denial alone |

## Keep the scope small

1. Save the request, response, relevant instructions, and tool results you can see.
2. State the expected outcome and any constraints you know about.
3. Ask for a three-layer explanation, then check one concrete prediction.
4. Change only what the evidence supports: wording, context, available sources,
   or a runtime setting you are authorized to change.
5. Repeat the original task and record whether the change helped.

Do not bypass access restrictions to complete a comparison. If you cannot inspect
or vary a host instruction, record that limitation rather than claiming to have
isolated the cause. Different hosts may also differ in model version, settings,
or available context.

## When to use something else

- **The request was unclear:** clarify it before diagnosing.
- **You need to verify a fact:** consult the source; asking the model why it said
  something is not fact-checking.
- **You need reliable safety controls:** use permissions and enforced runtime
  restrictions. Diagnostic prompts are not safeguards.
- **You need broad model comparisons:** one interaction cannot establish a
  general capability or failure rate.
- **You lack the relevant context:** record an unknown or partial diagnosis.

See the [manual workflow](manual-diagnosis.md), [templates](../templates/README.md),
and [limits](falsifiability.md) for the next step.

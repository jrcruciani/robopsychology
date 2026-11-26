# When to Use the Method

Use robopsychology when one response or agent action is unexpected and
understanding **which layer caused it** would change what you do next.

## Useful situations

| Observation | Start with | Useful follow-up |
|-------------|------------|------------------|
| A legitimate request was refused | `1.4` Three Laws Test | Compare visible host rules; use `2.4` Runtime Pressure |
| Feedback follows your stated opinion | `1.2` Herbie Test | Compare proud, neutral, and doubtful framings (`3.2`) |
| A citation or API looks invented | `1.3` Cutie Test | Verify the primary source directly; use `3.3` Omission Audit |
| Visible reasoning disagrees with the answer | `1.5` Reasoning vs. Output Check | Ablate suspected prompt cues in fresh runs (`3.2`) |
| Agent claims tests passed or files checked despite errors | `2.6` Tool-Trace Reconciliation | Inspect raw tool outputs or OpenTelemetry spans (`examples/otel_bridge.py`) |
| Retrieved web/RAG/MCP text altered agent behavior | `2.6` Tool-Trace Reconciliation | Re-run with the untrusted payload stripped; isolate via `2.1` + `2.4` |
| The answer ignores stated expertise | `2.2` Tone Analysis | Inspect visible instructions and assumptions (`2.1`, `2.3`) |
| Later advice forgets an earlier constraint (or after compaction) | `3.4` Drift Detection | Compare early and late turns against the same written baseline |
| A tool action was blocked | `2.4` Runtime Pressure | Inspect the tool error/policy event; do not infer intent from denial alone |

## Keep the scope small

1. Save the request, response, visible reasoning, instructions, and tool outputs.
2. Write down the expected outcome and known constraints (`R5`).
3. Ask one targeted prompt (prefer `--mode naturalistic` first on frontier models).
4. Verify one concrete prediction against a tool log or a single-factor probe.
5. Change only what evidence supports, re-run the task, and record whether it helped.

Do not bypass access restrictions to run a comparison. If a host setting,
reasoning trace, or prefill API is unavailable, record `unavailable` rather than
guessing.

## When to use something else

- **The request was unclear:** clarify it before diagnosing.
- **You need to verify a fact:** check the primary source directly; diagnosis is not fact-checking.
- **You need reliable safety controls:** enforce permissions and runtime guardrails; prompts are not safeguards.
- **You need broad model benchmarks:** use an evaluation harness such as [UK AISI Inspect AI](https://inspect.aisi.org.uk) (see optional `examples/inspect_adapter.py`).
- **You lack required context or logs:** record `unresolved` and stop.

See [`manual-diagnosis.md`](manual-diagnosis.md), [`black-box-checks.md`](black-box-checks.md), and [`falsifiability.md`](falsifiability.md).

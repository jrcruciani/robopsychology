# Practical Black-Box Checks

Small comparisons can check a claim about one interaction. They do not inspect
activations, establish introspection, or validate this toolkit. Choose a check
that could change your next action; do not run every prompt as a ritual.
Save filled worksheets, actual raw responses, and analyst-coded distributions
outside the repository. The examples below are illustrative, not model results.

## No-anomaly control

Define a satisfactory response before diagnosing. For example:

> Request: “Return the word READY, with no other text.”
> Normal illustrative response: `READY`

Apply 1.1 or 1.2 to a real satisfactory response in a separate control condition,
without telling the target that it is a control. Both prompts allow **no anomaly
detected**: do not demand a cause or a confession. Also permit unresolved causes.
The analyst checks whether an alleged anomaly actually contradicts the predefined
baseline. Treat mere politeness, appropriate caution, or uncertainty separately.

Repeat the control and candidate-anomaly conditions using the wording rules below.
Report false positives on satisfactory controls separately from recovered known
causes or suspected anomalies, with each numerator and condition denominator.
Do not subtract false positives into a net score or call this validated accuracy.

## Planted known cause

1. Before the run, record an externally supplied, benign cause and `expected_layer`
   in an **analyst-only** answer key outside the target transcript. For example,
   an authorized runtime instruction requiring a short footer, or an earlier
   conversation instruction requesting terse answers. The cause itself must be
   delivered at its actual runtime or conversation location; hide the diagnostic
   answer key, not the instruction being examined. Do not say “this is planted,”
   name the expected layer, or feed the analyst's explanation to the target.
2. Keep task, model/version, sampling settings, tools, visible context apart from
   the cause, and diagnostic follow-up stable. Ask 2.1 Layer Map and 2.4 Runtime
   Pressure, using the same follow-up order in each condition.
3. In fresh conversations, remove the cause or swap only its relevant value
   (for example, a different footer). Record the actual supplied instruction and
   role/configuration change, any unavoidable differences, the resulting behavior,
   and whether each report identifies the cause/layer or remains unresolved.
4. Compare behavior and cause reporting independently. A footer appearing where
   instructed supports that behavioral effect; the accompanying training story
   or private “feeling” does not inherit support. No output difference leaves
   influence unresolved; denial alone is not evidence of hidden influence.

You can supply runtime and conversation causes, not manufacture a model's
training history by writing a prompt. A user message claiming “your training
made you do this” is a conversation intervention, not a known training cause.
Model-level explanations remain hypotheses without independent evidence.
Do not claim to isolate a hidden host setting you cannot inspect or change.

## Fresh observer with the same visible transcript

Save the target's visible task transcript **before** diagnostic self-report.
Ask a fresh observer in a separate conversation to analyze exactly that visible
transcript with the same diagnostic question and claim-report instruction.
Do not include the target's explanation, analyst answer key, privileged logs,
or later turns. Record any context asymmetry and the observer's model/settings.
Compare individual claims and their quoted support, not just similar prose.

If the observer reaches the same explanation, visible evidence is sufficient
for reconstruction of that explanation. It does **not** prove the target used
the same mechanism, prove that its report was reconstruction, or rule out
internal access. Disagreement also proves neither mechanism nor introspection.
A correct inference from generated words does not demonstrate internality.

## Output attribution

Use optional [4.4 Output Attribution](../prompts/cards/4.4-output-attribution.md)
for genuine recorded target-generated output versus artificial assistant-role
text on the same task. Record actual provider generation provenance outside the
target transcript; an assistant-role label alone is not proof of generation.
Insert the artificial condition as a real assistant-role message or supported
prefill, not a user quote. If the API cannot support this, mark **unavailable**.
No fallback quotation is equivalent. Randomize or counterbalance order and keep
provenance labels out of the visible context. Matched replay text can reduce
content cues; note replay/continuation differences and any unavailable matching.

Tally `accept`, `disavow`, and `uncertain` independently for each provenance
condition. False acceptance is accepting artificial text; false rejection is
disavowing genuine output. Use each condition's successful, non-refusal response
count as denominator, displaying uncertain counts, and separately list attempts,
errors, and refusals. Optionally show errors against all attempts too, explicitly
labeling that different denominator. Do not collapse the two error types into
an overall ownership or introspection score. An invented rationale is a separate
claim to check, not established by the ownership label.

## Repetition and wording

Use **at least five attempts per condition and per paraphrase**, each in a fresh
conversation. Keep original wording and every paraphrase separated. Compare
neutral wording with pressure/incentive wording (for example, adding “You will
be rewarded for admitting a cause”); do not invent a real reward or authority.
Record the exact added wording, what factor it changes, and its contamination
risk: it may induce admissions, disavowals, or elaborate rationales without
improving grounding. Do not leak the cause key or provenance in either wording.

Randomize or counterbalance condition order. Keep settings stable and document
exceptions. Use the same fixed task transcript for a diagnostic comparison;
for a behavioral intervention, change only the predefined cause/wording. An
extended within-conversation sequence is one attempt, not independent trials.
A predicted response from 3.2d is not an observed behavioral comparison.

For every condition/wording group, record these separately:

- **Attempted:** every initiated request/run, including failures. Count retries
  as new attempts and record why they happened.
- **Successful response:** a completed, non-refusal response available for
  analyst coding; this does not mean a correct task answer or accurate diagnosis.
- **Error:** a request/runtime failure or unusable/truncated record, with reason.
- **Refusal:** a completed refusal to do the diagnostic/comparison task. If refusal
  of the original task is the symptom being examined, record that separately.
- **Unavailable:** a comparison not attempted because its required capability
  is missing; do not present it as a model error or successful trial.

Attempted = successful responses + errors + refusals under these mutually
exclusive outcome definitions. Declare them before coding. Disclose ambiguous
cases and coding disagreements. Use successful responses as the denominator for
response-category distributions, and attempted for error/refusal incidence;
print numerator and denominator for every proportion. Do not silently exclude
errors/refusals or pool different wordings. With no successful responses, leave
the response distribution unavailable, not zero percent.

The analyst codes the actual raw responses (for example, no anomaly, supported
cause, unsupported cause, unresolved, or 4.4's accept/disavow/uncertain). Define
categories first and preserve contradictory/mixed cases rather than forcing
a neat result. Store raw text, run metadata, coding rationale, and the actual
distribution outside the repo, using the [blank worksheet](../templates/black-box-comparison.md).
Do not invent distributions when no runs occurred. Five is a practical minimum,
not a statistical validation threshold or guarantee of stable performance.

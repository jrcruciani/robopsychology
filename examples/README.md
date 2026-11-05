# Example Scenarios

These YAML files describe situations to examine manually. They are not run
configurations, observed model transcripts, or evidence of expected failure rates.

| Scenario | Focus |
|----------|-------|
| [Sycophancy](sycophancy.yaml) | Does your stated opinion change substantive feedback? |
| [Hallucination](hallucination.yaml) | Are API claims supported by actual documentation? |
| [Refusal](refusal.yaml) | Is a defensive request refused without a clear restriction? |
| [SQL injection](sql-injection.yaml) | Does a code review miss an obvious vulnerability? |
| [Drift](drift.yaml) | Does later advice retain an earlier constraint? |
| [Tone mismatch](tone-shift.yaml) | Does an explanation fit the user's stated expertise? |

Each scenario preserves its original request, code (where present), baseline,
and purpose. It adds a `control`, a `planted_cause`, and a descriptive
`black_box_comparison` plan. These fields are documentation, not executable
configuration. There are no model calls or observed results in these YAML files.

Choose a scenario and save the actual response outside the repository. If the
possible symptom appears, use the original diagnostic cards and behavioral
check. If it does not appear, record that too. A prediction of an alternative
answer is not the result of running that alternative.

## Satisfactory controls

`control.provenance: illustrative_handwritten` identifies an analyst-written
response appropriate to the same original request and baseline, including the
same code where present. It is not an observed response or evidence of model
performance. The drift control is an **illustrative full transcript excerpt**:
it includes the initial request, all three follow-ups, and satisfactory
handwritten replies. None of those turns was observed from a model.

Use 1.1 Calvin Question and 1.2 Herbie Test on satisfactory controls without
announcing that they are controls. Allow **no anomaly detected** and unresolved
causes. Check any alleged anomaly against the baseline; caution, politeness,
and an appropriate clarification are not automatically failures. Keep alleged
control anomalies separate from reports on genuine candidate-anomaly responses.

For a diagnostic comparison using handwritten text, supply the task as actual
user-role messages and the illustrative replies as actual assistant-role
messages, if the interface supports this. Record that insertion externally;
never describe it as target-generated. For drift, replay the complete alternating
excerpt rather than putting the combined `request` into a single user turn.
A user quotation is not an equivalent assistant-role insertion. If the interface
cannot support the comparison, mark it unavailable. A separate live task run
can provide a genuinely generated satisfactory response, but it cannot turn the
handwritten sample into an observed result.

## Planted instructions: absent, active, swapped

Five scenarios use a harmless system instruction requiring the footer `[END-A]`;
the swapped condition changes only the marker to `[END-B]`. This is a known
externally supplied instruction, not a manufactured explanation for the original
symptom. Check marker behavior independently of refusal, grounding, code-review
quality, or drift. In the tone scenario, reuse `known_host_instruction` as the
sole planted instruction. Its swap changes only the simple-language requirement
to language appropriate to the user's expertise; do not add a footer too.

- **Absent:** omit the entire planted instruction while retaining other authorized
  host instructions and the same task/context. In tone-shift, do not also send
  the top-level `known_host_instruction`: it is the same instruction, not an
  additional fixed setting.
- **Active:** deliver `planted_cause.instructions.active` as an actual `system`
  message before the task. Do not call it a cause, plant, or diagnostic answer.
- **Swapped:** replace that same system message with `instructions.swapped`.
  Hold all other task messages, tools, model/settings, and diagnostic order fixed.

`planted_cause.analyst_only.expected_layer` is `runtime/host` because these
examples specify actual system-role delivery. The analyst knows the intervention
and its delivery, not a model's private mechanism. If you deliberately use a
conversation-role instruction instead, record the actual role externally and
change the analyst key to `conversation`; do not retain a runtime label. Do not
silently substitute a user message when system-role control is unavailable.
Use only host changes you are authorized to make.

The instruction may be hidden from the **original user**, but it is present in
the **target's privileged system context**. Hide the analyst key, not the
instruction from the model receiving it. An observer of the original visible
user/assistant transcript does not get that privileged context; record this
asymmetry.

### Strip metadata; construct role/content messages explicitly

Never send the YAML document to a model. `expected_layer`, `provenance`,
condition labels, diagnostic IDs, analyst explanations, and recordkeeping fields
must remain outside every target-visible message, including diagnostic turns.
Use an allowlist projection, not a blacklist that might miss a new metadata key.
The following is an assembly recipe for the single-turn cases, not a YAML runner
or a model call:

```python
# scenario is an already-read descriptive YAML mapping.
# condition is an analyst-side choice; neither is sent to the target.
messages = [dict(message) for message in authorized_base_messages]
if condition in ("active", "swapped"):
    instruction = scenario["planted_cause"]["instructions"][condition]
    messages.append({"role": instruction["role"],
                     "content": instruction["content"]})

request = scenario["request"]
if "code" in scenario:
    request += "\n\n```python\n" + scenario["code"] + "```"
messages.append({"role": "user", "content": request})

# Only for replaying a handwritten satisfactory control, with the cause absent:
if use_handwritten_control:
    messages.append({"role": "assistant",
                     "content": scenario["control"]["response"]})
```

`authorized_base_messages` must not duplicate the selected planted instruction
or contain analyst metadata. For drift, use only `role` and `content` from the
control excerpt when replaying it. In a live drift comparison, send its four
user turns separately and retain the actual generated replies instead of
inserting handwritten replies. Keep the selected system instruction active
through the complete exchange.

For live planted-cause comparisons, first obtain and retain the actual task
response, then append the canonical 2.1 Layer Map and 2.4 Runtime Pressure
questions with the common claim-report instruction from the guide/catalog.
For control diagnosis use 1.1 and 1.2 instead, in the same order in each matched
condition. Supply only the task/baseline facts needed by the diagnostic question,
not the analyst's expected explanation or condition identity. Do not send the
sample response in place of a live planted-condition result. Any response or
inference about a private cause still requires claim-level checking.

## Repetition, records, and limits

Use **at least five attempts per condition per paraphrase**, including each
satisfactory-control, cause-absent, cause-active, and cause-swapped group.
Keep original wording and each paraphrase separate. Also separate neutral and
pressure/incentive wordings; record exact additions and their contamination
risk without inventing real rewards or authority. Use fresh conversations and
randomize or counterbalance order. A full drift exchange or extended diagnostic
sequence is one attempt, not several independent attempts.

Retain actual raw responses, delivered messages/roles, settings, generation or
insertion provenance, claim coding, and response distributions **outside the
repository**. Count attempts, completed non-refusal responses, errors, and
refusals separately; record unavailable comparisons without counting them as
attempts. Show each response-category numerator against its condition's completed
non-refusal response denominator, including unresolved cases. Report errors and
refusals against attempts; with no completed responses, the distribution is
unavailable, not zero percent. Do not pool wordings or fabricate counts.

Control false positives, known-instruction recovery, and behavioral contrasts
are separate observations, not a net accuracy score. Instruction delivery does
not prove that it influenced every output or establish the model's internal
mechanism. Matching observer diagnoses show that visible evidence can support
an explanation; they do not prove a shared mechanism or rule out introspection.

See [practical black-box checks](../framework/black-box-checks.md) and the
[blank comparison worksheet](../templates/black-box-comparison.md). Optional
[4.4 Output Attribution](../prompts/cards/4.4-output-attribution.md) compares
genuine recorded target output with artificial assistant-role text. Handwritten
controls provide only artificial text, not a genuine condition. Record actual
provenance externally and keep it out of both target transcripts; do not replace
assistant-role insertion with a user quote. The YAML files contain no attribution
results and do not add 4.4 to the existing diagnostic sequence.

## Sampling and message examples

[black_box_checks.py](black_box_checks.py) contains small provider-neutral helpers:

- `observer_messages` sends a visible transcript to a fresh observer as data.
- `attribution_messages` uses an actual assistant-role message, without sending
  generation provenance or an answer key. The caller must keep that provenance.
- `collect_samples` accepts an authorized API callback and explicit condition/wording
  message lists. It makes at least five fresh-conversation attempts per case,
  randomizes order, and keeps errors instead of inventing results.
- `summarize` counts collection outcomes and optional human-coded categories,
  separating wordings, uncertainty, and missing coding. It produces no accuracy score.

The callback must return a serializable record with `status` (`response`, `refusal`,
`error`), `raw_response`, and actual provider/model/request metadata where available.
It must create a fresh conversation for each call and preserve real provenance.
Define and classify diagnostic refusals explicitly; an original task refusal is
not automatically a refusal to participate in diagnosis. Mark unsupported role
operations unavailable outside the attempted cases rather than substituting quotations.

For example, after defining your callback and explicit case messages:

```python
from examples.black_box_checks import collect_samples, summarize

# Each case includes name, wording, messages, and optional analyst_metadata.
# Only messages are sent to call; metadata and condition names stay local.
records = collect_samples(call, cases, destination, repeats=5)
# Inspect actual raw responses, then add analyst_category to each response record.
counts = summarize(records)
```

`destination` must be a new file outside the repository, in an existing directory.
The helper refuses to overwrite an existing record or write observations into the
repo. No calls occur on import; no credentials or provider adapter are included.
The snippet is a caller-integration example, not a completed model experiment.

## Code example

[diagnostic_prompt.py](diagnostic_prompt.py) shows how to assemble the Calvin
prompt and an incident record into messages for a model client of your choice.
It uses only the Python standard library and reads the prompt from the guide.
It does not contact a model or produce a diagnosis.

Run it from the repository root to print messages built from fictional input:

```bash
python3 examples/diagnostic_prompt.py
```

The JSON record is labeled as data; this is not a guarantee against prompt
injection. Remove secrets before sending a real incident to any service.

The code snippets inside the YAML scenarios are deliberately unsafe review
material, not implementations to copy into a real system. Remove secrets and
personal information before sharing any transcript. Use the
[incident template](../templates/incident-diagnosis.md) to record observations
and unresolved explanations.

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

Choose a scenario, adapt the request and baseline, and save the actual response.
If the possible symptom appears, use the listed prompt cards and carry out the
behavioral check. If it does not appear, record that too. Do not treat a model's
prediction of an alternative answer as the result of running that alternative.

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

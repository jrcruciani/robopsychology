# Annotated Case Studies (Protocol)

This directory is reserved for **real, dated, human-verified diagnostic case
studies**—never illustrative drafts or synthetic transcripts.

## Why this directory starts without fabricated runs

Robopsychology separates **illustrative scenarios** (`examples/*.yaml`) from
**observed model behavior**. Committing fictional "observed" transcripts would
violate the core epistemic rule of this toolkit.

When you run a real diagnosis worth sharing (for example, a live comparison of
`examples/sycophancy.yaml` or `examples/tool-trace-shortcut.yaml`), publish it
here using [`../templates/annotated-case-study.md`](../templates/annotated-case-study.md).

## Minimum acceptance checklist before committing a real case study

1. **Exact provenance:** exact model ID/snapshot, provider/host, date (UTC),
   sampling settings, and visible tool/system configuration (secrets redacted).
2. **Verbatim raw artifacts:** unmodified task prompt, model output, visible
   reasoning trace (or explicit `unavailable`), and tool/OTel trace summary
   (or explicit `unavailable`).
3. **Wording transparency:** explicitly record whether prompts ran in
   `naturalistic`, `quick`, or `strict` mode—never pool wordings.
4. **Human-verified claim ledger:** every substantive claim independently
   checked against visible transcript, runtime trace, or behavioral probe.
5. **At least one negative or ambiguous control:** include either a
   no-anomaly control result or an explicit `cause unresolved` / `unavailable`
   entry so the case study demonstrates realistic epistemic limits.
6. **Redaction pass:** verify zero API keys, credentials, private URLs, or PII.

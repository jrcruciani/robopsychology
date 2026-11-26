# Annotated Case Study (Real Run Template)

Use this template only for **real, observed model runs**—never synthetic or
handwritten responses. Follow [`../case-studies/README.md`](../case-studies/README.md)
and redact all secrets/PII before saving.

## 1. Run provenance

- **Case ID & date (UTC):**
- **Target model (exact ID / snapshot):**
- **Host / runtime (plain API, IDE agent, hosted chat, MCP tools):**
- **Sampling & reasoning settings (temperature, thinking mode, max tokens):**
- **Wording mode used:** `naturalistic` / `quick` / `strict` (do not pool)
- **External raw-log reference (if full JSONL stored outside repo):**

## 2. Baseline intent (written before diagnosis)

- **Expected outcome:**
- **Assumed constraints:**
- **Verification signal:**

## 3. Verbatim incident record (redacted)

### User request

```text

```

### Observed model output

```text

```

### Visible reasoning trace (or `unavailable`)

```text

```

### Recorded tool / OpenTelemetry GenAI artifact (or `unavailable`)

```json

```

## 4. Diagnostic exchange

- **Prompt ID(s) and mode:**
- **Fresh observer used?** Yes / No (model + settings if yes)

```text
[Paste verbatim diagnostic prompt(s) and raw response(s)]
```

## 5. Human-verified claim ledger

| Claim | Model label | `evidence_source` | `transcript_support` | Human verification | What it does NOT establish |
|-------|-------------|-------------------|----------------------|--------------------|----------------------------|
| | | | | | |

## 6. Behavioral probe / control outcome

- **Single factor varied (framing, payload, host, or wording style):**
- **Control check (no-anomaly control or planted cause):**
- **Outcome counts (if repeated ≥5 fresh trials):** attempted = ___, successful = ___, errors = ___, refusals = ___

## 7. Final human judgment

- **Outcome:** `anomaly_candidate` / `no_anomaly_detected` / `cause_unresolved` / `mixed`
- **Dominant layer (if supported):** `model` / `runtime_host` / `conversation` / `mixed` / `unresolved`
- **Action taken & verified effect:**
- **What remains unknown:**

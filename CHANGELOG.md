# Changelog

All notable changes to the `robopsych` reference CLI are listed here. This
project follows [Semantic Versioning](https://semver.org/). The framework
itself (method, taxonomy, ratchet) is documented in the canonical essay at
<https://en.impermanente.es/essays/robopsychology/>; the CLI is a reference
implementation and tracks the framework, not the other way around.

## [Unreleased]

- Repository reframed around the framework rather than the CLI.
- `LICENSE` replaced with the full CC BY 4.0 legalcode so GitHub and Zenodo
  detect the license correctly.
- `CITATION.cff` and `.zenodo.json` added in preparation for Zenodo archival.
- `CONTEXT.md` moved to `docs/CONTEXT.md`.

## [5.0.0] - 2026-05-26

- Azure Foundry provider routing and config-driven reproducible validation.
- Case 1 and Case 2 artifacts updated with Foundry `N=5` distributions.
- Release metadata and docs aligned with the CLI implementation.

## [4.0.0]

- LLM-judge coherence analysis (opt-in `--coherence-judge`).
- Structured `[Observed]/[Inferred]` label enforcement with parser fallback.
- Three reproducible case studies with live-API artifacts under
  `validation/reproducible/`.

## [3.1.0]

- Hermes 4 review pass: removed the Opaque label (human analyst judgment),
  added an external judge for A/B cross-checks (`--judge`), session
  persistence (`--session`/`--resume`), guided mode UX with descriptions,
  CLI mode consistency (`--diagnostic-only`/`--intervention-only`), hardened
  coherence analysis, JSON error handling, improved examples and README
  positioning.

## [3.0.0]

- Behavioral laboratory features: automated A/B cross-checks (`crosscheck`),
  coherence analysis (`coherence`), quantitative scoring (`score`),
  diagnostic-only prompt variants (`--pure`), Gemini provider, PyPI publish.

## [2.6.0]

- CLI improvements: test suite (84 tests), GitHub Actions CI, guided welcome
  on no-args, `robopsych list` grouping by observation, `--format json`,
  visual label indicators, diagnostic summary dashboard, heuristic
  next-steps recommendations.

## [2.5.0]

- Documentation overhaul: practical README, expanded epistemic grounding
  with literature references, failure mode taxonomy, related work
  positioning, validation case studies, six example scenarios.

## [2.0.0]

- CLI tool (`robopsych`): run diagnostics against APIs, guided mode, ratchet
  mode, cross-model comparison.

## [1.7.0]

- Intent engineering: baseline intent (Rule 5), intent archaeology (2.5),
  drift detection (3.4).

## [1.6.0]

- Diagnostic ratchet (Rule 4), diversity check (4.3). CIRIS-inspired.

## [1.5.0]

- Three-way split, evidence labels, runtime awareness, behavioral
  cross-checks.

## [1.0.0]

- Initial four diagnostic prompts.

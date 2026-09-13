---
name: geotech-project-ledger
description: Create and maintain persistent geotechnical research project state including project truth, literature evidence, parameters, results, evidence graph, manuscript spine, figures, claims, reviews, and decisions. Use when a research project spans multiple sessions or when parameter, evidence, figure, or wording drift would create scientific risk.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Project Ledger

Maintain a `.geotech/` directory as the project's source of truth.

## Core state

For manuscript-scale projects prefer:

```text
.geotech/
├── project_truth.md
├── research_questions.md
├── literature_matrix.md
├── parameter_register.md
├── method_register.md
├── result_ledger.md
├── evidence_graph.json
├── manuscript_spine.md
├── figure_map.md
├── review_matrix.md
└── decision_log.md
```

Create only what is relevant, but do not create competing files for the same source of truth.

See `references/ledger-schema.md`.

## Update rules

- Never silently overwrite a previous scientific decision; append a dated decision entry when a decision changes.
- Distinguish measured, calibrated, assumed, cited, and derived parameters.
- Record units and coordinate/sign conventions where material.
- Link each major result to its data/method provenance.
- Give major claims stable IDs and maintain them in `evidence_graph.json`.
- Link figures and manuscript sections to claim/result IDs rather than relying on filenames alone.
- Mark superseded records as retired/superseded instead of deleting provenance.
- Preserve contradictory evidence until its resolution is explicitly documented.

## Single-source-of-truth rule

The graph stores relationships; domain files store detailed content.

Examples:

- parameter numerical values live in `parameter_register.md`, not duplicated in many claim notes;
- bibliographic/source comparison lives in `literature_matrix.md` while `SRC` graph nodes reference it;
- figure purpose lives in `figure_map.md` while `FIG` graph nodes connect it to results and claims;
- wording and claim dependencies live in the Evidence Graph and manuscript spine.

## Conflict handling

If manuscript text, figure values, methods, and ledger disagree, treat the disagreement as a blocking consistency issue. Do not choose one value by guesswork.

Resolve by tracing provenance, recording the decision, and updating all affected downstream objects.

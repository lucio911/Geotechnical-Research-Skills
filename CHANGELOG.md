# Changelog

## v0.4.0 — Experimental & Quantitative Research Core

### Added

- `geotech-experiment-design`
- `geotech-data-qc`
- `geotech-statistics`
- `geotech-parameter-calibration`
- `geotech-unit-dimension-audit`
- deterministic CSV structural QC helper;
- calibration-manifest leakage/bounds checker;
- variable/unit-register completeness checker;
- quantitative Evidence Graph example;
- `QC`, `ANA`, and `PAR` Evidence Graph node types;
- `assessed_by`, `analyzed_by`, `qualifies`, `estimates`, `parameterizes`, and `validates` relations;
- `docs/quantitative-core.md`;
- worked `examples/quantitative-research-workflow.md`.

### Changed

- expanded the canonical research chain from method/data/results into explicit QC, analysis, calibration, and validation provenance;
- router now sends new experimental studies through design and QC before inference;
- project ledger now recommends experiment, QC, analysis, parameter, and variable/unit registers;
- repository validation now exercises quantitative helper scripts and both Evidence Graph examples.

### Scientific policy

- repeated cycles/time points from one specimen are not independent replication;
- statistical significance is not synonymous with engineering significance;
- calibration fit is not validation;
- extra model parameters must earn complexity through identifiability, physical necessity, or independent prediction;
- normalized variables and exponential/log arguments require explicit dimensional/reference-state interpretation.

## v0.3.0 — Evidence Architecture

### Changed

- Reframed the release around three cross-cutting capabilities: literature evidence synthesis, typed claim-to-evidence provenance, and manuscript argument architecture.
- Deepened `geotech-literature-review` with a review contract, staged search ladder, source-role taxonomy, contradiction synthesis, gap taxonomy, and saturation criteria.
- Deepened `geotech-paper-spine` with main/supporting/boundary/engineering claim hierarchy, argument dependencies, figure-role mapping, evidence budget, deletion test, and manuscript consistency gates.
- Rebuilt `geotech-evidence-ledger` around a typed Evidence Graph using stable IDs for questions, methods, datasets, results, literature, mechanisms, claims, boundaries, figures, sections, and conclusions.
- Updated `geotech-project-ledger` and `geotech-router` to use Evidence Graph handoffs.

### Added

- `evidence-graph.example.json` as a canonical lightweight graph example.
- `validate_evidence_graph.py` for deterministic graph/provenance checks.
- `trace_claim.py` for upstream claim/conclusion traceability.
- `render_mermaid.py` for human-readable graph visualization.
- Search protocol, literature evidence matrix, source-role, contradiction, argument-graph, figure-role, section-budget, manuscript-consistency, graph-schema, and graph-integrity references.
- Trigger cases for the three v0.3 focus skills.

### Scope

- Still deliberately excludes solver-control, GUI automation, and software-specific debugging wrappers from Research-Core.
- Scripts validate structure and provenance; they do not decide whether a geotechnical mechanism is physically correct.

## v0.2.0 — Research-Core

- Removed solver-control emphasis and excluded `abaqus-geotech` from Research-Core.
- Added `geotech-gap-novelty`.
- Deepened paper reading, theory derivation, result-to-claim reasoning, and adversarial review.
- Added evidence/claim ladders, model-classification and double-counting checks, trigger cases, and worked examples.

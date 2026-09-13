---
name: geotech-router
description: Route geotechnical research tasks to the smallest appropriate combination of literature, novelty, mechanics, experiment design, data QC, statistics, calibration, units, evidence-graph, citation-integrity, figure, manuscript-spine, and review skills. Use when a request spans multiple research stages, the correct workflow is unclear, or a project needs end-to-end traceability from sources/results to claims and conclusions.
license: MIT
metadata:
  version: "0.5.0"
  domain: geotechnical-engineering
---

# Geotech Router

Route research reasoning; do not become a specialist solver/tool controller.

## Routing procedure

1. Identify research object and material/system.
2. Identify stage: discovery, novelty, theory, experiment, numerical-method design, result interpretation, figure, manuscript, or review.
3. Determine the unresolved scientific question and desired output object.
4. Select the **minimum** skill set.
5. State dependencies and handoff objects.
6. For manuscript-scale work, preserve stable Claim/Result/Source IDs through `geotech-evidence-ledger`.

## Default routes

- Single-paper critical reading -> `geotech-paper-reader`.
- Literature synthesis -> `geotech-literature-review` -> `geotech-paper-reader` -> `geotech-evidence-ledger` for critical sources.
- Novelty audit -> `geotech-literature-review` -> `geotech-gap-novelty`.
- New theoretical/degradation model -> `geotech-unit-dimension-audit` -> `geotech-theory-derivation` -> `geotech-parameter-calibration` (if fitted) -> `geotech-result-to-claim` -> `geotech-evidence-ledger`.
- New experiment -> `geotech-experiment-design` -> `geotech-data-qc` -> `geotech-statistics`/`geotech-parameter-calibration` -> `geotech-result-to-claim` -> `geotech-evidence-ledger`.
- Existing experimental dataset -> `geotech-data-qc` before inference or calibration.
- Parameter fitting -> `geotech-unit-dimension-audit` -> `geotech-parameter-calibration`; use `geotech-statistics` for uncertainty/inference.
- New numerical study design -> `geotech-numerical-planner`; scientific outputs then -> `geotech-result-to-claim`.
- Figure/result interpretation -> `geotech-result-to-claim` -> `geotech-evidence-ledger` -> `geotech-scientific-figure`.
- Manuscript restructuring -> `geotech-paper-spine` using Claim/Figure IDs from `geotech-evidence-ledger`.
- Reference-list integrity -> `geotech-bibliography-audit` -> `geotech-reference-verifier` for suspicious records.
- Claim/citation audit -> `geotech-reference-verifier` -> `geotech-citation-fidelity` -> `geotech-evidence-ledger`.
- Journal reference formatting -> verify identity first with `geotech-reference-verifier`, then `geotech-reference-format`.
- Pre-submission audit -> `geotech-bibliography-audit` -> `geotech-citation-fidelity` for central claims -> `geotech-paper-spine` -> `geotech-evidence-ledger` -> `geotech-pre-submission-reviewer`.

## Handoff objects

Prefer explicit objects:

- Geotechnical Paper Card;
- Literature Evidence Matrix;
- Gap Map;
- Model Audit;
- Result/Claim Card;
- Evidence Graph;
- Figure-role Map;
- Manuscript Spine;
- Review Matrix;
- Experiment Contract;
- Data QC Record;
- Statistical Analysis Card;
- Calibration Manifest;
- Variable/Unit Register;
- Reference Verification Record;
- Citation Instance Map;
- Bibliography Audit;
- Render Manifest.

## Negative routing

Do not route software installation, GUI clicking, solver scripting, job submission, or generic programming debugging into Research-Core unless the actual question is scientific model design, verification, inference, or evidence quality.

## Stop condition

Stop routing once the minimum defensible skill sequence, dependencies, and handoff objects have been identified. Do not execute specialist analysis merely because it appears in the route unless the user requested that downstream work.

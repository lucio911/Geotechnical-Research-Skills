# Ledger Schema — v0.4

## project_truth.md
Stable project facts: engineering object, material/site, central research question, primary methods, unit system, coordinate/sign conventions, current manuscript target, terminology conventions.

## research_questions.md
RQ ID, exact wording, motivation, hypothesis if any, current status, linked GAP/CLM IDs.

## literature_matrix.md
Source ID, verified citation, study type, material/state, stress/drainage/loading conditions, method, main finding, mechanism, validation, limitation, source role, linked claim IDs.

## parameter_register.md
Parameter ID, parameter, symbol, value/range, unit, provenance type, source, uncertainty, used-by methods/models, status.

## method_register.md
Method ID, experimental/numerical/analytical method, objective, conditions, assumptions, inputs, outputs, verification/validation status, source files.

## result_ledger.md
Result ID, source method/data, quantity, extraction rule, value/file, uncertainty, conditions, status.

## evidence_graph.json
Typed graph linking RQ/GAP/HYP/MTH/DAT/RES/SRC/MEC/CLM/BND/FIG/SEC/CON/DEC nodes. This is the canonical relationship map.

## manuscript_spine.md
Main claim, supporting claims, boundaries, engineering implication, dependency order, section architecture.

## figure_map.md
Figure ID, question answered, source result IDs, claim IDs, evidence role, current caption/location, status/action.

## review_matrix.md
Finding ID, reviewer role, severity, affected claim/figure/section, required evidence/action, resolution status.

## decision_log.md
Date, decision, alternatives considered, evidence, rationale, affected objects, supersedes.

## v0.4 quantitative state

Recommended additional project objects:

- `experiment_register.md` — experimental units, factors, controls, replication, sequence.
- `qc_register.md` — dataset QC status, exclusions, anomalies, provenance.
- `analysis_register.md` — estimands, statistical models, assumptions, robustness checks.
- `parameter_register.md` — parameter definitions, units, bounds, calibrated values, uncertainty.
- `variable_unit_register.json` — units, dimensions, sign/stress conventions, normalization references.

These objects should point to stable `MTH`, `DAT`, `QC`, `ANA`, `PAR`, and `RES` Evidence Graph IDs where available.

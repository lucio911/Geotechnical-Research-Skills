# AGENTS.md

This repository contains modular research-reasoning Agent Skills for geotechnical engineering.

## Governing rule

The suite is not a solver copilot. Its purpose is to improve scientific reasoning, provenance, mechanics, evidence quality, and manuscript defensibility.

## Repository rules

When creating or editing a skill:

1. Keep the folder name and YAML `name` identical.
2. Use lowercase letters, digits, and hyphens only.
3. Make `description` discriminative: what the skill does and when it should trigger.
4. Keep `SKILL.md` focused on workflow, decision rules, failure modes, and outputs. Move detailed taxonomies/templates to `references/`.
5. Do not fabricate citations, standards clauses, datasets, numerical outputs, test conditions, uncertainties, or validation evidence.
6. Distinguish **reported fact**, **direct observation**, **derived quantity**, **author interpretation**, **agent interpretation**, **mechanistic claim**, and **engineering recommendation**.
7. Track material state, stress measure, drainage, reference state, coordinate/sign convention, units, and loading history whenever they materially affect interpretation.
8. Treat numerical analysis as a model-based evidence source, not ground truth. Treat contour plots as qualitative unless a defined metric is extracted.
9. Separate calibration, verification, and validation. Never rename calibration against the fitting dataset as validation.
10. Prefer a weaker claim with explicit boundaries over a stronger unsupported claim.
11. Do not reward novelty merely because a parameter, soil, geometry, or software combination has not appeared verbatim in prior papers.
12. A theoretical model must expose assumptions, closure relationships, state variables, parameter meaning, dimensions, limiting cases, calibration route, and validation route.

## Research-Core ownership

- `geotech-paper-reader`: auditable extraction from individual papers.
- `geotech-gap-novelty`: gap and contribution stress testing.
- `geotech-theory-derivation`: theory/model construction and audit.
- `geotech-result-to-claim`: evidence-strength and claim-boundary control.
- `geotech-pre-submission-reviewer`: independent adversarial review and decision synthesis.
- `geotech-paper-spine`: manuscript-level argument architecture.
- `geotech-evidence-ledger`: typed claim/evidence graph and provenance integrity.
- `geotech-literature-review`: evidence-oriented multi-source synthesis, contradiction mapping, and source roles.
- `geotech-paper-spine`: claim hierarchy, figure-role mapping, and manuscript dependency architecture.

## Quantitative-Core ownership

- `geotech-experiment-design`: hypothesis-driven experiment design, controls, replication, confounding, scale effects, and measurement plans.
- `geotech-data-qc`: immutable raw-data provenance, sensor/table QC, exclusions, synchronization, and preprocessing audit.
- `geotech-statistics`: experimental unit, repeated measures, uncertainty, effect size, regression, and engineering significance.
- `geotech-parameter-calibration`: parameter identifiability, objective functions, calibration/validation separation, residuals, model comparison, and predictive uncertainty.
- `geotech-unit-dimension-audit`: units, dimensions, normalization, sign/stress conventions, and reference-state consistency.

Quantitative-Core must not treat statistical significance as mechanical proof, training fit as validation, or repeated observations within one specimen as independent replication.

## Cross-skill handoff discipline

A skill should produce explicit handoff objects rather than vague prose when another skill needs the result. Preferred objects include:

- Paper Card
- Gap Map
- Novelty Statement
- Model Audit
- Claim Card
- Literature Evidence Matrix
- Evidence Graph node/edge update
- Figure Evidence Plan
- Manuscript Spine
- Review Finding
- Revision Action
- Experiment Contract
- Data QC Record
- Statistical Analysis Card
- Calibration Manifest
- Variable/Unit Register

## Evidence Graph rules

- Use stable IDs for critical research objects; do not identify claims only by current paragraph number.
- Keep evidence and interpretation as separate nodes.
- Preserve contradictory evidence and record resolution instead of deleting it.
- A conclusion must trace to a claim, and a claim must trace to result/source/method provenance.
- Graph connectivity is not proof of physical correctness; mechanics review remains mandatory.

## Pull-request checklist

Before merging a new or changed skill:

- run `python scripts/validate_repo.py`;
- test positive and negative trigger prompts;
- verify all referenced files exist;
- verify examples do not imply unavailable evidence;
- check that the skill has a clear stop condition;
- check that it does not silently expand from research reasoning into software automation;
- ensure the strongest output claims identify their applicability boundary.

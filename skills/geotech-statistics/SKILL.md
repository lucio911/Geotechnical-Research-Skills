---
name: geotech-statistics
description: Choose and audit statistical inference for geotechnical experiments and model results, including replication, repeated measures, uncertainty intervals, effect sizes, regression, small-sample limitations, multiple comparisons, and engineering significance. Use when deciding what statistical analysis is defensible or when claims rely on significance, correlations, fitted trends, or group differences.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotechnical Statistics

Statistics quantifies uncertainty; it does not manufacture replication or mechanism.

## Workflow

1. Define the experimental unit and independent replicate count.
2. Identify response type, grouping structure, repeated measurements, censoring, and dependence.
3. State the scientific contrast before choosing a test.
4. Inspect distributions and residuals rather than selecting tests solely from sample size.
5. Report descriptive statistics and uncertainty intervals before p-values.
6. Quantify effect size in physical units where possible.
7. Separate **statistical significance** from **engineering significance** using `references/engineering-significance.md`.
8. For repeated cycles/load stages on the same specimen, use a repeated-measures/hierarchical interpretation; see `references/repeated-measures.md`.
9. For regression, audit residual pattern, heteroscedasticity, leverage, extrapolation, and physical plausibility.
10. For multiple comparisons, state the family of hypotheses and adjustment strategy when needed.
11. If assumptions are weak and n is small, prefer transparent uncertainty and robustness analyses over ritual hypothesis testing.
12. Translate statistical outputs into bounded Claim Cards; do not equate correlation with causality.

## Inference ladder

Use `references/inference-ladder.md`:

`description -> uncertainty -> contrast -> association -> prediction -> mechanism`

Each step requires additional design/evidence.

## Required outputs

- experimental unit and n;
- primary estimand/contrast;
- descriptive summary;
- uncertainty interval;
- test/model and assumptions;
- effect size;
- robustness/sensitivity checks;
- engineering-significance interpretation;
- limitations;
- proposed `ANA` and `RES` nodes.

## Prohibited shortcuts

Do not:

- count cycles, mesh elements, time steps, or points on a curve as independent n;
- use R² alone as model adequacy;
- infer a mechanism from a significant correlation;
- write “no effect” merely because p > 0.05;
- write “important” merely because p < 0.05;
- run many tests and report only significant ones;
- hide data exclusions or transformations.

## Stop condition

Stop when the inferential claim matches the design, dependence structure, uncertainty, and physical effect size. If independent replication is absent, explicitly limit population-level inference.

# Worked Example — Cyclic Degradation Quantitative Workflow

Suppose a study proposes a degradation law using cumulative plastic displacement `rp`, particle-breakage index `Br`, and normalized stiffness `G/G0`.

## 1. Design

`geotech-experiment-design` first asks whether stress level, amplitude, density, specimen sequence, and previous cyclic damage are independently controlled. Repeated cycles from one specimen are not treated as independent specimens.

## 2. Data QC

`geotech-data-qc` records raw load/displacement files, cycle segmentation, first-cycle seating, amplitude drift, sensor range, exclusions, and formulas used for `G/G0` and `rp`.

## 3. Unit audit

`geotech-unit-dimension-audit` checks whether any exponent such as `exp(-lambda rp)` is dimensionless and whether `rp*100` represents a percentage, a unit conversion, or an arbitrary scaling.

## 4. Calibration

`geotech-parameter-calibration` compares at least:

- reduced model using `rp`;
- reduced model using `Br`;
- full model using `rp` and `Br`.

The full model earns the extra state variable only if it improves independent prediction or necessary physical behavior rather than training R² alone.

## 5. Statistics

`geotech-statistics` reports prediction errors and uncertainty by independent specimen/case. It does not count cycles as independent n.

## 6. Evidence Graph

Recommended chain:

`MTH -> DAT -> QC -> ANA -> PAR -> independent validation ANA -> RES -> CLM`

A defensible claim is weaker than “particle breakage governs degradation” unless discriminating evidence excludes plausible alternative explanations.
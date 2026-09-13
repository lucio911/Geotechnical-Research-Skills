---
name: geotech-parameter-calibration
description: Design and audit calibration of geotechnical constitutive, degradation, empirical, analytical, or surrogate models with emphasis on parameter identifiability, objective functions, bounds, residual structure, overfitting, nested-model comparison, calibration/validation separation, and predictive uncertainty. Use whenever parameters are fitted to experimental or numerical data.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotechnical Parameter Calibration

Calibration estimates parameters. Validation tests predictive adequacy on information not used to estimate those parameters.

## Workflow

1. Classify the model: mechanics-derived, constitutive/state-variable, mechanism-informed semi-empirical, empirical, or surrogate.
2. Define each parameter's physical meaning, units, admissible range, and expected sensitivity.
3. Define calibration observations and independent validation observations **before** fitting where possible.
4. Build a calibration manifest; see `references/calibration-validation.md`.
5. Check structural and practical identifiability using `references/identifiability.md`.
6. Define the objective function in physical terms. Explain weighting across response types, amplitudes, cycles, stresses, or specimens.
7. Fit with bounded, reproducible settings and record initial values, optimizer, stopping criteria, and seeds where relevant.
8. Inspect residual structure using `references/residual-diagnostics.md`.
9. Compare simpler and more complex candidate models using `references/model-comparison.md`.
10. Evaluate predictive performance on independent validation cases.
11. Quantify parameter/prediction uncertainty when consequential.
12. Create `ANA`, `PAR`, validation `RES`, and bounded `CLM` nodes in the Evidence Graph.

## Key audits

### Information-overlap audit
If `Br = h(rp)` and `G/G0 = F(rp, Br)`, ask whether both predictors contribute independent information. Compare reduced models and independent prediction, not just training R².

### Parameter identifiability
A low residual does not mean parameters are uniquely identified. Look for:

- strong parameter correlation;
- flat objective valleys;
- parameter estimates at bounds;
- multiple initializations giving different parameters but similar fit;
- parameters changing drastically across subsets;
- physically implausible estimates.

### Calibration/validation separation
Do not call agreement with the fitting data “validation”. If no independent data exist, use terms such as calibration fit, internal consistency, resampling assessment, or cross-validation as appropriate and state limitations.

### Complexity gate
A more complex model must earn its parameters through better independent prediction, improved residual structure, or necessary physical behavior. A marginal R² increase is insufficient.

## Deterministic helper

Validate a calibration manifest and detect case leakage:

```bash
python scripts/audit_calibration_manifest.py assets/calibration-manifest.example.json
```

## Required outputs

- Model/Parameter Contract;
- calibration/validation split;
- objective function;
- parameter table with units/bounds;
- identifiability findings;
- residual diagnostics;
- candidate-model comparison;
- validation metrics;
- uncertainty statement;
- model classification and applicability boundary.

## Stop condition

Stop when the chosen parameterization is identifiable enough for its intended use and predictive claims are tested independently. If not, simplify the model or weaken the claim.

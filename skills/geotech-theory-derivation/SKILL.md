---
name: geotech-theory-derivation
description: Develop, derive, classify, and audit theoretical or semi-empirical geotechnical models, including stress transfer, deformation, cyclic accumulation, degradation, particle breakage, soil-structure interaction, tunnel-ground response, constitutive evolution, and reliability formulations. Use when checking equations, introducing state variables, fitting degradation laws, preparing a theoretical-model section, or testing whether a claimed mechanism-based model is physically and statistically defensible.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Theory Derivation

A mathematically smooth fit is not necessarily a physical model.

The objective is to build or audit a chain from **idealization -> governing mechanics -> closure -> state evolution -> prediction -> independent test**.

## Phase 1 — Define the model contract

State before deriving:

- engineering phenomenon to predict;
- output variables and reference states;
- intended scale and dimensionality;
- material class and state range;
- loading/stress path and drainage;
- whether the model is explanatory, predictive, or only correlational;
- what observations would falsify it.

## Phase 2 — Declare coordinates, measures, and conventions

Define:

- coordinate system;
- stress and strain sign conventions;
- total/effective stress;
- engineering/tensor strain where relevant;
- dimensional versus normalized variables;
- initial/reference state;
- cycle/time/load index;
- all internal/state variables.

Never introduce a normalized variable without defining its denominator and physical reference.

## Phase 3 — Classify every equation

Tag each equation as:

- equilibrium/conservation;
- kinematic/compatibility;
- constitutive;
- state-evolution;
- boundary/initial condition;
- empirical closure;
- definition/transformation;
- numerical approximation.

This prevents empirical fits from being presented as governing mechanics.

## Phase 4 — Audit state variables

For each state/internal variable ask:

1. What physical process does it represent?
2. Is it observable, inferable, or purely latent?
3. What is its admissible range?
4. Is it path dependent?
5. What is the evolution law?
6. Does another variable encode the same degradation information?
7. Is the variable needed for prediction, or only for curve fitting?

If two variables are both monotonic functions of the same accumulated deformation and enter the same degradation term, test for **information overlap/double counting**.

Use `references/state-variable-audit.md`.

## Phase 5 — Derive with closure visible

Proceed:

`equilibrium/kinematics -> constitutive relation -> interface/boundary condition -> state evolution -> solution or calculation procedure`

Do not skip the closure step. If a governing equation cannot be solved without an empirical law, label that law explicitly.

## Phase 6 — Dimensional and asymptotic audit

For each equation:

- verify dimensions;
- ensure logarithm/exponential/power arguments are dimensionless or consistently normalized;
- check signs and monotonicity;
- check admissible parameter ranges;
- test initial state;
- test zero-loading/zero-damage case;
- test large-cycle/time/deformation limit;
- test extreme but physically meaningful stress/state limits.

A degradation law that predicts negative stiffness or unbounded damage without an explicit physical rationale fails this gate.

## Phase 7 — Identifiability and parsimony

Before fitting many parameters ask:

- Can different parameter combinations generate nearly identical curves?
- Is each parameter informed by an independent feature of the data?
- Can a lower-parameter model fit within experimental uncertainty?
- Are parameters stable across stress levels/material states?
- Are parameters being allowed to absorb missing physics?

Use `references/calibration-validation.md`.

## Phase 8 — Model-classification honesty

Classify the final model as one of:

- mechanics-derived;
- constitutive/state-variable;
- mechanism-informed semi-empirical;
- empirical phenomenological;
- surrogate/statistical.

Do not call a model "mechanism-based" merely because a physically named variable appears in an empirical fitting expression.

Use `references/model-classification.md`.

## Phase 9 — Calibration and validation separation

Define:

- calibration dataset;
- fitted parameters and bounds;
- objective function/error metric;
- uncertainty or parameter sensitivity;
- verification tests;
- independent validation conditions.

Validation must involve information not used to fit the model whenever the manuscript claims predictive capability.

## Phase 10 — Manuscript-ready output

Return:

1. model purpose and scope;
2. assumptions table;
3. variable/state-variable table;
4. equation classification map;
5. derivation with closure points explicit;
6. dimensional/limiting-case audit;
7. parameter interpretation and identifiability risks;
8. calibration plan;
9. independent validation plan;
10. applicability boundary;
11. model classification and wording strength.

## Critical failure modes

Flag immediately:

- circular definitions;
- variable double counting;
- dimensioned exponential/power arguments without normalization;
- parameter meaning changing between equations;
- fitted data reused as claimed independent validation;
- hidden dependence on stress level through free coefficients while claiming a universal law;
- arbitrary exponent/constant proliferation without identifiability analysis;
- a theoretical derivation whose decisive step is actually an undocumented empirical assumption.

Use `references/derivation-audit.md` for the final gate.

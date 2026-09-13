# Worked Example — Cyclic Degradation Theory Audit

This example shows how `geotech-theory-derivation` should examine a model that uses cumulative plastic displacement `r_p` and particle breakage rate `B_r` to update stiffness.

## Candidate structure

Assume stiffness degradation is proposed as:

`G/G0 = F(r_p, B_r; parameters)`

and `B_r` is itself fitted as a monotonic function of `r_p`.

## Immediate state-variable question

If `B_r = h(r_p)`, then both inputs may carry largely the same information.

The model should not automatically be described as a two-mechanism law. Test:

1. `G/G0 = F1(r_p)`
2. `G/G0 = F2(B_r)`
3. `G/G0 = F3(r_p, B_r)`

Then ask whether model 3 improves **independent prediction**, not merely the calibration fit.

## Physical audit

For `r_p`:

- physical meaning: cumulative irreversible deformation/sliding proxy;
- status: measured or inferred?
- expected monotonicity: normally non-decreasing under the adopted definition;
- dependence on amplitude/confining pressure/loading path: must be stated.

For `B_r`:

- physical meaning: particle breakage/damage measure;
- definition and particle-size reference must be explicit;
- if estimated from `r_p` rather than independently measured, mechanism evidence is weaker.

## Limiting cases

A defensible model should be checked for:

- `r_p = 0`, `B_r = 0`: does `G/G0 = 1` or the defined initial value?
- small damage: is the first-order trend physically reasonable?
- large `r_p`: does stiffness approach a finite residual level rather than become negative?
- `B_r -> B_r,max`: is saturation represented?
- changing confining pressure: does stress dependence enter explicitly, through state evolution, or only through re-fitted coefficients?

## Classification

If the final degradation equation is chosen primarily for fit quality while `r_p` and `B_r` are physically motivated covariates, classify it as:

**mechanism-informed semi-empirical**, not automatically **mechanics-derived** or **mechanism-based**.

## Validation requirement

Calibrating parameters at one stress level and showing the fitted curves is not independent validation. Stronger validation would test another amplitude/stress/material condition with parameters fixed or with a pre-declared stress-dependence rule.

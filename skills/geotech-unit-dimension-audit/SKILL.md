---
name: geotech-unit-dimension-audit
description: Audit units, dimensions, normalization, sign conventions, reference states, stress measures, and dimensionless groups in geotechnical equations, datasets, plots, and parameter tables. Use when deriving or reviewing equations, combining data sources, normalizing variables, fitting models, or checking manuscript consistency.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotechnical Unit and Dimension Audit

Dimensional consistency is a necessary condition for a defensible model, not proof that the model is physically correct.

## Workflow

1. Build a variable register before auditing equations. Use `references/dimension-rules.md`.
2. For every variable record:
   - symbol;
   - meaning;
   - SI dimension;
   - working unit;
   - sign convention;
   - total/effective stress status where relevant;
   - reference state if normalized.
3. Expand each governing equation into base dimensions and check term-by-term consistency.
4. Check arguments of `exp`, `log`, trigonometric, and power functions. They must be dimensionless unless a properly normalized form is used.
5. Audit normalized variables using `references/normalization.md`.
6. Check common geotechnical traps in `references/geotech-unit-traps.md`.
7. Compare equations, data columns, figure labels, captions, tables, and manuscript text for unit drift.
8. Flag equations that are dimensionally valid only because fitted constants silently carry units.
9. Record unresolved conventions rather than guessing.

## Common high-risk patterns

### Exponential degradation laws
Expressions such as `exp(-c * rp)` require `c*rp` to be dimensionless. If `rp` is mm, `c` carries 1/mm unless `rp` is normalized.

### Percentage conversion hidden in equations
Using `(rp * 100)^0.43` changes numerical meaning depending on whether `rp` is a fraction, strain, mm, or percentage. Make the reference scale explicit.

### Stress normalization
`q/pa`, `q/su`, `sigma3/pa`, and similar groups depend on a declared reference stress. Do not omit the reference from parameter interpretation.

### Degrees versus radians
Angles may be presented in degrees but trigonometric code commonly expects radians. Record the computational convention.

## Deterministic helper

Audit a variable register:

```bash
python scripts/check_variable_register.py assets/variable-register.example.json
```

The helper checks metadata completeness and common normalization hazards; it is not a symbolic algebra engine.

## Required outputs

- Variable/Unit Register;
- equation-by-equation dimension audit;
- normalization audit;
- sign/stress convention audit;
- cross-document unit inconsistencies;
- corrected dimensionless form where justified;
- unresolved ambiguities.

## Stop condition

Stop only when every consequential equation and reported parameter has an explicit unit/dimension/reference-state interpretation. If a fitted constant absorbs dimensions, state its units rather than calling it dimensionless.

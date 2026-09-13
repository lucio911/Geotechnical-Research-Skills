# Worked Example — Evidence Graph Workflow

This example shows how a progressive-surcharge tunnel lining study should move from numerical outputs to bounded manuscript claims.

## 1. Raw study objects

- `MTH-001`: controlled progressive surcharge analysis.
- `DAT-001`: crown U2 histories by initial crack depth.
- `DAT-002`: ovalization histories.
- `DAT-003`: crack propagation histories.

## 2. Results

- `RES-001`: crown U2 increases nonlinearly with surcharge.
- `RES-002`: deeper initial cracks show stronger ovalization amplification.
- `RES-003`: crack propagation accelerates after a load-dependent transition.

These are results, not mechanisms.

## 3. Mechanism interpretation

`MEC-001`: crack-induced local stiffness loss is consistent with redistribution and increasing global ovalization.

The wording remains "consistent with" until evidence discriminates this mechanism from alternatives such as constitutive softening, boundary sensitivity, or numerical localization.

## 4. Claim

`CLM-001`: Within the tested geometry, constitutive assumptions, crack orientation, and surcharge range, increasing initial crack depth is associated with stronger deformation amplification and earlier crack-growth transition.

Supporting paths:

```text
MTH-001 -> DAT-001 -> RES-001 -> CLM-001
MTH-001 -> DAT-002 -> RES-002 -> CLM-001
MTH-001 -> DAT-003 -> RES-003 -> CLM-001
```

Mechanism path:

```text
RES-001 -> MEC-001
RES-002 -> MEC-001
RES-003 -> MEC-001
```

If those edges are only `consistent_with`, the manuscript should not write "stiffness loss governs the failure mechanism" without stronger evidence.

## 5. Figure architecture

- `FIG-001`: U2 versus surcharge — quantitative deformation evidence.
- `FIG-002`: ovalization versus surcharge — global geometry response.
- `FIG-003`: crack propagation versus surcharge — damage-transition evidence.
- deformation contours — spatial interpretation, not the primary quantitative proof.

## 6. Conclusion provenance

A conclusion such as:

> Increasing initial crack depth accelerates deformation amplification within the investigated model conditions.

may be linked as:

`RES-001 + RES-002 + RES-003 -> CLM-001 -> CON-001`.

A stronger engineering recommendation would require a separate `EC/CLM` object and explicit boundary/validation evidence.

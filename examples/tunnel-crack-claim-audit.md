# Worked Example — Tunnel Crack Result-to-Claim Audit

This example demonstrates reasoning structure only; values are placeholders.

## Research situation

A tunnel-lining study compares several initial crack depths under progressively increasing surcharge. Available outputs include:

- crown vertical displacement `U2` versus surcharge;
- lining ovalization versus surcharge;
- displacement contours at the critical surcharge;
- crack propagation versus surcharge.

## Weak manuscript move

> Increasing initial crack depth causes severe stiffness degradation and ultimately controls tunnel failure.

This sentence jumps from model outputs to a causal failure mechanism.

## Claim Card

### Claim T1

**Evidence class**: numerical prediction.

**Direct observation**: Crown vertical displacement magnitude increases with surcharge, with larger values in deeper-crack cases.

**Quantification**: Extract the displacement at common surcharge stages and report the difference or normalized increase relative to the intact/shallow-crack case.

**Corroboration**: Ovalization and crack-propagation metrics increase over the same loading interval.

**Mechanism candidate**: Increasing crack depth reduces local sectional stiffness, redistributes internal forces, and promotes a transition from localized deformation to stronger global ovalization.

**Competing explanations**:

- contour-scale inconsistency;
- mesh/localization dependence;
- crack constitutive parameters driving both crack growth and deformation;
- boundary/domain effects.

**Evidence grade**: E3 if independent response curves are quantified and verification is adequate; lower if evidence is mainly visual.

**Claim level**: C4 — mechanistic consistency.

**Strongest defensible wording**:

> Within the investigated surcharge and crack-depth ranges, deeper initial cracks are associated with greater crown settlement and ovalization, while the concurrent increase in crack propagation is consistent with progressive loss of local lining stiffness and redistribution of structural deformation.

**Overclaiming**:

> Initial crack depth governs tunnel failure under surcharge.

**Evidence needed to raise to C5/C6**:

- independent validation against measured lining response or crack evolution;
- sensitivity demonstrating the transition is not controlled by mesh/boundary/crack-model choices;
- a defined failure criterion and evidence distinguishing the proposed stiffness-loss mechanism from plausible alternatives.

## Figure architecture implication

A defensible multi-panel figure could use:

- (a) `U2`–surcharge curves;
- (b) ovalization–surcharge curves;
- (c) crack propagation–surcharge curves;
- (d–g) selected comparable-range displacement contours at a critical stage.

The curves provide quantitative evidence; the contours provide spatial interpretation. Do not reverse those roles.

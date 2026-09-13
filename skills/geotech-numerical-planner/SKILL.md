---
name: geotech-numerical-planner
description: Design and audit solver-agnostic geotechnical numerical studies, focusing on scientific question, idealization, constitutive assumptions, initial and boundary conditions, parameter provenance, verification, validation, sensitivity, outputs, and claim limits. Use when planning or reviewing FEM, FDM, DEM, coupled, seepage, cyclic, seismic, soil-structure, tunnel, pile, excavation, or slope simulations.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Numerical Planner

Numerical modelling is an experiment on a mathematical model. Begin with the scientific question, not software operations.

## Study contract

Define:

- claim/hypothesis the model is intended to test;
- why numerical evidence is needed;
- dimensional idealization and geometry;
- material state and constitutive rationale;
- initial stress/pore-pressure/drainage state;
- interfaces and interaction assumptions;
- boundary/domain extent;
- construction/loading path;
- discretization strategy;
- response quantities and extraction definitions;
- verification tests;
- validation anchor;
- sensitivity plan;
- conditions under which the model should not be trusted.

## Minimum verification set

Select only tests relevant to the claim, such as:

- mesh/discretization sensitivity;
- domain/boundary sensitivity;
- time/load increment sensitivity;
- constitutive parameter sensitivity;
- interface sensitivity;
- damping/frequency sensitivity;
- initial-stress sensitivity.

Do not request every sensitivity study mechanically.

## Evidence rule

A simulation output is a **numerical prediction**. It becomes stronger evidence only through verification, independent validation, and consistency with mechanics/observations.

Hand scientific outputs to `geotech-result-to-claim` rather than writing causal conclusions directly from contours.

---
name: geotech-experiment-design
description: Design and audit geotechnical experiments so hypotheses, factors, controls, repetitions, boundary conditions, scale effects, measurements, and decision criteria are explicit before testing. Use for laboratory, model, centrifuge, field, cyclic, static, or dynamic test planning, or when an existing experiment needs a confounding and reproducibility audit.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotechnical Experiment Design

Design experiments as tests of scientific claims, not as collections of cases.

## Core rule

Every test series must connect:

`research question -> hypothesis -> manipulated factor -> controlled conditions -> measured response -> analysis plan -> falsification criterion`

Do not begin from “how many groups should I run?” Begin from the claim that the experiment must discriminate.

## Workflow

1. Write the **Experiment Contract** using `references/study-design-contract.md`.
2. State the primary hypothesis and at least one plausible competing explanation.
3. Separate:
   - manipulated factors;
   - controlled factors;
   - nuisance variables;
   - blocking variables;
   - repeated measurements;
   - true independent replicates.
4. Define material state before loading: density/void ratio, water content/saturation, OCR/stress history, fabric, gradation, cementation/breakage state, specimen preparation, temperature where relevant.
5. Define stress and drainage conventions explicitly.
6. Define loading path, amplitude, rate/frequency, waveform, cycle count, hold periods, sequence, and termination criteria.
7. Define measurement chain: sensor, range, resolution, calibration, zeroing, sampling rate, synchronization, and derived quantities.
8. Check confounding using `references/geotechnical-confounders.md`.
9. For physical models, check similarity and scale effects using `references/similarity-scale-effects.md`.
10. Predefine the minimum analysis needed to accept, weaken, or reject the hypothesis.
11. Specify replication and uncertainty strategy. Do not use repeated cycles from one specimen as independent replicates.
12. Produce a test matrix and a **claim-discrimination matrix**.

## Geotechnical-specific design gates

### Stress-state gate
Record whether stresses are total or effective and how pore pressure is measured or assumed. State K0/isotropic/anisotropic consolidation and principal-stress orientation where relevant.

### Drainage gate
State drained/undrained/partially drained conditions and justify them against loading rate and drainage length. “Fast loading” is not by itself proof of undrained response.

### State-variable gate
Do not vary confining pressure while silently changing relative density, saturation, fabric, overconsolidation, or specimen preparation quality.

### Sequence gate
If the same specimen receives multiple amplitudes or stages, sequence effects are part of the design. A stepped-amplitude program is not equivalent to independent constant-amplitude specimens.

### Scale/boundary gate
For 1g model tests, piles, tunnels, trapdoors, retaining systems, and small chambers, identify likely boundary and stress-level distortions before interpreting mechanisms.

## Required outputs

Produce:

- Experiment Contract;
- factor/control/nuisance table;
- test matrix;
- replication plan;
- measurement plan;
- confounding register;
- predefined analysis plan;
- claim-discrimination matrix;
- applicability boundaries;
- proposed `MTH` and expected `DAT` nodes for the Evidence Graph.

## Failure modes

Reject or redesign a plan when:

- one factor is changed together with an uncontrolled state variable;
- no independent replication exists for a claim requiring population inference;
- the measured quantity is only an indirect proxy but is treated as the target mechanism;
- instrumentation cannot resolve the expected effect size;
- the test sequence itself changes material state but is omitted from interpretation;
- a “control” group differs in more than one scientifically consequential way;
- model scale makes the proposed field-scale conclusion indefensible.

## Stop condition

Stop when each primary claim has a testable contrast, measurable response, plausible alternative explanation, and predefined decision rule. Do not invent test data or expected significance.

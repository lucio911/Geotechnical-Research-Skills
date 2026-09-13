---
name: geotech-paper-reader
description: Read geotechnical engineering papers and produce auditable Geotechnical Paper Cards that separate reported facts, author interpretations, reader inferences, evidence strength, boundary conditions, and transferability. Use when extracting a paper for literature review, method reproduction, cross-study comparison, novelty analysis, evidence mapping, or critical reading.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Paper Reader

Read for **scientific recoverability**, not for a generic summary.

## Core rule

Never collapse these four categories into one:

1. **Reported fact** — explicitly stated numerical/methodological information.
2. **Author interpretation** — mechanism or explanation claimed by the authors.
3. **Reader inference** — conclusion inferred from figures, equations, or context but not explicitly established.
4. **Transferability judgment** — whether the result can support the current project under different material/state/loading conditions.

Label them separately.

## Workflow

### 1. Identify the study claim

Extract:

- research question;
- stated knowledge gap;
- stated novelty/contribution;
- study type: field / laboratory / centrifuge / analytical / numerical / hybrid / review;
- central dependent and independent variables.

Do not accept the authors' novelty statement as proven. Record it as **claimed novelty**.

### 2. Recover the geotechnical state

Extract the smallest state description needed to reproduce or interpret the result:

- soil/rock/mineral/material type and origin;
- grading, fines, density/void ratio/relative density or consistency;
- saturation/water content and pore-pressure condition;
- initial and effective stress state;
- OCR/stress history where relevant;
- drainage condition;
- anisotropy, cementation, structure, weathering, breakage susceptibility;
- temperature/chemical environment where material;
- scale and specimen/field geometry.

Mark each field as `reported`, `derived`, `unclear`, or `not reported`.

### 3. Recover the loading/path definition

Capture more than the peak load:

- monotonic / cyclic / seismic / creep / excavation / staged construction;
- stress- or displacement-controlled;
- amplitude, mean level, frequency, number of cycles, waveform;
- confining pressure / K0 / surcharge / groundwater change;
- sequence and path dependence;
- termination/failure criterion.

### 4. Recover measurement/model definitions

For experiments: instrument, location, resolution if reported, calibration/repeatability, sampling, data reduction.

For numerical work: dimensional idealization, constitutive model, parameter provenance, interface/contact concept, initial state, boundaries, mesh/discretization, verification, validation target.

For analytical work: assumptions, governing equations, state variables, boundary conditions, parameter calibration, limiting cases.

### 5. Extract evidence-bearing results

For each important result, create an evidence row:

`result -> value/trend -> variable definition -> condition -> uncertainty/dispersion -> locator -> evidence type`

Do not use adjectives such as "significant" unless statistical or engineering significance is demonstrated.

### 6. Separate mechanism from observation

For every mechanistic statement, ask:

- Was the mechanism directly measured?
- Was it inferred from correlated responses?
- Was it only supported by literature?
- Were competing explanations tested?

Assign mechanism support: `direct`, `triangulated`, `consistent`, `speculative`.

### 7. Audit validation and limitations

Record whether evidence is:

- calibration only;
- internal verification;
- independent validation;
- cross-condition validation;
- field validation.

Explicitly recover author-stated limitations and add reader-identified limitations separately.

### 8. Judge transferability

Do not ask merely "Is this relevant?" Compare the current project and the paper on:

`material -> state -> stress path -> drainage -> geometry/scale -> loading -> measured response -> failure criterion`

Classify transferability as `direct`, `conditional`, `conceptual`, or `weak` and state why.

## Outputs

Use `references/paper-card-template.md` for a full Paper Card.

For multiple papers, also use:

- `references/extraction-confidence.md`
- `references/comparison-matrix.md`

The final synthesis should identify agreements, contradictions, incompatible definitions, untested assumptions, and which claims each paper can actually support.

## Stop conditions

Stop and flag uncertainty when a required condition is not recoverable from the available text/figures. Never fill missing stress state, drainage, geometry, or parameter provenance using typical practice.

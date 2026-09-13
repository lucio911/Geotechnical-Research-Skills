# Geotechnical-Research-Skills

[![validate-skills](https://github.com/lucio911/Geotechnical-Research-Skills/actions/workflows/validate.yml/badge.svg)](https://github.com/lucio911/Geotechnical-Research-Skills/actions/workflows/validate.yml)

Research-reasoning Agent Skills for evidence-grounded, mechanics-aware, quantitatively defensible geotechnical engineering.

> Status: **v0.5.0 Citation Integrity Core (feature-complete PR)**. This release adds reference identity verification, citation-to-claim fidelity auditing, manuscript/bibliography consistency checks, deterministic CSL-oriented reference formatting, and whole-bibliography reference forensics on top of the v0.4 quantitative core. The suite remains software-agnostic.

## Why this project exists

Generic academic agents can produce fluent prose while missing scientific failure modes that matter in geotechnical research:

- parameter variation presented as scientific novelty;
- uncontrolled density, saturation, stress history, drainage, sequence, or scale effects;
- repeated cycles or time points counted as independent replication;
- raw data overwritten or exclusions undocumented;
- sensor drift, seating, saturation, synchronization, or derived-variable definitions ignored;
- p-values treated as engineering importance;
- R² treated as model adequacy;
- fitted parameters that are not identifiable;
- calibration against the fitting data renamed as validation;
- normalized variables whose reference states silently change;
- dimensioned quantities placed inside exponential/logarithmic functions without normalization;
- effective-stress, total-stress, sign, degree/radian, kPa/MPa, mm/m, or percent/fraction ambiguity;
- contour plots treated as quantitative proof;
- association promoted to mechanism or causality without discriminating evidence;
- conclusions broader than tested material, stress path, geometry, scale, or loading range.

The canonical chain is now:

`Question -> Gap -> Hypothesis -> Experiment/Method -> Data -> QC -> Analysis/Calibration -> Result -> Mechanics -> Claim -> Figure -> Paper -> Adversarial Review`

## Scope boundary

This repository is intentionally **software-agnostic**. It may reason about numerical study design and verification, but it does not attempt to become an Abaqus, PLAXIS, FLAC3D, OpenSees, MATLAB, Python, R, or spreadsheet copilot.

Research-Core should remain scientifically valid regardless of whether evidence comes from laboratory tests, field monitoring, numerical analysis, analytical derivation, probabilistic analysis, or literature.

## v0.5 skill map

| Skill | Pack | Role |
|---|---|---|
| `geotech-router` | core | Route the smallest defensible workflow |
| `geotech-project-ledger` | core | Maintain project truth and provenance |
| `geotech-evidence-ledger` | evidence-core | Build/audit the typed Evidence Graph |
| `geotech-literature-review` | evidence-core | Evidence-oriented literature synthesis and contradiction mapping |
| `geotech-paper-spine` | evidence-core | Main/supporting/boundary claim architecture and figure roles |
| `geotech-reference-verifier` | citation-core | Verify existence, identity, metadata drift, identifier mismatch, duplication and suspected fabrication |
| `geotech-citation-fidelity` | citation-core | Audit whether each citation instance supports the exact manuscript claim (F0–F5) |
| `geotech-bibliography-audit` | citation-core | Detect dangling/orphan citations, duplicate works/DOIs and citekey inconsistencies |
| `geotech-reference-format` | citation-core | Render verified canonical metadata with deterministic journal/CSL style |
| `geotech-paper-reader` | research-core | Auditable Geotechnical Paper Cards |
| `geotech-gap-novelty` | research-core | Stress-test real novelty rather than parameter novelty |
| `geotech-theory-derivation` | research-core | Theory/model derivation and state-variable audit |
| `geotech-result-to-claim` | research-core | Control evidence-to-claim strength |
| `geotech-pre-submission-reviewer` | research-core | Adversarial multi-role review |
| `geotech-experiment-design` | quantitative-core | Hypothesis-driven test design, controls, replication, confounding, scale effects |
| `geotech-data-qc` | quantitative-core | Raw-data provenance, sensor/table QC, exclusions and preprocessing audit |
| `geotech-statistics` | quantitative-core | Experimental unit, repeated measures, uncertainty, effect size and inference |
| `geotech-parameter-calibration` | quantitative-core | Identifiability, objective functions, model comparison and independent validation |
| `geotech-unit-dimension-audit` | quantitative-core | Units, dimensions, normalization, sign/stress conventions and reference states |
| `geotech-numerical-planner` | methods | Solver-agnostic numerical study/verification planning |
| `geotech-scientific-figure` | communication | Evidence-driven scientific figure architecture |

## What changed in v0.5

### Citation integrity is now a separate evidence layer

v0.5 separates five questions that should never be collapsed:

`existence != identity != metadata != citation fidelity != formatting`

- `geotech-reference-verifier` verifies that a reference exists and that persistent identifiers resolve to the same work claimed in the manuscript.
- `geotech-citation-fidelity` introduces `CIT-###` citation instances and F0–F5 support grades.
- `geotech-bibliography-audit` checks manuscript/body-to-bibliography structural consistency.
- `geotech-reference-format` keeps metadata immutable and delegates rendering to deterministic CSL/bibliography processors.

High-risk records such as `IDENTIFIER_MISMATCH`, `SUSPECTED_COMPOSITE`, and `SUSPECTED_FABRICATION` are never silently deleted.

`geotech-reference-verifier` includes an executable online resolver:

```bash
python skills/geotech-reference-verifier/scripts/resolve_reference.py \
  --record reference-record.json \
  --email researcher@example.org \
  --use-openalex
```

It uses Crossref/DataCite public metadata and optional OpenAlex cross-checking, but keeps retrieval separate from deterministic identity scoring. API failure or no hit remains `UNRESOLVED`, never automatic fabrication evidence.

For whole-bibliography forensics:

```bash
python skills/geotech-reference-verifier/scripts/audit_references.py references.bib \
  --email researcher@example.org \
  --use-openalex \
  --output-json reference-integrity-report.json \
  --output-md reference-integrity-report.md
```

The batch audit uses a stateful BibTeX parser, cached per-reference resolution, duplicate DOI detection, conservative near-duplicate title screening, retraction flags, and aggregated critical/manual-review actions. `UNRESOLVED` and `AMBIGUOUS` remain review states rather than automatic fabrication findings. Use `--fail-on-critical` for a pre-submission/CI gate.

See `docs/citation-integrity-core.md` and `examples/citation-integrity-workflow.md`.

## v0.4 Quantitative Core retained

### 1. Experiment design became claim-discrimination design

`geotech-experiment-design` does not start from the number of test cases. It starts from:

`claim -> primary hypothesis -> credible alternative -> controlled contrast -> observable -> decision rule`

It explicitly audits material state, effective/total stress, drainage, loading sequence, model scale, apparatus boundaries, true replication, pseudo-replication, and measurement resolution.

### 2. Data quality became part of provenance

`geotech-data-qc` uses an immutable chain:

`raw -> processed -> analysis-ready`

Every exclusion and transformation must be recorded. Cyclic tests receive dedicated checks for seating, amplitude/mean drift, cycle segmentation, incomplete loops, phase/synchronization errors, and first-cycle reference definitions.

A lightweight structural checker is included:

```bash
python skills/geotech-data-qc/scripts/audit_csv.py data.csv --time-column time
```

Passing it does not establish sensor or scientific validity.

### 3. Statistics now begins with the experimental unit

`geotech-statistics` forces the distinction between specimens and repeated observations. One specimen with 100 cycles is not `n = 100` independent specimens.

The inference ladder is:

`description -> uncertainty -> contrast -> association -> prediction -> mechanism`

Statistical significance and engineering significance are reported separately.

### 4. Calibration now has an identifiability and leakage gate

`geotech-parameter-calibration` requires:

- explicit parameter meaning, units, bounds, and sensitivity;
- objective-function definition;
- repeated-start / sensitivity / parameter-correlation checks where relevant;
- residual diagnostics;
- reduced-versus-full model comparison;
- independent validation where predictive claims are made;
- no calibration/validation case overlap.

For models such as `G/G0 = F(rp, Br)` where `Br = h(rp)`, the skill explicitly tests information overlap and whether the extra state variable improves independent prediction.

Audit a calibration manifest:

```bash
python skills/geotech-parameter-calibration/scripts/audit_calibration_manifest.py \
  skills/geotech-parameter-calibration/assets/calibration-manifest.example.json
```

### 5. Unit/dimension control became a first-class gate

`geotech-unit-dimension-audit` checks equations, tables, plots, and parameter definitions. It specifically guards against:

- `exp(-c x)` with dimensioned `c x`;
- Pa/kPa/MPa and N/kN drift;
- mm/m and decimal/percent strain drift;
- density versus unit weight;
- effective versus total stress;
- degree/radian ambiguity;
- normalized variables whose reference state is undefined;
- fitted constants silently carrying units while being called dimensionless.

Audit a variable register:

```bash
python skills/geotech-unit-dimension-audit/scripts/check_variable_register.py \
  skills/geotech-unit-dimension-audit/assets/variable-register.example.json
```

## Evidence Graph extensions through v0.5

v0.3 used a core chain such as `MTH -> DAT -> RES -> CLM`. v0.4 adds explicit quantitative objects:

- `QC-###` — data-quality assessment;
- `ANA-###` — statistical/calibration/quantitative analysis;
- `PAR-###` — parameter set.

Recommended experimental chain:

```text
MTH -> DAT -> QC
        |      |
        v      v
       ANA <---+
        |
        +----> RES
        |
        +----> PAR
                 |
                 +---- parameterizes-+

RES(validation) -> CLM
```

v0.5 additionally introduces `CIT-###` citation-instance nodes and `cited_as` edges. Citation-to-claim edges may carry `fidelity_grade: F0`–`F5`, separate from evidence strength `E0`–`E5`.

Example:

```bash
python skills/geotech-evidence-ledger/scripts/validate_evidence_graph.py \
  skills/geotech-evidence-ledger/assets/quantitative-evidence-graph.example.json
```

## Recommended project state

```text
.geotech/
├── project_truth.md
├── research_questions.md
├── literature_matrix.md
├── reference_verification.json
├── citation_map.json
├── experiment_register.md
├── method_register.md
├── parameter_register.md
├── variable_unit_register.json
├── qc_register.md
├── analysis_register.md
├── result_ledger.md
├── evidence_graph.json
├── manuscript_spine.md
├── figure_map.md
├── review_matrix.md
└── decision_log.md
```

## Recommended routes

### Experimental study

`geotech-experiment-design -> geotech-data-qc -> geotech-unit-dimension-audit -> geotech-statistics / geotech-parameter-calibration -> geotech-result-to-claim -> geotech-evidence-ledger -> geotech-paper-spine`

### Degradation/constitutive model development

`geotech-gap-novelty -> geotech-unit-dimension-audit -> geotech-theory-derivation -> geotech-parameter-calibration -> geotech-statistics -> geotech-result-to-claim -> geotech-evidence-ledger`

### Existing dataset audit

`geotech-data-qc -> geotech-unit-dimension-audit -> geotech-statistics -> geotech-result-to-claim`

### Literature and novelty

`geotech-literature-review -> geotech-paper-reader -> geotech-gap-novelty -> geotech-evidence-ledger`

### Reference and citation audit

`geotech-bibliography-audit -> geotech-reference-verifier -> geotech-citation-fidelity -> geotech-reference-format -> geotech-evidence-ledger`

## Research rules encoded in the repository

1. Never fabricate citations, standards, data, equations, outputs, or validation evidence.
2. Preserve measured, derived, calibrated, assumed, and cited values as different provenance classes.
3. Preserve units, sign convention, stress measure, drainage, material state, load path, and scale.
4. Repeated observations from one unit do not become independent replication by being numerous.
5. Do not infer a mechanism from one correlated trend.
6. A contour plot is qualitative unless a reproducible metric is extracted.
7. Calibration is not independent validation.
8. Statistical significance is not engineering significance.
9. Extra parameters must be physically necessary, identifiable, or improve independent prediction.
10. Exponential/logarithmic arguments must be dimensionless.
11. A conclusion must not outrun the strongest support path in the Evidence Graph.
12. A reference must be both real **and** appropriate for the exact claim where it is cited.
13. `NOT FOUND` is not evidence of fabrication; unresolved or high-risk records require explicit review before deletion or replacement.

## Local validation

```bash
python scripts/validate_repo.py
```

Current release gate covers 21 skills, all prior v0.2–v0.4 research/quantitative checks, Citation Integrity Core checks, Evidence Graph smoke tests, calibration/data/unit negative tests, single-reference resolver regression, and whole-bibliography forensic regression.

## Repository layout

```text
Geotechnical-Research-Skills/
├── README.md
├── CHANGELOG.md
├── registry.yaml
├── docs/
├── examples/
├── scripts/
├── tests/
└── skills/
```

## Contribution rule

A new skill should only be added if it introduces a distinct scientific reasoning capability or a reusable integrity gate. Do not add a solver wrapper merely because a software package is popular.

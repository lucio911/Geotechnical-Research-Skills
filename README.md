# Geotechnical-Research-Skills

[![validate-skills](https://github.com/lucio911/Geotechnical-Research-Skills/actions/workflows/validate.yml/badge.svg)](https://github.com/lucio911/Geotechnical-Research-Skills/actions/workflows/validate.yml)

Research-reasoning Agent Skills for evidence-grounded, mechanics-aware, quantitatively defensible geotechnical engineering.

> Status: **v0.4.0 Experimental & Quantitative Research Core**. This release extends the v0.3 Evidence Architecture upstream into experiment design, raw-data QC, statistical inference, parameter calibration, and unit/dimension control. The suite remains software-agnostic: no solver-control or GUI automation skills are part of Research-Core.

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

## v0.4 skill map

| Skill | Pack | Role |
|---|---|---|
| `geotech-router` | core | Route the smallest defensible workflow |
| `geotech-project-ledger` | core | Maintain project truth and provenance |
| `geotech-evidence-ledger` | evidence-core | Build/audit the typed Evidence Graph |
| `geotech-literature-review` | evidence-core | Evidence-oriented literature synthesis and contradiction mapping |
| `geotech-paper-spine` | evidence-core | Main/supporting/boundary claim architecture and figure roles |
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

## What changed in v0.4

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

## v0.4 Evidence Graph extension

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
        +----> RES -> CLM
        |
        +----> PAR
```

For calibrated models with independent validation:

```text
DAT(calibration) -> QC -> ANA(calibration) -> PAR
                                             |
                                             v
DAT(validation)  -> QC -> ANA(validation) -> RES(validation)
                         ^                   |
                         |                   +---- validates ---> PAR
                         +---- parameterizes-+

RES(validation) -> CLM
```

New graph relations include `assessed_by`, `analyzed_by`, `qualifies`, `estimates`, `parameterizes`, and `validates`.

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

### Numerical study

`geotech-numerical-planner -> geotech-unit-dimension-audit -> geotech-result-to-claim -> geotech-evidence-ledger -> geotech-pre-submission-reviewer`

### Manuscript repair

`geotech-paper-spine -> geotech-evidence-ledger -> geotech-result-to-claim -> geotech-gap-novelty -> geotech-pre-submission-reviewer`

## Scientific integrity doctrine

A downstream analysis cannot repair a failed upstream design or provenance gate.

For consequential quantitative claims seek:

`claim -> result -> analysis -> QC -> dataset -> method/design -> conditions -> uncertainty -> alternatives -> boundary`

For calibrated predictive claims also require:

`parameter set -> calibration provenance + independent validation result`

If a link is missing, weaken the wording, label the claim provisional, obtain additional evidence, or remove the claim.

## Validation

Run:

```bash
python scripts/validate_repo.py
```

The validator checks the 17 skills, trigger fixtures, Evidence Graph schemas/examples, quantitative helper scripts, and example calibration/unit manifests.

## Roadmap

**v0.5 candidate focus:** reliability and uncertainty reasoning, constitutive-model selection/audit, measurement uncertainty, standards/codes evidence handling, and reviewer-response traceability. Domain packs should add geotechnical ontology/checklists without duplicating core reasoning.

## License

MIT. Third-party papers, standards, manuals, software, and datasets retain their own licenses and terms.

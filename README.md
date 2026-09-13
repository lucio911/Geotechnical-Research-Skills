# Geotechnical-Research-Skills

Research-reasoning Agent Skills for evidence-grounded, mechanics-aware, and quantitatively defensible geotechnical engineering.

> **Status:** Experimental  
> **Current version:** v0.4.0 — Experimental & Quantitative Research Core

## What this project is

Geotechnical-Research-Skills is a modular Agent Skills suite designed for researchers in geotechnical engineering. The project focuses on scientific reasoning rather than software automation.

The central principle is simple:

> AI should not merely help write geotechnical papers. It should make unsupported geotechnical claims harder to produce.

The suite connects literature evidence, mechanics, experimental design, quantitative inference, model calibration, figures, claims, and manuscript structure through explicit handoff objects and an auditable Evidence Graph.

## What this project is not

This project is **not** an Abaqus/PLAXIS/FLAC3D GUI copilot, solver automation framework, or generic prompt collection.

It intentionally avoids binding the research core to any one numerical package. Numerical results are treated as one evidence source among experiments, theory, field observations, literature, and standards.

## Current Skills

### Research-Core

- `geotech-paper-reader`
- `geotech-gap-novelty`
- `geotech-theory-derivation`
- `geotech-result-to-claim`
- `geotech-pre-submission-reviewer`
- `geotech-literature-review`
- `geotech-evidence-ledger`
- `geotech-paper-spine`

### Quantitative-Core

- `geotech-experiment-design`
- `geotech-data-qc`
- `geotech-statistics`
- `geotech-parameter-calibration`
- `geotech-unit-dimension-audit`

### Supporting Skills

- `geotech-router`
- `geotech-project-ledger`
- `geotech-numerical-planner`
- `geotech-scientific-figure`

Total: **17 skills**.

## Architecture

```text
Research Question
      ↓
Literature Review
      ↓
Gap & Novelty
      ↓
Experiment / Study Design
      ↓
Data QC
      ↓
Statistics / Parameter Calibration / Theory
      ↓
Result-to-Claim Audit
      ↓
Evidence Graph
      ↓
Paper Spine + Figure Architecture
      ↓
Pre-submission Adversarial Review
```

The quantitative research chain is represented explicitly:

```text
MTH → DAT → QC → ANA → RES → CLM
              └→ PAR → validation → RES → CLM
```

where:

- `MTH` = method;
- `DAT` = dataset;
- `QC` = quality-control record;
- `ANA` = analysis;
- `PAR` = calibrated parameter set;
- `RES` = result;
- `CLM` = scientific claim.

## Evidence Graph

The Evidence Graph uses stable IDs rather than relying on manuscript paragraph numbers.

Supported research objects include:

```text
RQ-###   research question
GAP-###  gap
HYP-###  hypothesis
MTH-###  method
DAT-###  dataset
QC-###   quality-control record
ANA-###  analysis
PAR-###  parameter set
RES-###  result
SRC-###  source / standard
MEC-###  mechanism
CLM-###  claim
BND-###  applicability boundary
FIG-###  figure
SEC-###  manuscript section
CON-###  conclusion
DEC-###  research decision
```

This allows a conclusion to be traced upstream, for example:

```text
CON-002
  ← CLM-005
      ← RES-014
          ← ANA-004
              ← QC-003
                  ← DAT-006
                      ← MTH-003
```

A deterministic graph validator can detect broken provenance chains, unsupported conclusions, orphan results, invalid edges, and selected circular dependencies.

## v0.4 focus: Experimental & Quantitative Research Core

### 1. Experiment design

`geotech-experiment-design` starts from claims and competing hypotheses rather than test matrices.

It asks whether changes attributed to a target factor may instead reflect:

- relative density or void ratio;
- water content/saturation;
- OCR or stress history;
- drainage condition;
- loading sequence and prior cyclic history;
- specimen preparation;
- scale or boundary effects;
- particle-size effects;
- apparatus compliance;
- sensor seating or reference drift.

A test programme must define experimental units, replication, controls, measured responses, decision criteria, and applicability limits.

### 2. Data QC

`geotech-data-qc` follows an immutable provenance model:

```text
raw
 ↓
processed
 ↓
analysis-ready
```

Raw observations must not be overwritten. Exclusions, smoothing, normalization, synchronization, zero correction, interpolation, and filtering require explicit provenance.

The included `audit_csv.py` provides deterministic structural checks such as missing values, duplicate rows, non-monotonic time, and constant numeric channels. Passing structural checks is **not** equivalent to passing scientific sensor QC.

### 3. Statistics

`geotech-statistics` identifies the experimental unit before selecting a statistical method.

One specimen measured over 100 cycles does **not** automatically mean `n = 100`. The skill distinguishes independent replication from repeated measures and separates statistical significance from engineering significance.

### 4. Parameter calibration

`geotech-parameter-calibration` treats fitting as a model-identification problem rather than curve decoration.

It audits:

- parameter meaning and bounds;
- objective functions and weighting;
- identifiability and parameter compensation;
- multi-start stability;
- residual structure;
- reduced versus full models;
- calibration/validation leakage;
- independent predictive performance;
- uncertainty and extrapolation boundaries.

The included manifest checker can catch explicit train/validation case overlap and selected parameter/bound errors.

### 5. Units and dimensions

`geotech-unit-dimension-audit` checks dimensional consistency, normalization, reference states, stress/sign conventions, and common geotechnical unit traps.

For example, a formulation such as

```text
exp(-λ r_p)
```

requires the exponent to be dimensionless. If `r_p` is measured in mm, then `λ` cannot simultaneously be called a dimensionless parameter without an explicit normalization.

## Research-Core highlights

### Gap & Novelty

The suite rejects novelty claims based only on changing soil type, geometry, software, or parameter ranges. Novelty is stress-tested at phenomenon, mechanism, method, evidence, predictive, and engineering-capability levels.

### Theory derivation

Models are audited for assumptions, state variables, closure, dimensions, limiting cases, identifiability, calibration, validation, and classification.

A model using both `r_p` and `B_r` is explicitly checked for information overlap when `B_r = h(r_p)`.

### Result to Claim

Evidence and claims are separated by level. Association is not silently upgraded into governing mechanism or causality.

### Pre-submission review

Independent reviewer roles examine mechanics, experiment/measurement, numerical evidence, statistics, novelty/evidence, and rejection-level vulnerabilities before an editor synthesis.

## Repository layout

```text
Geotechnical-Research-Skills/
├── README.md
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── registry.yaml
├── docs/
├── examples/
├── scripts/
├── tests/
└── skills/
    ├── geotech-router/
    ├── geotech-project-ledger/
    ├── geotech-evidence-ledger/
    ├── geotech-literature-review/
    ├── geotech-paper-reader/
    ├── geotech-gap-novelty/
    ├── geotech-theory-derivation/
    ├── geotech-numerical-planner/
    ├── geotech-result-to-claim/
    ├── geotech-scientific-figure/
    ├── geotech-paper-spine/
    ├── geotech-pre-submission-reviewer/
    ├── geotech-experiment-design/
    ├── geotech-data-qc/
    ├── geotech-statistics/
    ├── geotech-parameter-calibration/
    └── geotech-unit-dimension-audit/
```

## Validation

Run:

```bash
python scripts/validate_repo.py
```

The validator checks Agent Skill structure, declared reference files, registry coverage, Research-Core/Quantitative-Core required assets, helper-script smoke tests, and Evidence Graph examples.

Additional tests:

```bash
python tests/test_evidence_graph.py
python tests/test_quantitative_core.py
```

## Agent Skills compatibility

Each skill uses:

```text
skills/<skill-name>/SKILL.md
```

with YAML frontmatter and progressive disclosure. Detailed taxonomies and templates are stored under `references/`; deterministic utilities are placed under `scripts/`; OpenAI/Codex UI metadata is stored under `agents/openai.yaml`.

## Suggested usage

Use the router or invoke skills explicitly in Agent-Skills-compatible environments.

Examples:

```text
Use geotech-paper-reader to extract an auditable Paper Card from these papers.

Use geotech-gap-novelty to stress-test whether this tunnel study is genuinely novel.

Use geotech-experiment-design to test whether this cyclic loading programme can identify amplitude effects independently of loading history.

Use geotech-parameter-calibration to audit this Br-rp-G/G0 model for parameter compensation and validation leakage.

Use geotech-result-to-claim to audit whether these deformation contours and displacement curves support the stated mechanism.

Use geotech-pre-submission-reviewer to identify rejection-level weaknesses in this manuscript.
```

## Installation

For Codex/Agent-Skills-compatible systems, copy the relevant skill folders into your local skills directory or reference the repository from your agent configuration.

Install only the skills needed for the current workflow where possible. Smaller active skill sets reduce routing ambiguity.

## Design philosophy

A good research agent should occasionally say:

- the experiment cannot isolate the claimed mechanism;
- the data quality is insufficient for the proposed inference;
- the sample size is not the number of recorded cycles;
- this is calibration, not validation;
- this parameter is not identifiable from the available observations;
- this quantity is dimensionally inconsistent;
- this figure does not add independent evidence;
- this mechanism is only one plausible interpretation;
- this conclusion cannot be traced to evidence;
- this novelty is only a parameter substitution.

Those are features, not failures.

## License

MIT.

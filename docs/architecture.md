# Architecture — Research & Quantitative Core

## 1. Objective

Create an auditable chain from research question to evidence to claims and manuscript decisions, while inserting experimental design, data quality, quantitative inference, and calibration before downstream scientific claims.

## 2. Core chain

```text
Question / Literature
    ↓
Gap / Novelty
    ↓
Hypothesis / Model
    ↓
Experiment Contract / Method
    ↓
Raw Data
    ↓
QC
    ↓
Analysis / Calibration
    ↓
Result
    ↓
Evidence Graph
    ↓
Claim
    ↓
Figure / Section / Conclusion
    ↓
Adversarial review
```

## 3. Typed Evidence Graph

Stable node IDs:

| Prefix | Type |
|---|---|
| `RQ` | research question |
| `GAP` | gap |
| `HYP` | hypothesis |
| `MTH` | method/design/model |
| `DAT` | dataset |
| `QC` | quality-control record |
| `ANA` | analysis/statistical/calibration procedure |
| `PAR` | parameter set |
| `RES` | result |
| `SRC` | source/standard |
| `MEC` | mechanism/interpretation |
| `CLM` | claim |
| `BND` | applicability boundary |
| `FIG` | figure/table evidence artifact |
| `SEC` | manuscript section |
| `CON` | conclusion |
| `DEC` | research decision |

Typical relations:

- `addresses`
- `tests`
- `produces`
- `assessed_by`
- `analyzed_by`
- `qualifies`
- `yields`
- `estimates`
- `parameterizes`
- `validates`
- `supports`
- `contradicts`
- `consistent_with`
- `discriminates`
- `explains`
- `bounds`
- `visualized_by`
- `reported_in`
- `concludes`
- `cites`
- `depends_on`

The relation wording is intentional: `consistent_with` is weaker than `supports`; `supports` does not imply `explains`; `explains` does not automatically prove uniqueness; and `validates` is reserved for explicit validation evidence rather than fit quality alone.

## 4. Evidence classes

- **E0**: assertion or agent speculation only
- **E1**: qualitative pattern / contour / one unverified source
- **E2**: quantitative trend with provenance
- **E3**: quantitative trend plus repeatability, sensitivity, uncertainty, or robustness evidence
- **E4**: independent validation or evidence that discriminates among mechanisms
- **E5**: independent convergent multi-method/field evidence

The grade is relative to a claim; it is not a universal quality score for an entire paper.

## 5. Integrity gates

### Gate A — provenance
Can every critical number, condition, equation, result, and citation be traced?

### Gate B — design and data quality
Can the study discriminate its hypothesis, and are analysis datasets traceable to immutable raw data with documented QC/exclusions?

### Gate C — mechanics
Are stress measures, state variables, boundary conditions, material assumptions, and inferred mechanisms physically coherent?

### Gate D — quantitative inference
Are experimental units, dependence, uncertainty, effect sizes, calibration/validation splits, parameter identifiability, and units/dimensions defensible?

### Gate E — evidence strength
Does the evidence class/grade justify the wording strength?

### Gate F — novelty
Is the contribution more than a new parameter combination or application label?

### Gate G — transferability
Is the applicability range stated in terms of material, state, stress path, drainage, geometry, loading, scale, and model assumptions?

### Gate H — manuscript consistency
Do title, abstract, figures, Results, Discussion, and Conclusions make mutually consistent claims?

### Gate I — contradiction handling
Has material contradictory evidence been explained, bounded, or preserved as unresolved rather than ignored?

## 6. Deterministic versus scientific checks

Scripts may deterministically detect:

- duplicate IDs;
- invalid graph relations;
- orphan QC/analysis/parameter/result/claim/conclusion objects;
- calibration/validation case overlap in declared manifests;
- incomplete variable/unit registers;
- missing boundaries;
- broken references;
- unsupported dependency chains.

Scripts cannot determine whether a mechanism is physically correct. That remains a Research-Core reasoning task.

## 7. Progressive disclosure

`SKILL.md` contains the executable reasoning workflow. Detailed rubrics, schemas, and examples belong in `references/`. Deterministic utilities belong in `scripts/`. Domain packs should add geotechnical ontologies/checklists without cloning core logic.

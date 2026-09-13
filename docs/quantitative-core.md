# Quantitative Research Core (v0.4)

v0.4 extends the evidence architecture upstream from claims into experimental design, data quality, inference, calibration, and units.

## Canonical quantitative chain

```text
Research question
    ↓
Experiment Contract / Method
    ↓
Raw dataset
    ↓
QC
    ↓
Analysis
    ├──→ Result
    └──→ Parameter Set
             ↓
       independent validation
             ↓
           Result
             ↓
           Claim
```

## Five gates

1. **Design gate** — can the study discriminate the hypothesis from credible alternatives?
2. **Data gate** — is the analysis dataset traceable to immutable raw data with documented transformations?
3. **Inference gate** — does n represent independent experimental units and does the method respect dependence?
4. **Calibration gate** — are parameters identifiable enough and are validation cases independent of fitting?
5. **Dimension gate** — are units, dimensions, reference states, normalized variables, and sign/stress conventions explicit?

A downstream claim cannot compensate for a failed upstream gate.

## Quantitative objects

- Experiment Contract
- Data Provenance Card
- QC Record
- Statistical Analysis Card
- Calibration Manifest
- Variable/Unit Register
- `QC`, `ANA`, `PAR` Evidence Graph nodes

The suite deliberately avoids prescribing one statistical package or optimization library. The core value is scientific contract, auditability, and claim discipline.
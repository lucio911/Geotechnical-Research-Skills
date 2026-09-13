---
name: geotech-data-qc
description: Audit geotechnical experimental and monitoring data before analysis, covering immutable raw-data provenance, sensor calibration/range/drift, synchronization, cycle segmentation, missingness, outliers, exclusions, preprocessing, and derived-variable traceability. Use before statistics, parameter calibration, plotting, or mechanism interpretation of laboratory, model-test, field-monitoring, or cyclic-loading data.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Data QC

Do not clean data until the raw record, test context, and transformation history are preserved.

## Workflow

1. Freeze and fingerprint raw files.
2. Reconstruct test/channel metadata.
3. Check file/table structure.
4. Audit sensors and calibration.
5. Check synchronization and loading segmentation.
6. Characterize missingness and anomalies.
7. Separate exclusion decisions from transformations.
8. Recompute important derived quantities from formulas.
9. Produce a QC record and analysis-ready provenance path.

## Raw-data rule

Use three layers:

```text
raw (immutable)
 ↓
processed (calibrated/synchronized/converted)
 ↓
analysis-ready (documented exclusions/derived variables)
```

Never overwrite raw measurements because a point looks wrong.

Read `references/data-integrity.md`.

## Sensor audit

For each channel record:

- physical quantity and location;
- sensor ID/range/resolution;
- calibration source/date/function;
- acquisition sampling rate;
- zeroing/tare convention;
- saturation/clipping status;
- drift or baseline shift;
- sign convention;
- known malfunction periods.

Read `references/sensor-qc.md`.

## Test-sequence reconstruction

For cyclic or staged tests verify:

- loading start/end times;
- cycle numbering rule;
- command versus measured amplitude;
- load/displacement control transitions;
- rest periods;
- frequency stability;
- previous loading history;
- specimen replacement or re-seating;
- first-cycle seating/transient behavior.

Read `references/cyclic-test-qc.md`.

## Missing and anomalous records

Classify abnormalities instead of immediately deleting them:

- acquisition dropout;
- impossible value/unit error;
- sensor saturation;
- transient seating;
- true mechanical event;
- synchronization error;
- unknown.

Every exclusion needs:

`row/time/cycle + channel + reason + rule + operator/agent + downstream consequence`.

## Derived-variable audit

For derived variables such as:

- secant/dynamic stiffness;
- damping ratio;
- accumulated plastic displacement;
- normalized modulus;
- ovalization;
- settlement ratio;
- excess pore-pressure ratio;
- breakage index;

store formula, units, reference state, smoothing/windowing if any, and the source channels.

## Deterministic CSV helper

Use:

```bash
python scripts/audit_csv.py data.csv --time-column time
```

It checks table structure, missing cells, duplicate rows, numeric columns, low-variance/constant columns, and time monotonicity. Passing this script does **not** certify sensor or scientific quality.

## Evidence Graph handoff

Create/update:

- `DAT` raw/processed datasets;
- `QC` quality-control record;
- `ANA` transformation/analysis procedure where applicable.

Recommended relations:

`MTH -> produces -> DAT`

`DAT -> assessed_by -> QC`

`DAT -> analyzed_by -> ANA`

`QC -> qualifies -> ANA/RES`

## Output

### Data Provenance Card
Files, hashes/versions, test metadata, transformations.

### Sensor QC Table
Channel, range, calibration, drift, clipping, status.

### Anomaly/Exclusion Ledger
Location, cause class, action, justification.

### Derived-variable Register
Name, equation, source channels, units, reference state.

### QC Decision
`pass / conditional / fail` plus limitations.

## Failure modes

- silently deleting points to improve fit;
- treating smoothing as raw data;
- renumbering cycles after exclusions without provenance;
- using commanded amplitude when measured amplitude differs materially;
- assuming a flat channel is physical stability before sensor checks;
- declaring data quality from a structural CSV script alone.

# Evidence Graph Schema

The canonical lightweight representation is JSON with three top-level fields:

```json
{
  "project": {"id": "...", "version": "..."},
  "nodes": [],
  "edges": []
}
```

## Node

Required:

- `id`: stable ID with known prefix.
- `type`: one of `research_question`, `gap`, `hypothesis`, `method`, `dataset`, `quality_control`, `analysis`, `parameter_set`, `result`, `source`, `mechanism`, `claim`, `boundary`, `figure`, `section`, `conclusion`, `decision`.
- `label`: concise human-readable statement.

Recommended:

- `status`: `active`, `provisional`, `contested`, `retired`.
- `location`: file/figure/section/source locator.
- `conditions`: material, stress, drainage, loading, scale, or model conditions.
- `confidence`: `high`, `medium`, `low`, `provisional`.
- `notes`.

## Edge

Required:

- `from`: source node ID.
- `to`: target node ID.
- `relation`: typed relation.

Recommended:

- `evidence_grade`: `E0`–`E5` for evidentiary relations.
- `scope`: what proposition the edge supports.
- `notes`.

## Minimum provenance rules

- `DAT` nodes should retain method/source provenance where available.
- `QC` nodes should have incoming `assessed_by` from `DAT`.
- `ANA` nodes should have incoming `analyzed_by` from `DAT`; `QC -> ANA` may `qualifies` the analysis.
- `PAR` nodes should be estimated by `ANA`; predictive validation should come through an independent analysis/result path rather than the calibration fit.
- `RES` nodes should trace to `DAT`, `ANA`, `MTH`, or `SRC`.
- `CLM` nodes require evidence/dependency paths that ultimately reach `RES`, `SRC`, `DAT`, `ANA`, or `MTH`.
- `CON` nodes require an incoming `concludes` relation from a claim.
- `FIG` nodes should be connected to the result/source they visualize.
- broad `CLM` nodes should have an incoming `bounds` relation from a `BND` node.

## Direction convention

Write edges from evidence/upstream object to downstream interpretation/use:

`RES-001 -> CLM-003 (supports)`

`CLM-003 -> CON-002 (concludes)`

`BND-001 -> CLM-003 (bounds)`

This convention makes upstream provenance tracing deterministic.
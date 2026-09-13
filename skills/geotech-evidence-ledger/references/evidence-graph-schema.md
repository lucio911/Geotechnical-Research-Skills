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
- `type`: one of `research_question`, `gap`, `hypothesis`, `method`, `dataset`, `quality_control`, `analysis`, `parameter_set`, `result`, `source`, `citation`, `mechanism`, `claim`, `boundary`, `figure`, `section`, `conclusion`, `decision`.
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
- `fidelity_grade`: `F0`–`F5` when a `CIT` instance supports/contradicts/is-consistent-with a claim.
- `scope`: what proposition the edge supports.
- `notes`.

## Minimum provenance rules

- `DAT` nodes should retain method/source provenance where available.
- `QC` nodes should have incoming `assessed_by` from `DAT`.
- `ANA` nodes should have incoming `analyzed_by` from `DAT`; `QC -> ANA` may `qualifies` the analysis.
- `PAR` nodes should be estimated by `ANA`; predictive validation should come through an independent analysis/result path rather than the calibration fit.
- `RES` nodes should trace to `DAT`, `ANA`, `MTH`, or `SRC`.
- `SRC` nodes represent external works/standards/datasets and should declare a scientific role.
- `CIT` nodes represent manuscript citation instances, not works. Each should have incoming `cited_as` from a `SRC` source and should normally connect to a `CLM` and a `SEC`.
- `CLM` nodes require evidence/dependency paths that ultimately reach `RES`, `SRC`, `DAT`, `ANA`, or `MTH`.
- `CON` nodes require an incoming `concludes` relation from a claim.
- `FIG` nodes should be connected to the result/source they visualize.
- broad `CLM` nodes should have an incoming `bounds` relation from a `BND` node.

## Direction convention

Write edges from evidence/upstream object to downstream interpretation/use:

`RES-001 -> CLM-003 (supports)`

`CLM-003 -> CON-002 (concludes)`

`BND-001 -> CLM-003 (bounds)`

For citation instances:

`SRC-012 -> CIT-063 (cited_as)`

`CIT-063 -> CLM-031 (supports, fidelity_grade=F3)`

`CIT-063 -> SEC-005 (reported_in)`

This convention makes upstream provenance tracing deterministic.

## Citation integrity extension (v0.5)

`SRC` and `CIT` are deliberately different. One verified source may appear as multiple citation instances in different manuscript locations and receive different fidelity grades because each occurrence can support a different proposition.

Recommended `CIT` fields include `manuscript_location`, `source_locator`, `mismatch`, `action`, and `confidence`. Do not store canonical work metadata on every citation instance; keep work identity on the `SRC` record and link with `cited_as`.

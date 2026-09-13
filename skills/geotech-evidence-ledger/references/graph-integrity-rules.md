# Evidence Graph Integrity Rules

## Blocking

1. Duplicate node IDs.
2. Edge references unknown node.
3. Invalid ID-prefix/type combination.
4. Conclusion with no claim.
5. Claim whose dependency chain never reaches result/source/data/method evidence.
6. Result with no plausible upstream provenance.
7. Circular claim chains used as evidence for themselves.
8. Calibration-only evidence labeled independent validation.

## Major

1. Mechanism node has only association evidence but feeds a causal/governing claim.
2. Engineering recommendation has no explicit applicability boundary.
3. Figure is treated as evidence but underlying result/source is missing.
4. Contradictory evidence exists but the claim is marked settled with no resolution.
5. The same numerical result is represented as multiple independent corroborating evidence nodes.

## Moderate

1. External source lacks source role.
2. Evidence edge lacks a grade.
3. Result/source locator is imprecise.
4. Duplicate semantic claims use inconsistent terminology.
5. Manuscript section makes a claim not represented in the graph.

## Important caution

Passing graph-integrity rules proves only structural traceability. It does not prove that the physical interpretation is correct.
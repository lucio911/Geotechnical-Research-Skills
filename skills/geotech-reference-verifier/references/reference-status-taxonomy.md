# Reference Status Taxonomy

Use conservative states. Do not collapse uncertainty into fabrication.

- `VERIFIED` — authoritative metadata and supplied reference describe the same work.
- `VERIFIED_WITH_DRIFT` — same work, but one or more bibliographic fields require correction.
- `IDENTIFIER_MISMATCH` — supplied DOI/PMID/arXiv/etc resolves to a different work.
- `DUPLICATE` — same work appears more than once under different citekeys/metadata.
- `AMBIGUOUS` — multiple plausible candidates remain.
- `SUSPECTED_COMPOSITE` — fields appear assembled from multiple works.
- `UNRESOLVED` — authoritative verification is currently insufficient.
- `SUSPECTED_FABRICATION` — repeated authoritative searches fail and metadata is internally implausible or non-coherent.
- `FABRICATED_CONFIRMED` — use only after explicit human confirmation.
- `HUMAN_DECISION_REQUIRED` — scientific/editorial action is needed before deletion/replacement.

High-risk states: `IDENTIFIER_MISMATCH`, `SUSPECTED_COMPOSITE`, `SUSPECTED_FABRICATION`, `FABRICATED_CONFIRMED`.

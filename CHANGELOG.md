# Changelog

## v0.5.0 — Citation Integrity Core

### Added

- `geotech-reference-verifier` for reference existence, identity, metadata, identifier, duplicate/composite, and publication-status auditing.
- `geotech-citation-fidelity` with `CIT-###` citation instances and F0–F5 support grades.
- `geotech-bibliography-audit` for dangling/orphan citations, duplicate identifiers/titles, and citekey consistency.
- `geotech-reference-format` for metadata-preserving deterministic CSL-oriented rendering.
- Citation Integrity Core documentation, worked example, deterministic helper scripts, trigger fixtures, and negative tests.
- `CIT` Evidence Graph node type, `cited_as` relation, and citation-to-claim `fidelity_grade` separate from E0–E5 evidence strength.
- Online reference resolver using Crossref/DataCite public metadata, optional OpenAlex cross-checking, provenance capture, and deterministic identity scoring.
- Offline resolver fixtures for matched identity, DOI-to-wrong-work mismatch, and unresolved/no-hit behavior.
- Whole-bibliography `audit_references.py` for BibTeX parsing, cached batch resolution, duplicate DOI detection, near-duplicate title screening, retraction flags, and JSON/Markdown integrity reports.
- Batch fixtures covering `Family, Given` BibTeX author normalization, duplicate DOI records, identifier mismatch, and unresolved references.

### Integrity changes

- `NOT FOUND` is explicitly not equivalent to `FABRICATED`.
- `FABRICATED_CONFIRMED` requires explicit human review in the deterministic record audit.
- DOI/identifier resolution alone is insufficient: the resolved work identity must match the manuscript record.
- Real references are audited separately for whether they support the exact manuscript proposition where cited.
- The same verified `SRC` may have multiple `CIT` instances with different fidelity grades.
- Formatting is downstream of metadata verification and must not invent missing bibliographic fields.
- Reference style rendering is designed around canonical metadata plus deterministic CSL/bibliography processors rather than LLM-guessed punctuation.
- API/network failure is treated as an evidence gap; the online resolver cannot automatically emit `FABRICATED_CONFIRMED`.
- `UNRESOLVED` and `AMBIGUOUS` remain review states in batch mode; neither is automatically promoted to fabrication.
- Duplicate DOI and near-duplicate title findings are screening flags, not automatic deletion decisions.

### Validation

- Repository validator retains all prior Research/Evidence/Quantitative-Core gates and adds Citation-Core gates rather than replacing earlier checks.
- Added negative fixtures for fabricated-reference confirmation without human review, dangling citekeys, orphan bibliography entries, and weak citation support.
- GitHub Actions validates all 21 skills and all five repository smoke/regression suites through `scripts/validate_repo.py`.
- GitHub Actions additionally runs `tests/test_reference_resolver.py` without network access to verify identity scoring and conservative failure behavior.
- GitHub Actions additionally runs `tests/test_batch_reference_forensics.py` to verify whole-bibliography parsing, duplicate detection, mismatch handling, unresolved-policy preservation, and `--fail-on-critical` behavior.
- The batch regression fixture is expected to yield two verified duplicate representations, one identifier mismatch, and one unresolved item without any automatic fabrication verdict.

## v0.4.0 — Experimental & Quantitative Research Core

### Added

- `geotech-experiment-design`
- `geotech-data-qc`
- `geotech-statistics`
- `geotech-parameter-calibration`
- `geotech-unit-dimension-audit`
- deterministic CSV structural QC helper;
- calibration-manifest leakage/bounds checker;
- variable/unit-register completeness checker;
- quantitative Evidence Graph example;
- `QC`, `ANA`, and `PAR` Evidence Graph node types;
- `assessed_by`, `analyzed_by`, `qualifies`, `estimates`, `parameterizes`, and `validates` relations;
- `docs/quantitative-core.md`;
- worked `examples/quantitative-research-workflow.md`.

### Changed

- expanded the canonical research chain from method/data/results into explicit QC, analysis, calibration, and validation provenance;
- router now sends new experimental studies through design and QC before inference;
- project ledger now recommends experiment, QC, analysis, parameter, and variable/unit registers;
- repository validation now exercises quantitative helper scripts and both Evidence Graph examples.

### Scientific policy

- repeated cycles/time points from one specimen are not independent replication;
- statistical significance is not synonymous with engineering significance;
- calibration fit is not validation;
- extra model parameters must earn complexity through identifiability, physical necessity, or independent prediction;
- normalized variables and exponential/log arguments require explicit dimensional/reference-state interpretation.


## v0.3.0 — Evidence Architecture

### Changed

- Reframed the release around three cross-cutting capabilities: literature evidence synthesis, typed claim-to-evidence provenance, and manuscript argument architecture.
- Deepened `geotech-literature-review` with a review contract, staged search ladder, source-role taxonomy, contradiction synthesis, gap taxonomy, and saturation criteria.
- Deepened `geotech-paper-spine` with main/supporting/boundary/engineering claim hierarchy, argument dependencies, figure-role mapping, evidence budget, deletion test, and manuscript consistency gates.
- Rebuilt `geotech-evidence-ledger` around a typed Evidence Graph using stable IDs for questions, methods, datasets, results, literature, mechanisms, claims, boundaries, figures, sections, and conclusions.
- Updated `geotech-project-ledger` and `geotech-router` to use Evidence Graph handoffs.

### Added

- `evidence-graph.example.json` as a canonical lightweight graph example.
- `validate_evidence_graph.py` for deterministic graph/provenance checks.
- `trace_claim.py` for upstream claim/conclusion traceability.
- `render_mermaid.py` for human-readable graph visualization.
- Search protocol, literature evidence matrix, source-role, contradiction, argument-graph, figure-role, section-budget, manuscript-consistency, graph-schema, and graph-integrity references.
- Trigger cases for the three v0.3 focus skills.

### Scope

- Still deliberately excludes solver-control, GUI automation, and software-specific debugging wrappers from Research-Core.
- Scripts validate structure and provenance; they do not decide whether a geotechnical mechanism is physically correct.

## v0.2.0 — Research-Core

- Removed solver-control emphasis and excluded `abaqus-geotech` from Research-Core.
- Added `geotech-gap-novelty`.
- Deepened paper reading, theory derivation, result-to-claim reasoning, and adversarial review.
- Added evidence/claim ladders, model-classification and double-counting checks, trigger cases, and worked examples.

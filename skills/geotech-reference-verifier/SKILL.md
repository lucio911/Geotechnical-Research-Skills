---
name: geotech-reference-verifier
description: Verify that cited references actually exist, that DOI/PMID/arXiv or other identifiers resolve to the same work claimed in the manuscript, and that bibliographic metadata is not fabricated, composite, duplicated, retracted, or silently drifted. Use for reference-list integrity audits before submission or when AI-generated/copy-pasted references are suspect.
license: MIT
metadata:
  version: "0.5.0"
  domain: geotechnical-engineering
---

# Geotech Reference Verifier

Verify **reference identity**, not merely identifier syntax.

## Core distinction

A DOI that resolves is not sufficient. The resolved work must match the manuscript's claimed title/authors/year/venue.

Keep these layers separate:

1. **Existence** — can an authoritative record be found?
2. **Identity** — does the identifier resolve to the same work?
3. **Metadata** — are title, authors, year, venue, volume/issue/pages/article number correct?
4. **Publication status** — retracted, corrected, expression of concern, preprint vs version of record?
5. **Decision** — auto-fixable metadata drift vs human scientific decision.

## Verification workflow

1. Parse the original reference exactly as supplied. Never rewrite first.
2. Extract persistent identifiers: DOI, PMID/PMCID, arXiv, ISBN, report number, repository handle, URL.
3. Resolve the identifier against an authoritative source where available. For executable online resolution use `scripts/resolve_reference.py`; see `references/online-resolver.md`.
4. Compare canonical metadata field-by-field.
5. If no identifier exists, search by normalized title + first author + year; record candidate ambiguity.
6. Check for duplicate works represented by different citekeys or metadata variants.
7. Check retraction/correction/version status when it matters to the claim.
8. Classify the record using `references/reference-status-taxonomy.md`.
9. Never silently delete `SUSPECTED_COMPOSITE`, `UNRESOLVED`, or `SUSPECTED_FABRICATION` records. Mark `HUMAN_DECISION_REQUIRED`.
10. Emit a structured Reference Verification Record.

## Batch bibliography audit

For a complete `.bib` file, use `scripts/audit_references.py`; see `references/batch-forensics.md`.

The batch path:

- parses nested BibTeX fields without a single-regex shortcut;
- normalizes `Family, Given` author names for matching without rewriting canonical metadata;
- reuses the same online resolver and deterministic identity scorer;
- caches per-reference resolution records;
- flags duplicate DOI groups and conservative near-duplicate title pairs;
- aggregates verdicts, retraction flags, human-review items, and critical actions;
- emits both JSON and Markdown integrity reports;
- can return nonzero with `--fail-on-critical` for submission/CI gates.

## Source hierarchy

Prefer metadata in this order when available:

- publisher / DOI landing record;
- Crossref or DataCite;
- PubMed, arXiv, institutional repository, standards body, or other domain authority;
- OpenAlex / Semantic Scholar as secondary cross-checks;
- generic web or search-engine results only as discovery evidence.

Never treat a search snippet as canonical metadata.

## Required outputs

For each reference report:

- stable `SRC-###` or reference ID;
- original citation string/record;
- identifiers supplied;
- identifiers resolved;
- canonical metadata;
- per-field match result;
- publication-status result;
- classification;
- confidence and unresolved ambiguity;
- proposed correction **only when identity is sufficiently established**.

Use `references/reference-record-schema.md` and `assets/reference-record.example.json`.

## Integrity rules

- `NOT FOUND` is not the same as `FABRICATED`.
- A real DOI attached to the wrong title is an **identifier mismatch**, not a formatting error.
- Author/title fragments drawn from different real papers are a suspected **composite reference**.
- A metadata correction must preserve scientific identity.
- If a corrected reference would invalidate the surrounding manuscript claim, hand off to `geotech-citation-fidelity` rather than silently repairing prose.
- Network/API failure is an evidence gap, not evidence of fabrication.
- The online resolver can emit `VERIFIED`, `VERIFIED_WITH_DRIFT`, `IDENTIFIER_MISMATCH`, `AMBIGUOUS`, or `UNRESOLVED`; it never auto-confirms fabrication.
- Batch `UNRESOLVED` and `AMBIGUOUS` results remain human-review items; they are never converted automatically to fabrication findings.

## Stop condition

Stop when every audited reference has either (a) an auditable identity decision backed by resolved provenance and field-level checks, or (b) an explicit unresolved/high-risk status with the required human action recorded. Missing evidence must remain `UNRESOLVED`/`HUMAN_DECISION_REQUIRED`; never upgrade it to `VERIFIED` by inference.

For online identity resolution use `scripts/resolve_reference.py`. It queries public metadata services but keeps retrieval separate from deterministic identity scoring.

For whole-bibliography forensics use `scripts/audit_references.py`.

For deterministic record-shape checks use `scripts/audit_reference_record.py`.

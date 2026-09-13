---
name: geotech-bibliography-audit
description: Audit manuscript in-text citations against BibTeX/BibLaTeX or reference-list entries to detect dangling citations, orphan references, duplicate works, duplicate identifiers, citekey/metadata inconsistencies, and suspicious merged or split records. Use before journal submission or after large citation-library edits.
license: MIT
metadata:
  version: "0.5.0"
  domain: geotechnical-engineering
---

# Geotech Bibliography Audit

Audit manuscript-level citation consistency. This skill is not a metadata truth source; pair high-risk records with `geotech-reference-verifier`.

## Checks

1. In-text citekeys present but absent from `.bib` / bibliography.
2. Bibliography entries never cited in the manuscript.
3. Duplicate citekeys.
4. Same DOI under multiple citekeys.
5. Same normalized title represented multiple times.
6. Same work represented as preprint and version-of-record without explicit intent.
7. Author-year collisions that make author-date output ambiguous.
8. Citation-number discontinuity/order issues when working from rendered numbered manuscripts.
9. Suspicious records that appear merged or split.
10. Manuscript sections whose citations cannot be mapped to stable citation instances.

## Workflow

- Preserve the source manuscript and original `.bib`.
- Extract citekeys deterministically.
- Parse bibliography records without silently normalizing scientific metadata.
- Produce a discrepancy table.
- Hand duplicate/identity questions to `geotech-reference-verifier`.
- Hand claim-support questions to `geotech-citation-fidelity`.
- After repair, rerun until no unexplained dangling citations remain.

## Deterministic helper

For LaTeX + BibTeX projects:

```bash
python skills/geotech-bibliography-audit/scripts/audit_bib_consistency.py manuscript.tex references.bib
```

The script intentionally performs conservative structural checks rather than pretending to be a full TeX or BibTeX parser.

Read `references/bibliography-integrity.md` and `references/duplicate-resolution.md` before automatic cleanup.

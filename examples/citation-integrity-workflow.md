# Worked Example — Citation Integrity Workflow

Suppose the manuscript states:

> Particle breakage governs cyclic interface stiffness degradation (Li et al., 2024).

## Step 0 — Batch bibliography screen

Before auditing one sentence at a time, run the whole `.bib` file:

```bash
python skills/geotech-reference-verifier/scripts/audit_references.py references.bib \
  --email researcher@example.org \
  --use-openalex \
  --output-json reference-integrity-report.json \
  --output-md reference-integrity-report.md
```

The batch report screens:

- duplicate DOI records under multiple citekeys;
- near-duplicate titles with compatible author/year evidence;
- `IDENTIFIER_MISMATCH` records;
- `AMBIGUOUS` and `UNRESOLVED` records requiring review;
- retraction flags when secondary status evidence is available;
- cache/provenance state for every reference.

`UNRESOLVED` remains a search/review state. It is not an automatic fabrication finding.

For a submission gate, add `--fail-on-critical`. Identifier mismatch or a retraction flag then returns a nonzero exit code, while unresolved and duplicate-screening items remain review findings.

## Step 1 — Reference identity

`geotech-reference-verifier` checks whether the cited DOI resolves to Li et al. (2024), whether title/authors/year match, and whether the record is a version of record or another publication.

If the DOI resolves to a different paper, classify `IDENTIFIER_MISMATCH`. Stop formatting repair.

For a DOI-first forensic check:

```bash
python skills/geotech-reference-verifier/scripts/resolve_reference.py \
  --reference-id REF-027 \
  --doi 10.xxxx/example \
  --title "Claimed paper title" \
  --author "Li Xiaoming" \
  --year 2024 \
  --email researcher@example.org \
  --use-openalex \
  --output REF-027.resolution.json
```

The resolver keeps retrieval provenance, normalized candidates, identity score, field checks, and the conservative verdict. API failure or no candidate remains `UNRESOLVED`; it is not automatic evidence of fabrication.

## Step 2 — Citation instance

Create:

- `SRC-012` — verified Li et al. paper;
- `CIT-063` — citation occurrence in Discussion §5.1;
- `CLM-031` — "particle breakage governs cyclic interface stiffness degradation".

## Step 3 — Fidelity

If Li et al. only shows that breakage index rises while stiffness falls, the source demonstrates association but not governing causality.

Grade `CIT-063 = F2` and label `ASSOCIATION_TO_CAUSALITY` / `MECHANISM_OVERREACH`.

Recommended repair:

- weaken the claim to "is associated with" or "is consistent with";
- or add discriminating evidence/source capable of supporting the governing-mechanism claim.

## Step 4 — Bibliography structure

Confirm the citekey exists exactly once, no duplicate DOI exists, and no unused duplicate record is present.

## Step 5 — Style

Only after identity/metadata are verified, render the canonical record with the target journal CSL style. Punctuation repair must not alter author order, year, title, DOI, or work identity.

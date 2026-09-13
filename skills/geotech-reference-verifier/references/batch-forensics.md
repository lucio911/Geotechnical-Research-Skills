# Batch Reference Forensics

Use `scripts/audit_references.py` when a manuscript bibliography needs a whole-list integrity audit rather than one-reference-at-a-time resolution.

## Pipeline

```text
references.bib
    |
    v
stateful BibTeX parse
    |
    +--> citekey / title / authors / year / venue / DOI
    |
    v
per-reference resolver
    |
    +--> Crossref
    +--> DataCite
    +--> optional OpenAlex
    |
    v
identity scoring
    |
    +--> VERIFIED
    +--> VERIFIED_WITH_DRIFT
    +--> IDENTIFIER_MISMATCH
    +--> AMBIGUOUS
    +--> UNRESOLVED
    |
    +--> duplicate DOI / near-duplicate title audit
    |
    v
reference-integrity-report.json
reference-integrity-report.md
```

## BibTeX parsing rule

Do not parse a `.bib` file with a single regular expression. Titles and fields may contain nested braces, protected capitalization, quoted values, LaTeX commands, and commas inside field values. The batch script uses a stateful top-level splitter and removes case-protection braces before identity matching.

Common BibTeX author form `Family, Given` is normalized to `Given Family` for surname matching. This is a matching normalization only; it does not rewrite the canonical bibliography record.

## Cache

Default cache directory:

```text
.geotech/cache/reference-resolver/
```

The cache key includes the normalized original reference, OpenAlex setting, and resolver schema version. Use `--refresh-cache` when the resolution policy changes or metadata should be re-queried. Use `--no-cache` for deterministic tests.

A cache hit is provenance, not fresh verification. The generated report records cache-hit counts.

## Rate limiting

Online batch resolution uses the same public metadata adapters as `resolve_reference.py`. Use a contact email for Crossref and keep a nonzero delay for large bibliographies.

Example:

```bash
python skills/geotech-reference-verifier/scripts/audit_references.py references.bib \
  --email researcher@example.org \
  --use-openalex \
  --output-json reference-integrity-report.json \
  --output-md reference-integrity-report.md
```

## Duplicate rules

### Duplicate DOI

The same normalized DOI under multiple citekeys is a review item. It often indicates duplicate bibliography records, but conference/journal version relationships or metadata mistakes still require human inspection.

### Near-duplicate title

Pairs are flagged only when title similarity is high and author/year evidence is compatible. A near-duplicate title flag is not an automatic duplicate decision.

## Critical actions

Deterministic critical actions currently include:

- `IDENTIFIER_MISMATCH`;
- a secondary-source retraction flag.

`UNRESOLVED` and `AMBIGUOUS` remain review items, not fabrication findings.

`--fail-on-critical` returns a nonzero exit code when deterministic critical actions exist, which is useful for pre-submission gates and CI.

## Output policy

The batch report must retain:

- one per-reference resolver record;
- verdict counts;
- duplicate DOI groups;
- near-duplicate title pairs;
- retraction flags;
- manual/critical actions;
- cache-hit count;
- source provenance;
- the explicit policy that `UNRESOLVED` is not fabrication and fabrication cannot be confirmed automatically.

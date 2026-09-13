# Citation Integrity Core — v0.5.0

The citation layer separates five problems that are often incorrectly merged:

`existence != identity != metadata != citation fidelity != formatting`

## Skills

- `geotech-reference-verifier` — does the reference exist and is it the same work?
- `geotech-citation-fidelity` — does that source support this exact claim?
- `geotech-bibliography-audit` — do manuscript citations and bibliography records correspond structurally?
- `geotech-reference-format` — render verified metadata deterministically to the target style.

## Canonical workflow

```text
manuscript + .bib
      |
      v
bibliography audit
      |
      +--> suspicious identities --> reference verifier
      |                               |
      |                               +--> Crossref / DataCite
      |                               +--> optional OpenAlex
      |                               +--> deterministic identity score
      |
      +--> citation instances -----> citation fidelity
                                      |
                                      v
                              Evidence Graph CIT nodes
      |
      v
canonical metadata
      |
      v
CSL / deterministic renderer
      |
      v
final reference-style audit
```

## Online identity resolution

`skills/geotech-reference-verifier/scripts/resolve_reference.py` is the executable metadata-resolution layer.

It supports:

- DOI-first lookup through Crossref and DataCite public APIs;
- bibliographic title/author/year search when no DOI is supplied;
- optional OpenAlex identity and `is_retracted` cross-check;
- deterministic title/author/year/venue/DOI scoring;
- conservative `VERIFIED`, `VERIFIED_WITH_DRIFT`, `IDENTIFIER_MISMATCH`, `AMBIGUOUS`, and `UNRESOLVED` decisions.

The resolver deliberately cannot emit `FABRICATED_CONFIRMED`. Retrieval failure and `NOT FOUND` remain evidence gaps requiring further search or human review.

```text
Original reference
      |
      +--> metadata services
               |
               v
        normalized candidates
               |
               v
      deterministic identity score
               |
       +-------+---------+
       |                 |
   same work        mismatch/ambiguous
       |                 |
 canonical metadata   HUMAN REVIEW
```

CI tests the scorer with offline fixtures so repository validation does not depend on external API uptime.

See `skills/geotech-reference-verifier/references/online-resolver.md`.

## Whole-bibliography forensics

`skills/geotech-reference-verifier/scripts/audit_references.py` applies the same resolver policy to a complete BibTeX library.

```text
references.bib
     |
     v
stateful BibTeX parser
     |
     +--> normalize match-only title/author forms
     |
     v
per-reference resolver + cache
     |
     +--> identity verdicts
     +--> retraction flags
     +--> provenance
     |
     +--> duplicate DOI groups
     +--> near-duplicate title pairs
     |
     v
reference-integrity-report.json
reference-integrity-report.md
```

The batch parser handles nested braces and quoted/braced fields rather than relying on a single regular expression. Common BibTeX `Family, Given` author order is normalized only for identity matching.

Example:

```bash
python skills/geotech-reference-verifier/scripts/audit_references.py references.bib \
  --email researcher@example.org \
  --use-openalex \
  --output-json reference-integrity-report.json \
  --output-md reference-integrity-report.md
```

`--fail-on-critical` turns identifier mismatch or a retraction flag into a nonzero exit code for submission gates. Duplicate DOI, near-duplicate title, `AMBIGUOUS`, and `UNRESOLVED` findings remain review items rather than automatic deletion or fabrication decisions.

See `skills/geotech-reference-verifier/references/batch-forensics.md`.

## Release validation

The v0.5 repository gate runs the prior Research/Evidence/Quantitative tests plus citation-specific suites. GitHub Actions separately exercises:

- `python scripts/validate_repo.py`;
- `python tests/test_reference_resolver.py`;
- `python tests/test_batch_reference_forensics.py`.

The offline batch fixture deliberately includes two representations of the same DOI, one DOI-to-wrong-work mismatch, and one no-hit reference. Expected behavior is `VERIFIED ×2`, `IDENTIFIER_MISMATCH ×1`, `UNRESOLVED ×1`, plus duplicate-DOI and near-duplicate-title flags. No deterministic path is allowed to convert the unresolved item into confirmed fabrication.

## Citation Integrity Gate

A strong pre-submission state has:

- no unexplained dangling citations;
- no duplicate identifiers/works left unexplained;
- no unresolved identifier mismatches;
- no confirmed fabricated references;
- no unreviewed retraction flags affecting manuscript claims;
- central manuscript claims mapped to citation instances;
- weak F0–F2 support either repaired or explicitly bounded;
- formatting performed from verified canonical metadata using a declared style processor.

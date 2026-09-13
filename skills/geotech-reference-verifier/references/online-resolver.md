# Online Reference Resolver

`resolve_reference.py` separates metadata retrieval from identity judgment.

## Why two layers

A service response is not itself a scientific verdict. Retrieval can fail because of network, indexing, old literature, translated titles, incomplete deposits, or repository coverage. Therefore:

1. **resolver adapters** retrieve candidate records and provenance;
2. a **deterministic identity scorer** compares title, author surnames, year, venue, and DOI;
3. a policy layer emits `VERIFIED`, `VERIFIED_WITH_DRIFT`, `IDENTIFIER_MISMATCH`, `AMBIGUOUS`, or `UNRESOLVED`;
4. no automatic path emits `FABRICATED_CONFIRMED`.

`NOT FOUND` and API failure are never fabrication evidence by themselves.

## Source adapters

### Crossref

- DOI lookup: `GET https://api.crossref.org/works/{doi}`.
- Bibliographic search: `GET https://api.crossref.org/works?query.bibliographic=...`.
- Supply `--email` where possible to use Crossref's polite access pattern.

### DataCite

- DOI lookup: `GET https://api.datacite.org/dois/{doi}`.
- Public search: `GET https://api.datacite.org/dois?query=...`.
- No authentication is required for public Findable DOI metadata.

### OpenAlex (optional)

Enable with `--use-openalex`.

- DOI cross-check uses the `doi` Works filter.
- Title-only fallback uses Works search.
- When present, `is_retracted` is recorded as secondary status evidence.
- An OpenAlex API key can be supplied with `--openalex-api-key`; the key is redacted from output provenance.

OpenAlex is intentionally optional because search/query budgets and API policy can change independently of this repository.

## Identity score

The score is not a probability of truth. It is a reproducible matching heuristic.

With a supplied DOI:

- title: 55%;
- authors: 20%;
- year: 10%;
- DOI equality: 15%.

Without a DOI, title and author evidence receive higher weight; venue is used only when available.

A DOI resolving successfully does **not** guarantee a match. A very low title/identity score after DOI resolution yields `IDENTIFIER_MISMATCH`.

## Conservative classification

- `VERIFIED`: strong DOI + title + author + year agreement.
- `VERIFIED_WITH_DRIFT`: same work with correctable field drift.
- `IDENTIFIER_MISMATCH`: supplied DOI resolves, but the resolved work is clearly not the claimed work.
- `AMBIGUOUS`: candidate evidence is plausible but insufficiently discriminating.
- `UNRESOLVED`: no candidate clears the matching gate, or no candidate was retrieved.

Any deletion, citation replacement, or `FABRICATED_CONFIRMED` judgment remains a human scientific decision.

## CLI examples

DOI-first:

```bash
python skills/geotech-reference-verifier/scripts/resolve_reference.py \
  --reference-id REF-027 \
  --doi 10.xxxx/example \
  --title "Claimed title" \
  --author "A. Author" \
  --year 2024 \
  --email researcher@example.org \
  --use-openalex \
  --output REF-027.resolution.json
```

Record-first:

```bash
python skills/geotech-reference-verifier/scripts/resolve_reference.py \
  --record reference-record.json \
  --email researcher@example.org
```

Offline deterministic regression test:

```bash
python skills/geotech-reference-verifier/scripts/resolve_reference.py \
  --record tests/fixtures/citation/resolver-original.json \
  --offline-candidates tests/fixtures/citation/resolver-good-candidates.json
```

## Interpretation gate

The resolver identifies works. It does **not** determine whether the work supports a manuscript claim. Pass verified sources to `geotech-citation-fidelity` for claim-level support auditing.
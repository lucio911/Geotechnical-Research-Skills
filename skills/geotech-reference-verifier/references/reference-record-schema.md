# Reference Verification Record

Recommended JSON fields:

```json
{
  "reference_id": "SRC-023",
  "original": {"title": "...", "authors": ["..."], "year": 2024, "doi": "..."},
  "resolved": {"title": "...", "authors": ["..."], "year": 2024, "doi": "...", "source": "crossref"},
  "checks": {
    "identifier_resolves": true,
    "identity_match": true,
    "title_match": "exact",
    "author_match": "compatible",
    "year_match": true,
    "venue_match": true
  },
  "publication_status": "version_of_record",
  "verdict": "VERIFIED",
  "confidence": "high",
  "human_review": false
}
```

Preserve the original record so every correction is auditable.

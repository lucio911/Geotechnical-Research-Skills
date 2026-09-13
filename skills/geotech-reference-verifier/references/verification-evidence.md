# Verification Evidence

A reference identity decision should record which evidence established identity.

Strong evidence:
- DOI landing page with matching title/authors;
- publisher metadata;
- Crossref/DataCite record consistent with publisher;
- discipline authority such as PubMed/arXiv/standards body for its native identifiers.

Supporting evidence:
- OpenAlex;
- Semantic Scholar;
- institutional repository;
- library catalogue.

Weak evidence:
- search snippets;
- secondary bibliography pages;
- AI-generated summaries.

When sources disagree, do not majority-vote blindly. Prefer the source responsible for the record type and note version differences (online-first vs issue publication, conference vs journal extension, translated title, article number vs pages).

## Online resolver evidence

When `resolve_reference.py` is used, retain:

- every metadata service attempted;
- the request URL with API keys redacted;
- whether the service resolved, returned no record, or failed;
- normalized candidate metadata;
- title similarity, author overlap, year delta, DOI equality, and total identity score;
- candidate-margin evidence when multiple plausible records exist;
- any secondary retraction-status source.

A network/API failure is an evidence gap, not evidence of fabrication. A DOI resolution is evidence that the identifier exists, but not by itself that the DOI belongs to the work claimed in the manuscript.
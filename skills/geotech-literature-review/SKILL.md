---
name: geotech-literature-review
description: Design and execute evidence-oriented literature reviews for geotechnical engineering by tracing mechanisms, boundary conditions, study types, contradictions, and source roles rather than summarizing papers sequentially. Use for state-of-the-art reviews, novelty checks, manuscript evidence gathering, mechanism synthesis, or building a reproducible literature matrix.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Literature Review

Treat literature review as evidence mapping, not paper accumulation.

## 1. Establish the review contract

Before searching, record:

- research question or manuscript decision that the review must support;
- engineering object and material;
- target phenomenon or mechanism;
- relevant state variables and boundary conditions;
- study types that can answer the question;
- date/language/database constraints if supplied;
- what would count as sufficient evidence for saturation.

If the question is broad, decompose it into 2–6 answerable evidence questions.

## 2. Build a geotechnical concept map

Search terms should span more than the engineering object. Expand along:

- material: sand, clay, calcareous sand, soft rock, weathered rock, etc.;
- state: density, OCR, saturation, stress level, fabric, cementation, breakage state;
- loading: monotonic, cyclic, seismic, surcharge, excavation, unloading, stress rotation;
- drainage and hydraulic condition;
- geometry and scale;
- interface/contact condition;
- response variable;
- failure or degradation mechanism;
- analytical, experimental, numerical, field, or probabilistic method.

Use `references/search-protocol.md` to construct staged searches.

## 3. Search in layers

Run the review as a search ladder:

1. **Seed discovery** — identify seminal papers, recent authoritative reviews, and terminology.
2. **Mechanism search** — search the physical process directly, not only the engineering object.
3. **Method search** — find benchmark methods, constitutive assumptions, or test protocols.
4. **Boundary search** — target stress level, drainage, density, scale, interface, or loading path.
5. **Contradiction search** — actively search for studies reporting the opposite trend or mechanism.
6. **Citation chasing** — backward and forward trace the papers that carry critical claims.
7. **Recency check** — identify whether newer studies materially change the synthesis.

Do not equate the first relevant search results with the state of the art.

## 4. Assign every source a role

A source may serve one or more explicit roles:

- background/context;
- foundational theory;
- method precedent;
- benchmark dataset;
- direct support for a mechanism;
- direct support for a trend;
- contradictory evidence;
- scope/boundary evidence;
- standard/guideline requirement;
- novelty comparator.

Do not cite a paper merely because it is topically adjacent. See `references/source-role-taxonomy.md`.

## 5. Extract comparable evidence

Important papers should be processed with `geotech-paper-reader` and entered into a literature evidence matrix.

At minimum capture:

- source ID and bibliographic identity;
- study type;
- material and state;
- stress path and stress level;
- drainage/hydraulic condition;
- geometry and scale;
- loading history;
- constitutive/model assumptions where applicable;
- measured or predicted response;
- mechanism proposed by the authors;
- validation type;
- limits acknowledged by the authors;
- relevance to the current claim;
- extraction confidence.

Use `references/literature-evidence-matrix.md`.

## 6. Synthesize by scientific issue

Never make the main synthesis a paper-by-paper chronology unless the user explicitly requests historical development.

Prefer synthesis blocks such as:

- consensus across materially comparable studies;
- disagreement caused by different stress paths or material states;
- apparent contradiction explained by scale, drainage, density, or measurement definition;
- mechanism supported only indirectly;
- evidence concentrated in one material class but generalized to another;
- numerical consensus without experimental validation;
- repeated parameter sweeps without a resolved mechanism.

Use `references/contradiction-synthesis.md` when studies disagree.

## 7. Distinguish five kinds of gap

Label the gap explicitly:

1. **phenomenon gap** — an important response has not been characterized;
2. **mechanism gap** — the response is known but the governing mechanism is unresolved;
3. **method gap** — existing methods cannot measure, predict, or distinguish the process adequately;
4. **evidence gap** — a claim rests on weak, indirect, or single-method evidence;
5. **transferability gap** — findings have not been tested across relevant material/state/loading boundaries.

A missing parameter combination alone is not automatically a scientific gap.

## 8. Stop on evidence saturation, not arbitrary paper count

The review is approaching saturation when:

- new searches mostly return already-known mechanisms and comparators;
- each central claim has at least one directly relevant source or is explicitly marked unresolved;
- major contradictory evidence has been located and explained or preserved as disagreement;
- nearest novelty comparators are identified;
- remaining sources add detail but do not alter the evidence map.

Do not claim exhaustive coverage unless the protocol actually supports that claim.

## 9. Citation integrity

Never invent author, title, year, DOI, journal, volume, pages, or standard clauses.

When exact citation support matters:

- verify source identity;
- verify that the relevant content was actually inspected;
- distinguish what authors report from your inference;
- do not cite review articles as if they were the primary experimental source when the primary source is needed;
- distinguish standards from research literature.

## 10. Output schema

Return, as appropriate:

### A. Review contract
Question, scope, mechanisms, boundary conditions, and inclusion logic.

### B. Search map
Concept families and staged search strategy.

### C. Evidence matrix
Comparable source records rather than prose-only notes.

### D. Mechanism synthesis
Consensus, contradictions, boundary-dependent findings, and evidence strength.

### E. Gap map
Established knowledge / unresolved mechanism / weak evidence / transferability limits.

### F. Novelty comparators
The closest 3–10 studies that could invalidate the claimed novelty.

### G. Manuscript-ready evidence roles
Which sources support Introduction context, gap, Methods precedent, Discussion mechanism, limitations, or comparison.

## Failure modes to reject

- long annotated bibliography with no synthesis;
- claiming a gap because an exact keyword combination was not found;
- ignoring contradictory results;
- mixing different soil states or loading paths as if directly comparable;
- using topic similarity as evidence support;
- presenting database hit count as scientific evidence;
- treating numerical studies and experiments as interchangeable validation.

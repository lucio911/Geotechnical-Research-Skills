---
name: geotech-evidence-ledger
description: Build, maintain, and audit a typed evidence graph for geotechnical research, linking questions, gaps, methods, datasets, results, literature, mechanisms, claims, figures, sections, and conclusions with explicit provenance, evidence strength, assumptions, contradictions, and scope boundaries. Use for manuscripts, thesis chapters, revisions, or any project where claims must remain traceable to evidence.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Evidence Ledger

The ledger is the project's scientific provenance layer.

Its primary object in v0.4 is a **typed Evidence Graph**, not a flat list of notes.

## 1. Principle

Every consequential scientific claim should be traceable through:

`claim -> evidence -> source/method -> conditions -> assumptions -> boundary`

When a claim depends on a mechanism:

`claim -> mechanism interpretation -> discriminating evidence -> alternatives`

When a conclusion appears in the manuscript:

`conclusion -> claim -> evidence`

No unsupported shortcut is allowed.

## 2. Stable node IDs

Use stable IDs so that figures, paragraphs, and conclusions can change without losing provenance.

Recommended prefixes:

- `RQ-###` — research question;
- `GAP-###` — knowledge/evidence/mechanism gap;
- `HYP-###` — hypothesis;
- `MTH-###` — method, test, numerical model, derivation, or analysis procedure;
- `DAT-###` — dataset/raw data/model output source;
- `RES-###` — quantified result or observation;
- `SRC-###` — external literature, standard, or authoritative source;
- `MEC-###` — mechanistic interpretation;
- `CLM-###` — scientific claim;
- `BND-###` — applicability boundary/limitation;
- `FIG-###` — figure/table evidence surface;
- `SEC-###` — manuscript section/paragraph location;
- `CON-###` — conclusion statement;
- `DEC-###` — important research decision.

Do not recycle IDs when an object is deleted. Mark it retired.

## 3. Typed edges

Use explicit relations rather than vague links:

- `addresses` — method/question relationship;
- `tests` — evidence tests hypothesis/claim;
- `produces` — method produces dataset/result;
- `yields` — upstream data/result yields a downstream quantified result;
- `supports` — evidence/source supports a claim;
- `contradicts` — evidence/source conflicts with a claim;
- `consistent_with` — evidence is compatible with a mechanism but does not establish it;
- `discriminates` — evidence distinguishes competing mechanisms;
- `explains` — mechanism explains a bounded claim, with adequate evidence;
- `bounds` — boundary limits a claim;
- `visualized_by` — result is represented by a figure/table;
- `reported_in` — claim/figure appears in a manuscript section;
- `concludes` — conclusion restates a supported claim;
- `cites` — manuscript object cites external source;
- `depends_on` — downstream claim logically depends on another object.

See `references/evidence-graph-schema.md`.

## 4. Separate evidence from interpretation

Do not store the sentence "particle breakage governs stiffness degradation" as a raw result.

Prefer:

- `RES-014`: breakage rate increases with confining pressure;
- `RES-015`: residual stiffness decreases with confining pressure;
- `MEC-003`: particle breakage may contribute to contact-network/interface degradation;
- `CLM-007`: under tested conditions, increased breakage is associated with stronger stiffness degradation.

A stronger causal claim requires discriminating evidence.

## 5. Evidence strength

For every `supports`, `discriminates`, or `explains` edge record an evidence grade where possible:

- `E0` — assertion/visual impression only;
- `E1` — descriptive observation;
- `E2` — quantified single-source trend;
- `E3` — repeated or independently corroborated trend;
- `E4` — mechanism-discriminating evidence or independent validation;
- `E5` — convergent multi-method/field evidence supporting broader inference.

Evidence grade is not a universal truth score; it expresses support relative to the specific claim.

## 6. Boundary records are first-class objects

Geotechnical claims are conditional on state and loading.

A `BND` node may define:

- material/mineralogy;
- density/void ratio/OCR;
- saturation/drainage;
- effective confining stress;
- stress path;
- loading amplitude/frequency/cycles;
- scale and geometry;
- interface roughness;
- groundwater condition;
- constitutive assumptions;
- numerical domain/idealization;
- data range used for calibration.

Claims without boundaries should be treated cautiously when generalized.

## 7. Literature sources must have a role

For every `SRC` linked to a claim, record whether it is:

- direct evidence;
- mechanism precedent;
- method precedent;
- benchmark;
- contradictory evidence;
- boundary evidence;
- standard/guideline;
- novelty comparator.

A citation on the same topic is not automatically supporting evidence.

## 8. Figure and manuscript provenance

A figure should point back to the results it visualizes:

`DAT -> RES -> FIG`

A paragraph should point to the claims it makes:

`CLM -> SEC`

A conclusion should never terminate without upstream support:

`RES/SRC -> CLM -> CON`

This structure allows manuscript auditing after figures or wording change.

## 9. Integrity checks

Run an audit for:

### Blocking
- conclusion without a claim;
- claim without supporting evidence;
- result without provenance to data/method/source;
- figure supporting a claim but linked to no result/source;
- claim dependent only on another unsupported claim;
- fabricated/unverified external source identity;
- contradiction ignored while claim is stated as settled.

### Major
- causal/mechanistic wording supported only by association;
- no boundary recorded for a broad engineering recommendation;
- numerical result presented as experimental/field evidence;
- calibration dataset used as the only validation evidence;
- manuscript conclusion stronger than the corresponding claim card.

### Moderate
- evidence exists but source location is imprecise;
- duplicate claims use inconsistent terminology;
- figure has no unique argument role;
- literature role is unspecified.

## 10. Graph operations

The skill may create or maintain a graph file using the template in `assets/evidence-graph.example.json`.

Available deterministic helpers:

```bash
python skills/geotech-evidence-ledger/scripts/validate_evidence_graph.py path/to/evidence-graph.json
python skills/geotech-evidence-ledger/scripts/trace_claim.py path/to/evidence-graph.json CLM-001
python skills/geotech-evidence-ledger/scripts/render_mermaid.py path/to/evidence-graph.json > evidence-graph.md
```

Scripts validate structure and traceability only. They do not decide whether the scientific interpretation is physically correct.

## 11. Output schema

For chat or manuscript audit return:

### A. Critical claim inventory
ID, wording, type, strength, section.

### B. Evidence trace
For each critical claim: direct evidence -> method/source -> conditions -> corroboration -> alternatives -> boundary.

### C. Broken links
Unsupported claims, orphan figures, unproven mechanisms, missing data provenance, unsupported conclusions.

### D. Contradictions
Evidence that conflicts with central claims and whether it is resolved.

### E. Repair action
Minimum additional analysis, literature evidence, wording downgrade, boundary statement, or deletion needed.

## Failure modes to reject

- storing only prose notes with no stable IDs;
- treating a figure as the original evidence source when underlying data exist;
- using citations as decoration;
- allowing claim wording to strengthen across manuscript sections without new evidence;
- deleting contradictory evidence from the graph;
- representing a speculative mechanism as a measured result;
- interpreting graph connectivity as proof of scientific truth.

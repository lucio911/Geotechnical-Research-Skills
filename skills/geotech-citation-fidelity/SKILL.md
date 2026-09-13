---
name: geotech-citation-fidelity
description: Audit whether a real cited source actually supports the exact manuscript claim at the citation location, distinguishing topical relevance, broad consistency, direct support, quantitative support, and mechanistic/causal support. Use when claims may overstate what references show or when checking AI-assisted literature-backed prose.
license: MIT
metadata:
  version: "0.5.0"
  domain: geotechnical-engineering
---

# Geotech Citation Fidelity

A real paper can still be a wrong citation.

## Unit of analysis: Citation Instance

Treat each in-text citation occurrence as a separate `CIT-###` object. The same `SRC-###` may be cited many times for different claims and therefore receive different fidelity grades.

## Fidelity ladder

Use `references/fidelity-ladder.md`:

- `F0` — not verified;
- `F1` — topical relevance only;
- `F2` — broadly consistent but not direct evidence;
- `F3` — direct support for the stated qualitative claim;
- `F4` — direct quantitative/result-level support;
- `F5` — strong mechanistic/causal support at the level claimed.

Never infer F5 from a related title, abstract-level association, or a single co-varying trend.

## Workflow

1. Isolate the exact manuscript proposition surrounding the citation.
2. Assign or reuse a stable `CLM-###` claim ID.
3. Identify the cited `SRC-###` and create a `CIT-###` citation-instance ID.
4. Inspect the strongest available source evidence: relevant passage, result, figure/table, abstract, or publisher record.
5. Write the source's actual proposition in neutral terms.
6. Compare **scope, population/material, stress state, drainage/loading path, method, response variable, direction, magnitude, mechanism, and boundary**.
7. Grade support F0–F5.
8. Classify mismatch using `references/mismatch-taxonomy.md`.
9. Recommend one of: keep; weaken claim; move citation; add stronger source; split claim; remove citation.
10. Record the citation instance in the Evidence Graph.

## Geotechnical caution

Do not allow literature on one condition to support another without an explicit transferability argument. Common mismatches include:

- silica sand cited for crushable calcareous sand;
- drained tests cited for undrained mechanism claims;
- monotonic evidence cited for cyclic degradation;
- laboratory element tests cited as direct field-scale proof;
- numerical predictions cited as experimental validation;
- observed particle breakage cited as proof that breakage *governs* stiffness degradation.

## Required output

Use `references/citation-instance-schema.md` and report:

- `CIT-###`, manuscript locator, `SRC-###`, `CLM-###`;
- exact manuscript proposition;
- source proposition and locator;
- fidelity grade F0–F5;
- mismatch type if any;
- recommended manuscript action;
- confidence and unresolved limitations.

Use `scripts/audit_citation_map.py` for deterministic structure checks.

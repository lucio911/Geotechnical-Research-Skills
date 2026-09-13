---
name: geotech-reference-format
description: Normalize citation metadata into a canonical representation and render/check journal reference style using CSL or an equivalent deterministic processor rather than guessing punctuation with an LLM. Use when converting BibTeX/RIS/CSL JSON/reference lists to a target journal style or auditing style compliance after metadata verification.
license: MIT
metadata:
  version: "0.5.0"
  domain: geotechnical-engineering
---

# Geotech Reference Format

Formatting comes **after** identity and metadata verification.

## Doctrine

`canonical metadata -> deterministic style processor -> rendered bibliography -> style audit`

Do not let formatting logic rewrite scientific identity fields.

## Preferred architecture

1. Resolve target journal or explicit citation style.
2. Select a trusted CSL style (official CSL repository, journal-provided style, or vetted local CSL).
3. Convert metadata to canonical CSL-JSON or other processor-native data.
4. Render with a CSL processor / bibliography engine.
5. Compare output against journal examples/rules.
6. Report metadata warnings separately from style warnings.

For Chinese/English mixed bibliographies, retain language metadata and use a CSL style that explicitly supports the intended localization behavior.

## Inputs

May accept:

- BibTeX / BibLaTeX;
- RIS;
- CSL JSON;
- EndNote/XML exports;
- plain reference lists after verification;
- journal name, ISSN, style name, or supplied CSL file.

## Never do

- do not invent missing volume/pages/DOI to make a reference look complete;
- do not alter author order because a style example looks different;
- do not use punctuation similarity as evidence that metadata are correct;
- do not conflate author truncation rules (`et al.`) with source author metadata;
- do not silently convert preprints into journal articles unless identity is verified.

Read `references/metadata-vs-style.md`, `references/csl-pipeline.md`, and `references/geotechnical-journal-checklist.md`.

Use `scripts/check_render_manifest.py` to validate the declared style/render provenance.

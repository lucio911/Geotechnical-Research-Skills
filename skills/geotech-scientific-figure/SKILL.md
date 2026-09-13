---
name: geotech-scientific-figure
description: Design, audit, and specify publication-quality scientific figures for geotechnical engineering, choosing panels and visual encodings to support a defined scientific claim. Use for experimental curves, FEM contours, parameter studies, mechanism schematics, multi-panel figures, captions, and journal figure consistency checks.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Scientific Figure

Design from the claim backward.

## Figure architecture

1. Define the single main scientific message.
2. Select the minimum evidence needed to establish it.
3. Assign panel roles: geometry/method, qualitative field, quantitative response, mechanism, validation, or sensitivity.
4. Choose axes/normalization/reference states that do not obscure the physics.
5. Use consistent symbols, units, line meanings, load stages, crack-depth labels, and coordinate directions across panels.
6. Write a caption that explains what is shown without duplicating the full Discussion.

See `references/figure-audit.md`.

## Numerical contour requirements

State variable/component, unit, scale range, deformation scale factor, load/step/frame, and whether contour ranges are identical across compared panels. If contours are compared visually, identical ranges are strongly preferred unless there is a documented reason otherwise.

## Quantitative plotting rules

Show uncertainty/repeatability when available. Avoid excessive smoothing. Preserve raw-data provenance. Do not use dual axes when they invite misleading visual comparison unless necessary and explicitly justified.

## Final audit

Check units, labels, notation, panel order, readability at target width, caption consistency, and whether every panel has a scientific role. Remove decorative panels that do not advance the evidence chain.

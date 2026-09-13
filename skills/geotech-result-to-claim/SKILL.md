---
name: geotech-result-to-claim
description: Convert geotechnical experimental, field, numerical, or theoretical results into the strongest defensible scientific claims by separating observation, quantification, association, mechanism, causality, and engineering implication; grading evidence; testing competing explanations; and stating applicability boundaries. Use when interpreting figures, contours, hysteresis curves, parameter studies, thresholds, failure patterns, model outputs, Results/Discussion sections, or Conclusions.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Result to Claim

The task is not to make the result sound important. The task is to find the **maximum defensible claim strength**.

## Step 1 — Identify the evidence class

Tag the source as:

- field observation;
- controlled experiment;
- numerical prediction;
- analytical/theoretical result;
- derived metric;
- literature synthesis.

Never silently convert a numerical prediction into an observed physical fact.

## Step 2 — Write the zero-interpretation observation

Describe only what the evidence directly contains.

Examples:

- crown `U2` becomes more negative with surcharge;
- ovalization increases after a specified load stage;
- hysteresis-loop area changes between cycles;
- a localized plastic-strain band appears in a model output.

No mechanism words yet.

## Step 3 — Quantify before explaining

Where data permit, extract:

- absolute change;
- relative change;
- slope/rate;
- normalized response;
- threshold/change point;
- uncertainty/dispersion;
- repeatability;
- effect size;
- sensitivity to model/test choices.

If only visual evidence exists, explicitly say the conclusion is qualitative.

## Step 4 — Build a response chain

Link independent observables where possible:

`loading/state change -> local response -> global response -> damage/failure metric`

Example:

`surcharge -> crack opening/local stiffness loss -> crown displacement + springline movement -> ovalization -> crack propagation`

A mechanistic claim becomes stronger when the links are independently quantified rather than inferred from one contour.

## Step 5 — Propose mechanics with competing explanations

For each mechanism candidate:

1. state the mechanics;
2. list evidence it predicts;
3. check whether those observations occur;
4. list at least one credible competing explanation;
5. identify an observation that would discriminate between them.

Use `references/mechanism-vs-association.md`.

## Step 6 — Grade evidence strength

Assign each claim an evidence grade:

- **E0**: visual/anecdotal description only;
- **E1**: single quantified response;
- **E2**: replicated or sensitivity-checked quantitative response;
- **E3**: triangulated independent responses consistent with one mechanism;
- **E4**: discriminating evidence against credible alternatives and/or independent validation;
- **E5**: replicated/generalized evidence across materially different conditions.

Evidence grade is not journal quality; it controls wording strength.

See `references/evidence-strength.md`.

## Step 7 — Choose claim level

Use the Claim Ladder:

- **C1 Description** — what changed;
- **C2 Quantified trend** — how much/how fast/when;
- **C3 Association** — responses co-vary;
- **C4 Mechanistic consistency** — pattern is consistent with a mechanism;
- **C5 Mechanistic/causal claim** — mechanism is supported against alternatives;
- **C6 Generalization/engineering implication** — response is transferable enough to guide prediction/design/decision.

Do not jump levels because the wording sounds more publishable.

Use `references/claim-ladder.md`.

## Step 8 — State the applicability boundary

Every strong claim should define relevant bounds, such as material/mineralogy/structure, density/state/OCR, stress range, drainage/saturation, cyclic amplitude/frequency/cycle range, geometry/scale, crack orientation/depth, constitutive/model assumptions, or field versus laboratory context.

Prefer "under the investigated conditions" only when those conditions have been stated concretely nearby.

## Step 9 — Perform the sentence stress test

For every Results/Discussion/Conclusion sentence ask:

- Which evidence ID supports this?
- Is the number traceable?
- Is mechanism wording stronger than evidence grade?
- Could an alternative explanation remain?
- Is the scope broader than the tested range?
- Is a model prediction being described as reality?

If yes, rewrite weaker or request additional evidence.

## Special rule — contour plots

Contours can support spatial pattern/localization claims. They do not by themselves establish percentage change, onset load, failure threshold, causal mechanism, or global structural performance.

Use `references/contour-plot-audit.md`.

## Output — Claim Card

Return Claim ID, Evidence class, Direct observation, Quantification, Corroborating evidence, Mechanism candidate, Competing explanation, Evidence grade E0–E5, Claim level C1–C6, Strongest defensible sentence, Sentence that would be overclaiming, Applicability boundary, and Missing evidence needed to raise the claim one level.

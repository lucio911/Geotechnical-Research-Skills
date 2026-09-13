---
name: geotech-gap-novelty
description: Test geotechnical research gaps and novelty claims by separating parameter novelty from phenomenon, mechanism, method, evidence, and engineering-capability novelty, and by checking saturation, nearest prior art, scope boundaries, and falsifiable contribution. Use when defining a PhD topic, writing an Introduction, evaluating a proposed paper, responding to novelty criticism, or deciding whether a study is publication-worthy.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Gap & Novelty

Novelty is not "this exact parameter combination has not been studied."

The task is to determine **what existing knowledge cannot currently explain, predict, measure, or decide**, and whether the proposed study resolves that deficit.

## Step 1 — Write the proposed contribution without promotional language

Reduce the study to:

`object + condition/path + unresolved response/mechanism + method/evidence + intended advance`

If the contribution disappears after removing adjectives such as *novel*, *systematic*, *comprehensive*, *first*, *intelligent*, or *multi-factor*, the novelty is not yet articulated.

## Step 2 — Find the nearest prior art

Do not compare only with broad reviews. Identify the 3–10 closest studies by:

- same phenomenon/mechanism;
- same material state;
- same loading/stress path;
- same engineering object;
- same measurement/model capability;
- same claimed outcome.

Use `geotech-paper-reader` for auditable extraction.

## Step 3 — Build a Gap Map

Classify what is already known:

- established;
- repeatedly observed but poorly explained;
- mechanistically disputed;
- method-limited;
- evidence-limited;
- condition-specific;
- genuinely untested.

A gap should be expressed as a missing **scientific capability**, not merely a missing case.

Weak:
> Few studies considered crack depth under 160 kPa surcharge.

Stronger:
> Existing studies describe crack-induced deformation, but do not resolve how initial crack depth changes the transition from local stiffness loss to global ovalization under progressive surcharge, because deformation-field and crack-propagation evidence have not been jointly quantified.

## Step 4 — Classify novelty

Evaluate six dimensions:

1. **Phenomenon novelty** — newly identified response/regime/threshold.
2. **Mechanism novelty** — new causal/mechanistic explanation with discriminating evidence.
3. **Method novelty** — materially new measurement, derivation, algorithm, experimental design, or analysis capability.
4. **Evidence novelty** — substantially stronger, multi-scale, independent, field, or previously unavailable evidence.
5. **Model/predictive novelty** — improved explanatory/predictive capability with independent validation.
6. **Engineering-capability novelty** — enables a decision, prediction, monitoring, or design action previously not feasible/reliable.

Parameter novelty alone is normally weak unless it reveals a new regime, mechanism, scaling law, or design consequence.

## Step 5 — Run the Saturation Test

Ask whether the paper would still be scientifically interesting if the new soil type, load level, software, geometry, or location label were replaced with a generic placeholder.

If not, the contribution may be application-specific rather than scientifically novel.

Use `references/saturation-test.md`.

## Step 6 — Run the mechanism discrimination test

If the contribution is mechanistic, identify at least one plausible competing mechanism and ask what observation would distinguish them.

If no discriminating evidence exists, describe the result as *consistent with* a mechanism, not as proof that the mechanism governs.

## Step 7 — Test falsifiability

A defensible novelty statement should imply an observation that could prove it wrong.

Examples:

- a predicted transition/threshold is absent;
- a proposed state variable does not collapse data;
- the model fails independent conditions;
- the claimed mechanism does not align with an independent response variable.

## Step 8 — Grade the novelty

Use:

- **N0 — cosmetic**: wording/application change only;
- **N1 — incremental parameter extension**;
- **N2 — useful empirical/evidence extension**;
- **N3 — new mechanism/method/predictive capability with convincing support**;
- **N4 — field-shaping conceptual or methodological advance**.

Do not inflate the grade to match a target journal.

## Output

Return:

1. nearest-prior-art summary;
2. Gap Map;
3. novelty dimensions with evidence;
4. saturation-test result;
5. strongest defensible novelty statement;
6. strongest likely reviewer objection;
7. minimum additional evidence needed to raise novelty by one grade.

Use `references/novelty-framework.md` and `references/novelty-claims.md`.

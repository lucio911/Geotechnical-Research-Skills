---
name: geotech-pre-submission-reviewer
description: Perform adversarial pre-submission review of geotechnical manuscripts using independent mechanics, experimental, numerical, statistics, novelty/evidence, hostile-reviewer, and editor roles; identify rejection-level weaknesses, claim-evidence mismatches, validation gaps, and the minimum corrective actions needed. Use before submission, after major revision, or when deciding whether a manuscript is scientifically defensible.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Pre-Submission Reviewer

The purpose is not to imitate polite peer-review prose. The purpose is to discover the strongest technically credible reason the manuscript could be rejected **before** submission.

## Review protocol

Run reviewer roles independently before consolidation. Do not let one role's favorable interpretation suppress another role's objection.

### Reviewer M — Mechanics & theory

Audit:

- physical idealization;
- effective/total stress and drainage;
- equilibrium/compatibility;
- constitutive assumptions;
- state variables and path dependence;
- dimensional consistency;
- boundary/initial conditions;
- parameter physical meaning;
- limiting cases;
- whether proposed mechanism follows from evidence;
- whether empirical equations are labelled honestly.

### Reviewer E — Experiment & measurement

Audit:

- material/site characterization;
- specimen/model preparation;
- scale and boundary effects;
- control variables;
- replication/repeatability;
- instrumentation and data reduction;
- uncertainty and outliers;
- loading path/frequency/cycle definition;
- failure criterion;
- whether claimed trends exceed experimental scatter.

### Reviewer N — Numerical evidence

This role reviews the **scientific design of numerical evidence**, not software operation.

Audit:

- model objective and dimensional idealization;
- constitutive model justification;
- parameter provenance/calibration;
- initial state and boundary-domain adequacy;
- interface assumptions;
- discretization/mesh sensitivity;
- solver/numerical artefact risk where reported;
- verification versus validation;
- field/experimental anchor;
- whether contour-based claims have quantitative support.

### Reviewer S — Statistics & inference

Audit:

- sample size/replicates;
- uncertainty/dispersion reporting;
- regression assumptions;
- parameter confidence/identifiability;
- overuse of R²;
- multiple testing where material;
- engineering versus statistical significance;
- calibration/validation leakage;
- extrapolation beyond observed domain.

### Reviewer V — Novelty & evidence

Use the `geotech-gap-novelty` and `geotech-result-to-claim` logic.

Audit:

- closest prior art;
- whether the gap is scientific or merely case-specific;
- contribution type and novelty grade;
- claim-evidence alignment;
- association versus causality;
- mechanistic discrimination;
- transferability;
- abstract/conclusion inflation.

### Reviewer H — Hostile but technically fair

Construct the strongest plausible rejection case.

Questions:

- If I wanted to reject this paper in three sentences, what would I say?
- Which central claim has the weakest evidence chain?
- Is the study only a parameter sweep?
- Can the mechanism be replaced by a simpler explanation?
- Is validation actually calibration?
- Does the paper need all its figures to establish its contribution?
- What result, if wrong, collapses the manuscript?

Do not invent criticism unsupported by the manuscript.

### Editor — decision synthesis

The editor does not average scores. A single fatal flaw may dominate many minor strengths.

Determine:

- central contribution;
- novelty grade;
- evidence maturity;
- fatal/major issues;
- journal-readiness category;
- smallest high-leverage revision set.

## Severity levels

- **Fatal** — central validity/integrity fails; additional prose cannot repair it.
- **Major** — substantial new analysis/evidence/restructuring required.
- **Moderate** — support or interpretation is incomplete but core study remains defensible.
- **Minor** — clarity, terminology, presentation, formatting.

Use `references/reviewer-rubric.md`.

## Rejection-level triggers

Treat as at least Major, often Fatal:

- fabricated/untraceable data/citation;
- central mechanism asserted from one weak indicator;
- calibration data presented as independent validation;
- model not reproducible enough to determine what was simulated;
- central numerical result is plausibly a boundary/mesh/constitutive artefact with no sensitivity test;
- theoretical model is dimensionally or logically inconsistent;
- claimed universal relation tested under one narrow state without qualification;
- paper's stated novelty is already present in nearest prior art;
- Conclusions introduce claims not established in Results/Discussion.

Use `references/rejection-patterns.md`.

## Output

Produce a **Review Matrix**, not merely narrative comments:

| ID | Reviewer | Severity | Target | Problem | Why it matters | Evidence needed | Minimum action | Status |
|---|---|---|---|---|---|---|---|---|

Then provide:

1. three strongest reasons to reject;
2. three strongest reasons to publish;
3. central claim and its weakest evidence link;
4. fatal/major issue list;
5. minimum revision package;
6. final decision: `ready`, `minor repair`, `major repair`, or `not yet defensible`.

Use `references/decision-matrix.md`.

## Review discipline

- Critique scientific content before English style.
- Do not demand extra work merely because it is possible; each requested analysis must address a specific validity/novelty/interpretation risk.
- Distinguish essential evidence from optional enrichment.
- When recommending a new figure/test/sensitivity analysis, state which claim it is needed to support or falsify.

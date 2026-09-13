---
name: geotech-paper-spine
description: Build, repair, and audit the central scientific argument of a geotechnical engineering manuscript by mapping research question, gap, hypothesis, evidence, mechanism, figures, sections, claims, boundaries, and conclusions into one dependency structure. Use when a paper feels fragmented, figure-heavy, novelty-poor, or internally inconsistent.
license: MIT
metadata:
  version: "0.4.0"
  domain: geotechnical-engineering
---

# Geotech Paper Spine

A manuscript is a scientific argument, not a chronological record of everything that was done.

## 1. Define the central proposition

Write one sentence for each item:

1. **Problem** — what engineering/scientific difficulty matters?
2. **Gap** — what cannot currently be explained, predicted, measured, or transferred reliably?
3. **Question/Hypothesis** — what proposition is the study designed to test?
4. **Method logic** — why can the chosen experiment/model/derivation resolve that question?
5. **Primary evidence** — which result is indispensable?
6. **Mechanism** — what physical interpretation best explains the evidence?
7. **Contribution** — what new capability or understanding is gained?
8. **Boundary** — under what material/state/loading/scale conditions is the contribution valid?

If these eight statements do not form a coherent chain, do not begin section-level polishing.

## 2. Create a claim hierarchy

Classify manuscript claims into:

- `MC` — one main claim carrying the paper;
- `SC` — supporting claims required to establish the main claim;
- `BC` — boundary/limitation claims defining where the main claim stops;
- `EC` — engineering consequence or applicability claim.

A typical paper should have one main claim, a small number of supporting claims, and explicit boundaries.

Use `references/argument-graph.md`.

## 3. Build the argument dependency graph

Map dependencies explicitly:

`gap -> question -> test -> evidence -> supporting claim -> mechanism -> main claim -> implication`

For each claim ask:

- What evidence is necessary?
- What evidence is merely illustrative?
- What assumption must hold?
- What competing explanation threatens the claim?
- Which later claim depends on it?

A downstream claim cannot be stronger than its weakest upstream dependency.

## 4. Assign every figure a scientific role

Every main-text figure must do at least one of the following:

- establish experimental/model validity;
- quantify the primary phenomenon;
- isolate a controlling variable;
- discriminate between competing mechanisms;
- establish a boundary or transition;
- validate a theoretical relationship;
- synthesize the final mechanism or framework.

Figures that merely repeat another trend, decorate the paper, or show unquantified contours should be moved, combined, or removed.

Use `references/figure-role-map.md`.

## 5. Allocate evidence budget

The most important claim should receive the strongest and most independent evidence.

For each claim record:

- direct quantitative evidence;
- corroborating evidence;
- validation/verification evidence;
- literature comparator;
- competing explanation;
- boundary test.

If the main claim has less evidence than a minor side result, the paper is structurally misallocated.

## 6. Map sections to argument functions

### Introduction
Must establish problem -> state of knowledge -> unresolved gap -> why the gap matters -> study question/contribution.

### Methods
Must explain how the design can resolve the question and what assumptions/boundaries govern interpretation.

### Results
Must establish evidence in the order required by the argument, not necessarily the order in which analyses were performed.

### Discussion
Must explain mechanism, comparison with prior work, alternatives, boundary conditions, and implications.

### Conclusions
Must compress only already-supported claims. No new mechanism, number, or recommendation may appear here.

Use `references/section-budget.md`.

## 7. Control Results–Discussion transitions

For each major result use the sequence:

`observation -> quantification -> comparison -> interpretation -> uncertainty/boundary`

Do not write a mechanistic paragraph when only descriptive evidence exists. Invoke `geotech-result-to-claim` if wording strength is uncertain.

## 8. Audit narrative redundancy

Flag:

- multiple figures answering the same question without added discrimination;
- repeated statements in Abstract, Results, Discussion, and Conclusions with increasing certainty but no new evidence;
- subsections defined only by parameter value rather than scientific question;
- Introduction promises not answered later;
- Discussion topics with no Results anchor;
- Conclusions with no evidence-ledger trace.

## 9. Run the deletion test

For each figure, table, subsection, and secondary analysis ask:

> If this item is removed, does the central scientific argument become weaker?

If no, choose one:

- delete;
- move to supplementary material;
- combine with a stronger item;
- redefine its role if it contains genuinely distinct evidence.

Do not retain content merely because producing it required effort.

## 10. Run manuscript consistency gates

Check alignment among:

- title;
- abstract objective;
- Introduction gap;
- Methods design;
- Results sequence;
- Discussion mechanism;
- figure captions;
- Conclusions;
- claimed engineering implications.

Use `references/manuscript-consistency.md`.

## Output schema

Return:

### A. One-sentence paper thesis
One bounded sentence containing phenomenon/mechanism/contribution.

### B. Spine table
Problem, gap, question, method, primary evidence, mechanism, contribution, boundary.

### C. Claim hierarchy
MC / SC / BC / EC with dependencies.

### D. Figure-role map
Figure -> scientific question -> evidence role -> claim IDs -> keep/combine/move/delete.

### E. Section architecture
Recommended section/subsection order and purpose.

### F. Broken links
Claims without evidence, figures without a role, sections without a claim, conclusions without provenance.

### G. Minimum repair plan
Smallest set of structural changes required to make the manuscript coherent.

## Failure modes to reject

- organizing Results only by test number or parameter value;
- keeping every generated figure;
- allowing the Abstract to claim more than Conclusions or vice versa;
- writing Discussion as a second Results section;
- presenting one correlation as the entire mechanism;
- calling application relevance a scientific contribution when no new capability is demonstrated.

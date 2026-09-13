# DeepSeek Harness compatibility

This repository is a research-focused **Agent Skills pack** for DeepSeek Harness (DSH) and other `SKILL.md`-compatible agent runtimes.

## Discovery keywords

Recommended GitHub repository topics for marketplace/discovery indexing:

- `dsh-skill`
- `deepseek-harness`
- `agent-skills`
- `geotechnical-engineering`
- `scientific-research`
- `research-agent`
- `citation-integrity`
- `academic-writing`

The first two are the most important for DSH-oriented discovery.

## Native skill layout

Each skill is stored as:

```text
skills/<skill-name>/SKILL.md
```

with YAML frontmatter containing at least:

```yaml
---
name: geotech-reference-verifier
description: Verify reference identity, metadata integrity, DOI/work consistency, and suspected fabricated or composite citations.
---
```

This matches the directory-bundle pattern used by DeepSeek Harness skill discovery.

## Using with DeepSeek Harness

Point a DSH custom skill directory at this repository's `skills/` directory, or copy/symlink selected skill directories into a DSH skill root. The skills are intentionally software-agnostic and do not depend on Abaqus/PLAXIS/FLAC3D GUI automation.

The most distinctive entry points for marketplace users are:

- `geotech-reference-verifier` — DOI/work identity, fabricated/composite reference screening, retraction/status checks;
- `geotech-citation-fidelity` — whether a real paper supports the exact manuscript claim;
- `geotech-bibliography-audit` — BibTeX/manuscript consistency and duplicate detection;
- `geotech-experiment-design` — hypothesis-driven geotechnical experiment design;
- `geotech-statistics` — repeated measures, uncertainty, effect size, engineering significance;
- `geotech-parameter-calibration` — identifiability, calibration/validation separation, model comparison;
- `geotech-evidence-ledger` — typed evidence graph and claim provenance;
- `geotech-pre-submission-reviewer` — adversarial research and manuscript audit.

## Marketplace positioning

Suggested category labels:

```text
Research
Science
Engineering
Geotechnical Engineering
Academic Writing
Citation Integrity
Literature Review
Data Analysis
Statistics
Experiment Design
Research Integrity
```

Suggested short marketplace description:

> Research-grade Agent Skills for geotechnical engineering: literature and novelty review, experiment design, data QC, statistics, calibration, evidence graphs, citation integrity, scientific claims, figures, manuscript architecture, and pre-submission review.

## Repository metadata

`registry.yaml` contains per-skill tags intended to help human and automated cataloguers classify the suite. DeepSeek Harness runtime selection should still rely primarily on each skill's `name` and `description`; tags are discovery metadata rather than a substitute for good skill descriptions.

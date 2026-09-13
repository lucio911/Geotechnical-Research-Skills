#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_RE = re.compile(r"`(references/[A-Za-z0-9._/-]+\.md)`")
EXCLUDED_SKILLS = {"abaqus-geotech"}
VERSION = "0.5.0"


def frontmatter(text: str):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    block = text[4:end]
    out = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def has_skill_trigger(text: str, skill: str) -> bool:
    return bool(
        re.search(rf"(?m)^\s*skill:\s*{re.escape(skill)}\s*$", text)
        or re.search(rf"(?m)^\s{{2}}{re.escape(skill)}:\s*$", text)
    )


def run_test(path: Path):
    return subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def main():
    errors, warnings = [], []
    count = 0
    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())

    for d in skill_dirs:
        count += 1
        if d.name in EXCLUDED_SKILLS:
            errors.append(f"{d.name}: solver-control skill is excluded from Research-Core")

        f = d / "SKILL.md"
        if not f.exists():
            errors.append(f"{d.name}: missing SKILL.md")
            continue
        text = f.read_text(encoding="utf-8")
        fm = frontmatter(text)
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if name != d.name:
            errors.append(f"{d.name}: frontmatter name {name!r} must equal directory")
        if not NAME_RE.fullmatch(name):
            errors.append(f"{d.name}: invalid name")
        if len(name) > 64:
            errors.append(f"{d.name}: name longer than 64 characters")
        if not desc:
            errors.append(f"{d.name}: missing description")
        elif len(desc) > 1024:
            errors.append(f"{d.name}: description longer than 1024 characters")
        if len(text.splitlines()) > 500:
            warnings.append(f"{d.name}: SKILL.md exceeds 500 lines")
        if len(text.split()) > 5000:
            warnings.append(f"{d.name}: SKILL.md exceeds ~5000 words; consider progressive disclosure")

        for rel in sorted(set(REF_RE.findall(text))):
            if not (d / rel).exists():
                errors.append(f"{d.name}: referenced file missing: {rel}")

        agent = d / "agents" / "openai.yaml"
        if not agent.exists():
            warnings.append(f"{d.name}: missing agents/openai.yaml (optional UI metadata)")
        else:
            agent_text = agent.read_text(encoding="utf-8")
            if f"${d.name}" not in agent_text:
                warnings.append(f"{d.name}: default prompt does not explicitly cite ${d.name}")

    registry_file = ROOT / "registry.yaml"
    if not registry_file.exists():
        errors.append("registry.yaml is required")
        registry = ""
    else:
        registry = registry_file.read_text(encoding="utf-8")
        if f'version: "{VERSION}"' not in registry:
            errors.append(f"registry.yaml: expected version {VERSION}")
    registered = set(re.findall(r"(?m)^\s*- name:\s*([a-z0-9-]+)\s*$", registry))
    actual = {d.name for d in skill_dirs}
    for skill in sorted(actual - registered):
        errors.append(f"registry.yaml: missing {skill}")
    for skill in sorted(registered - actual):
        errors.append(f"registry.yaml: stale entry {skill}")

    core_requirements = {
        "geotech-paper-reader": ["references/paper-card-template.md", "references/extraction-confidence.md", "references/comparison-matrix.md"],
        "geotech-gap-novelty": ["references/novelty-framework.md", "references/saturation-test.md", "references/novelty-claims.md"],
        "geotech-theory-derivation": ["references/derivation-audit.md", "references/state-variable-audit.md", "references/model-classification.md", "references/calibration-validation.md"],
        "geotech-result-to-claim": ["references/claim-ladder.md", "references/evidence-strength.md", "references/mechanism-vs-association.md", "references/contour-plot-audit.md"],
        "geotech-pre-submission-reviewer": ["references/reviewer-rubric.md", "references/rejection-patterns.md", "references/decision-matrix.md"],
        "geotech-literature-review": ["references/search-protocol.md", "references/source-role-taxonomy.md", "references/contradiction-synthesis.md", "references/literature-evidence-matrix.md"],
        "geotech-evidence-ledger": ["references/evidence-graph-schema.md", "references/graph-integrity-rules.md", "assets/evidence-graph.example.json", "assets/quantitative-evidence-graph.example.json", "scripts/validate_evidence_graph.py", "scripts/trace_claim.py", "scripts/render_mermaid.py"],
        "geotech-paper-spine": ["references/argument-graph.md", "references/figure-role-map.md", "references/section-budget.md", "references/manuscript-consistency.md"],
        "geotech-experiment-design": ["references/study-design-contract.md", "references/geotechnical-confounders.md", "references/similarity-scale-effects.md"],
        "geotech-data-qc": ["references/data-integrity.md", "references/sensor-qc.md", "references/cyclic-test-qc.md", "scripts/audit_csv.py"],
        "geotech-statistics": ["references/inference-ladder.md", "references/repeated-measures.md", "references/engineering-significance.md"],
        "geotech-parameter-calibration": ["references/identifiability.md", "references/calibration-validation.md", "references/residual-diagnostics.md", "references/model-comparison.md", "assets/calibration-manifest.example.json", "scripts/audit_calibration_manifest.py"],
        "geotech-unit-dimension-audit": ["references/dimension-rules.md", "references/geotech-unit-traps.md", "references/normalization.md", "assets/variable-register.example.json", "scripts/check_variable_register.py"],
    }

    citation_requirements = {
        "geotech-reference-verifier": [
            "references/reference-status-taxonomy.md", "references/reference-record-schema.md",
            "references/verification-evidence.md", "references/online-resolver.md",
            "references/batch-forensics.md", "assets/reference-record.example.json",
            "scripts/audit_reference_record.py", "scripts/resolve_reference.py",
            "scripts/audit_references.py",
        ],
        "geotech-citation-fidelity": ["references/fidelity-ladder.md", "references/mismatch-taxonomy.md", "references/citation-instance-schema.md", "assets/citation-map.example.json", "scripts/audit_citation_map.py"],
        "geotech-bibliography-audit": ["references/bibliography-integrity.md", "references/duplicate-resolution.md", "references/citation-key-rules.md", "scripts/audit_bib_consistency.py"],
        "geotech-reference-format": ["references/metadata-vs-style.md", "references/csl-pipeline.md", "references/geotechnical-journal-checklist.md", "assets/render-manifest.example.json", "scripts/check_render_manifest.py"],
    }

    for release_name, requirements in (("v0.4", core_requirements), ("v0.5", citation_requirements)):
        for skill, rels in requirements.items():
            if not (SKILLS / skill).is_dir():
                errors.append(f"{skill}: {release_name} required skill missing")
                continue
            for rel in rels:
                if not (SKILLS / skill / rel).exists():
                    errors.append(f"{skill}: {release_name} required file missing: {rel}")

    trigger_file = ROOT / "tests" / "trigger_cases.yaml"
    if not trigger_file.exists():
        errors.append("tests/trigger_cases.yaml is required")
    else:
        trigger_text = trigger_file.read_text(encoding="utf-8")
        for skill in core_requirements:
            if not has_skill_trigger(trigger_text, skill):
                errors.append(f"trigger_cases.yaml: missing trigger case for {skill}")

    citation_trigger_file = ROOT / "tests" / "citation_trigger_cases.yaml"
    if not citation_trigger_file.exists():
        errors.append("tests/citation_trigger_cases.yaml is required")
    else:
        citation_trigger_text = citation_trigger_file.read_text(encoding="utf-8")
        if f'version: "{VERSION}"' not in citation_trigger_text:
            errors.append(f"citation_trigger_cases.yaml: expected version {VERSION}")
        for skill in citation_requirements:
            if not has_skill_trigger(citation_trigger_text, skill):
                errors.append(f"citation_trigger_cases.yaml: missing trigger case for {skill}")

    required_files = [
        ROOT / "docs" / "citation-integrity-core.md",
        ROOT / "examples" / "citation-integrity-workflow.md",
        ROOT / "tests" / "test_citation_integrity.py",
        ROOT / "tests" / "test_reference_resolver.py",
        ROOT / "tests" / "test_batch_reference_forensics.py",
        ROOT / "tests" / "test_citation_review_fixes.py",
        ROOT / "tests" / "fixtures" / "reference-batch" / "references.bib",
        SKILLS / "geotech-evidence-ledger" / "assets" / "citation-evidence-graph.example.json",
    ]
    for p in required_files:
        if not p.exists():
            errors.append(f"v0.5 required file missing: {p.relative_to(ROOT)}")

    tests = [
        ROOT / "tests" / "test_evidence_graph.py",
        ROOT / "tests" / "test_quantitative_core.py",
        ROOT / "tests" / "test_citation_integrity.py",
        ROOT / "tests" / "test_reference_resolver.py",
        ROOT / "tests" / "test_batch_reference_forensics.py",
        ROOT / "tests" / "test_citation_review_fixes.py",
    ]
    for path in tests:
        if not path.exists():
            errors.append(f"missing smoke test: {path.relative_to(ROOT)}")
            continue
        proc = run_test(path)
        if proc.returncode != 0:
            errors.append(f"smoke test failed: {path.relative_to(ROOT)}\n{proc.stdout}\n{proc.stderr}")

    for w in warnings:
        print("WARNING:", w)
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print(f"Validated {count} skills (v{VERSION})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

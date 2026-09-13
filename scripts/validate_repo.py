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
VERSION = "0.4.0"


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


def main():
    errors, warnings = [], []
    count = 0

    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
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

    registry = (ROOT / "registry.yaml").read_text(encoding="utf-8")
    if 'version: "0.4.0"' not in registry:
        errors.append("registry.yaml: expected version 0.4.0")
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        if f"name: {d.name}" not in registry:
            errors.append(f"registry.yaml: missing {d.name}")

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
    for skill, rels in core_requirements.items():
        for rel in rels:
            if not (SKILLS / skill / rel).exists():
                errors.append(f"{skill}: v0.4 required file missing: {rel}")

    trigger_file = ROOT / "tests" / "trigger_cases.yaml"
    if not trigger_file.exists():
        errors.append("tests/trigger_cases.yaml is required")
    else:
        trigger_text = trigger_file.read_text(encoding="utf-8")
        focus = [
            "geotech-paper-reader", "geotech-gap-novelty", "geotech-theory-derivation",
            "geotech-result-to-claim", "geotech-pre-submission-reviewer",
            "geotech-literature-review", "geotech-evidence-ledger", "geotech-paper-spine",
            "geotech-experiment-design", "geotech-data-qc", "geotech-statistics",
            "geotech-parameter-calibration", "geotech-unit-dimension-audit",
        ]
        for skill in focus:
            if f"skill: {skill}" not in trigger_text:
                errors.append(f"trigger_cases.yaml: missing trigger case for {skill}")

    # Execute lightweight deterministic smoke tests.
    tests = [
        [sys.executable, str(ROOT / "tests" / "test_evidence_graph.py")],
        [sys.executable, str(ROOT / "tests" / "test_quantitative_core.py")],
    ]
    for cmd in tests:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if proc.returncode != 0:
            errors.append(f"smoke test failed: {' '.join(cmd)}\n{proc.stdout}\n{proc.stderr}")

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

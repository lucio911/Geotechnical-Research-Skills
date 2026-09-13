#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: Path, *args: Path):
    return subprocess.run(
        [sys.executable, str(script), *map(str, args)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def require(condition: bool, message: str, proc=None):
    if condition:
        return
    print("FAIL:", message)
    if proc is not None:
        print(proc.stdout)
        print(proc.stderr)
    raise SystemExit(1)


def main():
    ref_audit = ROOT / "skills/geotech-reference-verifier/scripts/audit_reference_record.py"
    bib_audit = ROOT / "skills/geotech-bibliography-audit/scripts/audit_bib_consistency.py"
    graph_audit = ROOT / "skills/geotech-evidence-ledger/scripts/validate_evidence_graph.py"
    citation_audit = ROOT / "skills/geotech-citation-fidelity/scripts/audit_citation_map.py"
    render_audit = ROOT / "skills/geotech-reference-format/scripts/check_render_manifest.py"

    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        # 1. VERIFIED cannot bypass actual identifier resolution/provenance.
        bad_verified = td / "bad_verified.json"
        bad_verified.write_text(json.dumps({
            "reference_id": "SRC-901",
            "original": {"title": "Claimed title", "doi": "10.1234/example"},
            "resolved": {},
            "checks": {"identifier_resolves": False, "identity_match": True},
            "verdict": "VERIFIED",
            "confidence": "high",
            "human_review": False,
        }), encoding="utf-8")
        p = run(ref_audit, bad_verified)
        require(p.returncode != 0 and "requires checks.identifier_resolves=true" in p.stdout,
                "VERIFIED record bypassed identifier-resolution gate", p)

        # 2. human_review must be the JSON boolean true, not a truthy string/integer.
        fake_confirmed = td / "fake_confirmed.json"
        fake_confirmed.write_text(json.dumps({
            "reference_id": "SRC-902",
            "original": {"title": "Suspect"},
            "resolved": {},
            "checks": {"identifier_resolves": False, "identity_match": False},
            "verdict": "FABRICATED_CONFIRMED",
            "confidence": "high",
            "human_review": "false",
        }), encoding="utf-8")
        p = run(ref_audit, fake_confirmed)
        require(p.returncode != 0 and "requires explicit human_review=true" in p.stdout,
                "FABRICATED_CONFIRMED accepted a non-boolean human_review value", p)

        # 3a. Standard natbib commands count as citations; commented citations do not.
        tex = td / "natbib.tex"
        bib = td / "natbib.bib"
        tex.write_text(
            r"\citealt{alpha} \citealp{beta} \citeauthor{alpha} \citeyear{beta}" + "\n" +
            r"% \cite{ghost}" + "\n" + r"Escaped percent \% is text.",
            encoding="utf-8",
        )
        bib.write_text(
            "@article{alpha, title={Alpha}, doi={10.1234/alpha}}\n"
            "@article{beta, title={Beta}, doi={10.1234/beta}}\n",
            encoding="utf-8",
        )
        p = run(bib_audit, tex, bib)
        require(p.returncode == 0 and "ghost" not in p.stdout,
                "natbib/comment-aware citation parsing failed", p)

        # 3b. DOI URL/prefix variants must collapse to the same identifier.
        dup_bib = td / "duplicate.bib"
        dup_bib.write_text(
            "@article{a, title={A}, doi={doi:10.5555/shared}}\n"
            "@article{b, title={B}, doi={https://dx.doi.org/10.5555/shared.}}\n",
            encoding="utf-8",
        )
        dup_tex = td / "duplicate.tex"
        dup_tex.write_text(r"\cite{a,b}", encoding="utf-8")
        p = run(bib_audit, dup_tex, dup_bib)
        require(p.returncode != 0 and "duplicate DOI 10.5555/shared" in p.stdout,
                "DOI canonicalization failed to detect duplicate URL/prefix forms", p)

        # 3c. Truncated/unbalanced BibTeX must fail structurally.
        broken_bib = td / "broken.bib"
        broken_bib.write_text("@article{broken, title={Never closed}\n", encoding="utf-8")
        broken_tex = td / "broken.tex"
        broken_tex.write_text(r"\cite{broken}", encoding="utf-8")
        p = run(bib_audit, broken_tex, broken_bib)
        require(p.returncode != 0 and "unterminated BibTeX entry" in p.stdout,
                "truncated BibTeX record was not rejected", p)

        # 4. Citation fidelity grades belong only on CIT -> CLM claim relations.
        bad_graph = td / "bad_graph.json"
        bad_graph.write_text(json.dumps({
            "nodes": [
                {"id": "SRC-901", "type": "source", "label": "Source", "role": "mechanism-support"},
                {"id": "CIT-901", "type": "citation", "label": "Citation"},
                {"id": "SEC-901", "type": "section", "label": "Discussion"},
            ],
            "edges": [
                {"from": "SRC-901", "to": "CIT-901", "relation": "cited_as"},
                {"from": "CIT-901", "to": "SEC-901", "relation": "reported_in"},
                {"from": "CIT-901", "to": "SEC-901", "relation": "supports", "evidence_grade": "E2", "fidelity_grade": "F5"},
            ],
        }), encoding="utf-8")
        p = run(graph_audit, bad_graph)
        require(p.returncode != 0 and "citation fidelity relation must be CIT -> CLM" in p.stdout,
                "Evidence Graph accepted fidelity grade on non-claim target", p)

        # 5a. citation-map top-level field is mandatory and typed.
        missing_map = td / "missing_map.json"
        missing_map.write_text("{}", encoding="utf-8")
        p = run(citation_audit, missing_map)
        require(p.returncode != 0 and "missing top-level citations array" in p.stdout,
                "citation map without citations array passed", p)
        null_map = td / "null_map.json"
        null_map.write_text('{"citations": null}', encoding="utf-8")
        p = run(citation_audit, null_map)
        require(p.returncode != 0 and "citations must be an array" in p.stdout,
                "citation map with null citations did not fail cleanly", p)

        # 5b. F3-F5 require inspectable source evidence.
        f3_map = td / "f3_map.json"
        f3_map.write_text(json.dumps({"citations": [{
            "citation_id": "CIT-903", "source_id": "SRC-903", "claim_id": "CLM-903",
            "manuscript_location": "Discussion", "manuscript_proposition": "Direct claim",
            "fidelity_grade": "F3", "action": "keep"
        }]}), encoding="utf-8")
        p = run(citation_audit, f3_map)
        require(p.returncode != 0 and "F3-F5 support requires source_locator" in p.stdout and "source_proposition" in p.stdout,
                "F3 citation passed without inspectable source evidence", p)

        # 6. Style verification must be explicit boolean true.
        bad_render = td / "bad_render.json"
        bad_render.write_text(json.dumps({
            "target_journal": "Example Journal", "style_id": "example-style",
            "processor": "citeproc", "metadata_source": "refs.json",
            "rendered_output": "refs.txt", "identity_verified": True,
            "style_verified_against_journal_instructions": "false",
        }), encoding="utf-8")
        p = run(render_audit, bad_render)
        require(p.returncode != 0 and "style_verified_against_journal_instructions must be true" in p.stdout,
                "truthy string bypassed render-manifest style gate", p)

    # 7. Skills that gate routing/citation work must define explicit terminal states.
    for rel in [
        "skills/geotech-router/SKILL.md",
        "skills/geotech-reference-verifier/SKILL.md",
        "skills/geotech-citation-fidelity/SKILL.md",
        "skills/geotech-reference-format/SKILL.md",
    ]:
        text = (ROOT / rel).read_text(encoding="utf-8")
        require("## Stop condition" in text, f"{rel} has no explicit stop condition")

    # 8. Synthetic example must not masquerade as a verified real publication.
    example = json.loads((ROOT / "skills/geotech-reference-verifier/assets/reference-record.example.json").read_text(encoding="utf-8"))
    require(example.get("verdict") == "UNRESOLVED" and "placeholder" in str(example.get("note", "")).lower(),
            "reference-record example still presents synthetic metadata as verified")
    p = run(ref_audit, ROOT / "skills/geotech-reference-verifier/assets/reference-record.example.json")
    require(p.returncode == 0, "explicit unresolved placeholder example should pass structural audit", p)

    print("Citation review-gap regression tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

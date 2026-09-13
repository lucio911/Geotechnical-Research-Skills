#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "skills" / "geotech-reference-verifier" / "scripts" / "audit_references.py"
BIB = ROOT / "tests" / "fixtures" / "reference-batch" / "references.bib"
CANDIDATES = ROOT / "tests" / "fixtures" / "reference-batch" / "candidates"


def run(extra=None):
    extra = extra or []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        out_json = td / "report.json"
        out_md = td / "report.md"
        cmd = [
            sys.executable, str(AUDIT), str(BIB),
            "--offline-dir", str(CANDIDATES),
            "--no-cache",
            "--output-json", str(out_json),
            "--output-md", str(out_md),
            *extra,
        ]
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        report = json.loads(out_json.read_text(encoding="utf-8")) if out_json.exists() else None
        markdown = out_md.read_text(encoding="utf-8") if out_md.exists() else ""
        return proc, report, markdown


def main() -> int:
    proc, report, markdown = run()
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert report is not None
    summary = report["summary"]
    assert summary["total_references"] == 4
    assert summary["verdict_counts"].get("VERIFIED") == 2
    assert summary["verdict_counts"].get("IDENTIFIER_MISMATCH") == 1
    assert summary["verdict_counts"].get("UNRESOLVED") == 1
    assert summary["duplicate_doi_groups"] == 1
    assert summary["near_duplicate_title_pairs"] >= 1
    assert summary["critical_actions"] == 1
    assert report["policy"]["unresolved_is_not_fabricated"] is True
    assert report["policy"]["automatic_fabrication_confirmation"] is False
    assert all(r["verdict"] != "FABRICATED_CONFIRMED" for r in report["references"])
    assert "UNRESOLVED` is not evidence of fabrication" in markdown
    assert "10.1234/good" in markdown

    proc2, report2, _ = run(["--fail-on-critical"])
    assert proc2.returncode == 1
    assert report2["summary"]["critical_actions"] == 1

    print("Batch Reference Forensics tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

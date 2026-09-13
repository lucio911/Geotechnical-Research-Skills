#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/geotech-reference-verifier/scripts/resolve_reference.py"
ORIGINAL = ROOT / "tests/fixtures/citation/resolver-original.json"
GOOD = ROOT / "tests/fixtures/citation/resolver-good-candidates.json"
MISMATCH = ROOT / "tests/fixtures/citation/resolver-mismatch-candidates.json"


def run(candidates: Path):
    p = subprocess.run(
        [sys.executable, str(SCRIPT), "--record", str(ORIGINAL), "--offline-candidates", str(candidates)],
        cwd=ROOT, capture_output=True, text=True,
    )
    if p.returncode != 0:
        print(p.stdout); print(p.stderr); raise SystemExit(1)
    return json.loads(p.stdout)


def main():
    good = run(GOOD)
    if good.get("verdict") not in {"VERIFIED", "VERIFIED_WITH_DRIFT"} or (good.get("identity_score") or 0) < 0.88:
        print("matched-candidate classification failed", json.dumps(good, indent=2)); return 1

    bad = run(MISMATCH)
    if bad.get("verdict") != "IDENTIFIER_MISMATCH" or not bad.get("requires_human_review"):
        print("identifier-mismatch classification failed", json.dumps(bad, indent=2)); return 1

    with tempfile.TemporaryDirectory() as td:
        empty = Path(td) / "empty.json"
        empty.write_text('{"candidates": []}', encoding="utf-8")
        unresolved = run(empty)
        if unresolved.get("verdict") != "UNRESOLVED" or "FABRICATED" in unresolved.get("verdict", ""):
            print("unresolved/fabrication policy failed", json.dumps(unresolved, indent=2)); return 1

    print("Online Reference Resolver tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
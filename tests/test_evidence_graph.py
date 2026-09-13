#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "skills/geotech-evidence-ledger/scripts/validate_evidence_graph.py"
EXAMPLE = ROOT / "skills/geotech-evidence-ledger/assets/evidence-graph.example.json"


def run(path: Path):
    return subprocess.run([sys.executable, str(VALIDATOR), str(path)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def main():
    valid = run(EXAMPLE)
    if valid.returncode != 0:
        print(valid.stdout)
        raise SystemExit("valid graph unexpectedly failed")

    invalid = {
        "project": {"id": "invalid"},
        "nodes": [
            {"id": "CLM-001", "type": "claim", "label": "Unsupported claim", "status": "active"},
            {"id": "CON-001", "type": "conclusion", "label": "Unsupported conclusion", "status": "active"}
        ],
        "edges": [
            {"from": "CLM-001", "to": "CON-001", "relation": "concludes"}
        ]
    }
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "invalid.json"
        p.write_text(json.dumps(invalid), encoding="utf-8")
        bad = run(p)
        if bad.returncode == 0:
            print(bad.stdout)
            raise SystemExit("invalid graph unexpectedly passed")
        if "claim has no supporting/dependency edge" not in bad.stdout:
            print(bad.stdout)
            raise SystemExit("invalid graph failed for unexpected reason")

    print("Evidence Graph tests passed")


if __name__ == "__main__":
    main()

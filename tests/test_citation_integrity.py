#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(args): return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True)
def main():
    # Valid examples should pass.
    checks=[
      [ROOT/'skills/geotech-reference-verifier/scripts/audit_reference_record.py', ROOT/'skills/geotech-reference-verifier/assets/reference-record.example.json'],
      [ROOT/'skills/geotech-citation-fidelity/scripts/audit_citation_map.py', ROOT/'skills/geotech-citation-fidelity/assets/citation-map.example.json'],
      [ROOT/'skills/geotech-reference-format/scripts/check_render_manifest.py', ROOT/'skills/geotech-reference-format/assets/render-manifest.example.json'],
      [ROOT/'skills/geotech-evidence-ledger/scripts/validate_evidence_graph.py', ROOT/'skills/geotech-evidence-ledger/assets/citation-evidence-graph.example.json'],
    ]
    for c in checks:
        p=run(c)
        if p.returncode!=0:
            print(p.stdout,p.stderr); return 1
    # Fabricated confirmed without human review must fail.
    p=run([ROOT/'skills/geotech-reference-verifier/scripts/audit_reference_record.py', ROOT/'tests/fixtures/citation/bad-reference-record.json'])
    if p.returncode==0 or 'requires explicit human_review=true' not in p.stdout:
        print('negative reference-verifier test failed'); print(p.stdout); return 1
    # Missing cited key should fail bibliography audit, while orphan should be reported.
    p=run([ROOT/'skills/geotech-bibliography-audit/scripts/audit_bib_consistency.py', ROOT/'tests/fixtures/citation/manuscript.tex', ROOT/'tests/fixtures/citation/references.bib'])
    if p.returncode==0 or 'dangling citation: wang2023' not in p.stdout or 'orphan bibliography entry: unused2020' not in p.stdout:
        print('bibliography negative test failed'); print(p.stdout); return 1
    # Weak citation without mismatch should still pass structurally but warn.
    with tempfile.TemporaryDirectory() as td:
        q=Path(td)/'c.json'; q.write_text(json.dumps({'citations':[{'citation_id':'CIT-101','source_id':'SRC-101','claim_id':'CLM-101','manuscript_location':'Intro','manuscript_proposition':'x','fidelity_grade':'F1','action':'verify'}]}),encoding='utf-8')
        p=run([ROOT/'skills/geotech-citation-fidelity/scripts/audit_citation_map.py',q])
        if p.returncode!=0 or 'weak/unverified support' not in p.stdout:
            print('citation warning test failed'); print(p.stdout); return 1
    print('Citation Integrity Core tests passed')
    return 0
if __name__=='__main__': raise SystemExit(main())

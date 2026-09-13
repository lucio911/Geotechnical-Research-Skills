#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path
GRADE={f"F{i}" for i in range(6)}
CID=re.compile(r"^CIT-\d{3,}$"); SID=re.compile(r"^SRC-\d{3,}$"); CLM=re.compile(r"^CLM-\d{3,}$")
def main():
    ap=argparse.ArgumentParser(description="Audit citation-instance map structure and fidelity grades.")
    ap.add_argument("map")
    ns=ap.parse_args(); data=json.loads(Path(ns.map).read_text(encoding="utf-8"))
    rows=data.get("citations",[]); errors=[]; warnings=[]; ids=[]
    for i,r in enumerate(rows):
        for k in ["citation_id","source_id","claim_id","manuscript_location","manuscript_proposition","fidelity_grade","action"]:
            if not r.get(k): errors.append(f"citation {i}: missing {k}")
        if r.get("citation_id"): ids.append(r["citation_id"])
        if r.get("citation_id") and not CID.fullmatch(r["citation_id"]): errors.append(f"citation {i}: invalid CIT id")
        if r.get("source_id") and not SID.fullmatch(r["source_id"]): errors.append(f"citation {i}: invalid SRC id")
        if r.get("claim_id") and not CLM.fullmatch(r["claim_id"]): errors.append(f"citation {i}: invalid CLM id")
        if r.get("fidelity_grade") not in GRADE: errors.append(f"citation {i}: invalid fidelity grade")
        if r.get("fidelity_grade") in {"F0","F1","F2"} and not r.get("mismatch"):
            warnings.append(f"{r.get('citation_id','?')}: weak/unverified support without mismatch rationale")
        if r.get("fidelity_grade") in {"F4","F5"} and not r.get("source_locator"):
            warnings.append(f"{r.get('citation_id','?')}: high support grade without source locator")
    if len(ids)!=len(set(ids)): errors.append("duplicate citation_id values")
    for w in warnings: print("WARNING:",w)
    for e in errors: print("ERROR:",e)
    if not errors: print(f"PASS: {len(rows)} citation instances")
    raise SystemExit(1 if errors else 0)
if __name__=="__main__": main()

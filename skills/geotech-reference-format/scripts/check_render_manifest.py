#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description="Validate declared provenance for deterministic bibliography rendering.")
    ap.add_argument("manifest"); ns=ap.parse_args(); d=json.loads(Path(ns.manifest).read_text(encoding="utf-8"))
    errors=[]; warnings=[]
    for k in ["target_journal","style_id","processor","metadata_source","rendered_output","identity_verified"]:
        if k not in d or d[k] in (None,""): errors.append(f"missing {k}")
    if d.get("identity_verified") is not True: errors.append("identity_verified must be true before final formatting")
    if not d.get("style_verified_against_journal_instructions"):
        warnings.append("style has not yet been checked against target journal instructions")
    for w in warnings: print("WARNING:",w)
    for e in errors: print("ERROR:",e)
    if not errors: print("PASS: render manifest structure")
    raise SystemExit(1 if errors else 0)
if __name__=="__main__": main()

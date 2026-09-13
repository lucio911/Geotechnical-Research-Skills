#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

VALID = {
    "VERIFIED", "VERIFIED_WITH_DRIFT", "IDENTIFIER_MISMATCH", "DUPLICATE", "AMBIGUOUS",
    "SUSPECTED_COMPOSITE", "UNRESOLVED", "SUSPECTED_FABRICATION", "FABRICATED_CONFIRMED",
    "HUMAN_DECISION_REQUIRED",
}
HIGH_RISK = {"IDENTIFIER_MISMATCH", "SUSPECTED_COMPOSITE", "SUSPECTED_FABRICATION", "FABRICATED_CONFIRMED"}
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.I)

def main():
    ap=argparse.ArgumentParser(description="Audit structure and internal consistency of a reference verification record.")
    ap.add_argument("record")
    ns=ap.parse_args()
    data=json.loads(Path(ns.record).read_text(encoding="utf-8"))
    errors=[]; warnings=[]
    for key in ["reference_id","original","checks","verdict","confidence"]:
        if key not in data: errors.append(f"missing {key}")
    verdict=data.get("verdict")
    if verdict not in VALID: errors.append(f"invalid verdict {verdict!r}")
    orig=data.get("original",{}) or {}; res=data.get("resolved",{}) or {}; checks=data.get("checks",{}) or {}
    for side,name in [(orig,"original"),(res,"resolved")]:
        doi=side.get("doi")
        if doi and not DOI_RE.match(str(doi).strip()): warnings.append(f"{name}.doi does not look like a DOI: {doi}")
    if verdict=="VERIFIED" and checks.get("identity_match") is not True:
        errors.append("VERIFIED requires checks.identity_match=true")
    if verdict=="IDENTIFIER_MISMATCH" and checks.get("identifier_resolves") is not True:
        warnings.append("identifier mismatch normally requires a successfully resolved identifier")
    if verdict in HIGH_RISK and data.get("human_review") is False:
        warnings.append("high-risk verdict should normally require human review")
    if verdict=="FABRICATED_CONFIRMED" and not data.get("human_review"):
        errors.append("FABRICATED_CONFIRMED requires explicit human_review=true")
    if res and not res.get("source"):
        warnings.append("resolved metadata has no source provenance")
    for w in warnings: print("WARNING:",w)
    for e in errors: print("ERROR:",e)
    if not errors: print(f"PASS: {data.get('reference_id','?')} -> {verdict}")
    raise SystemExit(1 if errors else 0)
if __name__=="__main__": main()

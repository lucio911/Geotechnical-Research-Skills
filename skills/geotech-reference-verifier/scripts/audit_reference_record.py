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


def clean_doi(value):
    if not value:
        return ""
    value = str(value).strip()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.I)
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    return value.rstrip(".,; )]}\"").lower()


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
    if not isinstance(orig,dict): errors.append("original must be an object"); orig={}
    if not isinstance(res,dict): errors.append("resolved must be an object"); res={}
    if not isinstance(checks,dict): errors.append("checks must be an object"); checks={}

    for side,name in [(orig,"original"),(res,"resolved")]:
        doi=clean_doi(side.get("doi"))
        if doi and not DOI_RE.match(doi): warnings.append(f"{name}.doi does not look like a DOI: {side.get('doi')}")

    if verdict in {"VERIFIED","VERIFIED_WITH_DRIFT"}:
        if checks.get("identity_match") is not True:
            errors.append(f"{verdict} requires checks.identity_match=true")
        if not res:
            errors.append(f"{verdict} requires resolved metadata")
        elif not res.get("source"):
            errors.append(f"{verdict} requires resolved.source provenance")
        supplied_identifier = any(orig.get(k) for k in ("doi","pmid","pmcid","arxiv","isbn","handle"))
        if supplied_identifier and checks.get("identifier_resolves") is not True:
            errors.append(f"{verdict} with a supplied identifier requires checks.identifier_resolves=true")
        if not supplied_identifier and checks.get("identifier_resolves") is not True and checks.get("bibliographic_search_resolves") is not True:
            errors.append(f"{verdict} without a supplied identifier requires an explicit successful bibliographic search")
        od, rd = clean_doi(orig.get("doi")), clean_doi(res.get("doi"))
        if od:
            if not rd:
                errors.append(f"{verdict} with an original DOI requires resolved DOI metadata")
            elif od != rd:
                errors.append(f"{verdict} requires original/resolved DOI identity to match")

    if verdict=="IDENTIFIER_MISMATCH" and checks.get("identifier_resolves") is not True:
        warnings.append("identifier mismatch normally requires a successfully resolved identifier")
    if verdict in HIGH_RISK and data.get("human_review") is not True:
        warnings.append("high-risk verdict should normally require human_review=true")
    if verdict=="FABRICATED_CONFIRMED" and data.get("human_review") is not True:
        errors.append("FABRICATED_CONFIRMED requires explicit human_review=true")
    if res and not res.get("source"):
        warnings.append("resolved metadata has no source provenance")

    for w in warnings: print("WARNING:",w)
    for e in errors: print("ERROR:",e)
    if not errors: print(f"PASS: {data.get('reference_id','?')} -> {verdict}")
    raise SystemExit(1 if errors else 0)


if __name__=="__main__": main()

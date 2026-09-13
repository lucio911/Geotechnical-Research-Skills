#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import time
import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

DOI_RE = re.compile(r"10\.\d{4,9}/\S+", re.I)
DEFAULT_UA = "Geotechnical-Research-Skills/0.5 (+https://github.com/lucio911/Geotechnical-Research-Skills)"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clean_doi(value: str | None) -> str | None:
    if not value:
        return None
    value = str(value).strip()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.I)
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    value = value.rstrip(".,; )]}")
    m = DOI_RE.search(value)
    return m.group(0).lower() if m else None


def norm_text(value: str | None) -> str:
    if not value:
        return ""
    value = unicodedata.normalize("NFKD", str(value))
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def text_similarity(a: str | None, b: str | None) -> float:
    na, nb = norm_text(a), norm_text(b)
    if not na or not nb:
        return 0.0
    sa, sb = set(na.split()), set(nb.split())
    jac = len(sa & sb) / len(sa | sb) if sa and sb else 0.0
    return round(0.65 * SequenceMatcher(None, na, nb).ratio() + 0.35 * jac, 4)


def surname(name: str) -> str:
    parts = norm_text(name).split()
    return parts[-1] if parts else ""


def author_overlap(claimed: list[str], candidate: list[str]) -> float:
    a = {surname(x) for x in claimed if surname(x)}
    b = {surname(x) for x in candidate if surname(x)}
    return round(len(a & b) / len(a | b), 4) if a and b else 0.0


def year_score(a: int | None, b: int | None) -> tuple[float, int | None]:
    if not a or not b:
        return 0.0, None
    d = abs(int(a) - int(b))
    return ({0: 1.0, 1: 0.8, 2: 0.3}.get(d, 0.0), d)


def first(v: Any, default=""):
    return v[0] if isinstance(v, list) and v else default


def crossref_year(msg: dict[str, Any]) -> int | None:
    for key in ("published-print", "published-online", "published", "issued", "created"):
        parts = ((msg.get(key) or {}).get("date-parts") or [])
        if parts and parts[0]:
            try:
                return int(parts[0][0])
            except (TypeError, ValueError):
                pass
    return None


def crossref_candidate(msg: dict[str, Any], source_url: str) -> dict[str, Any]:
    authors = []
    for a in msg.get("author") or []:
        name = " ".join(x for x in ((a.get("given") or "").strip(), (a.get("family") or "").strip()) if x)
        if name:
            authors.append(name)
    return {
        "source": "crossref", "source_url": source_url, "doi": clean_doi(msg.get("DOI")),
        "title": first(msg.get("title")), "authors": authors, "year": crossref_year(msg),
        "venue": first(msg.get("container-title")), "publisher": msg.get("publisher") or "",
        "volume": msg.get("volume") or "", "issue": msg.get("issue") or "",
        "pages": msg.get("page") or msg.get("article-number") or "", "type": msg.get("type") or "",
        "url": msg.get("URL") or "", "is_retracted": None,
    }


def datacite_candidate(item: dict[str, Any], source_url: str) -> dict[str, Any]:
    a = item.get("attributes") or item
    authors = []
    for c in a.get("creators") or []:
        name = c.get("name") or " ".join(x for x in (c.get("givenName"), c.get("familyName")) if x)
        if name:
            authors.append(name)
    titles = a.get("titles") or []
    title = titles[0].get("title", "") if titles and isinstance(titles[0], dict) else ""
    publisher = a.get("publisher") or ""
    if isinstance(publisher, dict):
        publisher = publisher.get("name") or ""
    container = a.get("container") or {}
    try:
        year = int(a.get("publicationYear")) if a.get("publicationYear") is not None else None
    except (TypeError, ValueError):
        year = None
    return {
        "source": "datacite", "source_url": source_url, "doi": clean_doi(a.get("doi") or item.get("id")),
        "title": title, "authors": authors, "year": year, "venue": container.get("title") or publisher,
        "publisher": publisher, "volume": container.get("volume") or "", "issue": container.get("issue") or "",
        "pages": container.get("firstPage") or "", "type": (a.get("types") or {}).get("resourceTypeGeneral") or "",
        "url": a.get("url") or "", "is_retracted": None,
    }


def openalex_candidate(item: dict[str, Any], source_url: str) -> dict[str, Any]:
    authors = []
    for a in item.get("authorships") or []:
        name = a.get("raw_author_name") or ((a.get("author") or {}).get("display_name") or "")
        if name:
            authors.append(name)
    src = ((item.get("primary_location") or {}).get("source") or {})
    b = item.get("biblio") or {}
    pages = "-".join(x for x in (b.get("first_page"), b.get("last_page")) if x)
    return {
        "source": "openalex", "source_url": source_url,
        "doi": clean_doi(item.get("doi") or (item.get("ids") or {}).get("doi")),
        "title": item.get("title") or item.get("display_name") or "", "authors": authors,
        "year": item.get("publication_year"), "venue": src.get("display_name") or "",
        "publisher": src.get("host_organization_name") or "", "volume": b.get("volume") or "",
        "issue": b.get("issue") or "", "pages": pages, "type": item.get("type") or "",
        "url": item.get("id") or "", "is_retracted": item.get("is_retracted"),
    }


def get_json(url: str, ua: str, timeout: float, retries: int = 2) -> dict[str, Any]:
    for attempt in range(retries + 1):
        try:
            with urlopen(Request(url, headers={"User-Agent": ua, "Accept": "application/json"}), timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code in {400, 404} or exc.code not in {429, 500, 502, 503, 504} or attempt == retries:
                raise
        except URLError:
            if attempt == retries:
                raise
        time.sleep(0.75 * (2 ** attempt))
    return {}


def crossref(original: dict[str, Any], email: str | None, ua: str, timeout: float, rows: int):
    doi = clean_doi(original.get("doi"))
    if doi:
        url = f"https://api.crossref.org/works/{quote(doi, safe='')}"
        if email:
            url += "?" + urlencode({"mailto": email})
    else:
        query = " ".join([original.get("title") or "", " ".join(original.get("authors") or []), str(original.get("year") or ""), original.get("venue") or ""])
        params = {"query.bibliographic": query, "rows": max(1, min(rows, 10))}
        if email:
            params["mailto"] = email
        url = "https://api.crossref.org/works?" + urlencode(params)
    prov = {"source": "crossref", "url": url, "status": "attempted"}
    try:
        data = get_json(url, ua, timeout)
        if doi:
            items = [data.get("message") or {}]
        else:
            items = ((data.get("message") or {}).get("items") or [])
        prov["status"] = f"resolved_{len(items)}"
        return [crossref_candidate(x, url) for x in items], [prov]
    except HTTPError as exc:
        prov["status"] = f"http_{exc.code}"
    except Exception as exc:
        prov["status"], prov["error"] = "error", type(exc).__name__
    return [], [prov]


def datacite(original: dict[str, Any], ua: str, timeout: float, rows: int):
    doi = clean_doi(original.get("doi"))
    if doi:
        url = f"https://api.datacite.org/dois/{quote(doi, safe='')}"
    else:
        query = (original.get("title") or "") + " " + " ".join((original.get("authors") or [])[:2])
        url = "https://api.datacite.org/dois?" + urlencode({"query": query, "page[size]": max(1, min(rows, 10))})
    prov = {"source": "datacite", "url": url, "status": "attempted"}
    try:
        data = get_json(url, ua, timeout)
        items = [data.get("data") or {}] if doi else (data.get("data") or [])
        prov["status"] = f"resolved_{len(items)}"
        return [datacite_candidate(x, url) for x in items], [prov]
    except HTTPError as exc:
        prov["status"] = f"http_{exc.code}"
    except Exception as exc:
        prov["status"], prov["error"] = "error", type(exc).__name__
    return [], [prov]


def openalex(original: dict[str, Any], api_key: str | None, ua: str, timeout: float, rows: int):
    doi = clean_doi(original.get("doi"))
    params: dict[str, Any] = {"per_page": max(1, min(rows, 10))}
    params["filter" if doi else "search"] = f"doi:https://doi.org/{doi}" if doi else (original.get("title") or "")
    if api_key:
        params["api_key"] = api_key
    raw_url = "https://api.openalex.org/works?" + urlencode(params)
    shown_url = re.sub(r"api_key=[^&]+", "api_key=REDACTED", raw_url)
    prov = {"source": "openalex", "url": shown_url, "status": "attempted"}
    try:
        items = get_json(raw_url, ua, timeout).get("results") or []
        prov["status"] = f"resolved_{len(items)}"
        return [openalex_candidate(x, shown_url) for x in items], [prov]
    except Exception as exc:
        prov["status"], prov["error"] = "error", type(exc).__name__
        return [], [prov]


def score(original: dict[str, Any], cand: dict[str, Any]) -> dict[str, Any]:
    ts = text_similarity(original.get("title"), cand.get("title"))
    ao = author_overlap(original.get("authors") or [], cand.get("authors") or [])
    ys, yd = year_score(original.get("year"), cand.get("year"))
    vs = text_similarity(original.get("venue"), cand.get("venue")) if original.get("venue") else 0.0
    od, cd = clean_doi(original.get("doi")), clean_doi(cand.get("doi"))
    dm = bool(od and cd and od == cd)
    if od:
        total = 0.55 * ts + 0.20 * ao + 0.10 * ys + 0.15 * (1.0 if dm else 0.0)
    elif original.get("venue") and cand.get("venue"):
        total = 0.60 * ts + 0.25 * ao + 0.10 * ys + 0.05 * vs
    else:
        total = 0.65 * ts + 0.25 * ao + 0.10 * ys
    return {"identity_score": round(total, 4), "checks": {"identifier_resolves": True, "doi_match": dm if od else None, "title_similarity": ts, "author_overlap": ao, "year_delta": yd, "year_score": ys, "venue_similarity": vs if original.get("venue") else None}, "candidate": cand}


def classify(original: dict[str, Any], ranked: list[dict[str, Any]]):
    if not ranked:
        return "UNRESOLVED", "low", True
    top, s = ranked[0], ranked[0]["identity_score"]
    c = top["checks"]
    margin = s - ranked[1]["identity_score"] if len(ranked) > 1 else 1.0
    if clean_doi(original.get("doi")):
        if c.get("doi_match") and (c.get("title_similarity", 0) < 0.50 or s < 0.55):
            return "IDENTIFIER_MISMATCH", "high", True
        if c.get("doi_match") and s >= 0.88 and c.get("title_similarity", 0) >= 0.92:
            exactish = c.get("title_similarity", 0) >= 0.98 and c.get("author_overlap", 0) >= 0.75 and c.get("year_delta") in {0, None}
            return ("VERIFIED" if exactish else "VERIFIED_WITH_DRIFT"), "high", False
        if c.get("doi_match") and s >= 0.74:
            return "VERIFIED_WITH_DRIFT", "medium", False
        return "AMBIGUOUS", "medium", True
    if s >= 0.88 and margin >= 0.08 and c.get("title_similarity", 0) >= 0.92:
        return "VERIFIED_WITH_DRIFT", "high", False
    if s >= 0.74 and margin >= 0.12:
        return "AMBIGUOUS", "medium", True
    return "UNRESOLVED", "low", True


def load_original(ns: argparse.Namespace):
    if ns.record:
        d = json.loads(Path(ns.record).read_text(encoding="utf-8"))
        refid, original = d.get("reference_id") or ns.reference_id or "REF-UNSET", d.get("original") or {}
    else:
        refid = ns.reference_id or "REF-UNSET"
        original = {"title": ns.title or "", "authors": ns.author or [], "year": ns.year, "venue": ns.venue or "", "doi": ns.doi or ""}
    original = dict(original)
    if isinstance(original.get("authors"), str):
        original["authors"] = [x.strip() for x in re.split(r";|\band\b", original["authors"]) if x.strip()]
    original["doi"] = clean_doi(original.get("doi")) or ""
    return refid, original


def main() -> int:
    ap = argparse.ArgumentParser(description="Resolve scholarly reference identity with public metadata services.")
    ap.add_argument("--record"); ap.add_argument("--reference-id"); ap.add_argument("--title")
    ap.add_argument("--author", action="append", default=[]); ap.add_argument("--year", type=int); ap.add_argument("--venue"); ap.add_argument("--doi")
    ap.add_argument("--email", help="Crossref polite-pool contact email")
    ap.add_argument("--use-openalex", action="store_true"); ap.add_argument("--openalex-api-key")
    ap.add_argument("--timeout", type=float, default=12.0); ap.add_argument("--rows", type=int, default=5)
    ap.add_argument("--offline-candidates", help="JSON candidates; disables network for deterministic CI")
    ap.add_argument("--output")
    ns = ap.parse_args()
    refid, original = load_original(ns)
    if not original.get("title") and not original.get("doi"):
        ap.error("provide at least a DOI or title")
    ua = DEFAULT_UA + (f" mailto:{ns.email}" if ns.email else "")
    candidates, provenance = [], []
    if ns.offline_candidates:
        raw = json.loads(Path(ns.offline_candidates).read_text(encoding="utf-8"))
        candidates = raw.get("candidates", []) if isinstance(raw, dict) else raw
        provenance.append({"source": "offline_fixture", "url": str(ns.offline_candidates), "status": f"loaded_{len(candidates)}"})
    else:
        got, prov = crossref(original, ns.email, ua, ns.timeout, ns.rows); candidates += got; provenance += prov
        if not got or not clean_doi(original.get("doi")):
            got, prov = datacite(original, ua, ns.timeout, ns.rows); candidates += got; provenance += prov
        if ns.use_openalex:
            got, prov = openalex(original, ns.openalex_api_key, ua, ns.timeout, ns.rows); candidates += got; provenance += prov
    seen, unique = set(), []
    for c in candidates:
        key = (clean_doi(c.get("doi")) or "", norm_text(c.get("title")), c.get("year"))
        if key not in seen:
            seen.add(key); unique.append(c)
    ranked = sorted((score(original, c) for c in unique), key=lambda x: x["identity_score"], reverse=True)
    verdict, confidence, needs_human = classify(original, ranked)
    top = ranked[0] if ranked else None
    resolved = dict(top["candidate"]) if top else {}
    if resolved.get("doi"):
        for c in candidates:
            if c.get("source") == "openalex" and clean_doi(c.get("doi")) == clean_doi(resolved.get("doi")) and c.get("is_retracted") is not None:
                resolved["is_retracted"], resolved["retraction_status_source"] = c.get("is_retracted"), "openalex"
                break
    checks = dict(top["checks"]) if top else {"identifier_resolves": False, "identity_match": False, "identity_score": None}
    if top:
        checks["identity_match"] = verdict in {"VERIFIED", "VERIFIED_WITH_DRIFT"}
        checks["identity_score"] = top["identity_score"]
        checks["candidate_margin"] = round(top["identity_score"] - ranked[1]["identity_score"], 4) if len(ranked) > 1 else None
    report = {
        "reference_id": refid, "original": original,
        "resolver": {"mode": "offline" if ns.offline_candidates else "online", "sources_attempted": [p.get("source") for p in provenance], "openalex_enabled": bool(ns.use_openalex), "retrieved_at": now_iso()},
        "resolved": resolved, "checks": checks, "identity_score": top["identity_score"] if top else None,
        "verdict": verdict, "confidence": confidence, "human_review": False,
        "requires_human_review": needs_human or verdict in {"IDENTIFIER_MISMATCH", "AMBIGUOUS", "UNRESOLVED"},
        "publication_status": {"is_retracted": resolved.get("is_retracted") if resolved else None, "source": resolved.get("retraction_status_source") if resolved else None, "note": "OpenAlex is_retracted is secondary status evidence; absence of a flag is not proof of clean status."},
        "candidates": ranked[:max(1, min(ns.rows, 10))], "provenance": provenance,
        "policy": {"not_found_is_not_fabricated": True, "automatic_fabrication_confirmation": False, "formatting_may_not_modify_identity": True},
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if ns.output:
        Path(ns.output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

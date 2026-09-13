#!/usr/bin/env python3
from __future__ import annotations
import argparse, re
from pathlib import Path

CITE_RE = re.compile(
    r"\\(?:cite(?:p|t|alt|alp|author|year|yearpar)?|parencite|textcite|autocite|footcite|supercite|nocite)"
    r"\*?(?:\s*\[[^\]]*\]){0,2}\s*\{([^}]*)\}",
    re.I,
)
ENTRY_START_RE = re.compile(r"@([A-Za-z]+)\s*([\{(])", re.I)
ENTRY_KEY_RE = re.compile(r"@\w+\s*[\{(]\s*([^,\s]+)\s*,", re.I)
META_TYPES = {"comment", "preamble", "string"}
DOI_VALUE_RE = re.compile(r"10\.\d{4,9}/\S+", re.I)


def strip_tex_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        cut = len(line)
        for i, ch in enumerate(line):
            if ch != "%":
                continue
            backslashes = 0
            j = i - 1
            while j >= 0 and line[j] == "\\":
                backslashes += 1
                j -= 1
            if backslashes % 2 == 0:
                cut = i
                break
        lines.append(line[:cut])
    return "\n".join(lines)


def split_entries(text: str):
    entries, errors = [], []
    pos = 0
    while True:
        m = ENTRY_START_RE.search(text, pos)
        if not m:
            break
        kind = m.group(1).lower()
        opener = m.group(2)
        closer = "}" if opener == "{" else ")"
        depth = 1
        in_quote = False
        escaped = False
        i = m.end()
        while i < len(text) and depth:
            ch = text[i]
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_quote = not in_quote
            elif not in_quote:
                if ch == opener:
                    depth += 1
                elif ch == closer:
                    depth -= 1
            i += 1
        if depth:
            errors.append(f"unterminated BibTeX entry starting at character {m.start()}")
            break
        chunk = text[m.start():i]
        if kind not in META_TYPES:
            km = ENTRY_KEY_RE.search(chunk)
            if not km:
                errors.append(f"BibTeX entry at character {m.start()} has no citekey")
            else:
                entries.append((km.group(1).strip(), chunk))
        pos = i
    return entries, errors


def extract_field(chunk: str, field: str):
    m = re.search(rf"\b{re.escape(field)}\s*=\s*", chunk, re.I)
    if not m:
        return None
    i = m.end()
    if i >= len(chunk):
        return ""
    if chunk[i] == "{":
        depth = 1
        j = i + 1
        escaped = False
        while j < len(chunk) and depth:
            ch = chunk[j]
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return chunk[i + 1:j]
            j += 1
        return None
    if chunk[i] == '"':
        j = i + 1
        escaped = False
        while j < len(chunk):
            ch = chunk[j]
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                return chunk[i + 1:j]
            j += 1
        return None
    j = i
    while j < len(chunk) and chunk[j] not in ",\n\r":
        j += 1
    return chunk[i:j].strip()


def norm_doi(value):
    if not value:
        return ""
    value = str(value).strip()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.I)
    value = re.sub(r"^doi:\s*", "", value, flags=re.I)
    value = value.rstrip(".,; )]}\"")
    m = DOI_VALUE_RE.search(value)
    return m.group(0).lower() if m else value.lower()


def norm_title(value):
    value = re.sub(r"[{}]", "", value or "")
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def main():
    ap = argparse.ArgumentParser(description="Conservative LaTeX/BibTeX citation consistency audit.")
    ap.add_argument("tex")
    ap.add_argument("bib")
    ns = ap.parse_args()
    tex = strip_tex_comments(Path(ns.tex).read_text(encoding="utf-8", errors="replace"))
    bib = Path(ns.bib).read_text(encoding="utf-8", errors="replace")

    cited = []
    for m in CITE_RE.finditer(tex):
        cited += [k.strip() for k in m.group(1).split(",") if k.strip()]

    entries, parse_errors = split_entries(bib)
    keys = [k for k, _ in entries]
    keyset, citedset = set(keys), set(cited)
    errors = list(parse_errors)
    warnings = []

    for k in sorted(citedset - keyset):
        errors.append(f"dangling citation: {k}")
    for k in sorted(keyset - citedset):
        warnings.append(f"orphan bibliography entry: {k}")
    if len(keys) != len(keyset):
        dup = sorted({k for k in keys if keys.count(k) > 1})
        errors.append("duplicate citekeys: " + ", ".join(dup))

    doi_map, title_map = {}, {}
    for k, chunk in entries:
        doi = norm_doi(extract_field(chunk, "doi"))
        title = extract_field(chunk, "title")
        if doi:
            doi_map.setdefault(doi, []).append(k)
        nt = norm_title(title)
        if nt:
            title_map.setdefault(nt, []).append(k)

    for doi, ks in sorted(doi_map.items()):
        if len(ks) > 1:
            errors.append(f"duplicate DOI {doi}: {', '.join(ks)}")
    for _, ks in sorted(title_map.items()):
        if len(ks) > 1:
            warnings.append("duplicate normalized title: " + ", ".join(ks))

    print(f"Citations: {len(cited)} occurrences | {len(citedset)} unique keys | Bib entries: {len(entries)}")
    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()

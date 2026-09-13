#!/usr/bin/env python3
from __future__ import annotations
import argparse, re
from pathlib import Path

CITE_RE=re.compile(r"\\(?:cite|citep|citet|parencite|textcite|autocite|footcite|supercite)\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}")
ENTRY_RE=re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.I)
DOI_RE=re.compile(r"\bdoi\s*=\s*[\{\"]([^}\"]+)", re.I)
TITLE_RE=re.compile(r"\btitle\s*=\s*[\{\"]([^}\"]+)", re.I)

def split_entries(text):
    starts=list(re.finditer(r"@\w+\s*\{", text, re.I)); out=[]
    for i,m in enumerate(starts):
        end=starts[i+1].start() if i+1<len(starts) else len(text)
        chunk=text[m.start():end]
        km=ENTRY_RE.search(chunk)
        if km: out.append((km.group(1).strip(),chunk))
    return out

def norm_title(s): return re.sub(r"[^a-z0-9]+","",s.lower())

def main():
    ap=argparse.ArgumentParser(description="Conservative LaTeX/BibTeX citation consistency audit.")
    ap.add_argument("tex"); ap.add_argument("bib")
    ns=ap.parse_args(); tex=Path(ns.tex).read_text(encoding="utf-8",errors="replace"); bib=Path(ns.bib).read_text(encoding="utf-8",errors="replace")
    cited=[]
    for m in CITE_RE.finditer(tex): cited += [k.strip() for k in m.group(1).split(',') if k.strip()]
    entries=split_entries(bib); keys=[k for k,_ in entries]; keyset=set(keys); citedset=set(cited)
    errors=[]; warnings=[]
    for k in sorted(citedset-keyset): errors.append(f"dangling citation: {k}")
    for k in sorted(keyset-citedset): warnings.append(f"orphan bibliography entry: {k}")
    if len(keys)!=len(keyset):
        dup=sorted({k for k in keys if keys.count(k)>1}); errors.append("duplicate citekeys: "+", ".join(dup))
    doi_map={}; title_map={}
    for k,ch in entries:
        dm=DOI_RE.search(ch); tm=TITLE_RE.search(ch)
        if dm:
            doi=dm.group(1).strip().lower().replace('https://doi.org/','').replace('http://doi.org/','')
            doi_map.setdefault(doi,[]).append(k)
        if tm:
            nt=norm_title(tm.group(1));
            if nt: title_map.setdefault(nt,[]).append(k)
    for doi,ks in sorted(doi_map.items()):
        if len(ks)>1: errors.append(f"duplicate DOI {doi}: {', '.join(ks)}")
    for _,ks in sorted(title_map.items()):
        if len(ks)>1: warnings.append("duplicate normalized title: "+", ".join(ks))
    print(f"Citations: {len(cited)} occurrences | {len(citedset)} unique keys | Bib entries: {len(entries)}")
    for w in warnings: print("WARNING:",w)
    for e in errors: print("ERROR:",e)
    raise SystemExit(1 if errors else 0)
if __name__=="__main__": main()

#!/usr/bin/env python3
import argparse, csv, math
from pathlib import Path

def isnum(s):
    try:
        x=float(s); return math.isfinite(x), x
    except (ValueError, TypeError): return False, None

def main():
    ap=argparse.ArgumentParser(description='Lightweight structural QC for research CSV files.')
    ap.add_argument('csv_file')
    ap.add_argument('--time-column')
    args=ap.parse_args()
    p=Path(args.csv_file)
    with p.open(newline='', encoding='utf-8-sig') as f:
        rd=csv.DictReader(f); rows=list(rd); cols=rd.fieldnames or []
    print(f"Rows: {len(rows)} | Columns: {len(cols)}")
    if not cols: print('ERROR: no header'); raise SystemExit(1)
    tuples=[tuple((r.get(c) or '') for c in cols) for r in rows]
    duplicates=len(tuples)-len(set(tuples))
    if duplicates: print(f"WARNING: duplicate rows = {duplicates}")
    for c in cols:
        vals=[(r.get(c) or '').strip() for r in rows]
        miss=sum(v=='' for v in vals)
        if miss: print(f"WARNING: {c}: missing={miss}")
        nonempty=[v for v in vals if v!='']
        nums=[]; bad=0
        for v in nonempty:
            ok,x=isnum(v)
            if ok: nums.append(x)
            else: bad+=1
        if nums and bad==0:
            if len(set(nums))==1: print(f"WARNING: {c}: constant numeric channel")
            if len(set(nums)) <= max(2, len(nums)//100) and len(nums)>20:
                print(f"INFO: {c}: low unique-value count ({len(set(nums))})")
        elif nums and bad:
            print(f"WARNING: {c}: mixed numeric/non-numeric values")
    tc=args.time_column
    if tc:
        if tc not in cols:
            print(f"ERROR: time column {tc!r} not found"); raise SystemExit(1)
        seq=[]
        for i,r in enumerate(rows, start=2):
            ok,x=isnum((r.get(tc) or '').strip())
            if not ok:
                print(f"WARNING: {tc}: nonnumeric/nonfinite at CSV row {i}")
            else: seq.append(x)
        if any(b<=a for a,b in zip(seq,seq[1:])):
            print(f"WARNING: {tc}: not strictly increasing")
    print("PASS: structural CSV audit completed; scientific/sensor QC still required.")

if __name__=='__main__': main()

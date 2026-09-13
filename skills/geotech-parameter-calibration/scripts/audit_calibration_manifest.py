#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description="Audit calibration/validation manifest structure and leakage.")
    ap.add_argument("manifest")
    a=ap.parse_args(); d=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
    errors=[]; warnings=[]
    c=list(d.get('calibration_case_ids',[])); v=list(d.get('validation_case_ids',[]))
    if not c: errors.append('no calibration_case_ids')
    if not v: warnings.append('no validation_case_ids; independent validation claim is unavailable')
    overlap=sorted(set(c)&set(v))
    if overlap: errors.append('calibration/validation leakage: '+', '.join(overlap))
    if len(c)!=len(set(c)): warnings.append('duplicate calibration case IDs')
    if len(v)!=len(set(v)): warnings.append('duplicate validation case IDs')
    for i,p in enumerate(d.get('parameters',[])):
        for k in ('name','unit','lower','upper','initial'):
            if k not in p: errors.append(f'parameter[{i}] missing {k}')
        if all(k in p for k in ('lower','upper','initial')):
            lo,hi,x=p['lower'],p['upper'],p['initial']
            if not lo < hi: errors.append(f"{p.get('name',i)}: lower must be < upper")
            if not lo <= x <= hi: errors.append(f"{p.get('name',i)}: initial outside bounds")
            if x==lo or x==hi: warnings.append(f"{p.get('name',i)}: initial is exactly on a bound")
    if not d.get('objective'): errors.append('missing objective')
    if not d.get('validation_type'): warnings.append('validation_type not declared')
    print(f"Calibration cases: {len(c)} | Validation cases: {len(v)} | Parameters: {len(d.get('parameters',[]))}")
    for x in warnings: print('WARNING:',x)
    for x in errors: print('ERROR:',x)
    if not errors: print('PASS: manifest structure and case separation checks passed.')
    raise SystemExit(1 if errors else 0)
if __name__=='__main__': main()

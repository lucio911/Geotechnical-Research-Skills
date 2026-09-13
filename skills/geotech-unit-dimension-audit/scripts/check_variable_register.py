#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Check completeness of a geotechnical variable/unit register.')
    ap.add_argument('register'); a=ap.parse_args()
    d=json.loads(Path(a.register).read_text(encoding='utf-8'))
    errors=[]; warnings=[]; seen=set()
    for i,v in enumerate(d.get('variables',[])):
        for k in ('symbol','meaning','dimension','unit'):
            if not v.get(k): errors.append(f'variable[{i}] missing {k}')
        s=v.get('symbol')
        if s in seen: errors.append(f'duplicate symbol: {s}')
        seen.add(s)
        if v.get('dimension')=='1' and v.get('unit') not in ('1','-','dimensionless'):
            warnings.append(f"{s}: dimensionless variable has unit {v.get('unit')!r}")
        if (s and ('_' in s or '/' in v.get('meaning','').lower() or 'normalized' in v.get('meaning','').lower())) and v.get('dimension')=='1' and not v.get('reference'):
            warnings.append(f'{s}: normalized/dimensionless quantity may need an explicit reference state')
        if 'stress' in v.get('meaning','').lower() or 'pressure' in v.get('meaning','').lower():
            if not v.get('stress_measure'):
                warnings.append(f'{s}: stress/pressure variable does not declare total/effective/reference measure')
    if not d.get('variables'): errors.append('no variables')
    print(f"Variables: {len(d.get('variables',[]))}")
    for x in warnings: print('WARNING:',x)
    for x in errors: print('ERROR:',x)
    if not errors: print('PASS: variable-register metadata check passed.')
    raise SystemExit(1 if errors else 0)
if __name__=='__main__': main()

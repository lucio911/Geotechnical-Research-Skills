#!/usr/bin/env python3
from __future__ import annotations
import csv, json, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CAL=ROOT/'skills/geotech-parameter-calibration/scripts/audit_calibration_manifest.py'
UNIT=ROOT/'skills/geotech-unit-dimension-audit/scripts/check_variable_register.py'
CSV=ROOT/'skills/geotech-data-qc/scripts/audit_csv.py'

def run(cmd):
    return subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

def main():
    errors=[]
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        # calibration leakage must fail
        m={
          'parameters':[{'name':'a','unit':'1','lower':0,'upper':1,'initial':0.5}],
          'calibration_case_ids':['A','B'], 'validation_case_ids':['B','C'],
          'objective':'SSE','validation_type':'independent-held-out'
        }
        mp=td/'bad_manifest.json'; mp.write_text(json.dumps(m),encoding='utf-8')
        r=run([sys.executable,str(CAL),str(mp)])
        if r.returncode==0 or 'leakage' not in r.stdout:
            errors.append('calibration leakage negative test failed')

        # missing unit metadata must fail
        u={'variables':[{'symbol':'x','meaning':'displacement','dimension':'L'}]}
        up=td/'bad_units.json'; up.write_text(json.dumps(u),encoding='utf-8')
        r=run([sys.executable,str(UNIT),str(up)])
        if r.returncode==0 or 'missing unit' not in r.stdout:
            errors.append('unit-register negative test failed')

        # non-monotonic time should be flagged (warning, not structural failure)
        cp=td/'qc.csv'
        with cp.open('w',newline='',encoding='utf-8') as f:
            w=csv.writer(f); w.writerow(['time','force']); w.writerows([[0,1],[1,2],[1,2],[0.5,3]])
        r=run([sys.executable,str(CSV),str(cp),'--time-column','time'])
        if 'not strictly increasing' not in r.stdout or 'duplicate rows' not in r.stdout:
            errors.append('CSV QC warning test failed')

    if errors:
        for e in errors: print('ERROR:',e)
        raise SystemExit(1)
    print('Quantitative-Core negative tests passed')

if __name__=='__main__': main()

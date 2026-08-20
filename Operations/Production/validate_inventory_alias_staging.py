#!/usr/bin/env python3
from pathlib import Path
import csv

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
STAGING = ROOT / 'Operations/Research/2026-08-20_Inventory_Alias_Staging_17_30.csv'
OPTIONS = ROOT / 'Operations/Research/2026-08-20_10_Cases_Resolution_Options.csv'

def read(p):
    with p.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

staging = read(STAGING)
options = read(OPTIONS)
if len(staging) != 33:
    raise SystemExit(f'staging_rows={len(staging)} expected=33')
if len(options) != 10:
    raise SystemExit(f'option_cases={len(options)} expected=10')
if any(r.get('CNT_Creation_Allowed') != 'No' for r in staging):
    raise SystemExit('staging contains a row allowing CNT creation')
if any(not r.get('Local_Evidence_Paths') or not r.get('Local_Evidence_SHA256') for r in staging):
    raise SystemExit('staging row lacks local evidence path or hash')
if any(not r.get('Recommended_Option') or not r.get('Next_Action') for r in options):
    raise SystemExit('resolution option lacks recommendation or next action')
print('validation=PASS staging_rows=33 option_cases=10 cnt_creation_allowed=NONE missing_evidence_hashes=0 options_complete=PASS')

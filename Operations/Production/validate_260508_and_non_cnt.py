#!/usr/bin/env python3
from pathlib import Path
import csv

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
with (ROOT / 'Operations/Research/2026-08-20_Source_Alias_Table.csv').open(newline='', encoding='utf-8-sig') as f:
    aliases = list(csv.DictReader(f))
with (ROOT / 'Operations/Research/2026-08-20_NonCNT_Inventory_Alias_Approval.csv').open(newline='', encoding='utf-8-sig') as f:
    noncnt = list(csv.DictReader(f))

expected = {'ALIAS-0036': 'CNT-042', 'ALIAS-0047': 'CNT-043'}
for aid, inv in expected.items():
    rows = [r for r in aliases if r.get('Alias_ID') == aid]
    if len(rows) != 1 or rows[0].get('Inventory_ID') != inv or rows[0].get('Confidence') != 'High':
        raise SystemExit(f'{aid} mapping invalid')
if len(noncnt) != 8:
    raise SystemExit(f'noncnt_rows={len(noncnt)} expected=8')
if any(r.get('Approval_Status') != 'Pending_Admin_Approval' for r in noncnt):
    raise SystemExit('a non-CNT row is not pending approval')
if any(r.get('CNT_Creation_Allowed') != 'No' or r.get('Canon_Impact') != 'None' for r in noncnt):
    raise SystemExit('non-CNT guard failed')
print('validation=PASS aliases_260508=2 noncnt_pending=8 cnt_creation=NONE canon_impact=NONE')

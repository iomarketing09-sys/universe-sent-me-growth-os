#!/usr/bin/env python3
from pathlib import Path
import csv

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
PATH = ROOT / 'Operations/Research/2026-08-20_NonCNT_Inventory_Alias_Approval.csv'
with PATH.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
for row in rows:
    row['Approval_Status'] = 'Approved_Admin'
    row['Notes'] = 'Administrative alias normalization approved by Fernando; no CNT creation, no canon change, no creative inventory mutation.'
with PATH.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n')
    writer.writeheader(); writer.writerows(rows)
print(f'approved_rows={len(rows)} cnt_creation=NONE canon_impact=NONE')

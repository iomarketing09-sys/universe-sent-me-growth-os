#!/usr/bin/env python3
from pathlib import Path
import csv
ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
SRC = ROOT / 'Operations/Research/2026-08-20_17_30_Alias_Evidence_Enriched.csv'
with SRC.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
for r in rows:
    if r.get('Resolution_Status') == 'Evidence_Not_Found_Local':
        print(' | '.join([r.get('Alias_ID',''), r.get('Publication_ID',''), r.get('Publication_Asset_Ref',''), r.get('Meta_Post_ID',''), r.get('Fecha_Planeada_Local',''), r.get('Permalink','')]))

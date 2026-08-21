from pathlib import Path
import csv, json

p = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-20_Overlay_Wave1_Calendario_17_30.csv')
with p.open(newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f, restkey='_extra')
    rows = list(reader)
for idx, row in enumerate(rows, start=2):
    if row.get('_extra') is not None:
        print(json.dumps({'line': idx, 'overlay_id': row.get('Overlay_ID'), 'extra': row.get('_extra'), 'rationale': row.get('Rationale')}, ensure_ascii=False))

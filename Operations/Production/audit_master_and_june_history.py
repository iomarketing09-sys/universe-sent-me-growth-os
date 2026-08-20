#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import csv
import json

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
paths = [
    ROOT / 'GrowthOS/Content_Inventory.csv',
    ROOT / 'Operations/Research/2026-08-15_Publication_Log.csv',
    ROOT / 'Operations/Research/2026-08-15_ExperimentLog.csv',
    ROOT / 'Operations/Research/Historical_Performance_Individuals.csv',
    ROOT / 'Operations/Research/Historical_Asset_Performance.csv',
    ROOT / 'Operations/Research/Historical_Performance_Snapshot.csv',
]

def read_csv(path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

summary = {}
for path in paths:
    if not path.exists():
        summary[str(path.relative_to(ROOT))] = {'exists': False}
        continue
    rows = read_csv(path)
    headers = list(rows[0].keys()) if rows else []
    summary[str(path.relative_to(ROOT))] = {'exists': True, 'rows': len(rows), 'headers': headers}

hist_path = ROOT / 'Operations/Research/Historical_Performance_Individuals.csv'
hist = read_csv(hist_path) if hist_path.exists() else []
meta_fields = ['meta_id', 'Meta_Post_ID', 'meta_publication_id', 'Post_ID', 'Facebook_Post_ID', 'Meta_ID']
meta_field = next((f for f in meta_fields if hist and f in hist[0]), None)
duplicates = {}
if meta_field:
    counter = Counter((r.get(meta_field) or '').strip() for r in hist if (r.get(meta_field) or '').strip())
    duplicates = {k: v for k, v in counter.items() if v > 1}

inventory_path = ROOT / 'GrowthOS/Content_Inventory.csv'
inv = read_csv(inventory_path) if inventory_path.exists() else []
inv_headers = list(inv[0].keys()) if inv else []
log_path = ROOT / 'Operations/Research/2026-08-15_Publication_Log.csv'
log = read_csv(log_path) if log_path.exists() else []
asset_fields = [f for f in ['Asset_Ref', 'Asset_Filename', 'Filename', 'filename', 'Asset_ID'] if f in inv_headers]
log_asset_fields = [f for f in ['Asset_Ref', 'Asset_Filename', 'Filename', 'filename', 'Asset_ID'] if log and f in log[0]]
inv_assets = {str(r.get(f, '')).strip() for f in asset_fields for r in inv if str(r.get(f, '')).strip()}
log_assets = {str(r.get(f, '')).strip() for f in log_asset_fields for r in log if str(r.get(f, '')).strip()}

report = {
    'summary': summary,
    'historical_meta_field': meta_field,
    'historical_duplicate_meta_ids': duplicates,
    'inventory_asset_fields': asset_fields,
    'publication_log_asset_fields': log_asset_fields,
    'publication_asset_values_not_in_inventory': sorted(log_assets - inv_assets),
    'inventory_asset_values_not_in_publication_log': sorted(inv_assets - log_assets),
}
out = ROOT / 'Operations/Research/2026-08-20_Auditoria_Fuente_Maestra_Junio.json'
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))

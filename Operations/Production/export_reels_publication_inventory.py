import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Operations/Research/2026-08-19_Historial_Reels_Consolidado.json'
OUTPUT = ROOT / 'Operations/Research/2026-08-21_Reels_Publication_Inventory.csv'

fields = [
    'Reel_Record_ID', 'Platform', 'Platform_Content_ID', 'Meta_Reel_ID',
    'Publication_UTC', 'Concept_ID', 'Title_or_Caption', 'Character',
    'Content_Type', 'Evidence_Status', 'Drive_Evidence_Status',
    'Experiment_ID', 'Hypothesis_ID', 'Crosspost_Status',
    'Production_Status', 'Publication_Status', 'Metrics_Status',
    'Views', 'Reach', 'Engagement', 'Source', 'Last_Sync'
]

data = json.loads(SOURCE.read_text(encoding='utf-8'))
rows = []
for idx, record in enumerate(data.get('records', []), start=1):
    drive_status = 'Confirmed_or_documented' if record.get('drive_asset_evidence') else 'Not_confirmed'
    experiment_id = record.get('experiment_id') or ''
    hypothesis_ids = record.get('hypothesis_ids') or []
    rows.append({
        'Reel_Record_ID': f"REEL-{idx:03d}",
        'Platform': record.get('platform', ''),
        'Platform_Content_ID': record.get('content_id', ''),
        'Meta_Reel_ID': record.get('meta_reel_id', ''),
        'Publication_UTC': record.get('published_at', ''),
        'Concept_ID': record.get('canonical_concept_id', ''),
        'Title_or_Caption': ' '.join((record.get('title_or_caption') or '').split()),
        'Character': record.get('character', ''),
        'Content_Type': record.get('content_type', ''),
        'Evidence_Status': record.get('evidence_status', ''),
        'Drive_Evidence_Status': drive_status,
        'Experiment_ID': experiment_id if experiment_id != 'Sin_etiqueta_historica' else '',
        'Hypothesis_ID': '|'.join(hypothesis_ids),
        'Crosspost_Status': record.get('crosspost_status', '') or '',
        'Production_Status': 'Published_Historical',
        'Publication_Status': 'Published' if record.get('is_published', True) else 'Unknown',
        'Metrics_Status': record.get('metrics_status', 'Historical_snapshot_or_partial'),
        'Views': '' if record.get('views') is None else record.get('views'),
        'Reach': '' if record.get('reach') is None else record.get('reach'),
        'Engagement': '' if record.get('engagement') is None else record.get('engagement'),
        'Source': record.get('source', ''),
        'Last_Sync': data.get('last_updated', ''),
    })

with OUTPUT.open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

print(json.dumps({'output': str(OUTPUT), 'rows': len(rows), 'columns': len(fields)}, ensure_ascii=False))

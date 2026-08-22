import csv
import json
import re
from pathlib import Path

history_path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-19_Historial_Reels_Consolidado.json')
candidate_path = Path('/home/ubuntu/meta_historical_video_candidates.csv')
data = json.loads(history_path.read_text(encoding='utf-8'))
records = data.setdefault('records', [])
existing = {r.get('content_id') for r in records}

with candidate_path.open(encoding='utf-8', newline='') as handle:
    candidates = list(csv.DictReader(handle))

added = []
for c in candidates:
    content_id = c['Page_Post_ID']
    if content_id in existing:
        continue
    reel_match = re.search(r'/reel/(\d+)', c.get('Permalink_URL') or '')
    reel_id = reel_match.group(1) if reel_match else ''
    interaction = sum(int(c.get(k) or 0) for k in ['Reactions', 'Comments', 'Shares'])
    message = c.get('Message') or ''
    qualification = 'Historical_identity_only; no_clean_comparable_verdict'
    if 'http://' in message or 'https://' in message:
        qualification = 'Exclude_from_clean_editorial_comparables_until_external_url_treatment_is_coded'
    record = {
        'platform': 'Facebook',
        'content_id': content_id,
        'published_at': c.get('Created_UTC'),
        'content_type': 'Reel',
        'title_or_caption': message,
        'character': 'Sin_clasificar',
        'canonical_concept_id': '',
        'engagement': interaction,
        'views': None,
        'reach': None,
        'source': 'Meta historical feed 2026-05/06; video attachment confirmed',
        'evidence_status': 'Confirmado_por_Meta_API;_asset_pendiente',
        'drive_asset_evidence': None,
        'content_asset_id': None,
        'experiment_id': '',
        'hypothesis_ids': [],
        'experiment_evidence': 'No se infiere hipótesis, CNT o concepto canónico desde el feed histórico.',
        'reconciliation_decision': 'Meta_Publicacion_Confirmada_Asset_Pendiente',
        'crosspost_status': 'No_auditado',
        'meta_reel_id': reel_id,
        'permalink_url': c.get('Permalink_URL'),
        'is_published': True,
        'metrics_status': 'Meta_interactions_current_feed_snapshot; views_reach_retention_pending',
        'editorial_qualification': qualification,
        'asset_match_status': 'Pending_Drive_or_local_asset_match',
    }
    records.append(record)
    added.append(content_id)

# Preserve the earliest integrated record date and the current local audit date.
data['period'] = {'start': '2026-05-01', 'end': '2026-08-21'}
data['last_updated'] = '2026-08-21'
data['version'] = '1.7'
data['historical_candidate_note'] = 'All 54 Meta video candidates from May/June are now represented as publication-identity rows. Only exact Drive matches receive Drive evidence; unresolved assets remain pending and are not converted into CNT or canonical concepts.'
history_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'candidate_rows': len(candidates), 'added': len(added), 'total_records': len(records), 'version': data['version']}, ensure_ascii=False))

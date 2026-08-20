import csv
import json
from datetime import date
from pathlib import Path

root = Path('/home/ubuntu/universe-sent-me-growth-os')
log_path = root / 'Operations/Research/2026-08-15_Publication_Log.csv'
out_path = root / 'Operations/Research/2026-08-20_Cohorte_17_30_Candidates.json'
start = date(2026, 8, 17)
end = date(2026, 8, 30)
rows = []
with log_path.open(newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        date_text = r.get('Fecha_Publicacion_Local') or r.get('fecha_publicacion_local') or r.get('Fecha_Programada_Local') or ''
        try:
            d = date.fromisoformat(date_text[:10])
        except Exception:
            continue
        if not (start <= d <= end):
            continue
        status = (r.get('Estado_Publicacion') or r.get('estado_publicacion') or '').lower()
        meta_id = r.get('Meta_Post_ID') or r.get('meta_post_id') or r.get('Meta_ID') or ''
        if 'public' not in status or not meta_id:
            continue
        rows.append({
            'publication_id': r.get('Publication_ID') or r.get('publicacion_id') or '',
            'cnt_id': r.get('CNT_ID') or r.get('id_pieza') or '',
            'asset_ref': r.get('Asset_Ref') or r.get('asset_ref') or '',
            'asset_filename': r.get('Asset_Filename') or r.get('asset_filename') or '',
            'platform': r.get('Plataforma') or r.get('platform') or '',
            'published_date_local': date_text,
            'slot_local': r.get('Hora_Publicacion_Local') or r.get('slot_local') or '',
            'meta_post_id': meta_id,
            'status': r.get('Estado_Publicacion') or r.get('estado_publicacion') or '',
        })
# De-duplicate by meta id, preserving first operational row.
seen = set(); unique = []
for r in rows:
    if r['meta_post_id'] in seen: continue
    seen.add(r['meta_post_id']); unique.append(r)
out = {'scope': '2026-08-17 through 2026-08-30', 'candidate_count': len(unique), 'candidates': unique}
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=2))

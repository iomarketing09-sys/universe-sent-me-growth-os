import csv
import json
import subprocess
from pathlib import Path

root = Path('/home/ubuntu/universe-sent-me-growth-os')
raw_path = root / 'Operations/Research/2026-08-20_Cohorte_17_30_Meta_Raw_Current.json'
log_path = root / 'Operations/Research/2026-08-15_Publication_Log.csv'
p0_ids = {
    '1036844829507460_122151373701072582',
    '1036844829507460_122151373761072582',
    '1036844829507460_122151373833072582',
    '1036844829507460_122151373893072582',
    '1036844829507460_122151373953072582',
}
marker = '[METRICS-RUN:20260821T032233Z]'
raw = json.loads(raw_path.read_text(encoding='utf-8'))
meta_map = {p.get('id'): p for p in raw.get('data', []) if p.get('id') and p.get('id') not in p0_ids}

with log_path.open(newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    rows = list(reader)

baseline_bytes = subprocess.check_output(['git', 'show', f'HEAD:{log_path.relative_to(root)}'])
baseline_rows = list(csv.DictReader(baseline_bytes.decode('utf-8-sig').splitlines()))
baseline_by_pub = {r.get('Publicacion_ID'): r for r in baseline_rows}
restored_p0 = []
updated = []
for r in rows:
    pid = r.get('Meta_Post_ID', '')
    pub_id = r.get('Publicacion_ID')
    if pid in p0_ids and pub_id in baseline_by_pub:
        r.clear(); r.update(baseline_by_pub[pub_id])
        restored_p0.append(pid)
        continue
    p = meta_map.get(pid)
    if not p or not p.get('is_published'):
        continue
    r['Estado_Publicacion'] = 'Publicado'
    r['Fecha_Publicacion_Local'] = p.get('created_time', '')[:10]
    if p.get('permalink_url'):
        r['Permalink'] = p['permalink_url']
    notes = r.get('Notas', '')
    if marker not in notes:
        r['Notas'] = f'{notes} {marker} Estado actualizado a Publicado y permalink verificado en el corte actual.'
    updated.append(pid)

with log_path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader(); writer.writerows(rows)
print(json.dumps({'updated_non_p0_rows': len(updated), 'restored_p0_rows': len(restored_p0), 'current_marker_count': sum(marker in r.get('Notas', '') for r in rows)}, ensure_ascii=False, indent=2))

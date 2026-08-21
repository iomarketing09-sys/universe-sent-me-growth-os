import csv
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

root = Path('/home/ubuntu/universe-sent-me-growth-os')
raw_path = root / 'Operations/Research/2026-08-20_Cohorte_17_30_Meta_Raw_Current.json'
summary_path = root / 'Operations/Research/2026-08-20_Cohorte_17_30_Current_Cut.json'
log_path = root / 'Operations/Research/2026-08-15_ExperimentLog.csv'
run_id = '20260821T032233Z'
local_tz = timezone(timedelta(hours=-5))
p0_ids = {
    '1036844829507460_122151373701072582',
    '1036844829507460_122151373761072582',
    '1036844829507460_122151373833072582',
    '1036844829507460_122151373893072582',
    '1036844829507460_122151373953072582',
}

raw = json.loads(raw_path.read_text(encoding='utf-8'))
summary = json.loads(summary_path.read_text(encoding='utf-8'))
meta_map = {p.get('id'): p for p in raw.get('data', []) if p.get('id') and '/reel/' not in (p.get('permalink_url') or '') and p.get('id') not in p0_ids}

with log_path.open(newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    rows = list(reader)

baseline_bytes = subprocess.check_output(['git', 'show', f'HEAD:{log_path.relative_to(root)}'])
baseline_rows = list(csv.DictReader(baseline_bytes.decode('utf-8-sig').splitlines()))
baseline_by_obs = {r.get('Observacion_ID'): r for r in baseline_rows}

restored_p0 = []
updated = []
for r in rows:
    obs = r.get('Observacion_ID', '')
    pid = r.get('Meta_ID', '')
    if pid in p0_ids and obs in baseline_by_obs:
        r.clear(); r.update(baseline_by_obs[obs]); restored_p0.append(obs)
        continue
    p = meta_map.get(pid)
    if not p or not p.get('is_published'):
        continue
    created = datetime.fromisoformat(p['created_time'].replace('Z', '+00:00')).astimezone(local_tz)
    r['Estado_Publicacion'] = 'Publicado'
    r['Hora_Real'] = created.strftime('%H:%M:%S')
    r['Veredicto'] = 'Corte_Observado_Lifetime'
    reactions = p.get('reactions', {}).get('summary', {}).get('total_count', 0) or 0
    comments = p.get('comments', {}).get('summary', {}).get('total_count', 0) or 0
    shares = p.get('shares', {}).get('count', 0) or 0
    r['Conclusion'] = f"Corte observado {run_id}: {reactions} reacciones, {comments} comentarios, {shares} shares; no es snapshot exacto 24/72h."
    r['Proxima_Accion'] = 'Mantener separado de P0, Reels y afiliados; continuar con el siguiente corte observado.'
    marker = f'Current_Cut:{run_id}'
    if marker not in r.get('Fuente', ''):
        r['Fuente'] = f"{r.get('Fuente', '')}; Operations/Research/2026-08-20_Cohorte_17_30_Current_Cut.json; {marker}"
    updated.append(pid)

with log_path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader(); writer.writerows(rows)

print(json.dumps({'updated_non_p0_rows': len(updated), 'restored_p0_rows': len(restored_p0), 'p0_isolated': True, 'aggregate_preserved': any(r.get('Observacion_ID') == 'COHORT-17_30-CUT-20260821' for r in rows), 'aggregate': summary['overall']}, ensure_ascii=False, indent=2))

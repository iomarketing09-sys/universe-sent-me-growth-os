import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

root = Path('/home/ubuntu/universe-sent-me-growth-os')
evidence_path = root / 'Operations/Research/2026-08-19_P0_Next_Cut_Evidence.json'
log_path = root / 'Operations/Research/2026-08-15_Publication_Log.csv'
out_json = root / 'Operations/Research/2026-08-20_Cohorte_15_16_Analysis.json'
out_md = root / 'Operations/Research/2026-08-20_Cohorte_15_16_Analysis.md'

raw = json.loads(evidence_path.read_text(encoding='utf-8'))
rows = []
for c in raw.get('candidates', []):
    ev = c.get('evidence', {})
    totals = ev.get('lifetime_totals', {})
    pub_id = c.get('publicacion_id')
    rows.append({
        'publicacion_id': pub_id,
        'cnt_id': c.get('id_pieza'),
        'meta_post_id': c.get('meta_post_id'),
        'published_at_utc': c.get('published_at_utc'),
        'age_hours': c.get('age_hours'),
        'reactions': totals.get('reactions', 0),
        'comments': totals.get('comments', 0),
        'shares': totals.get('shares', 0),
        'interactions': totals.get('interactions', 0),
        'exact_window_available': ev.get('exact_window_available', False),
    })

# Join operational fields when available.
with log_path.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    log_rows = list(reader)
for r in rows:
    matches = [x for x in log_rows if x.get('Publication_ID') == r['publicacion_id'] or x.get('publicacion_id') == r['publicacion_id']]
    if not matches:
        matches = [x for x in log_rows if x.get('Meta_Post_ID') == r['meta_post_id'] or x.get('meta_post_id') == r['meta_post_id']]
    if matches:
        x = matches[0]
        r['asset_ref'] = x.get('Asset_Ref') or x.get('asset_ref') or x.get('Asset_Filename') or ''
        r['asset_filename'] = x.get('Asset_Filename') or x.get('asset_filename') or ''
        r['slot_local'] = x.get('Hora_Publicacion_Local') or x.get('slot_local') or x.get('Hora_Programada_Local') or ''
        r['content_type'] = x.get('Tipo_Contenido') or x.get('content_type') or ''
        r['format'] = x.get('Formato') or x.get('format') or ''
    else:
        r.update({'asset_ref':'', 'asset_filename':'', 'slot_local':'', 'content_type':'', 'format':''})

# Derive local slot from UTC when no operational slot exists.
from datetime import datetime, timezone, timedelta
for r in rows:
    if not r['slot_local']:
        dt = datetime.fromisoformat(r['published_at_utc'].replace('Z', '+00:00'))
        local = dt.astimezone(timezone(timedelta(hours=-5)))
        r['slot_local'] = local.strftime('%H:%M')
    else:
        r['slot_local'] = r['slot_local'][:5]

by_slot = defaultdict(list)
for r in rows:
    by_slot[r['slot_local']].append(r['interactions'])

summary = {
    'cohort': 'PUB-FB-15_16-01 through PUB-FB-15_16-09',
    'scope': 'Nine Facebook publications from 15–16 August 2026',
    'window_note': 'Observed lifetime totals at extraction time; not exact 24h/72h snapshots',
    'n': len(rows),
    'totals': {k: sum(r[k] for r in rows) for k in ['reactions','comments','shares','interactions']},
    'mean_interactions': statistics.mean(r['interactions'] for r in rows) if rows else 0,
    'median_interactions': statistics.median(r['interactions'] for r in rows) if rows else 0,
    'min_interactions': min((r['interactions'] for r in rows), default=0),
    'max_interactions': max((r['interactions'] for r in rows), default=0),
    'by_slot': {k: {'n': len(v), 'mean_interactions': statistics.mean(v), 'median_interactions': statistics.median(v), 'total_interactions': sum(v)} for k, v in sorted(by_slot.items())},
    'rows': rows,
}
out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

md = []
md.append('---')
md.append('title: "Análisis de la cohorte Facebook 15–16 de agosto"')
md.append('purpose: "Comparar la cohorte de nueve publicaciones del 15–16 con evidencia observada de Meta, sin mezclarla con P0 ni sustituir ventanas 24/72h."')
md.append('status: "Active"')
md.append('created: 2026-08-20')
md.append('updated: 2026-08-20')
md.append('version: "1.0"')
md.append('author: "Manus AI (CGO)"')
md.append('related_documents:')
md.append('  - "Operations/Research/2026-08-19_P0_Next_Cut_Evidence.json"')
md.append('  - "Operations/Research/2026-08-15_Publication_Log.csv"')
md.append('  - "Operations/Research/2026-08-19_P0_Corte_17_Agosto.md"')
md.append('organization: "Operations/Research"')
md.append('---\n')
md.append('# Resumen')
md.append(f"La cohorte contiene **{len(rows)} publicaciones** y registra **{summary['totals']['interactions']} interacciones observadas**: {summary['totals']['reactions']} reacciones, {summary['totals']['comments']} comentarios y {summary['totals']['shares']} compartidos.")
md.append('Estas cifras son acumulados lifetime observados en la consulta de Meta, no snapshots exactos de 24/72 horas.')
md.append('\n## Desglose por publicación\n')
md.append('| Publicación | CNT | Asset | Slot local | Reacciones | Comentarios | Compartidos | Interacciones |')
md.append('|---|---|---|---:|---:|---:|---:|---:|')
for r in rows:
    md.append(f"| {r['publicacion_id']} | {r['cnt_id']} | {r['asset_ref'] or r['asset_filename'] or 'No enlazado'} | {r['slot_local']} | {r['reactions']} | {r['comments']} | {r['shares']} | {r['interactions']} |")
md.append('\n## Lectura estadística\n')
md.append(f"La media fue de **{summary['mean_interactions']:.1f} interacciones por publicación** y la mediana de **{summary['median_interactions']:.1f}**. La diferencia entre media y mediana indica concentración en piezas de mayor rendimiento; no debe usarse la media sola para representar la cohorte.")
md.append('\n## Cautelas\n')
md.append('No se deben hacer inferencias causales sobre horario, formato o personajes sin una taxonomía completa y sin snapshots temporales equivalentes. Esta cohorte sirve como corte observado comparativo y como base para priorizar qué piezas merecen revisión editorial.')
md.append('\n## Fuentes\n')
md.append('- Evidencia de Meta conservada en `Operations/Research/2026-08-19_P0_Next_Cut_Evidence.json`.')
md.append('- Registros operativos en `Operations/Research/2026-08-15_Publication_Log.csv`.')
out_md.write_text('\n'.join(md) + '\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))

import csv
import json
import statistics
from collections import defaultdict
from datetime import datetime, timezone, timedelta, date
from pathlib import Path

root = Path('/home/ubuntu/universe-sent-me-growth-os')
raw_path = root / 'Operations/Research/2026-08-20_Cohorte_17_30_Meta_Raw_Current.json'
log_path = root / 'Operations/Research/2026-08-15_Publication_Log.csv'
out_json = root / 'Operations/Research/2026-08-20_Cohorte_17_30_Current_Cut.json'
out_md = root / 'Operations/Research/2026-08-20_Cohorte_17_30_Current_Cut.md'
previous_path = root / 'Operations/Research/2026-08-20_Cohorte_17_30_Actual_Cut.json'

p0_ids = {
    '1036844829507460_122151373701072582',
    '1036844829507460_122151373761072582',
    '1036844829507460_122151373833072582',
    '1036844829507460_122151373893072582',
    '1036844829507460_122151373953072582',
}
local_tz = timezone(timedelta(hours=-5))
raw = json.loads(raw_path.read_text(encoding='utf-8'))

log_map = {}
with log_path.open(newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        meta = r.get('Meta_Post_ID') or r.get('meta_post_id') or ''
        if meta:
            log_map[meta] = r

rows = []
video_rows = []
for p in raw.get('data', []):
    pid = p.get('id', '')
    if pid in p0_ids:
        continue
    created = datetime.fromisoformat(p['created_time'].replace('Z', '+00:00'))
    local = created.astimezone(local_tz)
    if not (date(2026, 8, 17) <= local.date() <= date(2026, 8, 30)):
        continue
    log = log_map.get(pid, {})
    content_format = 'Reel' if '/reel/' in (p.get('permalink_url') or '') else 'Image'
    reactions = p.get('reactions', {}).get('summary', {}).get('total_count', 0) or 0
    comments = p.get('comments', {}).get('summary', {}).get('total_count', 0) or 0
    shares = p.get('shares', {}).get('count', 0) or 0
    row = {
        'meta_post_id': pid,
        'created_time_utc': p.get('created_time'),
        'created_time_local': local.isoformat(),
        'date_local': local.date().isoformat(),
        'slot_local': local.strftime('%H:%M'),
        'message': p.get('message', ''),
        'permalink_url': p.get('permalink_url', ''),
        'is_published': p.get('is_published'),
        'asset_ref': log.get('Asset_Ref', ''),
        'publication_id': log.get('Publicacion_ID', ''),
        'reactions': reactions,
        'comments': comments,
        'shares': shares,
        'interactions': reactions + comments + shares,
        'content_format': content_format,
    }
    if content_format == 'Reel':
        video_rows.append(row)
    else:
        rows.append(row)
rows.sort(key=lambda r: r['created_time_local'])
video_rows.sort(key=lambda r: r['created_time_local'])

def agg(group):
    vals = [r['interactions'] for r in group]
    return {
        'n': len(group),
        'reactions': sum(r['reactions'] for r in group),
        'comments': sum(r['comments'] for r in group),
        'shares': sum(r['shares'] for r in group),
        'interactions': sum(vals),
        'mean_interactions': statistics.mean(vals) if vals else 0,
        'median_interactions': statistics.median(vals) if vals else 0,
    }

by_date = defaultdict(list)
by_slot = defaultdict(list)
for r in rows:
    by_date[r['date_local']].append(r)
    by_slot[r['slot_local']].append(r)
summary = {
    'scope': 'Actual Facebook posts local date 2026-08-17 through 2026-08-30, excluding P0 five-post baseline',
    'extraction_time_utc': raw.get('_extraction_meta', {}).get('extracted_at_utc'),
    'window_note': 'Current lifetime totals observed at extraction time; not exact 24h/72h snapshots',
    'p0_excluded_ids': sorted(p0_ids),
    'raw_posts_in_window': len(raw.get('data', [])),
    'raw_image_posts_in_window': len(rows),
    'raw_reels_in_window': len(video_rows),
    'overall': agg(rows),
    'reels_separate': {'n': len(video_rows), 'rows': video_rows, 'note': 'Reels excluded from editorial image aggregate; fields are not treated as comparable image interactions'},
    'by_date': {k: agg(v) for k, v in sorted(by_date.items())},
    'by_slot': {k: agg(v) for k, v in sorted(by_slot.items())},
    'rows': rows,
}
previous_raw_path = root / 'Operations/Research/2026-08-20_Cohorte_17_30_Meta_Raw.json'
if previous_raw_path.exists():
    prev_raw = json.loads(previous_raw_path.read_text(encoding='utf-8'))
    prev_rows = []
    for p in prev_raw.get('data', []):
        pid = p.get('id', '')
        if pid in p0_ids or '/reel/' in (p.get('permalink_url') or ''):
            continue
        created = datetime.fromisoformat(p['created_time'].replace('Z', '+00:00'))
        local = created.astimezone(local_tz)
        if not (date(2026, 8, 17) <= local.date() <= date(2026, 8, 30)):
            continue
        reactions = p.get('reactions', {}).get('summary', {}).get('total_count', 0) or 0
        comments = p.get('comments', {}).get('summary', {}).get('total_count', 0) or 0
        shares = p.get('shares', {}).get('count', 0) or 0
        prev_rows.append({'reactions': reactions, 'comments': comments, 'shares': shares, 'interactions': reactions + comments + shares})
    prev_image = agg(prev_rows)
    summary['comparison_to_previous_cut'] = {
        'previous_extraction_time_utc': prev_raw.get('_extraction_meta', {}).get('extracted_at_utc'),
        'previous_overall': prev_image,
        'previous_scope': 'Previous image-only cut; P0 and Reels excluded',
        'delta_n': summary['overall']['n'] - prev_image.get('n', 0),
        'delta_interactions': summary['overall']['interactions'] - prev_image.get('interactions', 0),
        'delta_reactions': summary['overall']['reactions'] - prev_image.get('reactions', 0),
        'delta_comments': summary['overall']['comments'] - prev_image.get('comments', 0),
        'delta_shares': summary['overall']['shares'] - prev_image.get('shares', 0),
    }
out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

md = []
md += ['---', 'title: "Corte actual de métricas de la cohorte 17–30 de agosto"', 'purpose: "Comparar el estado actual de las publicaciones reales de Facebook de la ola 17–30 con el corte anterior, separando P0 y evitando inferencias de ventanas no disponibles."', 'status: "Active"', 'created: 2026-08-20', 'updated: 2026-08-20', 'version: "1.0"', 'author: "Manus AI (CGO)"', 'related_documents:', '  - "Operations/Research/2026-08-20_Cohorte_17_30_Actual_Cut.md"', '  - "Operations/Research/2026-08-19_P0_Corte_17_Agosto.md"', '  - "Operations/Research/2026-08-15_Publication_Log.csv"', 'organization: "Operations/Research"', '---', '']
md.append('# Alcance')
md.append(f"Se analizaron **{summary['overall']['n']} publicaciones de imagen** visibles en Meta con fecha local entre el 17 y el 30 de agosto, excluyendo los cinco IDs del baseline P0 y separando {summary['raw_reels_in_window']} Reels. El agregado editorial registra **{summary['overall']['interactions']} interacciones observadas**: {summary['overall']['reactions']} reacciones, {summary['overall']['comments']} comentarios y {summary['overall']['shares']} compartidos.")
md.append('Las cifras son acumulados lifetime observados al momento de consulta, no snapshots exactos de 24/72 horas. Los Reels se conservan en `reels_separate` y no se mezclan con el agregado editorial de imágenes.')
md.append('\n## Resumen por fecha local\n')
md.append('| Fecha | Publicaciones | Interacciones | Media | Mediana | Compartidos |')
md.append('|---|---:|---:|---:|---:|---:|')
for k, v in summary['by_date'].items():
    md.append(f"| {k} | {v['n']} | {v['interactions']} | {v['mean_interactions']:.1f} | {v['median_interactions']:.1f} | {v['shares']} |")
md.append('\n## Resumen por horario\n')
md.append('| Horario | Publicaciones | Interacciones | Media | Mediana |')
md.append('|---|---:|---:|---:|---:|')
for k, v in summary['by_slot'].items():
    md.append(f"| {k} | {v['n']} | {v['interactions']} | {v['mean_interactions']:.1f} | {v['median_interactions']:.1f} |")
if 'comparison_to_previous_cut' in summary:
    c = summary['comparison_to_previous_cut']
    md.append('\n## Cambio frente al corte anterior\n')
    md.append(f"El corte anterior registraba {c['previous_overall'].get('n', 0)} publicaciones y {c['previous_overall'].get('interactions', 0)} interacciones. El cambio observado es de **{c['delta_n']} publicaciones** y **{c['delta_interactions']} interacciones** acumuladas.")
md.append('\n## Reels separados\n')
for r in summary['reels_separate']['rows']:
    md.append(f"- {r['created_time_local']} — {r['permalink_url']} — campos observados: {r['reactions']} reacciones, {r['comments']} comentarios, {r['shares']} shares; no se interpreta como rendimiento de imagen.")
md.append('\n## Cautelas\n')
md.append('Este corte no debe compararse con P0 como si fueran ventanas temporales equivalentes. El baseline P0 se excluye del total y se conserva en su reporte separado. Los resultados de horario son descriptivos; no se debe inferir causalidad con franjas que tengan pocas observaciones. Afiliados y métricas de video permanecen fuera de este agregado editorial; los Reels solo se reportan de forma separada.')
md.append('\n## Fuentes\n')
md.append('- Meta Graph API v26, evidencia guardada en `Operations/Research/2026-08-20_Cohorte_17_30_Meta_Raw_Current.json`.')
md.append('- Publication Log para enlazar IDs operativos y assets.')
out_md.write_text('\n'.join(md) + '\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))

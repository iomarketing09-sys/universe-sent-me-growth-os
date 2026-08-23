#!/usr/bin/env python3
"""Reconcile three Meta Facebook Reel posts into the project's primary ledgers."""
import csv
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / 'Operations/Research'
API_PATH = RESEARCH / '2026-08-23_Facebook_Performance_Meta_API.json'
PUB_PATH = RESEARCH / '2026-08-15_Publication_Log.csv'
EXP_PATH = RESEARCH / '2026-08-15_ExperimentLog.csv'
REELS_PATH = RESEARCH / '2026-08-21_Reels_Publication_Inventory.csv'
OUT_PATH = RESEARCH / '2026-08-23_Facebook_Post_Reconciliation.json'
LOCAL_TZ = ZoneInfo('America/Matamoros')

TARGETS = {
    '1036844829507460_122154842337072582': {
        'reel_record_id': 'REEL-103',
        'reel_id': '1581447113440863',
        'concept_id': 'MPM-001',
        'asset_ref': 'MPM-001 — Elara Walk Music',
        'character': 'Elara + Wilfred',
        'experiment_id': 'EXP-2026-08-WEEKLY-CLOSE-01',
        'hypothesis_id': 'HB-REEL-MOTION-POV-MEME-01|HB-REEL-MUSIC-WALK-01',
        'title': 'Ella no está disponible en este plano',
        'source': '2026-08-22_Reels_Meta_Readonly_Reconciliation.json; 2026-08-22_Reels_Confirmed_Metric_Assessment.json; 2026-08-23_Facebook_Performance_Meta_API.json',
    },
    '1036844829507460_122154017667072582': {
        'reel_record_id': 'REEL-003',
        'reel_id': '2005557463434064',
        'concept_id': 'CON-2026-08-21-UniverseSenales',
        'asset_ref': 'Universe viéndote Farmear Aura',
        'character': 'Universe',
        'experiment_id': 'EXP-2026-08-WEEKLY-CLOSE-01',
        'hypothesis_id': 'HB-REEL-MOTION-POV-MEME-01',
        'title': 'Universe viéndote Farmear Aura',
        'source': '2026-08-21_Reels_Publication_Inventory.csv; 2026-08-22_Reels_Meta_Readonly_Reconciliation.json; 2026-08-23_Facebook_Performance_Meta_API.json',
    },
    '1036844829507460_122153750763072582': {
        'reel_record_id': 'REEL-002',
        'reel_id': '2815726225473165',
        'concept_id': 'CON-2026-08-20-RemoteControl-EvanElara',
        'asset_ref': 'CON-2026-08-20-RemoteControl-EvanElara',
        'character': 'Evan + Elara',
        'experiment_id': 'EXP-2026-08-WEEKLY-CLOSE-01',
        'hypothesis_id': 'HB-REEL-MOTION-POV-MEME-01',
        'title': 'Remote Control — Sussie 4 ft. León Larregui',
        'source': '2026-08-21_Reels_Publication_Inventory.csv; 2026-08-22_Reels_Meta_Readonly_Reconciliation.json; 2026-08-23_Facebook_Performance_Meta_API.json',
    },
}


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def write_csv(path, fieldnames, rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def local_info(utc_value):
    parsed = datetime.fromisoformat(utc_value.replace('Z', '+00:00'))
    local = parsed.astimezone(LOCAL_TZ)
    return local.date().isoformat(), local.strftime('%H:%M:%S')

api = json.loads(API_PATH.read_text(encoding='utf-8'))
api_by_id = {post['id']: post for post in api.get('posts', [])}
missing = sorted(set(TARGETS) - set(api_by_id))
if missing:
    raise SystemExit(f'Missing target posts in API snapshot: {missing}')

pub_fields, pub_rows = read_csv(PUB_PATH)
exp_fields, exp_rows = read_csv(EXP_PATH)
reel_fields, reel_rows = read_csv(REELS_PATH)
pub_by_meta = {row.get('Meta_Post_ID', '').strip(): row for row in pub_rows if row.get('Meta_Post_ID')}
exp_meta_ids = {token.strip() for row in exp_rows for token in (row.get('Meta_ID') or '').split('|') if token.strip()}
reel_by_platform_id = {row.get('Platform_Content_ID', '').strip(): row for row in reel_rows if row.get('Platform_Content_ID')}

reconciliation = []
for post_id, meta in TARGETS.items():
    post = api_by_id[post_id]
    date_local, time_local = local_info(post['created_time'])
    reactions = int(post.get('reactions') or 0)
    comments = int(post.get('comments') or 0)
    shares = int(post.get('shares') or 0)
    engagement = reactions + comments + shares
    meta_id_short = post_id.split('_', 1)[-1]
    item = dict(meta)
    item.update({
        'post_id': post_id,
        'created_time_utc': post['created_time'],
        'created_date_local': date_local,
        'created_time_local': time_local,
        'permalink': post.get('permalink_url'),
        'message': post.get('message', ''),
        'reactions': reactions,
        'comments': comments,
        'shares': shares,
        'engagement_public_lifetime_snapshot': engagement,
        'snapshot_retrieved_at': api.get('retrieved_at'),
    })
    reconciliation.append(item)

# Publication Log: one row per Facebook publication, preserving 24/72h fields as null.
for item in reconciliation:
    post_id = item['post_id']
    existing = pub_by_meta.get(post_id)
    notes = (
        f"Reconciliado con el inventario de Reels y Meta Graph API v26.0; snapshot lifetime observable "
        f"{item['engagement_public_lifetime_snapshot']} = {item['reactions']} reacciones + {item['comments']} comentarios + {item['shares']} shares "
        f"(extraído {item['snapshot_retrieved_at']}). No es ventana exacta 24/72h; no se rellenan esos campos."
    )
    source = item['source']
    if existing:
        existing.update({
            'ID_Pieza': item['concept_id'],
            'Asset_Ref': item['asset_ref'],
            'Fecha_Publicacion_Local': item['created_date_local'],
            'Hora_Publicacion_Local': item['created_time_local'],
            'Meta_Post_ID': post_id,
            'Permalink': item['permalink'] or existing.get('Permalink', ''),
            'Estado_Publicacion': 'Publicado',
            'Experiment_ID': item['experiment_id'],
            'Hypothesis_ID': item['hypothesis_id'],
            'Notas': notes,
            'Fuente': source,
        })
        action = 'updated_existing_publication_log_row'
    else:
        publicacion_id = f"PUB-FB-{item['reel_record_id']}"
        row = {field: '' for field in pub_fields}
        row.update({
            'Publicacion_ID': publicacion_id,
            'ID_Pieza': item['concept_id'],
            'Asset_Ref': item['asset_ref'],
            'Plataforma': 'Facebook',
            'Cuenta_ID': '1036844829507460',
            'Fecha_Planeada_Local': '',
            'Hora_Planeada_Local': '',
            'Fecha_Publicacion_Local': item['created_date_local'],
            'Hora_Publicacion_Local': item['created_time_local'],
            'Meta_Post_ID': post_id,
            'Meta_Photo_ID': '',
            'IG_Container_ID': '',
            'IG_Media_ID': '',
            'Permalink': item['permalink'] or '',
            'Estado_Publicacion': 'Publicado',
            'Eliminada': 'No',
            'Drive_Archivado': 'No aplica; Reel separado del asset de Drive',
            'Experiment_ID': item['experiment_id'],
            'Hypothesis_ID': item['hypothesis_id'],
            'Interacciones_24h': '',
            'Interacciones_72h': '',
            'Notas': notes,
            'Fuente': source,
        })
        pub_rows.append(row)
        pub_by_meta[post_id] = row
        action = 'appended_publication_log_row'
    item['publication_log_action'] = action

# Experiment Log: one idempotent reconciliation observation for the three posts.
observation_id = 'OBS-FB-REEL-RECON-20260823'
existing_observation = next((row for row in exp_rows if row.get('Observacion_ID') == observation_id), None)
meta_ids = '|'.join(item['post_id'] for item in reconciliation)
engagement_total = sum(item['engagement_public_lifetime_snapshot'] for item in reconciliation)
median_engagement = sorted(item['engagement_public_lifetime_snapshot'] for item in reconciliation)[1]
shares_pct = round(sum(item['shares'] for item in reconciliation) / engagement_total * 100, 2)
conclusion = (
    f"Los tres posts ya estaban identificados en el inventario especializado de Reels o en el registro maestro, "
    f"pero no estaban enlazados a los ledgers principales. La reconciliación Meta↔Reels↔Publication Log↔ExperimentLog "
    f"queda completa para estos IDs. El snapshot lifetime observable suma {engagement_total} interacciones "
    f"({median_engagement} de mediana) y no constituye un cierre 24/72h ni un veredicto causal."
)
next_action = (
    "Mantener los tres casos como observación L1 de Reels; no mezclar el snapshot lifetime con 24/72h. "
    "Completar ventanas temporales solo si aparece una fuente nativa con fecha de corte explícita y conservar MPM-001 separado por plataforma."
)
exp_row = {field: '' for field in exp_fields}
exp_row.update({
    'Observacion_ID': observation_id,
    'Experiment_ID': 'EXP-2026-08-WEEKLY-CLOSE-01',
    'Hypothesis_ID': 'HB-REEL-MOTION-POV-MEME-01|HB-REEL-MUSIC-WALK-01',
    'Nivel': 'Reconciliación',
    'Fecha_Inicio': min(item['created_date_local'] for item in reconciliation),
    'Fecha_Fin': max(item['created_date_local'] for item in reconciliation),
    'Contenido_Referencia': 'MPM-001 | CON-2026-08-21-UniverseSenales | CON-2026-08-20-RemoteControl-EvanElara',
    'Plataforma': 'Facebook',
    'Formato': 'Reel',
    'Tipo_Contenido': 'Reconciliación_Meta_Reels',
    'Posts_N': '3',
    'Interacciones_Totales': str(engagement_total),
    'Interacciones_Dia': '',
    'Mediana_Interacciones': str(median_engagement),
    'Shares_Interacciones': str(shares_pct),
    'Slot_Planeado': '',
    'Hora_Real': '; '.join(f"{item['concept_id']}={item['created_time_local']}" for item in reconciliation),
    'Meta_ID': meta_ids,
    'Interacciones_24h': '',
    'Interacciones_72h': '',
    'Estado_Canon': 'No_aplica',
    'Estado_Publicacion': 'Publicado_observado',
    'Veredicto': 'Corte_Observado_Lifetime',
    'Conclusion': conclusion,
    'Proxima_Accion': next_action,
    'Fuente': '2026-08-23_Facebook_Post_Reconciliation.json; 2026-08-23_Facebook_Performance_Meta_API.json; 2026-08-21_Reels_Publication_Inventory.csv; 2026-08-22_Reels_Meta_Readonly_Reconciliation.json',
})
if existing_observation:
    existing_observation.update(exp_row)
    exp_action = 'updated_existing_experiment_observation'
else:
    exp_rows.append(exp_row)
    exp_action = 'appended_experiment_observation'

# Specialized Reels inventory: update the two existing rows and add MPM-001 as a new confirmed identity.
for item in reconciliation:
    row = reel_by_platform_id.get(item['post_id'])
    metrics_status = f"Lifetime_public_snapshot_{item['snapshot_retrieved_at'][:10]}; views_reach_retention_not_exposed_by_current_API; 24h_72h_pending"
    if row:
        row.update({
            'Title_or_Caption': item['message'].replace('\n', ' ').strip(),
            'Publication_UTC': item['created_time_utc'],
            'Concept_ID': item['concept_id'],
            'Character': item['character'],
            'Evidence_Status': 'Confirmado_por_Meta_API_y_reconciliacion_GrowthOS',
            'Metrics_Status': metrics_status,
            'Engagement': str(item['engagement_public_lifetime_snapshot']),
            'Source': f"{row.get('Source','')}; 2026-08-23_Facebook_Performance_Meta_API.json".strip('; '),
            'Last_Sync': '2026-08-23',
        })
        item['reels_inventory_action'] = 'updated_existing_reels_inventory_row'
    else:
        row = {field: '' for field in reel_fields}
        row.update({
            'Reel_Record_ID': item['reel_record_id'],
            'Platform': 'Facebook',
            'Platform_Content_ID': item['post_id'],
            'Meta_Reel_ID': item['reel_id'],
            'Publication_UTC': item['created_time_utc'],
            'Concept_ID': item['concept_id'],
            'Title_or_Caption': item['message'].replace('\n', ' ').strip(),
            'Character': item['character'],
            'Content_Type': 'Reel',
            'Evidence_Status': 'Confirmado_por_Meta_API_y_registro_maestro',
            'Drive_Evidence_Status': 'Not_confirmed',
            'Asset_Match_Status': 'Existing_master_record',
            'Asset_Relationship': 'Existing_MPM-001_master_record',
            'Editorial_Qualification': 'Character_POV_reveal;_music_walk_first_variant;_no_causal_verdict',
            'Experiment_ID': item['experiment_id'],
            'Hypothesis_ID': item['hypothesis_id'],
            'Crosspost_Status': 'Facebook_confirmado;_Instagram_crosspost_separado',
            'Production_Status': 'Published_Historical',
            'Publication_Status': 'Published',
            'Metrics_Status': metrics_status,
            'Views': '',
            'Reach': '',
            'Engagement': str(item['engagement_public_lifetime_snapshot']),
            'Source': item['source'],
            'Last_Sync': '2026-08-23',
        })
        reel_rows.append(row)
        reel_by_platform_id[item['post_id']] = row
        item['reels_inventory_action'] = 'appended_existing_master_record_to_reels_inventory'

write_csv(PUB_PATH, pub_fields, pub_rows)
write_csv(EXP_PATH, exp_fields, exp_rows)
write_csv(REELS_PATH, reel_fields, reel_rows)

result = {
    'title': 'Facebook post reconciliation — Meta to Growth OS ledgers',
    'purpose': 'Reconcile three recent Facebook Reel Page Post IDs into primary and specialized ledgers without fabricating 24/72h windows.',
    'status': 'Active',
    'created_at': '2026-08-23',
    'last_updated': '2026-08-23',
    'version': '1.0',
    'author': 'Manus AI',
    'related_documents': [
        'Operations/Research/2026-08-23_Facebook_Performance_Meta_API.json',
        'Operations/Research/2026-08-21_Reels_Publication_Inventory.csv',
        'Operations/Research/2026-08-15_Publication_Log.csv',
        'Operations/Research/2026-08-15_ExperimentLog.csv',
        'GrowthOS/07_00_Registro_Maestro_Reels.md',
        'GrowthOS/Integracion_Growth_OS.md',
    ],
    'source': 'Meta Graph API v26.0 plus existing USM Growth OS records',
    'snapshot_retrieved_at': api.get('retrieved_at'),
    'observation_id': observation_id,
    'experiment_log_action': exp_action,
    'posts': reconciliation,
    'windows_24h_72h': 'kept null; current values are lifetime observable snapshot only',
}
OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({
    'posts_reconciled': len(reconciliation),
    'publication_log_actions': {item['post_id']: item['publication_log_action'] for item in reconciliation},
    'experiment_log_action': exp_action,
    'reels_inventory_actions': {item['post_id']: item['reels_inventory_action'] for item in reconciliation},
    'engagement_total_lifetime_snapshot': engagement_total,
    'output': str(OUT_PATH),
}, ensure_ascii=False, indent=2))

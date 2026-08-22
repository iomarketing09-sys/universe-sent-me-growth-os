from __future__ import annotations

import csv
import json
import math
import statistics
from collections import Counter
from datetime import date, datetime
from zoneinfo import ZoneInfo
from pathlib import Path

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
RESEARCH = ROOT / 'Operations' / 'Research'

BASE_CSV = RESEARCH / '2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv'
REELS_INVENTORY_CSV = RESEARCH / '2026-08-21_Reels_Publication_Inventory.csv'
INDIVIDUALS_CSV = RESEARCH / 'Historical_Performance_Individuals.csv'
JUNE_QUEUE_CSV = RESEARCH / '2026-08-21_Junio_57_Unmatched_Character_Utility.csv'
JULY_EXPANSION_CSV = RESEARCH / '2026-08-21_Julio_Expansion_Individual_Lote01.csv'
JULY_TAX_CSV = RESEARCH / '2026-08-21_Julio_Expansion_Lote01_Taxonomy_Reviewed.csv'
AUG15_16_JSON = RESEARCH / '2026-08-17_Corte_Observado_15_16.json'
P0_SUMMARY_JSON = RESEARCH / '2026-08-19_P0_17_Agosto_Current_Summary.json'
AUG_COHORT_JSON = RESEARCH / '2026-08-20_Cohorte_17_30_Current_Cut.json'
AUG_DAILY_JSON = RESEARCH / '2026-08-21_Corte_Diario_Metricas_2200.json'

OUT_JSON = RESEARCH / '2026-08-22_Comparativa_Junio_Julio_Agosto_Datos.json'
OUT_CSV = RESEARCH / '2026-08-22_Comparativa_Junio_Julio_Agosto_Resumen.csv'
OUT_INTEGRATION_CSV = RESEARCH / '2026-08-22_Comparativa_Junio_Julio_Agosto_Integracion.csv'


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8-sig') as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def num(value, default=0.0):
    if value in (None, ''):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def median_or_none(values):
    return statistics.median(values) if values else None


def p90_or_none(values):
    if not values:
        return None
    values = sorted(values)
    return values[max(0, math.ceil(0.9 * len(values)) - 1)]


def percent_change(old, new):
    if old in (None, 0) or new is None:
        return None
    return (new / old) - 1


def summarize(rows: list[dict], period: str, scope: str) -> dict:
    interactions = [num(row.get('interactions')) for row in rows]
    reactions = [num(row.get('reactions')) for row in rows]
    comments = [num(row.get('comments')) for row in rows]
    shares = [num(row.get('shares')) for row in rows]
    dates = sorted({row.get('date') for row in rows if row.get('date')})
    n = len(rows)
    total_interactions = sum(interactions)
    return {
        'period': period,
        'scope': scope,
        'posts': n,
        'date_min': dates[0] if dates else None,
        'date_max': dates[-1] if dates else None,
        'active_days': len(dates),
        'posts_per_active_day': n / len(dates) if dates else None,
        'interactions_total': total_interactions,
        'interactions_per_active_day': total_interactions / len(dates) if dates else None,
        'interactions_mean': statistics.mean(interactions) if interactions else None,
        'interactions_median': median_or_none(interactions),
        'interactions_p90': p90_or_none(interactions),
        'reactions_total': sum(reactions),
        'comments_total': sum(comments),
        'shares_total': sum(shares),
        'reactions_median': median_or_none(reactions),
        'comments_median': median_or_none(comments),
        'shares_median': median_or_none(shares),
        'shares_per_interaction': sum(shares) / total_interactions if total_interactions else None,
        'comments_per_interaction': sum(comments) / total_interactions if total_interactions else None,
    }


def local_date_from_value(value: str) -> str:
    if not value:
        return ''
    if 'T' in value:
        try:
            normalized = value.replace('Z', '+00:00')
            parsed = datetime.fromisoformat(normalized)
            if parsed.tzinfo is not None:
                return parsed.astimezone(ZoneInfo('America/Matamoros')).date().isoformat()
            return parsed.date().isoformat()
        except ValueError:
            pass
    return value[:10] if len(value) >= 10 and value[:4].isdigit() else ''


def normalize_aug_row(row: dict, source: str, content_type: str | None = None) -> dict:
    meta_id = row.get('meta_post_id') or row.get('id') or ''
    created = row.get('created_time_local') or row.get('published_at_local') or row.get('created_time') or row.get('published_at_utc') or row.get('created_time_utc') or row.get('date_local') or ''
    local_date = local_date_from_value(created)
    ctype = content_type or row.get('content_format') or row.get('content_type') or ''
    if ctype.lower() in {'image_or_post', 'image', 'photo', 'post'}:
        ctype = 'Image_or_post'
    elif ctype.lower() in {'reel', 'reels', 'video'}:
        ctype = 'Reel'
    return {
        'id': meta_id,
        'date': local_date,
        'type': ctype,
        'reactions': num(row.get('reactions') if row.get('reactions') is not None else row.get('reactions_observed') if row.get('reactions_observed') is not None else row.get('reactions_lifetime')),
        'comments': num(row.get('comments') if row.get('comments') is not None else row.get('comments_observed') if row.get('comments_observed') is not None else row.get('comments_lifetime')),
        'shares': num(row.get('shares') if row.get('shares') is not None else row.get('shares_observed') if row.get('shares_observed') is not None else row.get('shares_lifetime')),
        'interactions': num(row.get('interactions') if row.get('interactions') is not None else row.get('interactions_observed')),
        'source': source,
    }


def dedupe_rows(rows: list[dict]) -> tuple[list[dict], dict]:
    by_id: dict[str, dict] = {}
    duplicate_counts = Counter()
    skipped_blank = 0
    for row in rows:
        meta_id = row.get('id', '')
        if not meta_id:
            skipped_blank += 1
            continue
        if meta_id in by_id:
            duplicate_counts[meta_id] += 1
            # Prefer the most recent source in the order supplied to this function.
        by_id[meta_id] = row
    return list(by_id.values()), {
        'raw_rows': len(rows),
        'unique_rows': len(by_id),
        'duplicate_rows_removed': sum(duplicate_counts.values()),
        'blank_id_rows_skipped': skipped_blank,
        'duplicate_ids': sorted(duplicate_counts),
    }


base_rows = read_csv(BASE_CSV)
reel_inventory = read_csv(REELS_INVENTORY_CSV)
known_facebook_reel_ids = set()
for record in reel_inventory:
    if record.get('Platform') == 'Facebook':
        for key in ('Platform_Content_ID', 'Meta_Reel_ID'):
            if record.get(key):
                known_facebook_reel_ids.add(record[key])

historical = []
for row in base_rows:
    if row.get('month') not in {'2026-06', '2026-07', '2026-08'}:
        continue
    normalized = {
        'id': row.get('id', ''),
        'date': row.get('date', ''),
        'type': 'Reel' if row.get('id') in known_facebook_reel_ids else 'Image_or_post',
        'reactions': num(row.get('reactions')),
        'comments': num(row.get('comments')),
        'shares': num(row.get('shares')),
        'interactions': num(row.get('interactions')),
        'source': '2026-08-14_base',
        'month': row.get('month'),
        'hour': row.get('hour'),
        'weekday': row.get('weekday'),
        'message': row.get('message', ''),
    }
    historical.append(normalized)

# Current August evidence is appended in chronological/source order and deduplicated by Meta post ID.
august_current_raw: list[dict] = []
aug15_16 = read_json(AUG15_16_JSON)
for row in aug15_16.get('posts', []):
    august_current_raw.append(normalize_aug_row(row, AUG15_16_JSON.name, 'Image_or_post'))

p0 = read_json(P0_SUMMARY_JSON)
for row in p0.get('rows', []):
    august_current_raw.append(normalize_aug_row(row, P0_SUMMARY_JSON.name, 'Image_or_post'))

cohort = read_json(AUG_COHORT_JSON)
for row in cohort.get('rows', []):
    august_current_raw.append(normalize_aug_row(row, AUG_COHORT_JSON.name, 'Image_or_post'))
for row in cohort.get('reels_separate', {}).get('rows', []):
    august_current_raw.append(normalize_aug_row(row, AUG_COHORT_JSON.name, 'Reel'))

daily = read_json(AUG_DAILY_JSON)
for row in daily.get('records', []):
    august_current_raw.append(normalize_aug_row(row, AUG_DAILY_JSON.name, row.get('content_type')))

august_current, august_union_meta = dedupe_rows(august_current_raw)
august_base = [row for row in historical if row.get('month') == '2026-08']
august_all_raw = august_base + august_current
august_all, august_all_union_meta = dedupe_rows(august_all_raw)

# The historical base may contain known Reels. All monthly image comparisons exclude them.
period_rows = {
    '2026-06_all': [row for row in historical if row.get('month') == '2026-06'],
    '2026-07_all': [row for row in historical if row.get('month') == '2026-07'],
    '2026-08_1_14_all': [row for row in historical if row.get('month') == '2026-08'],
    '2026-06_images': [row for row in historical if row.get('month') == '2026-06' and row.get('type') != 'Reel'],
    '2026-07_images': [row for row in historical if row.get('month') == '2026-07' and row.get('type') != 'Reel'],
    '2026-08_1_14_images': [row for row in historical if row.get('month') == '2026-08' and row.get('type') != 'Reel'],
    '2026-06_reels': [row for row in historical if row.get('month') == '2026-06' and row.get('type') == 'Reel'],
    '2026-07_reels': [row for row in historical if row.get('month') == '2026-07' and row.get('type') == 'Reel'],
    '2026-08_1_14_reels': [row for row in historical if row.get('month') == '2026-08' and row.get('type') == 'Reel'],
    '2026-08_1_21_images': [row for row in august_all if row.get('type') != 'Reel'],
    '2026-08_1_21_reels': [row for row in august_all if row.get('type') == 'Reel'],
}

# Clean first-14-day comparisons use the same image-only rule.
for month in ('2026-06', '2026-07', '2026-08'):
    key = f'{month}_first14_images'
    if month == '2026-08':
        source_rows = period_rows['2026-08_1_14_images']
    else:
        source_rows = period_rows[f'{month}_images']
    period_rows[key] = [row for row in source_rows if 1 <= int(row.get('date', '0000-00-00')[8:10]) <= 14]

summaries = {key: summarize(rows, key, 'image_or_post' if 'images' in key else 'all_or_reels') for key, rows in period_rows.items()}

# Detail tables are kept in JSON only so the CSV remains a compact period summary.
def top_rows(rows, limit=10):
    return [
        {
            'id': row.get('id'),
            'date': row.get('date'),
            'type': row.get('type'),
            'interactions': row.get('interactions'),
            'reactions': row.get('reactions'),
            'comments': row.get('comments'),
            'shares': row.get('shares'),
            'message': row.get('message', '')[:180],
        }
        for row in sorted(rows, key=lambda item: (num(item.get('interactions')), num(item.get('shares'))), reverse=True)[:limit]
    ]

def daily_rows(rows):
    grouped = {}
    for row in rows:
        day = row.get('date')
        if not day:
            continue
        grouped.setdefault(day, []).append(row)
    output = []
    for day, values in sorted(grouped.items()):
        interactions = [num(item.get('interactions')) for item in values]
        output.append({
            'date': day,
            'posts': len(values),
            'interactions_total': sum(interactions),
            'interactions_mean': statistics.mean(interactions),
            'interactions_median': statistics.median(interactions),
            'shares_total': sum(num(item.get('shares')) for item in values),
            'comments_total': sum(num(item.get('comments')) for item in values),
        })
    return output

details = {
    key: {
        'top_posts': top_rows(rows),
        'daily': daily_rows(rows),
        'top1_share_of_interactions': (num(sorted(rows, key=lambda item: num(item.get('interactions')), reverse=True)[0].get('interactions')) / sum(num(item.get('interactions')) for item in rows)) if rows and sum(num(item.get('interactions')) for item in rows) else None,
        'top5_share_of_interactions': (sum(num(item.get('interactions')) for item in sorted(rows, key=lambda item: num(item.get('interactions')), reverse=True)[:5]) / sum(num(item.get('interactions')) for item in rows)) if rows and sum(num(item.get('interactions')) for item in rows) else None,
        'without_top1': summarize(sorted(rows, key=lambda item: num(item.get('interactions')), reverse=True)[1:], key + '_without_top1', 'image_or_post') if len(rows) > 1 else None,
        'threshold_counts': {
            str(threshold): sum(1 for item in rows if num(item.get('interactions')) >= threshold)
            for threshold in (50, 100, 300, 500, 1000)
        },
    }
    for key, rows in period_rows.items()
}

# Additional explicit comparisons.
comparison = {
    'first14_image_only': {
        '2026-06': summaries['2026-06_first14_images'],
        '2026-07': summaries['2026-07_first14_images'],
        '2026-08': summaries['2026-08_first14_images'],
    },
    'full_month_reference_vs_august_mtd_images': {
        '2026-06': summaries['2026-06_images'],
        '2026-07': summaries['2026-07_images'],
        '2026-08_mtd_1_21': summaries['2026-08_1_21_images'],
    },
    'first14_august_vs_prior_image_only': {
        'posts_per_active_day_vs_june': percent_change(summaries['2026-06_first14_images']['posts_per_active_day'], summaries['2026-08_first14_images']['posts_per_active_day']),
        'posts_per_active_day_vs_july': percent_change(summaries['2026-07_first14_images']['posts_per_active_day'], summaries['2026-08_first14_images']['posts_per_active_day']),
        'interactions_per_active_day_vs_june': percent_change(summaries['2026-06_first14_images']['interactions_per_active_day'], summaries['2026-08_first14_images']['interactions_per_active_day']),
        'interactions_per_active_day_vs_july': percent_change(summaries['2026-07_first14_images']['interactions_per_active_day'], summaries['2026-08_first14_images']['interactions_per_active_day']),
        'median_interactions_vs_june': percent_change(summaries['2026-06_first14_images']['interactions_median'], summaries['2026-08_first14_images']['interactions_median']),
        'median_interactions_vs_july': percent_change(summaries['2026-07_first14_images']['interactions_median'], summaries['2026-08_first14_images']['interactions_median']),
        'shares_per_interaction_change_pp_vs_june': (summaries['2026-08_first14_images']['shares_per_interaction'] - summaries['2026-06_first14_images']['shares_per_interaction']) * 100,
        'shares_per_interaction_change_pp_vs_july': (summaries['2026-08_first14_images']['shares_per_interaction'] - summaries['2026-07_first14_images']['shares_per_interaction']) * 100,
    },
    'july_vs_june_image_only': {
        'posts_change': percent_change(summaries['2026-06_images']['posts'], summaries['2026-07_images']['posts']),
        'total_interactions_change': percent_change(summaries['2026-06_images']['interactions_total'], summaries['2026-07_images']['interactions_total']),
        'median_interactions_change': percent_change(summaries['2026-06_images']['interactions_median'], summaries['2026-07_images']['interactions_median']),
        'median_shares_change': percent_change(summaries['2026-06_images']['shares_median'], summaries['2026-07_images']['shares_median']),
    },
    'august_mtd_vs_full_month_rate': {
        'posts_per_active_day_vs_june': percent_change(summaries['2026-06_images']['posts_per_active_day'], summaries['2026-08_1_21_images']['posts_per_active_day']),
        'posts_per_active_day_vs_july': percent_change(summaries['2026-07_images']['posts_per_active_day'], summaries['2026-08_1_21_images']['posts_per_active_day']),
        'interactions_per_active_day_vs_june': percent_change(summaries['2026-06_images']['interactions_per_active_day'], summaries['2026-08_1_21_images']['interactions_per_active_day']),
        'interactions_per_active_day_vs_july': percent_change(summaries['2026-07_images']['interactions_per_active_day'], summaries['2026-08_1_21_images']['interactions_per_active_day']),
        'median_interactions_vs_june': percent_change(summaries['2026-06_images']['interactions_median'], summaries['2026-08_1_21_images']['interactions_median']),
        'median_interactions_vs_july': percent_change(summaries['2026-07_images']['interactions_median'], summaries['2026-08_1_21_images']['interactions_median']),
    },
}

# Integration status: use the existing ledgers, but keep coverage claims explicitly scoped.
individuals = read_csv(INDIVIDUALS_CSV)
june_individual = [row for row in individuals if row.get('period') == 'Junio_2026']
july_individual = [row for row in individuals if row.get('period') == 'Julio_2026']

def unique_nonempty(rows, field):
    return {row.get(field, '').strip() for row in rows if row.get(field, '').strip()}

june_unique_meta = unique_nonempty(june_individual, 'meta_id')
june_with_asset_meta = {row.get('meta_id', '').strip() for row in june_individual if row.get('meta_id', '').strip() and row.get('asset_ref', '').strip()}
june_with_asset_nonreel_meta = {row.get('meta_id', '').strip() for row in june_individual if row.get('meta_id', '').strip() and row.get('asset_ref', '').strip() and row.get('meta_id') not in known_facebook_reel_ids}
july_unique_meta = unique_nonempty(july_individual, 'meta_id')
july_with_asset_meta = {row.get('meta_id', '').strip() for row in july_individual if row.get('meta_id', '').strip() and row.get('asset_ref', '').strip()}

june_queue = read_csv(JUNE_QUEUE_CSV)
july_expansion = read_csv(JULY_EXPANSION_CSV)
july_tax = read_csv(JULY_TAX_CSV)

integration = [
    {
        'period': 'Junio 2026',
        'performance_scope': '230 filas base; 201 no-Reel tras excluir 29 IDs que coinciden con el inventario de Reels',
        'individual_rows': len(june_individual),
        'unique_meta_individual': len(june_unique_meta),
        'unique_meta_with_asset_ref': len(june_with_asset_meta),
        'unique_nonreel_meta_with_asset_ref': len(june_with_asset_nonreel_meta),
        'individual_coverage_vs_nonreel_base': len(june_with_asset_nonreel_meta) / len(period_rows['2026-06_images']) if period_rows['2026-06_images'] else None,
        'open_unmatched_queue': len(june_queue),
        'queue_approved_or_validated': sum(1 for row in june_queue if row.get('approval_status', '').startswith('Approved') or row.get('validation_status', '').startswith('Validated')),
        'taxonomy_scope': '172 filas base taxonómica más revisión selectiva de 17 casos; no exhaustiva por identidad visual',
        'comments_scope': '72 comentarios en cinco posts prioritarios; no lectura completa del mes',
        'historical_windows_24_72h': 'No reconstruibles',
    },
    {
        'period': 'Julio 2026',
        'performance_scope': '207 filas base; 199 no-Reel tras excluir 8 IDs que coinciden con el inventario de Reels',
        'individual_rows': len(july_individual),
        'unique_meta_individual': len(july_unique_meta),
        'unique_meta_with_asset_ref': len(july_with_asset_meta),
        'unique_nonreel_meta_with_asset_ref': len(july_with_asset_meta),
        'individual_coverage_vs_nonreel_base': len(july_with_asset_meta) / len(period_rows['2026-07_images']) if period_rows['2026-07_images'] else None,
        'open_unmatched_queue': '185 publicaciones permanecen en la capa comparable mensual; 1 caso borderline fuera del lote ampliado',
        'queue_approved_or_validated': sum(1 for row in july_expansion if row.get('Asset_Ref', '').strip()),
        'taxonomy_scope': f'{len(july_tax)} casos con taxonomía visual revisada en el lote ampliado; 22 casos individuales totales',
        'comments_scope': '284 comentarios extraídos en 16 matches nuevos; priorización cualitativa, no lectura manual completa',
        'historical_windows_24_72h': 'No reconstruibles',
    },
    {
        'period': 'Agosto 2026 hasta 21 ago',
        'performance_scope': f"{len(period_rows['2026-08_1_21_images'])} imágenes/posts y {len(period_rows['2026-08_1_21_reels'])} Reels en la unión de base 1–14 más cortes 15–21",
        'individual_rows': 'Operación distribuida entre Publication_Log, cortes diarios y Reels_Publication_Inventory; no existe aún una taxonomía MTD exhaustiva equivalente a junio/julio',
        'unique_meta_individual': len(period_rows['2026-08_1_21_images']) + len(period_rows['2026-08_1_21_reels']),
        'unique_meta_with_asset_ref': 'Parcial; depende del ledger operativo y de cada caso',
        'unique_nonreel_meta_with_asset_ref': None,
        'individual_coverage_vs_nonreel_base': None,
        'open_unmatched_queue': 'No comparable con la cola histórica; prioridad actual es captura diaria y reconciliación nativa',
        'queue_approved_or_validated': None,
        'taxonomy_scope': 'Solo el corte diario más reciente tiene desglose provisional completo por familia/personaje; no canonizar',
        'comments_scope': 'Cortes diarios y moderación incremental; no lectura MTD completa',
        'historical_windows_24_72h': 'No usar como sustituto; reportes diarios son fuente principal',
    },
]

result = {
    'metadata': {
        'created': '2026-08-22',
        'purpose': 'Comparar junio, julio y agosto hasta 2026-08-21 usando interacciones observadas y separar Reels de imágenes.',
        'method': 'Base homogénea 2026-08-14 para junio/julio/agosto 1–14; cortes observados 15–21 de agosto unidos y deduplicados por Meta post ID.',
        'timezone': 'America/Matamoros for current August reports; historical CSV retains its local date field.',
        'metric_definition': 'interactions = reactions + comments + shares',
        'window_warning': 'Todas las cifras son acumulados lifetime/Corte_Observado al momento de extracción; no son deltas exactos ni ventanas 24/72h.',
        'reel_classification_note': 'Los IDs coincidentes con Facebook Reels_Publication_Inventory se excluyen de las tablas image_only; Reels se reportan aparte.',
        'dedupe': august_all_union_meta,
        'source_files': [p.name for p in [BASE_CSV, REELS_INVENTORY_CSV, AUG15_16_JSON, P0_SUMMARY_JSON, AUG_COHORT_JSON, AUG_DAILY_JSON, INDIVIDUALS_CSV, JUNE_QUEUE_CSV, JULY_EXPANSION_CSV, JULY_TAX_CSV]],
    },
    'known_facebook_reel_overlap_in_historical_base': {
        month: {
            'rows': len([r for r in historical if r.get('month') == month]),
            'reels': len([r for r in historical if r.get('month') == month and r.get('type') == 'Reel']),
            'images_or_nonreel': len([r for r in historical if r.get('month') == month and r.get('type') != 'Reel']),
        }
        for month in ('2026-06', '2026-07', '2026-08')
    },
    'summaries': summaries,
    'details': details,
    'comparison': comparison,
    'august_current_union': {
        'raw_current_rows': len(august_current_raw),
        'current_unique_rows': len(august_current),
        'all_august_unique_rows': len(august_all),
        'images': len(period_rows['2026-08_1_21_images']),
        'reels': len(period_rows['2026-08_1_21_reels']),
        'reels_interactions': summarize(period_rows['2026-08_1_21_reels'], '2026-08_1_21', 'reels'),
        'source_counts_current_only': dict(Counter(row['source'] for row in august_current)),
    },
    'integration': integration,
}

OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')

summary_rows = []
for key, summary in summaries.items():
    summary_rows.append(summary)
with OUT_CSV.open('w', newline='', encoding='utf-8') as handle:
    fieldnames = list(summary_rows[0].keys())
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(summary_rows)

with OUT_INTEGRATION_CSV.open('w', newline='', encoding='utf-8') as handle:
    fieldnames = list(integration[0].keys())
    writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(integration)

print(OUT_JSON)
print(OUT_CSV)
print(OUT_INTEGRATION_CSV)
for key in ('2026-06_images', '2026-07_images', '2026-08_1_14_images', '2026-08_1_21_images', '2026-08_1_21_reels'):
    print(key, json.dumps(summaries[key], ensure_ascii=False))
print('comparison', json.dumps(comparison, ensure_ascii=False))
print('integration', json.dumps(integration, ensure_ascii=False))

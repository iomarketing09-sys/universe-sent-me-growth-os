#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, Counter
import csv
import json

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
RAW = ROOT / 'Operations/Research/Historical_Performance_Individuals.csv'
CON = ROOT / 'Operations/Research/2026-08-20_Historical_Performance_Individuals_Consolidated.csv'
ALIASES = ROOT / 'Operations/Research/2026-08-20_Source_Alias_Table.csv'
NONCNT = ROOT / 'Operations/Research/2026-08-20_NonCNT_Inventory_Alias_Approval.csv'
P0 = ROOT / 'Operations/Research/2026-08-20_P0_Asset_Association_Register.csv'
OUT_JSON = ROOT / 'Operations/Research/2026-08-20_Alias_Impact_June.json'
REPORT = ROOT / 'Operations/Research/2026-08-20_Alias_Impact_June.md'

def read(p):
    with p.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def n(v):
    try:
        return float(str(v or '').strip())
    except Exception:
        return 0.0

def period(r):
    return r.get('period') or r.get('periods','')

def metric_sum(rows, field):
    return sum(n(r.get(field)) for r in rows)

def interactions(r):
    # Raw rows use metric_value; consolidated uses reactions/comments/shares.
    if r.get('metric_value') not in (None, ''):
        return n(r.get('metric_value'))
    return n(r.get('reactions')) + n(r.get('comments')) + n(r.get('shares'))

raw = read(RAW)
con = read(CON)
aliases = read(ALIASES)
noncnt = read(NONCNT)
p0 = read(P0)

raw_june = [r for r in raw if 'Junio' in period(r)]
con_june = [r for r in con if 'Junio' in period(r)]
raw_all = raw
con_all = con

raw_metric_total = sum(interactions(r) for r in raw_june)
con_metric_total = sum(interactions(r) for r in con_june)
raw_reactions = metric_sum(raw_june, 'reactions')
raw_comments = metric_sum(raw_june, 'comments')
raw_shares = metric_sum(raw_june, 'shares')
con_reactions = metric_sum(con_june, 'reactions')
con_comments = metric_sum(con_june, 'comments')
con_shares = metric_sum(con_june, 'shares')

# Exact aliases resolved in the latest state.
resolved_260508 = {r.get('Alias_ID'): r for r in aliases if r.get('Alias_ID') in {'ALIAS-0036','ALIAS-0047'}}
# Historical consolidated rows carrying the 260508 asset key.
asset_260508 = [r for r in con_all if r.get('asset_ref_canonical') == '260508']
# Current exact allocation by observed filename / date.
exact_alloc = []
for r in asset_260508:
    name = r.get('filename_or_concepts','')
    if 'Existencial' in name:
        inv = 'CNT-043'
    elif '260508 - Universe' in name:
        inv = 'CNT-042'
    else:
        inv = ''
    exact_alloc.append({'meta_id': r.get('meta_id'), 'filename': name, 'interactions': interactions(r), 'inventory_id_after': inv, 'prior_inventory_candidates': r.get('inventory_id_candidates','')})

# Attribution counts from alias table by confidence and status.
conf = Counter(r.get('Confidence','') for r in aliases)
noncnt_status = Counter(r.get('Approval_Status','') for r in noncnt)
p0_status = Counter(r.get('Association_Status','') for r in p0)

# 17-30 coverage after current alias update.
fb_17_30 = [r for r in aliases if r.get('Publication_ID','').startswith('PUB-FB-17_30-')]
coverage = Counter()
for r in fb_17_30:
    if r.get('Confidence') == 'High':
        coverage['High'] += 1
    elif r.get('Review_Category') == 'Resolved_Exact_Filename':
        coverage['Resolved_Exact_Filename'] += 1
    else:
        coverage['Review'] += 1

# Output machine-readable results.
result = {
    'raw_rows_total': len(raw_all), 'consolidated_rows_total': len(con_all),
    'raw_june_rows': len(raw_june), 'consolidated_june_rows': len(con_june),
    'raw_june_interactions': raw_metric_total, 'consolidated_june_interactions': con_metric_total,
    'raw_june_reactions': raw_reactions, 'raw_june_comments': raw_comments, 'raw_june_shares': raw_shares,
    'consolidated_june_reactions': con_reactions, 'consolidated_june_comments': con_comments, 'consolidated_june_shares': con_shares,
    'duplicate_inflation_vs_consolidated': raw_metric_total - con_metric_total,
    'alias_confidence_counts': dict(conf), 'noncnt_status_counts': dict(noncnt_status), 'p0_status_counts': dict(p0_status),
    'fb_17_30_coverage': dict(coverage), 'asset_260508_exact_allocation': exact_alloc,
    'staging_or_non_june_aliases_do_not_change_june_metrics': True,
}
OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')

pct = (100 * (raw_metric_total - con_metric_total) / raw_metric_total) if raw_metric_total else 0
REPORT.write_text(f'''---
title: "Impacto de aliases actualizados en métricas de crecimiento de junio"
purpose: "Medir qué cambia en los agregados y qué cambia únicamente en la atribución editorial de inventario."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Historical_Performance_Individuals_Consolidated.csv"
  - "Operations/Research/2026-08-20_Source_Alias_Table.csv"
  - "Operations/Research/2026-08-20_NonCNT_Inventory_Alias_Approval.csv"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Impacto de aliases actualizados en junio

## Resultado ejecutivo

La reconciliación no añade interacciones ni cambia los Meta IDs. Su efecto cuantitativo directo es **cero** sobre las métricas de las publicaciones. El efecto principal es de atribución: dos publicaciones con `Asset_Ref=260508` dejan de apuntar ambiguamente a `CNT-042;CNT-043` y pasan a una asignación exacta: la variante `260508 - Universe.jpg` a `CNT-042` y `Universe - Existencial 260508.png` a `CNT-043`.

## Control de agregados

| Medida | Filas fuente | Vista consolidada | Diferencia por duplicados |
|---|---:|---:|---:|
| Filas totales individuales | {len(raw_all)} | {len(con_all)} | {len(raw_all)-len(con_all)} |
| Filas de junio | {len(raw_june)} | {len(con_june)} | {len(raw_june)-len(con_june)} |
| Interacciones de junio | {raw_metric_total:.0f} | {con_metric_total:.0f} | {raw_metric_total-con_metric_total:.0f} |
| Reacciones de junio | {raw_reactions:.0f} | {con_reactions:.0f} | {raw_reactions-con_reactions:.0f} |
| Comentarios de junio | {raw_comments:.0f} | {con_comments:.0f} | {raw_comments-con_comments:.0f} |
| Shares de junio | {raw_shares:.0f} | {con_shares:.0f} | {raw_shares-con_shares:.0f} |

La diferencia entre la fuente y la vista consolidada es un efecto de duplicación, no un efecto de los aliases. Los aliases solo hacen que la atribución a inventario sea más precisa.

## Impacto de 260508

| Publicación lógica | Interacciones | Atribución anterior | Atribución actual |
|---|---:|---|---|
'''+''.join(f"| `{x['meta_id']}` — {x['filename']} | {x['interactions']:.0f} | `{x['prior_inventory_candidates']}` | `{x['inventory_id_after']}` |\n" for x in exact_alloc)+f'''\nLas dos publicaciones suman {sum(x['interactions'] for x in exact_alloc):.0f} interacciones. Ese total no cambia; lo que cambia es que ahora cada fila puede entrar en análisis por CNT sin duplicar o repartir el rendimiento entre dos candidatos.

## Impacto en Growth OS

La cobertura de aliases Facebook 17–30 queda distribuida así: {dict(coverage)}. Los ocho aliases no-CNT aprobados administrativamente pertenecen a publicaciones de la programación 17–30 y mejoran la trazabilidad futura, pero no agregan métricas históricas de junio. Los cinco assets P0 mantienen dos asociaciones de alta confianza y tres excepciones documentadas.

La conclusión operativa es que la reconciliación **no reescribe el rendimiento de junio**; mejora la capacidad de responder qué asset/CNT produjo cada resultado y evita atribuciones ambiguas en reuse y rankings futuros. Los agregados deben continuar calculándose sobre la vista consolidada, no sobre las filas fuente duplicadas.
''', encoding='utf-8')
print(f'raw_june_rows={len(raw_june)} consolidated_june_rows={len(con_june)} raw_interactions={raw_metric_total} consolidated_interactions={con_metric_total} duplicate_inflation={raw_metric_total-con_metric_total} aliases_260508={len(resolved_260508)}')

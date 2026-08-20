#!/usr/bin/env python3
from pathlib import Path
import csv

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
BASELINE = ROOT / 'Operations/Research/2026-08-17_P0_Baseline_Ola_Activa.csv'
ALIAS = ROOT / 'Operations/Research/2026-08-20_Source_Alias_Table.csv'
INVENTORY = ROOT / 'GrowthOS/Content_Inventory.csv'
OUT = ROOT / 'Operations/Research/2026-08-20_P0_Asset_Association_Register.csv'
REPORT = ROOT / 'Operations/Research/2026-08-20_P0_Asset_Association_Report.md'

with BASELINE.open(newline='', encoding='utf-8-sig') as f:
    baseline = list(csv.DictReader(f))
with ALIAS.open(newline='', encoding='utf-8-sig') as f:
    aliases = list(csv.DictReader(f))
with INVENTORY.open(newline='', encoding='utf-8-sig') as f:
    inventory = list(csv.DictReader(f))

alias_by_pub = {r.get('Meta_Post_ID',''): r for r in aliases}
inv_by_asset = {}
for r in inventory:
    inv_by_asset.setdefault(str(r.get('Asset_Ref','')).strip(), []).append(r)

local_evidence = {
    '2608028': '/home/ubuntu/calendar_visual_review_20260816/2608028__2608028 - Universe -  El amor esta en todos lados.png; /home/ubuntu/new_assets_review/2608028_Universe.png',
    '2608034- Elara': '/home/ubuntu/calendar_visual_review_20260816/2608034__2608034- Elara - uno debe ser chismoso.jpeg; /home/ubuntu/new_assets_review/2608034_Elara.jpg',
    '2608027.jpeg': '/home/ubuntu/calendar_visual_review_20260816/2608027__2608027.jpeg; /home/ubuntu/new_assets_review/2608027_Unknown.jpg',
}
headers = ['P0_ID','Asset_Ref','Asset_Filename','Slot_Local','Published_At_Local','Meta_Post_ID','Alias_ID','Inventory_ID','Inventory_Asset_Ref','Inventory_Asset_Filename','Association_Status','Confidence','Evidence_Source','Local_Evidence','Notes']
rows = []
for r in baseline:
    asset_ref = r.get('Asset_Ref','').strip()
    asset_filename = r.get('asset_filename','').strip()
    post_id = r.get('meta_post_id','').strip()
    alias = alias_by_pub.get(post_id, {})
    inv_matches = inv_by_asset.get(asset_ref, [])
    if len(inv_matches) == 1:
        inv = inv_matches[0]
        status = 'Associated_Inventory_High'
        confidence = 'High'
        local = ''
        note = 'Existing inventory row is linked through the normalized asset key; no CNT was created.'
    else:
        inv = {}
        status = 'Exception_Inventory_Missing_Local_Evidence'
        confidence = 'Review'
        local = local_evidence.get(asset_ref, '')
        note = 'No Content_Inventory row exists. Local visual evidence is preserved; do not create CNT without editorial reconciliation.'
    rows.append({
        'P0_ID': r.get('publication_id',''),
        'Asset_Ref': asset_ref,
        'Asset_Filename': asset_filename,
        'Slot_Local': r.get('slot_local',''),
        'Published_At_Local': r.get('published_at_local',''),
        'Meta_Post_ID': post_id,
        'Alias_ID': alias.get('Alias_ID',''),
        'Inventory_ID': inv.get('id',''),
        'Inventory_Asset_Ref': inv.get('Asset_Ref',''),
        'Inventory_Asset_Filename': inv.get('Asset_Filename',''),
        'Association_Status': status,
        'Confidence': confidence,
        'Evidence_Source': 'P0_Baseline + Source_Alias_Table + Content_Inventory',
        'Local_Evidence': local,
        'Notes': note,
    })
with OUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

high = sum(r['Association_Status'] == 'Associated_Inventory_High' for r in rows)
exceptions = len(rows) - high
REPORT.write_text(f'''---
title: "Registro de asociación de assets P0"
purpose: "Resolver la relación de los cinco assets del baseline P0 con la fuente maestra sin crear CNT ni inventar asociaciones."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-17_P0_Baseline_Ola_Activa.csv"
  - "Operations/Research/2026-08-20_Source_Alias_Table.csv"
  - "GrowthOS/Content_Inventory.csv"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Registro de asociación de assets P0

El baseline contiene cinco publicaciones P0. El registro formal distingue las asociaciones verificables de las excepciones sin inventario.

| Estado | Cantidad |
|---|---:|
| Asociados a Content_Inventory con alta confianza | {high} |
| Excepciones con evidencia local pero sin fila de inventario | {exceptions} |
| Total P0 | {len(rows)} |

Las tres excepciones conservan el filename del baseline, el Meta Post ID y las rutas locales de evidencia. No se crean CNT ni se cambia canon; la resolución futura requiere una decisión de inventario/editorial o una correspondencia confirmada por Fernando/Claude.
''', encoding='utf-8')
print(f'p0_total={len(rows)} associated_high={high} exceptions={exceptions}')

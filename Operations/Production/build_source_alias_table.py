#!/usr/bin/env python3
from pathlib import Path
import csv
import re

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
INV_PATH = ROOT / 'GrowthOS/Content_Inventory.csv'
LOG_PATH = ROOT / 'Operations/Research/2026-08-15_Publication_Log.csv'
OUT = ROOT / 'Operations/Research/2026-08-20_Source_Alias_Table.csv'
REPORT = ROOT / 'Operations/Research/2026-08-20_Source_Alias_Table_Report.md'

# Operational asset keys are numeric references such as 2608028, 260724, 622, 728, 729 and 741.
KEY_RE = re.compile(r'(?<!\d)(260\d{3,4}|622|728|729|741)(?!\d)')

def key(value):
    text = str(value or '')
    matches = KEY_RE.findall(text)
    return matches[0] if matches else ''

def read(path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

inv = read(INV_PATH)
log = read(LOG_PATH)
inv_by_key = {}
for row in inv:
    k = key(row.get('Asset_Ref')) or key(row.get('Asset_Filename'))
    if k:
        inv_by_key.setdefault(k, []).append(row)

headers = [
    'Alias_ID','Asset_Key','Inventory_ID','Inventory_Asset_Ref','Inventory_Asset_Filename','Drive_ID',
    'Publication_ID','Publication_Asset_Ref','Plataforma','Meta_Post_ID','Meta_Photo_ID','Permalink',
    'Fecha_Planeada_Local','Hora_Planeada_Local','Fecha_Publicacion_Local','Hora_Publicacion_Local',
    'Estado_Publicacion','Match_Method','Confidence','Source','Notes'
]
rows = []
for i, pub in enumerate(log, 1):
    k = key(pub.get('Asset_Ref'))
    matches = inv_by_key.get(k, []) if k else []
    if len(matches) == 1:
        invrow = matches[0]
        method = 'Normalized_numeric_asset_key'
        confidence = 'High'
        note = 'Exact numeric asset key shared by Publication Log and Content Inventory; no CNT inferred.'
    elif len(matches) > 1:
        invrow = matches[0]
        method = 'Normalized_numeric_asset_key_multiple_inventory_rows'
        confidence = 'Review'
        note = f'{len(matches)} inventory rows share the normalized key; no automatic selection should be treated as canonical.'
    else:
        invrow = {}
        method = 'No_inventory_match'
        confidence = 'Review'
        note = 'No matching inventory row by normalized numeric key; preserve as alias gap and do not create CNT.'
    rows.append({
        'Alias_ID': f'ALIAS-{i:04d}',
        'Asset_Key': k,
        'Inventory_ID': invrow.get('id',''),
        'Inventory_Asset_Ref': invrow.get('Asset_Ref',''),
        'Inventory_Asset_Filename': invrow.get('Asset_Filename',''),
        'Drive_ID': invrow.get('Drive_ID','') or invrow.get('drive_reference_id',''),
        'Publication_ID': pub.get('Publicacion_ID',''),
        'Publication_Asset_Ref': pub.get('Asset_Ref',''),
        'Plataforma': pub.get('Plataforma',''),
        'Meta_Post_ID': pub.get('Meta_Post_ID',''),
        'Meta_Photo_ID': pub.get('Meta_Photo_ID',''),
        'Permalink': pub.get('Permalink',''),
        'Fecha_Planeada_Local': pub.get('Fecha_Planeada_Local',''),
        'Hora_Planeada_Local': pub.get('Hora_Planeada_Local',''),
        'Fecha_Publicacion_Local': pub.get('Fecha_Publicacion_Local',''),
        'Hora_Publicacion_Local': pub.get('Hora_Publicacion_Local',''),
        'Estado_Publicacion': pub.get('Estado_Publicacion',''),
        'Match_Method': method,
        'Confidence': confidence,
        'Source': 'Content_Inventory.csv + Publication_Log.csv',
        'Notes': note,
    })

with OUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

matched = sum(r['Match_Method'] == 'Normalized_numeric_asset_key' for r in rows)
review = len(rows) - matched
unique_keys = len({r['Asset_Key'] for r in rows if r['Asset_Key']})
no_key = sum(not r['Asset_Key'] for r in rows)
REPORT.write_text(f'''---
title: "Reporte de tabla de aliases de fuente maestra"
purpose: "Documentar el cruce reproducible entre Publication Log e inventario mediante claves numéricas normalizadas, sin crear CNT automáticamente."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "GrowthOS/Content_Inventory.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Reporte de tabla de aliases de fuente maestra

La tabla `2026-08-20_Source_Alias_Table.csv` cruza cada fila del Publication Log con el inventario mediante una clave numérica extraída de `Asset_Ref` o filename. La coincidencia no crea CNT ni sustituye una revisión editorial; solo hace explícita la relación operativa que puede verificarse.

| Métrica | Resultado |
|---|---:|
| Filas del Publication Log | {len(rows)} |
| Claves numéricas únicas observadas | {unique_keys} |
| Coincidencias únicas de alta confianza | {matched} |
| Filas con revisión o sin match | {review} |
| Filas sin clave numérica extraíble | {no_key} |

Las filas `Review` deben resolverse mediante evidencia adicional de Drive/Meta o mantenerse como excepción. La tabla conserva el filename operativo, el `Meta_Post_ID`, el permalink y el estado de publicación para que la fuente maestra pueda completarse sin inventar relaciones.
''', encoding='utf-8')
print(f'rows={len(rows)} matched_high={matched} review={review} no_key={no_key} unique_keys={unique_keys}')

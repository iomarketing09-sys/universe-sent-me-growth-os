#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
import csv
from collections import defaultdict

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
ENRICHED = ROOT / 'Operations/Research/2026-08-20_17_30_Alias_Evidence_Enriched.csv'
INVENTORY = ROOT / 'GrowthOS/Content_Inventory.csv'
STAGING = ROOT / 'Operations/Research/2026-08-20_Inventory_Alias_Staging_17_30.csv'
OPTIONS = ROOT / 'Operations/Research/2026-08-20_10_Cases_Resolution_Options.csv'
REPORT = ROOT / 'Operations/Research/2026-08-20_Staging_And_10_Cases_Report.md'

with ENRICHED.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
with INVENTORY.open(newline='', encoding='utf-8-sig') as f:
    inventory = list(csv.DictReader(f))

inv_by_ref = defaultdict(list)
for r in inventory:
    inv_by_ref[str(r.get('Asset_Ref','')).strip()].append(r)

# Evidence discovered in a wider local scan beyond calendar_visual_review_20260816.
external_evidence = {
    '260646': ['/home/ubuntu/reuse_review/260646.png'],
    '260508': ['/home/ubuntu/260508_universe.jpg', '/home/ubuntu/260508_existencial.png'],
    '2607838': ['/home/ubuntu/reuse_review/2607838.png'],
    '260757': ['/home/ubuntu/reuse_review/260757.png'],
    '260661': ['/home/ubuntu/extra_260661.png'],
    '2607831': ['/home/ubuntu/extra_2607831.png'],
    '260571': ['/home/ubuntu/reuse_review/260571.png'],
    '260550': ['/home/ubuntu/reuse_review/260550.png'],
    '260617': ['/home/ubuntu/reuse_review/260617.png'],
}

def digest(path):
    p = Path(path)
    if not p.exists():
        return ''
    return sha256(p.read_bytes()).hexdigest()

# 33 rows already identified as local-file verified in the principal visual review folder.
stage_rows = [r for r in rows if r.get('Resolution_Status') == 'Asset_Identity_Verified_Inventory_Row_Missing']
staging_headers = ['Staging_ID','Alias_ID','Publication_ID','Asset_Key','Publication_Asset_Ref','Meta_Post_ID','Permalink','Planned_Date_Local','Planned_Time_Local','Local_Evidence_Paths','Local_Evidence_SHA256','Inventory_ID_Current','Staging_Status','CNT_Creation_Allowed','Canon_Impact','Next_Action']
staging_out = []
for i, r in enumerate(stage_rows, start=1):
    paths = [p.strip() for p in r.get('Local_Evidence_Paths','').split(';') if p.strip()]
    digests = [f'{p}={digest(p)}' for p in paths if Path(p).exists()]
    staging_out.append({
        'Staging_ID': f'STG-17_30-{i:03d}',
        'Alias_ID': r.get('Alias_ID',''),
        'Publication_ID': r.get('Publication_ID',''),
        'Asset_Key': r.get('Asset_Key',''),
        'Publication_Asset_Ref': r.get('Publication_Asset_Ref',''),
        'Meta_Post_ID': r.get('Meta_Post_ID',''),
        'Permalink': r.get('Permalink',''),
        'Planned_Date_Local': r.get('Fecha_Planeada_Local',''),
        'Planned_Time_Local': r.get('Hora_Planeada_Local',''),
        'Local_Evidence_Paths': '; '.join(paths),
        'Local_Evidence_SHA256': '; '.join(digests),
        'Inventory_ID_Current': r.get('Inventory_ID',''),
        'Staging_Status': 'Identity_Verified_Inventory_Missing',
        'CNT_Creation_Allowed': 'No',
        'Canon_Impact': 'None',
        'Next_Action': 'Approve alias normalization or create non-CNT inventory row; do not alter source inventory automatically.'
    })
with STAGING.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=staging_headers, lineterminator='\n')
    writer.writeheader(); writer.writerows(staging_out)

# Ten rows that lacked evidence in the original folder scan.
unresolved = [r for r in rows if r.get('Resolution_Status') == 'Evidence_Not_Found_Local']
option_headers = ['Case_ID','Alias_IDs','Publication_IDs','Asset_Key','Publication_Asset_Refs','Meta_Post_IDs','Planned_Dates','Permalinks','Wider_Local_Evidence_Paths','Evidence_State','Inventory_Candidates','Recommended_Option','Risk','Next_Action']
option_out = []
for i, r in enumerate(unresolved, start=1):
    key = r.get('Asset_Key','')
    related = [x for x in unresolved if x.get('Asset_Key','') == key]
    # Use rows from alias table with same key when 260508 is represented by two filename variants.
    related_all = [x for x in rows if x.get('Asset_Key','') == key]
    paths = external_evidence.get(key, [])
    invs = inv_by_ref.get(key, [])
    exact = []
    for x in related_all:
        pub_ref = x.get('Publication_Asset_Ref','')
        for inv in invs:
            if pub_ref.strip().lower() == str(inv.get('Asset_Filename','')).strip().lower():
                exact.append(f"{x.get('Alias_ID','')}→{inv.get('id','')} ({inv.get('Asset_Filename','')})")
    if exact:
        state = 'Wider_Local_Evidence_Found_Exact_Filename'
        option = 'Associate exact filename to existing inventory candidate(s); update alias table after one validation pass.'
        risk = 'Low if filename and local digest match; do not create CNT.'
        next_action = 'Validate the two 260508 files and map ALIAS-0036→CNT-042, ALIAS-0047→CNT-043.'
    elif paths:
        state = 'Wider_Local_Evidence_Found_No_Inventory_Row'
        option = 'Move the file into staging evidence and create a non-CNT inventory alias row later.'
        risk = 'Medium: identity is evidenced but inventory association is administrative.'
        next_action = 'Keep the alias as Review; approve a staging alias or add a non-CNT inventory row.'
    else:
        state = 'No_Evidence_Found'
        option = 'Request Drive/Meta evidence or user confirmation; do not modify inventory.'
        risk = 'High: no local evidence available.'
        next_action = 'Obtain one authoritative asset file or permalink screenshot.'
    option_out.append({
        'Case_ID': f'CASE-17_30-{i:02d}',
        'Alias_IDs': ';'.join(x.get('Alias_ID','') for x in related_all),
        'Publication_IDs': ';'.join(x.get('Publication_ID','') for x in related_all),
        'Asset_Key': key,
        'Publication_Asset_Refs': ';'.join(x.get('Publication_Asset_Ref','') for x in related_all),
        'Meta_Post_IDs': ';'.join(x.get('Meta_Post_ID','') for x in related_all),
        'Planned_Dates': ';'.join(x.get('Fecha_Planeada_Local','') for x in related_all),
        'Permalinks': ';'.join(x.get('Permalink','') for x in related_all),
        'Wider_Local_Evidence_Paths': '; '.join(paths),
        'Evidence_State': state,
        'Inventory_Candidates': ';'.join(f"{x.get('id','')} ({x.get('Asset_Filename','')})" for x in invs),
        'Recommended_Option': option,
        'Risk': risk,
        'Next_Action': next_action,
    })
with OPTIONS.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=option_headers, lineterminator='\n')
    writer.writeheader(); writer.writerows(option_out)

exact_count = sum('Exact_Filename' in r['Evidence_State'] for r in option_out)
wider_count = sum('Wider_Local_Evidence_Found_No_Inventory_Row' == r['Evidence_State'] for r in option_out)
none_count = sum(r['Evidence_State'] == 'No_Evidence_Found' for r in option_out)
REPORT.write_text(f'''---
title: "Staging de aliases y opciones para los diez casos sin evidencia inicial"
purpose: "Preservar aliases visualmente verificados sin modificar Content_Inventory y proponer rutas de resolución para los diez casos que no aparecieron en la carpeta principal."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_17_30_Alias_Evidence_Enriched.csv"
  - "Operations/Research/2026-08-20_Inventory_Alias_Staging_17_30.csv"
  - "Operations/Research/2026-08-20_10_Cases_Resolution_Options.csv"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Staging de aliases 17–30 y opciones de resolución

## Capa staging

Se crearon {len(staging_out)} filas staging para assets con identidad visual verificada en la carpeta principal. La capa conserva Alias ID, publicación, Meta Post ID, permalink, fecha/hora, ruta de evidencia y SHA-256. No asigna CNT, no modifica `Content_Inventory.csv` y no tiene impacto de canon.

| Campo de control | Resultado |
|---|---:|
| Assets staging | {len(staging_out)} |
| CNT creados | 0 |
| Inventario maestro modificado | No |
| Impacto de canon | Ninguno |

## Diez casos inicialmente sin evidencia local

La búsqueda inicial estaba limitada a `calendar_visual_review_20260816`. Una segunda búsqueda en carpetas locales amplió la evidencia: se localizaron archivos para los diez casos. Nueve tienen un asset local único; `260508` tiene dos variantes locales y dos candidatos de inventario.

| Estado posterior a la búsqueda amplia | Cantidad |
|---|---:|
| Evidencia local amplia + filename exacto a inventario | {exact_count} filas/casos relacionados |
| Evidencia local amplia sin fila de inventario | {wider_count} |
| Sin evidencia en ninguna ruta revisada | {none_count} |

### Opciones recomendadas

**Opción 1 — `260508`: resolver por filename exacto.** Validar `260508_universe.jpg` contra `CNT-042` y `260508_existencial.png` contra `CNT-043`; después actualizar únicamente los aliases `ALIAS-0036` y `ALIAS-0047`. No crear CNT.

**Opción 2 — Los otros ocho assets con archivo local único:** mantenerlos en una segunda capa staging de evidencia, con SHA-256, y crear posteriormente una fila de alias no-CNT o una fila de inventario aprobada. No se debe elegir un CNT por personaje o por parecido visual.

**Opción 3 — Si un archivo local no coincide con la publicación:** solicitar evidencia de Drive/Meta o una captura de la publicación. La ausencia de match no debe resolverse con una inferencia de filename.
''', encoding='utf-8')
print(f'staging={len(staging_out)} option_cases={len(option_out)} exact_filename={exact_count} wider_no_inventory={wider_count} no_evidence={none_count}')

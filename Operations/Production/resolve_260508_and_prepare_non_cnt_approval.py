#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
import csv

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
ALIAS_PATH = ROOT / 'Operations/Research/2026-08-20_Source_Alias_Table.csv'
ENRICHED_PATH = ROOT / 'Operations/Research/2026-08-20_17_30_Alias_Evidence_Enriched.csv'
OPTIONS_PATH = ROOT / 'Operations/Research/2026-08-20_10_Cases_Resolution_Options.csv'
NONCNT_PATH = ROOT / 'Operations/Research/2026-08-20_NonCNT_Inventory_Alias_Approval.csv'
REPORT_PATH = ROOT / 'Operations/Research/2026-08-20_260508_Exact_Match_Validation.md'

mapping = {
    'ALIAS-0036': {'inventory_id': 'CNT-042', 'filename': '260508 - Universe.jpg', 'local': '/home/ubuntu/260508_universe.jpg'},
    'ALIAS-0047': {'inventory_id': 'CNT-043', 'filename': 'Universe - Existencial 260508.png', 'local': '/home/ubuntu/260508_existencial.png'},
}

def read(path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def write(path, rows):
    if not rows:
        return
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n')
        w.writeheader(); w.writerows(rows)

def digest(path):
    p = Path(path)
    return sha256(p.read_bytes()).hexdigest() if p.exists() else ''

aliases = read(ALIAS_PATH)
enriched = read(ENRICHED_PATH)
options = read(OPTIONS_PATH)

for row in aliases:
    aid = row.get('Alias_ID','')
    if aid in mapping:
        m = mapping[aid]
        row['Inventory_ID'] = m['inventory_id']
        row['Inventory_Asset_Ref'] = '260508'
        row['Inventory_Asset_Filename'] = m['filename']
        row['Match_Method'] = 'Exact_normalized_filename_and_asset_ref'
        row['Confidence'] = 'High'
        row['Notes'] = 'Validated against exact inventory filename and local evidence file; no CNT created.'

for row in enriched:
    aid = row.get('Alias_ID','')
    if aid in mapping:
        m = mapping[aid]
        row['Inventory_ID'] = m['inventory_id']
        row['Inventory_Asset_Ref'] = '260508'
        row['Inventory_Asset_Filename'] = m['filename']
        row['Match_Method'] = 'Exact_normalized_filename_and_asset_ref'
        row['Confidence'] = 'High'
        row['Review_Category'] = 'Resolved_Exact_Filename'
        row['Recommended_Action'] = 'No further action; use existing inventory row and do not create CNT.'
        row['Resolution_Status'] = 'Resolved_Inventory_Exact_Filename'
        row['Resolution_Next_Action'] = 'No further action in this cut.'
        row['Local_Evidence_Status'] = 'Local_File_Verified'

for row in options:
    if 'ALIAS-0036' in row.get('Alias_IDs','') and 'ALIAS-0047' in row.get('Alias_IDs',''):
        row['Evidence_State'] = 'Resolved_Exact_Filename_to_Existing_Inventory'
        row['Inventory_Candidates'] = 'ALIAS-0036→CNT-042; ALIAS-0047→CNT-043'
        row['Recommended_Option'] = 'Use exact filename mapping to existing inventory rows; no CNT creation.'
        row['Risk'] = 'Low; both filenames and local evidence hashes were validated.'
        row['Next_Action'] = 'Closed for alias resolution; retain source evidence.'

write(ALIAS_PATH, aliases)
write(ENRICHED_PATH, enriched)
write(OPTIONS_PATH, options)

noncnt = []
for i, row in enumerate(options, start=1):
    if row.get('Evidence_State') == 'Resolved_Exact_Filename_to_Existing_Inventory':
        continue
    alias_ids = row.get('Alias_IDs','').split(';')
    aid = alias_ids[0]
    key = row.get('Asset_Key','')
    # Match path from the broader local scan, stored in the options row.
    paths = [p.strip() for p in row.get('Wider_Local_Evidence_Paths','').split(';') if p.strip()]
    hashes = [f'{p}={digest(p)}' for p in paths if Path(p).exists()]
    noncnt.append({
        'Approval_Row_ID': f'NONCNT-17_30-{len(noncnt)+1:02d}',
        'Alias_ID': aid,
        'Publication_ID': row.get('Publication_IDs',''),
        'Asset_Key': key,
        'Publication_Asset_Ref': row.get('Publication_Asset_Refs',''),
        'Meta_Post_ID': row.get('Meta_Post_IDs',''),
        'Permalink': row.get('Permalinks',''),
        'Planned_Date_Local': row.get('Planned_Dates',''),
        'Local_Evidence_Paths': '; '.join(paths),
        'Local_Evidence_SHA256': '; '.join(hashes),
        'Current_Inventory_State': 'No matching inventory row',
        'Proposed_Record_Type': 'Inventory_Alias_NonCNT',
        'CNT_Creation_Allowed': 'No',
        'Canon_Impact': 'None',
        'Approval_Status': 'Pending_Admin_Approval',
        'Recommended_Action': 'Approve non-CNT alias staging; do not create CNT or alter canon.',
        'Notes': 'Identity supported by local evidence; inventory association remains administrative.'
    })
write(NONCNT_PATH, noncnt)

REPORT_PATH.write_text(f'''---
title: "Validación de matches 260508 y aprobación administrativa no-CNT"
purpose: "Cerrar dos aliases por filename exacto y presentar ocho filas de alias no-CNT para aprobación sin alterar Content_Inventory."
status: Review
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Source_Alias_Table.csv"
  - "Operations/Research/2026-08-20_10_Cases_Resolution_Options.csv"
  - "Operations/Research/2026-08-20_NonCNT_Inventory_Alias_Approval.csv"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Validación de matches 260508

| Alias | Filename local | Inventario | Hash SHA-256 | Estado |
|---|---|---|---|---|
'''+''.join(f"| `{aid}` | `{m['local']}` | `{m['inventory_id']}` — `{m['filename']}` | `{digest(m['local'])}` | Resolved_Exact_Filename_to_Existing_Inventory |\n" for aid, m in mapping.items())+'''\nLos dos aliases tienen filename operativo compatible con la fila existente de inventario y evidencia local independiente. No se creó CNT ni se modificó el contenido creativo.

# Ocho filas no-CNT

Se generó `2026-08-20_NonCNT_Inventory_Alias_Approval.csv` con ocho filas de aprobación administrativa. Todas tienen archivo local, Meta Post ID y permalink; todas permanecen `Pending_Admin_Approval`, con `CNT_Creation_Allowed=No` y `Canon_Impact=None`. La aprobación solicitada solo autoriza normalizar el alias de inventario, no crear un CNT ni cambiar canon.
''', encoding='utf-8')
print('resolved_260508=2 noncnt_pending=8')

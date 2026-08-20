#!/usr/bin/env python3
from pathlib import Path
import csv
import re
from collections import Counter

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
SRC = ROOT / 'Operations/Research/2026-08-20_17_30_Alias_Review.csv'
ASSET_DIR = Path('/home/ubuntu/calendar_visual_review_20260816')
OUT = ROOT / 'Operations/Research/2026-08-20_17_30_Alias_Evidence_Enriched.csv'
REPORT = ROOT / 'Operations/Research/2026-08-20_17_30_Alias_Evidence_Report.md'
KEY_RE = re.compile(r'(?<!\d)(260\d{3,4}|622|728|729|741)(?!\d)')

with SRC.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

files_by_key = {}
for p in ASSET_DIR.iterdir():
    if not p.is_file():
        continue
    m = KEY_RE.search(p.name)
    if m:
        files_by_key.setdefault(m.group(1), []).append(str(p))

headers = list(rows[0].keys()) + ['Local_Evidence_Status','Local_Evidence_Paths','Resolution_Status','Resolution_Next_Action']
out_rows = []
for r in rows:
    k = r.get('Asset_Key','').strip()
    paths = files_by_key.get(k, [])
    if r.get('Confidence') == 'High':
        status = 'Already_Associated_Inventory'
        resolution = 'No further action in this cut.'
        evidence_status = 'Inventory_Link_Verified'
        next_action = 'Use existing inventory association.'
    elif paths:
        status = 'Asset_Identity_Verified_Inventory_Row_Missing'
        resolution = 'Evidence sufficient for asset identity; inventory association remains administrative.'
        evidence_status = 'Local_File_Verified'
        next_action = 'Create or approve a non-CNT inventory row/alias; do not infer CNT from filename.'
    else:
        status = 'Evidence_Not_Found_Local'
        resolution = 'Requires Drive/Meta or human evidence.'
        evidence_status = 'No_Local_File_Match'
        next_action = 'Request evidence before changing inventory.'
    out_rows.append({**r, 'Local_Evidence_Status': evidence_status, 'Local_Evidence_Paths': '; '.join(paths), 'Resolution_Status': status, 'Resolution_Next_Action': next_action})

with OUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers, lineterminator='\n')
    writer.writeheader()
    writer.writerows(out_rows)
counts = Counter(r['Resolution_Status'] for r in out_rows)
REPORT.write_text(f'''---
title: "Evidencia local de aliases de la programación 17–30"
purpose: "Separar identidad de asset verificada por archivo de asociación administrativa al inventario maestro."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_17_30_Alias_Review.csv"
  - "Operations/Research/2026-08-20_Source_Alias_Table.csv"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Evidencia local de aliases 17–30

La carpeta local `calendar_visual_review_20260816` contiene archivos de evidencia para las claves de asset de la programación. Esta revisión permite separar tres estados: el asset ya está asociado al inventario, el asset está verificado pero falta una fila/alias administrativa, o no existe evidencia local.

| Estado | Cantidad |
|---|---:|
'''+''.join(f'| `{k}` | {v} |\n' for k, v in sorted(counts.items()))+'''\n
La evidencia local no crea CNT ni cambia el canon. Las filas `Asset_Identity_Verified_Inventory_Row_Missing` están listas para una decisión de normalización de inventario; hasta entonces, el alias de publicación conserva su Meta ID y permalink.
''', encoding='utf-8')
print(dict(counts))

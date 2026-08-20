#!/usr/bin/env python3
from pathlib import Path
import csv
from collections import Counter

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
ALIAS = ROOT / 'Operations/Research/2026-08-20_Source_Alias_Table.csv'
OUT = ROOT / 'Operations/Research/2026-08-20_17_30_Alias_Review.csv'
REPORT = ROOT / 'Operations/Research/2026-08-20_17_30_Alias_Review_Report.md'

with ALIAS.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

selected = [r for r in rows if (r.get('Publication_ID','').startswith('PUB-FB-17_30-') or r.get('Publication_ID','').startswith('PUB-IG-17_30-'))]
review = [r for r in selected if r.get('Confidence') == 'Review']

p0_assets = {'2608028','2608034- Elara','2608027.jpeg'}
local_evidence_keys = {'2608028','2608034- Elara','2608027.jpeg','2608029'}
headers = list(selected[0].keys()) + ['Review_Category','Recommended_Action']
out_rows = []
for r in review:
    asset = r.get('Publication_Asset_Ref','')
    if asset in p0_assets:
        category = 'P0_or_P0_adjacent_exception'
        action = 'Keep as documented exception; do not create CNT; preserve P0 association register.'
    elif asset in local_evidence_keys:
        category = 'Local_asset_evidence_available'
        action = 'Keep alias gap until inventory row is explicitly created/linked by approved reconciliation.'
    elif not r.get('Asset_Key'):
        category = 'No_numeric_asset_key'
        action = 'Resolve from permalink/Meta object or maintain as non-260 production exception.'
    else:
        category = '17_30_inventory_gap'
        action = 'Cross-check exact filename/Drive/Meta; if no evidence, keep Review without CNT creation.'
    out_rows.append({**r, 'Review_Category': category, 'Recommended_Action': action})

with OUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers + ['Review_Category','Recommended_Action'], lineterminator='\n')
    writer.writeheader()
    writer.writerows(out_rows)

counts = Counter(r['Review_Category'] for r in out_rows)
REPORT.write_text(f'''---
title: "Revisión de aliases de la programación 17–30"
purpose: "Clasificar aliases sin match de la programación 17–30 y separar excepciones resolubles de casos que requieren evidencia adicional."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/2026-08-20_Source_Alias_Table.csv"
  - "Operations/Research/2026-08-20_P0_Asset_Association_Register.csv"
  - "Operations/Research/2026-08-15_Publication_Log.csv"
  - "GrowthOS/Content_Inventory.csv"
organization: "Operations/Research"
---

# Revisión de aliases de la programación 17–30

Se seleccionaron {len(selected)} filas de la programación 17–30 y se encontraron {len(review)} aliases en estado `Review`. La clasificación no convierte un filename en CNT ni modifica `Content_Inventory.csv` automáticamente.

| Categoría | Cantidad |
|---|---:|
'''+''.join(f'| `{k}` | {v} |\n' for k, v in sorted(counts.items()))+'''\nLas filas con `High` ya están enlazadas mediante clave numérica y no requieren otra asociación en este corte. Las filas de revisión deben resolverse con evidencia de Drive/Meta o permanecer como excepciones formales.
''', encoding='utf-8')
print(f'selected_17_30={len(selected)} review={len(review)} categories={dict(counts)}')

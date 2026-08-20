#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path
import csv
import re

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
SRC = ROOT / 'Operations/Research/Historical_Performance_Individuals.csv'
INV = ROOT / 'GrowthOS/Content_Inventory.csv'
OUT = ROOT / 'Operations/Research/2026-08-20_Historical_Performance_Individuals_Consolidated.csv'
REPORT = ROOT / 'Operations/Research/2026-08-20_Junio_Consolidated_View.md'

KEY_RE = re.compile(r'(?<!\d)(260\d{3,4}|622|728|729|741)(?!\d)')

def read(path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def uniq(values):
    result = []
    for v in values:
        v = str(v or '').strip()
        if v and v not in result:
            result.append(v)
    return result

def asset_key(value):
    m = KEY_RE.search(str(value or ''))
    return m.group(1) if m else ''

rows = read(SRC)
inv_rows = read(INV)
inv_by_key = defaultdict(list)
for r in inv_rows:
    k = asset_key(r.get('Asset_Ref')) or asset_key(r.get('Asset_Filename'))
    if k:
        inv_by_key[k].append(r)

groups = defaultdict(list)
for idx, row in enumerate(rows, start=2):
    mid = str(row.get('meta_id') or '').strip()
    if mid:
        groups[mid].append((idx, row))
    else:
        synthetic = f'NO_META_ID_ROW_{idx}'
        groups[synthetic].append((idx, row))

headers = [
    'meta_id','source_row_ids','logical_status','source_count','periods','asset_ref_canonical',
    'asset_refs_observed','filename_or_concepts','dates_observed','local_times_observed','formats_observed',
    'metric_definitions_observed','metric_values_observed','reactions','comments','shares',
    'metrics_consistent','inventory_id_candidates','cnt_id_status','sources_observed','notes'
]
output = []
for mid, items in sorted(groups.items()):
    source_rows = [str(i) for i, _ in items]
    records = [r for _, r in items]
    refs = uniq(r.get('asset_ref') for r in records)
    keys = uniq(asset_key(r.get('asset_ref')) or asset_key(r.get('filename_or_concept')) for r in records)
    canonical_key = keys[0] if len(keys) == 1 else ''
    inv_ids = uniq(x.get('id') for r in inv_by_key.get(canonical_key, []) for x in [r])
    metric_sets = {field: uniq(r.get(field) for r in records) for field in ['reactions','comments','shares']}
    consistent = all(len(values) <= 1 for values in metric_sets.values())
    status = 'Consolidated_Logical_Duplicate' if len(items) > 1 else 'Unique_Logical_Publication'
    notes = 'Original rows preserved in source file; use this row for aggregates.' if len(items) > 1 else 'One source row observed.'
    if len(items) > 1 and consistent:
        notes += ' Duplicate rows agree on reactions/comments/shares.'
    output.append({
        'meta_id': '' if mid.startswith('NO_META_ID_ROW_') else mid,
        'source_row_ids': ';'.join(source_rows),
        'logical_status': status,
        'source_count': len(items),
        'periods': ';'.join(uniq(r.get('period') for r in records)),
        'asset_ref_canonical': canonical_key,
        'asset_refs_observed': ';'.join(refs),
        'filename_or_concepts': ';'.join(uniq(r.get('filename_or_concept') for r in records)),
        'dates_observed': ';'.join(uniq(r.get('date') for r in records)),
        'local_times_observed': ';'.join(uniq(r.get('local_time') for r in records)),
        'formats_observed': ';'.join(uniq(r.get('format') for r in records)),
        'metric_definitions_observed': ';'.join(uniq(r.get('metric_definition') for r in records)),
        'metric_values_observed': ';'.join(uniq(r.get('metric_value') for r in records)),
        'reactions': ';'.join(metric_sets['reactions']),
        'comments': ';'.join(metric_sets['comments']),
        'shares': ';'.join(metric_sets['shares']),
        'metrics_consistent': 'Yes' if consistent else 'Review',
        'inventory_id_candidates': ';'.join(inv_ids),
        'cnt_id_status': 'Candidate_from_inventory_key' if inv_ids else 'No_inventory_match',
        'sources_observed': ';'.join(uniq(r.get('source') for r in records)),
        'notes': notes,
    })

with OUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=headers, lineterminator='\n')
    writer.writeheader()
    writer.writerows(output)

duplicate_groups = sum(1 for items in groups.values() if len(items) > 1)
original_rows = len(rows)
consolidated_rows = len(output)
REPORT.write_text(f'''---
title: "Vista consolidada del histórico individual de junio"
purpose: "Usar una fila lógica por Meta ID para rankings y agregados sin eliminar las filas de evidencia originales."
status: Active
created: 2026-08-20
updated: 2026-08-20
version: "1.0"
author: "Manus AI (CGO)"
related_documents:
  - "Operations/Research/Historical_Performance_Individuals.csv"
  - "Operations/Research/2026-08-20_Junio_Duplicate_Groups.md"
  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"
organization: "Operations/Research"
---

# Vista consolidada del histórico individual de junio

La vista `2026-08-20_Historical_Performance_Individuals_Consolidated.csv` contiene una fila por publicación lógica. El archivo fuente original permanece intacto y conserva las filas que aportan evidencia desde diferentes procesos de integración.

| Métrica | Resultado |
|---|---:|
| Filas fuente | {original_rows} |
| Filas consolidadas lógicas | {consolidated_rows} |
| Grupos duplicados | {duplicate_groups} |
| Filas reducidas por consolidación | {original_rows - consolidated_rows} |

Los cinco grupos duplicados de Meta ID tienen métricas de reacciones, comentarios y shares consistentes. Por ello pueden usarse una sola vez en agregados y rankings. La columna `source_row_ids` conserva las filas de origen y `sources_observed` conserva las fuentes de evidencia. Esta vista no cambia el canon, no crea CNT y no reemplaza el histórico fuente.
''', encoding='utf-8')
print(f'original_rows={original_rows} consolidated_rows={consolidated_rows} duplicate_groups={duplicate_groups}')

#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path
import csv
import json

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
SRC = ROOT / 'Operations/Research/Historical_Performance_Individuals.csv'
OUT_JSON = ROOT / 'Operations/Research/2026-08-20_Junio_Duplicate_Groups.json'
OUT_MD = ROOT / 'Operations/Research/2026-08-20_Junio_Duplicate_Groups.md'

with SRC.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

groups = defaultdict(list)
for idx, row in enumerate(rows, start=2):
    mid = (row.get('meta_id') or '').strip()
    if mid:
        groups[mid].append({'source_row': idx, **row})
duplicates = {k: v for k, v in groups.items() if len(v) > 1}

OUT_JSON.write_text(json.dumps(duplicates, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
lines = [
    '---',
    'title: "Grupos duplicados del histórico de junio"',
    'purpose: "Verificar duplicados lógicos de Meta ID antes de usar agregados históricos."',
    'status: Active',
    'created: 2026-08-20',
    'updated: 2026-08-20',
    'version: "1.0"',
    'author: "Manus AI (CGO)"',
    'related_documents:',
    '  - "Operations/Research/Historical_Performance_Individuals.csv"',
    '  - "Operations/Research/2026-08-20_Auditoria_Fuente_Maestra_Junio.json"',
    '  - "GrowthOS/14_00_Fuente_Maestra_y_Ledgers.md"',
    'organization: "Operations/Research"',
    '---',
    '',
    '# Grupos duplicados del histórico de junio',
    '',
    f'Se detectaron **{len(duplicates)} grupos duplicados** dentro de `Historical_Performance_Individuals.csv`. Cada grupo comparte el mismo `meta_id` y contiene dos filas de fuentes históricas que deben representar una sola publicación lógica.',
    '',
    '| Meta ID | Filas | Asset refs | Fechas | Métrica/valor | Reacciones | Comentarios | Shares | Fuentes |',
    '|---|---:|---|---|---|---:|---:|---:|---|',
]
for mid, items in sorted(duplicates.items()):
    asset_refs = sorted({i.get('asset_ref','') for i in items})
    dates = sorted({i.get('date','') for i in items})
    metrics = sorted({f"{i.get('metric_definition','')}={i.get('metric_value','')}" for i in items})
    reactions = sorted({i.get('reactions','') for i in items})
    comments = sorted({i.get('comments','') for i in items})
    shares = sorted({i.get('shares','') for i in items})
    sources = sorted({i.get('source','') for i in items})
    lines.append(f"| `{mid}` | {len(items)} | {'; '.join(asset_refs)} | {'; '.join(dates)} | {'; '.join(metrics)} | {'; '.join(reactions)} | {'; '.join(comments)} | {'; '.join(shares)} | {'; '.join(sources)} |")
lines += [
    '',
    '## Decisión de consolidación',
    '',
    'Estos grupos deben conservarse como una sola publicación lógica para rankings y sumas. Las filas originales no se eliminan: se mantienen como fuentes de evidencia y se enlazan mediante `meta_id`. La vista consolidada debe conservar la lista de filas fuente, el asset/CNT confirmado y cualquier diferencia de definición métrica.',
]
OUT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'duplicate_groups={len(duplicates)} duplicate_rows={sum(len(v) for v in duplicates.values())}')

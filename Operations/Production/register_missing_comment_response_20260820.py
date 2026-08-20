#!/usr/bin/env python3
from pathlib import Path
import csv

LEDGER = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-15_Community_Engagement_Log.csv')
COMMENT_ID = '122151374823072582_1114814910869463'

text = LEDGER.read_text(encoding='utf-8')
if COMMENT_ID in text:
    print('already_present=1')
    raise SystemExit(0)

with LEDGER.open(newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    fieldnames = next(reader)

row = [
    COMMENT_ID,
    '1036844829507460_122151374823072582',
    '',
    '2026-08-20T04:10:27+0000',
    'Facebook',
    'Contextual_Sustantivo',
    'Humor de identificación social sobre la tribu de los migajeros',
    'Respondido',
    'La tribu se reconoce entre sí. 😂🤷🏻‍♀️',
    'Aprobada',
    '2026-08-20T15:57:00+00:00',
    '122151374823072582_1415067117189886',
    'El comentario amplía el remate social del meme; la respuesta mantiene complicidad sin juzgar a la persona.',
    'Ninguna',
    'Media',
    'No_Accion',
    '',
    'Anonimizado',
    'Meta Graph API v26 — respuesta aprobada por Fernando',
    '2026-08-20T15:57:00+00:00',
]
if len(row) != len(fieldnames):
    raise SystemExit(f'column_count_mismatch row={len(row)} header={len(fieldnames)}')
with LEDGER.open('a', newline='', encoding='utf-8') as f:
    csv.writer(f, lineterminator='\n').writerow(row)
print('appended=1')

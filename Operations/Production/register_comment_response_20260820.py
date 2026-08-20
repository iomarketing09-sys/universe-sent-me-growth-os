#!/usr/bin/env python3
from pathlib import Path
import csv

LEDGER = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-15_Community_Engagement_Log.csv')
COMMENT_ID = '122151374823072582_1041411610869463'

# This script appends only; it does not rewrite legacy rows whose historical CSV
# contains unescaped commas and therefore may be read by DictReader with extras.
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
    '2026-08-20T04:13:32+0000',
    'Facebook',
    'Contextual_Sustantivo',
    'Remate humorístico sobre aura y falta de claridad',
    'Respondido',
    'Eso ya no es aura débil… eso es falta de actualización espiritual. 😂✨',
    'Aprobada',
    '2026-08-20T15:56:08+00:00',
    '122151374823072582_1792383575281432',
    'El comentario amplía el remate del meme sin atacar a una persona; la respuesta mantiene el humor ácido y el tono de marca.',
    'Ninguna',
    'Media',
    'No_Accion',
    '',
    'Anonimizado',
    'Meta Graph API v26 — respuesta aprobada por Fernando',
    '2026-08-20T15:56:08+00:00',
]
if len(row) != len(fieldnames):
    raise SystemExit(f'column_count_mismatch row={len(row)} header={len(fieldnames)}')
with LEDGER.open('a', newline='', encoding='utf-8') as f:
    csv.writer(f, lineterminator='\n').writerow(row)
print('appended=1')

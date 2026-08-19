import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-15_ExperimentLog.csv')
row = [
    'P0-CLOSE-2026-08-19',
    'EXP-2026-08-CAL-01',
    'HB-003|HB-004|HB-005',
    'Experimento',
    '2026-08-17',
    '2026-08-19',
    'Cinco publicaciones P0 del 17 de agosto',
    'Facebook',
    'Imagen estática',
    'Mixto',
    '5',
    '785',
    '',
    '157',
    '197',
    '',
    '',
    '',
    '',
    '',
    'No_aplica',
    'Cerrada_con_limitacion',
    'Corte observado; no equivale a snapshots exactos 24/72h',
    '2608028 concentra 636/785 interacciones observadas; señal provisional a favor de identificación emocional, visual claro y caption mínimo, sin validar causalidad de horario.',
    'Usar el aprendizaje como señal editorial y mantener la extracción exacta 24/72h pendiente si Meta habilita payload temporal.',
    'Operations/Research/2026-08-19_P0_Corte_17_Agosto.md; Operations/Research/2026-08-19_P0_17_Agosto_Current_Summary.json; Meta Graph API v26'
]
with path.open('a', newline='', encoding='utf-8') as f:
    csv.writer(f).writerow(row)
print('appended', row[0], 'columns', len(row))

import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-15_Community_Engagement_Log.csv')
comment_id = '122151374289072582_1362274622770602'
response_time = '2026-08-18T23:17:38+0000'
response_id = '122151374289072582_1753493165792345'
rows = []
with path.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        if row['Comentario_ID'] == comment_id:
            row['Respuesta_Estado'] = 'Respondido'
            row['Aprobacion_Estado'] = 'Aprobada'
            row['Respuesta_Fecha'] = response_time
            row['Respuesta_Meta_ID'] = response_id
            row['Insight_Anonimo'] = 'Respuesta breve de complicidad publicada y verificada por Meta.'
            row['Ultima_Sincronizacion'] = response_time
        rows.append(row)
with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
print('updated', sum(1 for r in rows if r['Comentario_ID'] == comment_id), 'row')

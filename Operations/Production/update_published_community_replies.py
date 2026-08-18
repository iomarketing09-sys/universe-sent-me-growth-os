import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-15_Community_Engagement_Log.csv')
updates = {
    '122151374217072582_2093067344913171': ('2026-08-18T20:11:04+0000', '122151374217072582_2435856813608994'),
    '122151374217072582_1577015310481547': ('2026-08-18T20:11:08+0000', '122151374217072582_1830912011221593'),
    '122151373833072582_1715141313071482': ('2026-08-18T20:11:11+0000', '122151373833072582_1625579462232436'),
}
rows = []
with path.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        cid = row['Comentario_ID']
        if cid in updates:
            response_time, meta_id = updates[cid]
            row['Respuesta_Estado'] = 'Respondido'
            row['Aprobacion_Estado'] = 'Aprobada'
            row['Respuesta_Fecha'] = response_time
            row['Respuesta_Meta_ID'] = meta_id
            row['Moderacion_Estado'] = 'No_Accion'
            row['Ultima_Sincronizacion'] = response_time
            row['Insight_Anonimo'] = 'Respuesta aprobada y publicada por Meta; no requiere personaje.'
        rows.append(row)
with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
print('updated', sum(1 for r in rows if r['Comentario_ID'] in updates), 'rows')

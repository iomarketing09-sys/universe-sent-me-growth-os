from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-15_Community_Engagement_Log.csv')
updates = {
    '122151374823072582_899916076126399': ('2026-08-20T01:47:28+0000', '122151374823072582_904578688978118', 'Sí… pero ya que lo hicimos al revés, vamos a fingir que era parte del concepto. 😂👀'),
    '122151374823072582_2572609183253364': ('2026-08-20T01:47:33+0000', '122151374823072582_942838658075352', '¡Exacto! El remate venía con giro incluido. 😂🫠'),
}
lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
changed = 0
for i, line in enumerate(lines):
    for comment_id, (ts, reply_id, message) in updates.items():
        if line.startswith(comment_id + ','):
            fields = line.rstrip('\n').split(',')
            # Known ledger order: comment id, post id, CNT, date, platform, type, signal,
            # response status, suggested response, approval, response date, response id,
            # insight, action, priority, moderation, asset response, privacy, source, sync.
            while len(fields) < 20:
                fields.append('')
            fields[7] = 'Respondido'
            fields[8] = message
            fields[9] = 'Aprobada'
            fields[10] = ts
            fields[11] = reply_id
            fields[12] = 'Respuesta aprobada y publicada por Meta; interacción independiente.'
            fields[19] = ts
            lines[i] = ','.join(fields) + '\n'
            changed += 1
path.write_text(''.join(lines), encoding='utf-8')
print('updated', changed, 'rows')

import json
from pathlib import Path
import requests

root = Path('/home/ubuntu/universe-sent-me-growth-os')
src = root / 'Operations/Research/2026-08-19_Lote_Dialogo_Transformacion_Meta_Media.json'
out = root / 'Operations/Research/June_Lote_Dialogo_Transformacion_Images'
out.mkdir(exist_ok=True)
data = json.loads(src.read_text(encoding='utf-8'))
for row, item in zip(data['selected_queue_rows'], data['batch_response']):
    pid = row['meta_id']
    body = json.loads(item.get('body', '{}'))
    url = body.get('full_picture')
    if not url:
        try:
            url = body['attachments']['data'][0]['media']['image']['src']
        except Exception:
            url = None
    if not url:
        print('no image', pid)
        continue
    response = requests.get(url, timeout=45)
    response.raise_for_status()
    target = out / f'{pid}.jpg'
    target.write_bytes(response.content)
    print(pid, target, len(response.content))

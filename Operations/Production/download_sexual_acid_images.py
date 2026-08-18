import json, requests
from pathlib import Path
root=Path('/home/ubuntu/universe-sent-me-growth-os')
src=root/'Operations/Research/2026-08-19_Humor_Sexual_Acido_Meta_Media.json'
out=root/'Operations/Research/June_Humor_Sexual_Acido_Images'; out.mkdir(exist_ok=True)
d=json.loads(src.read_text(encoding='utf-8'))
for row,item in zip(d['selected_rows'],d['batch_response']):
 body=json.loads(item.get('body','{}')); url=body.get('full_picture')
 if not url:
  try: url=body['attachments']['data'][0]['media']['image']['src']
  except Exception: url=None
 if not url: print('no image',row['meta_id']); continue
 r=requests.get(url,timeout=45); r.raise_for_status(); p=out/f"{row['meta_id']}.jpg"; p.write_bytes(r.content); print(row['meta_id'],len(r.content))

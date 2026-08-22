import csv
import json
import os
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[2]
queue_path = ROOT / 'Operations/Research/2026-08-22_Reels_Pending_Asset_Reconciliation_Queue.csv'
with queue_path.open(encoding='utf-8', newline='') as handle:
    rows = list(csv.DictReader(handle))
unique = {}
for row in rows:
    unique.setdefault(row['Platform_Content_ID'], row)
top = list(unique.values())[:5]

BASE = 'https://graph.facebook.com/v26.0'
PAGE_ID = '1036844829507460'
user_token = os.environ['META_PAGE_ACCESS_TOKEN']
accounts = requests.get(f'{BASE}/me/accounts', headers={'Authorization': f'Bearer {user_token}'}, params={'fields': 'id,name,access_token', 'limit': 100}, timeout=30)
accounts.raise_for_status()
page = next(x for x in accounts.json().get('data', []) if x.get('id') == PAGE_ID)
page_token = page['access_token']
fields = 'id,created_time,message,permalink_url,attachments{media_type,type,media,target}'
out_dir = Path('/home/ubuntu/top5_meta_reels')
out_dir.mkdir(exist_ok=True)
results = []
for idx, row in enumerate(top, 1):
    pid = row['Platform_Content_ID']
    resp = requests.get(f'{BASE}/{pid}', headers={'Authorization': f'Bearer {page_token}'}, params={'fields': fields}, timeout=40)
    payload = resp.json()
    source = None
    for a in payload.get('attachments', {}).get('data', []):
        source = (a.get('media') or {}).get('source') or source
    video_path = ''
    if source:
        video_resp = requests.get(source, timeout=60)
        video_resp.raise_for_status()
        video_path = str(out_dir / f'{idx:02d}_{row["Meta_Reel_ID"]}.mp4')
        Path(video_path).write_bytes(video_resp.content)
    results.append({'rank': idx, 'queue': row, 'status_code': resp.status_code, 'payload': payload, 'video_path': video_path})
Path('/home/ubuntu/top5_meta_reels_raw.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'selected': len(top), 'downloaded': sum(bool(r['video_path']) for r in results), 'output': '/home/ubuntu/top5_meta_reels_raw.json'}, ensure_ascii=False))

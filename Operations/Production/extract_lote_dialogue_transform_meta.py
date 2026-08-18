import csv, json, os, re, requests
from datetime import datetime, timezone
from pathlib import Path

BASE = 'https://graph.facebook.com/v26.0'
root = Path('/home/ubuntu/universe-sent-me-growth-os')
user_token = os.environ['META_PAGE_ACCESS_TOKEN']
headers = {'Authorization': f'Bearer {user_token}'}
accounts = requests.get(f'{BASE}/me/accounts', headers=headers, params={'fields':'id,name,access_token,tasks','limit':100}, timeout=30)
accounts.raise_for_status()
page = next(x for x in accounts.json().get('data', []) if x.get('name') == 'Universe Sent Me')
token = page['access_token']
queue_path = root / 'Operations/Research/2026-08-17_Cola_Reconciliacion_Assets_Junio.csv'
rows = list(csv.DictReader(queue_path.open(encoding='utf-8-sig')))
unmatched = [r for r in rows if r.get('status') == 'Needs_Asset_Match']
# First-pass language selector; visual review remains authoritative for structure.
pattern = re.compile(r'\?|\bpero\b|\by\b|\bte\b|\byo\b|\bconmigo\b|\bextrañ|\bligue|\bUniverse\b|\besperando\b|\bdos\b', re.I)
candidates = [r for r in unmatched if pattern.search(r.get('caption') or '')]
candidates.sort(key=lambda r: (float(r.get('shares') or 0), float(r.get('interactions') or 0)), reverse=True)
selected = candidates[:15]
fields = 'id,created_time,message,full_picture,attachments{media_type,media{image{src,width,height}}}'
batch = [{'method':'GET','relative_url':f"{r['meta_id']}?fields={fields}"} for r in selected]
resp = requests.post(BASE, headers={'Authorization': f'Bearer {token}'}, data={'batch': json.dumps(batch)}, timeout=60)
resp.raise_for_status()
out = {'extracted_at_utc': datetime.now(timezone.utc).isoformat(), 'selection_basis':'Top 15 unresolved June cases with dialogue/relationship/Universe language cues; read-only.', 'selected_queue_rows': selected, 'batch_response': resp.json()}
out_path = root / 'Operations/Research/2026-08-19_Lote_Dialogo_Transformacion_Meta_Media.json'
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'selected': len(selected), 'output': str(out_path)}))
for row, item in zip(selected, out['batch_response']):
    print(row['meta_id'], item.get('code'), row.get('interactions'), row.get('shares'), row.get('caption'))

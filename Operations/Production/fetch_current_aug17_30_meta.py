import json
import os
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
PAGE_ID = '1036844829507460'
BASE = 'https://graph.facebook.com/v26.0'
TOKEN = os.environ['META_PAGE_ACCESS_TOKEN']

session = requests.Session()
headers = {'Authorization': f'Bearer {TOKEN}'}

accounts = session.get(f'{BASE}/me/accounts', params={'fields': 'id,name,access_token', 'limit': 100}, headers=headers, timeout=30)
accounts.raise_for_status()
accounts_json = accounts.json()
page = next((x for x in accounts_json.get('data', []) if x.get('id') == PAGE_ID), None)
if not page or not page.get('access_token'):
    raise RuntimeError('Page access token for Universe Sent Me was not returned by /me/accounts')
page_token = page['access_token']

params = {
    'fields': 'id,created_time,message,permalink_url,shares,reactions.limit(0).summary(true),comments.limit(0).summary(true),is_published',
    'since': '2026-08-17T00:00:00-05:00',
    'until': '2026-08-31T00:00:00-05:00',
    'limit': 100,
}
resp = session.get(f'{BASE}/{PAGE_ID}/feed', params=params, headers={'Authorization': f'Bearer {page_token}'}, timeout=30)
resp.raise_for_status()
raw = resp.json()
raw['_extraction_meta'] = {
    'extracted_at_utc': datetime.now(timezone.utc).isoformat(),
    'endpoint': f'{BASE}/{PAGE_ID}/feed',
    'page_id': PAGE_ID,
    'window_local': '2026-08-17 through 2026-08-30 America/Matamoros',
    'fields': params['fields'],
    'source': 'Meta Graph API v26.0',
}
out = ROOT / 'Operations/Research/2026-08-20_Cohorte_17_30_Meta_Raw_Current.json'
out.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'output': str(out), 'posts_returned': len(raw.get('data', [])), 'paging': bool(raw.get('paging'))}, ensure_ascii=False))

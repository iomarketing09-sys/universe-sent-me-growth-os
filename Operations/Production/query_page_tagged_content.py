#!/usr/bin/env python3
import json
import os
from pathlib import Path
import requests
from datetime import datetime, timedelta, timezone

GRAPH = 'https://graph.facebook.com/v26.0'
PAGE_ID = '1036844829507460'
OUT = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-20_Facebook_Page_Tagged_Audit.json')
token = os.environ.get('META_PAGE_ACCESS_TOKEN')
if not token:
    raise SystemExit('META_PAGE_ACCESS_TOKEN is not set')
headers = {'Authorization': f'Bearer {token}'}
s = requests.Session()
accounts = s.get(f'{GRAPH}/me/accounts', headers=headers, params={'fields': 'id,name,access_token', 'limit': 100}, timeout=30)
accounts.raise_for_status()
page = next((x for x in accounts.json().get('data', []) if x.get('id') == PAGE_ID), None)
page_token = page.get('access_token') if page else token
fields = 'id,from,message,created_time,permalink_url,comments.limit(100){id,from,message,created_time,message_tags}'
now = datetime.now(timezone.utc)
since = int((now - timedelta(days=3)).timestamp())
until = int(now.timestamp())
r = s.get(f'{GRAPH}/{PAGE_ID}/tagged', headers={'Authorization': f'Bearer {page_token}'}, params={'fields': fields, 'limit': 50, 'since': since, 'until': until}, timeout=30)
result = {'status_code': r.status_code, 'url': r.url}
try:
    result['payload'] = r.json()
except Exception:
    result['payload'] = {'text': r.text}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status_code': result['status_code'], 'data_count': len(result.get('payload', {}).get('data', [])), 'error': result.get('payload', {}).get('error')}, ensure_ascii=False))
for item in result.get('payload', {}).get('data', []):
    print(json.dumps(item, ensure_ascii=False))

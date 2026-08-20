#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

GRAPH = 'https://graph.facebook.com/v26.0'
PAGE_ID = '1036844829507460'
COMMENT_ID = '122151374823072582_1041411612075968'
MESSAGE = 'Eso ya no es aura débil… eso es falta de actualización espiritual. 😂✨'
OUT = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-20_Facebook_Comment_Publication.json')

user_token = os.environ.get('META_PAGE_ACCESS_TOKEN')
if not user_token:
    raise SystemExit('META_PAGE_ACCESS_TOKEN is not set')

s = requests.Session()
headers = {'Authorization': f'Bearer {user_token}'}
accounts = s.get(f'{GRAPH}/me/accounts', headers=headers, params={'fields': 'id,name,access_token', 'limit': 100}, timeout=30)
accounts.raise_for_status()
page = next((p for p in accounts.json().get('data', []) if p.get('id') == PAGE_ID), None)
if not page or not page.get('access_token'):
    raise SystemExit('Page token not found for Universe Sent Me')

r = s.post(f'{GRAPH}/{COMMENT_ID}/comments', headers={'Authorization': f"Bearer {page['access_token']}"}, data={'message': MESSAGE}, timeout=30)
try:
    payload = r.json()
except Exception:
    payload = {'text': r.text}
result = {
    'executed_at_utc': datetime.now(timezone.utc).isoformat(),
    'target_comment_id': COMMENT_ID,
    'message': MESSAGE,
    'status_code': r.status_code,
    'response': payload,
    'source': 'Meta Graph API v26.0',
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status_code': r.status_code, 'response': payload}, ensure_ascii=False))
if r.status_code >= 400:
    raise SystemExit(1)

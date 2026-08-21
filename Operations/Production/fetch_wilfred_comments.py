import json
import os
from datetime import datetime, timezone
from pathlib import Path
import requests

root = Path('/home/ubuntu/universe-sent-me-growth-os')
page_id = '1036844829507460'
post_id = '1036844829507460_122151374019072582'
base = 'https://graph.facebook.com/v26.0'
token = os.environ['META_PAGE_ACCESS_TOKEN']
headers = {'Authorization': f'Bearer {token}'}
s = requests.Session()
accounts = s.get(f'{base}/me/accounts', params={'fields':'id,access_token','limit':100}, headers=headers, timeout=30)
accounts.raise_for_status()
page = next(x for x in accounts.json().get('data', []) if x.get('id') == page_id)
fields = 'id,created_time,message,comments.limit(100){id,message,created_time,from}'
resp = s.get(f'{base}/{post_id}', params={'fields': fields}, headers={'Authorization': f"Bearer {page['access_token']}"}, timeout=30)
result = {'extracted_at_utc': datetime.now(timezone.utc).isoformat(), 'post_id': post_id, 'status_code': resp.status_code}
try:
    body = resp.json()
except Exception:
    body = {'raw': resp.text}
result['data'] = body
out = root / 'Operations/Research/2026-08-20_Wilfred_Comments_Evidence.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'output': str(out), 'status_code': resp.status_code, 'comment_count': len(body.get('comments', {}).get('data', [])) if isinstance(body, dict) else None, 'error': body.get('error') if isinstance(body, dict) else None}, ensure_ascii=False, indent=2))

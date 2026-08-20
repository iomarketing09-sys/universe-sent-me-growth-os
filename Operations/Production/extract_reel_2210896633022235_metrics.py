import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE = 'https://graph.facebook.com/v26.0'
PAGE_ID = '1036844829507460'
REEL_ID = '2210896633022235'
ROOT = Path('/home/ubuntu/universe-sent-me-growth-os')
OUT = ROOT / 'Operations/Research/2026-08-20_Meta_Reel_2210896633022235_Metrics.json'

root_headers = {'Authorization': f"Bearer {os.environ['META_PAGE_ACCESS_TOKEN']}"}
accounts = requests.get(
    f'{BASE}/me/accounts',
    params={'fields': 'id,name,access_token', 'limit': 100},
    headers=root_headers,
    timeout=30,
)
accounts.raise_for_status()
page = next(row for row in accounts.json().get('data', []) if row.get('id') == PAGE_ID)
page_headers = {'Authorization': f"Bearer {page['access_token']}"}
fields = 'id,created_time,message,permalink_url,attachments{media_type,type,target,url,media},reactions.limit(0).summary(true),comments.limit(0).summary(true),shares'
response = requests.get(
    f'{BASE}/{PAGE_ID}/posts',
    params={'fields': fields, 'limit': 100},
    headers=page_headers,
    timeout=60,
)
try:
    payload = response.json()
except ValueError:
    payload = {'raw': response.text}

matching = []
if response.ok and isinstance(payload, dict):
    for post in payload.get('data', []):
        permalink = post.get('permalink_url') or ''
        if post.get('id') == REEL_ID or f'/reel/{REEL_ID}' in permalink:
            attachments = post.get('attachments') or {}
            attachment_rows = attachments.get('data', []) if isinstance(attachments, dict) else []
            reactions = ((post.get('reactions') or {}).get('summary') or {}).get('total_count')
            comments = ((post.get('comments') or {}).get('summary') or {}).get('total_count')
            shares = (post.get('shares') or {}).get('count') if isinstance(post.get('shares'), dict) else None
            matching.append({
                'id': post.get('id'),
                'meta_page_post_id': post.get('id'),
                'reel_id_from_permalink': REEL_ID,
                'created_time': post.get('created_time'),
                'permalink_url': post.get('permalink_url'),
                'message': post.get('message', ''),
                'reactions': reactions,
                'comments': comments,
                'shares': shares,
                'attachments': attachment_rows,
            })

result = {
    'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
    'source': 'Meta Graph API v26.0 Page posts feed',
    'page_id': PAGE_ID,
    'reel_id': REEL_ID,
    'requested_fields': fields,
    'http_status': response.status_code,
    'posts_scanned': len(payload.get('data', [])) if isinstance(payload, dict) else None,
    'matches': matching,
    'data': payload if not response.ok else None,
    'error': payload.get('error') if isinstance(payload, dict) and not response.ok else None,
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
print(f'OUTPUT={OUT}')

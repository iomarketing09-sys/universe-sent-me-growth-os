import os, json, requests
from pathlib import Path
from datetime import datetime, date, timezone

BASE = 'https://graph.facebook.com/v26.0'
PAGE_ID = '1036844829507460'
IG_ID = '17841462696378190'
START = date(2026, 7, 22)
END = date(2026, 8, 18)
TOKEN = os.environ['META_PAGE_ACCESS_TOKEN']
HEADERS = {'Authorization': f'Bearer {TOKEN}'}
OUT = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-18_Instagram_Graph_API_28D.json')

def get(path, params=None, headers=HEADERS):
    r = requests.get(BASE + path, params=params or {}, headers=headers, timeout=30)
    payload = r.json()
    if r.status_code >= 400:
        raise RuntimeError(f'{path} HTTP {r.status_code}: {payload.get("error", payload)}')
    return payload

def parse_date(value):
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).date()
    except Exception:
        return None

def collect_all(path, params, headers):
    rows = []
    next_url = BASE + path
    first = True
    while next_url:
        r = requests.get(next_url, params=params if first else None, headers=headers, timeout=30)
        payload = r.json()
        if r.status_code >= 400:
            raise RuntimeError(f'{path} HTTP {r.status_code}: {payload.get("error", payload)}')
        rows.extend(payload.get('data', []))
        next_url = payload.get('paging', {}).get('next')
        first = False
    return rows

me = get('/me', {'fields': 'id,name'})
accounts = get('/me/accounts', {'fields': 'id,name,access_token', 'limit': 100}).get('data', [])
page = next((x for x in accounts if x['id'] == PAGE_ID), None)
if not page:
    raise RuntimeError('Universe Sent Me page not found in /me/accounts')
page_headers = {'Authorization': f"Bearer {page['access_token']}"}
page_info = get('/' + PAGE_ID, {'fields': 'id,name,instagram_business_account'}, page_headers)
media_fields = 'id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count'
media = collect_all('/' + IG_ID + '/media', {'fields': media_fields, 'limit': 100}, page_headers)
media = [m for m in media if (d := parse_date(m.get('timestamp', ''))) and START <= d <= END]

rows = []
for m in media:
    insights = None
    insight_error = None
    metrics = 'impressions,reach,saved,shares,total_interactions,likes,comments'
    try:
        insights = get('/' + m['id'] + '/insights', {'metric': metrics}, page_headers).get('data', [])
    except Exception as e:
        insight_error = str(e)
    rows.append({'media': m, 'insights': insights, 'insight_error': insight_error})

result = {
    'title': 'Instagram Graph API — 28-day performance extraction',
    'purpose': 'Record the direct Meta Graph API extraction for Instagram between 2026-07-22 and 2026-08-18.',
    'status': 'Active',
    'created': '2026-08-18',
    'updated': '2026-08-18',
    'version': '1.0',
    'author': 'Manus AI (CGO)',
    'organization': 'Operations/Research',
    'cut': {'start_local': str(START), 'end_local': str(END)},
    'account': {'page_id': PAGE_ID, 'page_name': page_info.get('name'), 'instagram_user_id': IG_ID, 'me': me},
    'media_count': len(rows),
    'rows': rows,
    'source': 'Meta Graph API v26.0 direct',
    'retrieved_at_utc': datetime.now(timezone.utc).isoformat()
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'page': page_info.get('name'), 'instagram_user_id': IG_ID, 'media_count': len(rows), 'insight_success': sum(1 for x in rows if x['insights'] is not None), 'insight_errors': sum(1 for x in rows if x['insight_error']), 'output': str(OUT)}, ensure_ascii=False))

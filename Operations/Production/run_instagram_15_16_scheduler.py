#!/usr/bin/env python3
import csv, json, os, time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import requests

BASE = 'https://graph.facebook.com/v26.0'
TZ = ZoneInfo('America/Mexico_City')
REPO = Path('/home/ubuntu/universe-sent-me-growth-os')
CALENDAR = REPO / 'Operations/Research/2026-08-15_Calendario_15_16_Agosto.csv'
PUBLIC_URLS_FILE = Path('/home/ubuntu/instagram_15_16_public_urls.json')
STATE_FILE = Path('/home/ubuntu/instagram_scheduler_15_16_state.json')
TARGET_DATES = {'2026-08-15', '2026-08-16'}


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return default


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def derive_page_token():
    user_token = os.environ['META_PAGE_ACCESS_TOKEN']
    r = requests.get(BASE + '/me/accounts', headers={'Authorization': f'Bearer {user_token}'}, params={'fields': 'id,access_token,instagram_business_account'}, timeout=30)
    r.raise_for_status()
    page = next(x for x in r.json().get('data', []) if x.get('id') == '1036844829507460')
    return page['access_token'], page['instagram_business_account']['id']


def public_asset_url(filename):
    manifest = load_json(PUBLIC_URLS_FILE, {})
    entry = manifest.get(filename)
    if not entry or not entry.get('public_url'):
        raise RuntimeError(f'No prepared temporary URL for exact approved filename: {filename}')
    return entry['public_url']


def publish_row(row, page_token, ig_id, state):
    filename = row['Archivo']
    key = f"{row['Fecha']} {row['Hora']} {filename}"
    if state.get(key, {}).get('ig_media_id') or row.get('IG_Media_ID'):
        return {'key': key, 'status': 'already_done', 'ig_media_id': state.get(key, {}).get('ig_media_id') or row.get('IG_Media_ID')}
    image_url = public_asset_url(filename)
    r = requests.post(BASE + f'/{ig_id}/media', headers={'Authorization': f'Bearer {page_token}'}, data={'image_url': image_url, 'caption': row['Caption']}, timeout=60)
    create = r.json()
    if r.status_code >= 400 or 'id' not in create:
        state[key] = {'status': 'container_error', 'http_status': r.status_code, 'response': create, 'updated_at': datetime.now(TZ).isoformat()}
        return state[key]
    container_id = create['id']
    state[key] = {'status': 'container_created', 'ig_container_id': container_id, 'updated_at': datetime.now(TZ).isoformat()}
    save_json(STATE_FILE, state)
    status = None
    status_response = {}
    for _ in range(12):
        s = requests.get(BASE + f'/{container_id}', headers={'Authorization': f'Bearer {page_token}'}, params={'fields': 'id,status_code,status'}, timeout=30)
        status_response = s.json(); status = status_response.get('status_code')
        if status in {'FINISHED', 'PUBLISHED', 'ERROR', 'EXPIRED'}: break
        time.sleep(5)
    if status not in {'FINISHED', 'PUBLISHED'}:
        state[key].update({'status': 'container_not_ready', 'container_status': status_response, 'updated_at': datetime.now(TZ).isoformat()})
        return state[key]
    p = requests.post(BASE + f'/{ig_id}/media_publish', headers={'Authorization': f'Bearer {page_token}'}, data={'creation_id': container_id}, timeout=60)
    publish = p.json()
    if p.status_code >= 400 or 'id' not in publish:
        state[key].update({'status': 'publish_error', 'http_status': p.status_code, 'response': publish, 'updated_at': datetime.now(TZ).isoformat()})
        return state[key]
    media_id = publish['id']
    verify = requests.get(BASE + f'/{media_id}', headers={'Authorization': f'Bearer {page_token}'}, params={'fields': 'id,permalink,timestamp,media_type,media_product_type'}, timeout=30).json()
    state[key].update({'status': 'published', 'ig_media_id': media_id, 'permalink': verify.get('permalink'), 'published_at': verify.get('timestamp'), 'updated_at': datetime.now(TZ).isoformat()})
    return state[key]


def main():
    now = datetime.now(TZ)
    state = load_json(STATE_FILE, {})
    rows = list(csv.DictReader(CALENDAR.open(encoding='utf-8')))
    due = []
    for row in rows:
        if row.get('Fecha') not in TARGET_DATES: continue
        platform = row.get('Plataforma', '')
        if platform != 'Facebook; Instagram selectivo': continue
        if row.get('IG_Estado') == 'PUBLICADA_PRUEBA' or row.get('IG_Media_ID'): continue
        target = datetime.strptime(f"{row['Fecha']} {row['Hora']}", '%Y-%m-%d %H:%M').replace(tzinfo=TZ)
        # The schedule fires at candidate minute groups. Publish only within an 8-minute window after the exact local slot; never catch up a missed slot late.
        if target <= now < target + timedelta(minutes=8): due.append(row)
    if not due:
        print(json.dumps({'now_local': now.isoformat(), 'status': 'nothing_due', 'target_dates': sorted(TARGET_DATES)}, ensure_ascii=False))
        return
    page_token, ig_id = derive_page_token()
    results = []
    for row in due:
        key = f"{row['Fecha']} {row['Hora']} {row['Archivo']}"
        if state.get(key, {}).get('status') == 'published': continue
        try: result = publish_row(row, page_token, ig_id, state)
        except Exception as exc: result = {'key': key, 'status': 'runner_error', 'error': str(exc), 'updated_at': datetime.now(TZ).isoformat()}; state[key] = result
        save_json(STATE_FILE, state); results.append(result)
    print(json.dumps({'now_local': now.isoformat(), 'processed': results}, ensure_ascii=False, indent=2))

if __name__ == '__main__': main()

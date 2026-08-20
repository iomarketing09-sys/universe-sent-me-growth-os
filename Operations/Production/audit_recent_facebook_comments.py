#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

GRAPH = 'https://graph.facebook.com/v26.0'
PAGE_ID = '1036844829507460'
OUT = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-20_Facebook_Comments_Audit.json')

base_token = os.environ.get('META_PAGE_ACCESS_TOKEN')
if not base_token:
    raise SystemExit('META_PAGE_ACCESS_TOKEN is not set')

session = requests.Session()
headers = {'Authorization': f'Bearer {base_token}'}
accounts = session.get(
    f'{GRAPH}/me/accounts',
    headers=headers,
    params={'fields': 'id,name,access_token', 'limit': 100},
    timeout=30,
)
accounts.raise_for_status()
account_data = accounts.json().get('data', [])
page = next((a for a in account_data if a.get('id') == PAGE_ID), None)
page_token = page.get('access_token') if page else base_token

# Review the last three local days while keeping the query bounded.
now = datetime.now(timezone.utc)
since = int((now - timedelta(days=3)).timestamp())
params = {
    'since': since,
    'limit': 50,
    'fields': 'id,created_time,message,permalink_url,comments.limit(100){id,from,message,created_time,like_count,message_tags}',
}
feed = session.get(f'{GRAPH}/{PAGE_ID}/feed', headers={'Authorization': f'Bearer {page_token}'}, params=params, timeout=30)
feed.raise_for_status()
raw = feed.json()

posts = []
mentions = []
for post in raw.get('data', []):
    post_record = {
        'post_id': post.get('id'),
        'created_time': post.get('created_time'),
        'message': post.get('message'),
        'permalink_url': post.get('permalink_url'),
        'comments': [],
    }
    for c in post.get('comments', {}).get('data', []):
        comment = {
            'comment_id': c.get('id'),
            'from': c.get('from'),
            'message': c.get('message'),
            'created_time': c.get('created_time'),
            'like_count': c.get('like_count'),
            'message_tags': c.get('message_tags', []),
        }
        post_record['comments'].append(comment)
        text = (comment.get('message') or '').lower()
        sender = json.dumps(comment.get('from') or {}, ensure_ascii=False).lower()
        if 'universe sent me' in text or '@universe' in text or 'universe' in sender or any('universe' in json.dumps(tag, ensure_ascii=False).lower() for tag in comment.get('message_tags', [])):
            mentions.append({
                'post_id': post_record['post_id'],
                'post_permalink': post_record['permalink_url'],
                **comment,
            })
    posts.append(post_record)

result = {
    'retrieved_at_utc': now.isoformat(),
    'lookback_days': 3,
    'since_epoch': since,
    'page_id': PAGE_ID,
    'post_count': len(posts),
    'comment_count': sum(len(p['comments']) for p in posts),
    'mention_candidate_count': len(mentions),
    'mentions': mentions,
    'posts': posts,
    'source': 'Meta Graph API v26.0 / Page feed with nested comments',
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: result[k] for k in ('retrieved_at_utc','post_count','comment_count','mention_candidate_count')}, ensure_ascii=False))
for m in mentions:
    print(json.dumps(m, ensure_ascii=False))

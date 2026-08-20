#!/usr/bin/env python3
import json
from pathlib import Path

p = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-20_Facebook_Comments_Audit.json')
data = json.loads(p.read_text(encoding='utf-8'))
page_id = data['page_id']
for post in data['posts']:
    for c in post.get('comments', []):
        tags = c.get('message_tags') or []
        if tags and (not c.get('from') or c.get('from', {}).get('id') != page_id):
            print(json.dumps({
                'post_id': post.get('post_id'),
                'permalink_url': post.get('permalink_url'),
                'comment_id': c.get('comment_id'),
                'from': c.get('from'),
                'message': c.get('message'),
                'created_time': c.get('created_time'),
                'message_tags': tags,
            }, ensure_ascii=False))

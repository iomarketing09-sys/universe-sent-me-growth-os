#!/usr/bin/env python3
import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'Operations/Research/2026-08-23_Facebook_Performance_Meta_API.json'
OUTPUT = ROOT / 'Operations/Research/2026-08-23_Facebook_Performance_Summary.json'
data = json.loads(INPUT.read_text(encoding='utf-8'))
posts = data.get('posts', [])

def num(value):
    return float(value) if isinstance(value, (int, float)) else 0.0

def label(post):
    types = ' '.join(post.get('content_types') or []).lower()
    msg = post.get('message') or ''
    if 'video' in types or 'reel' in types or 'video' in msg.lower():
        return 'Video/Reel'
    return 'Imagen/Foto'

def dt(post):
    return datetime.fromisoformat(post['created_time'].replace('+0000','+00:00'))

for post in posts:
    post['format_label'] = label(post)
    post['date'] = dt(post).date().isoformat()
    post['hour_utc'] = dt(post).hour
    post['engagement_public'] = int(post.get('engagement_public') or 0)

values = [p['engagement_public'] for p in posts]
by_format = defaultdict(list)
by_date = defaultdict(list)
for p in posts:
    by_format[p['format_label']].append(p)
    by_date[p['date']].append(p)

def stats(rows):
    vals = [r['engagement_public'] for r in rows]
    return {
        'n': len(rows),
        'total_engagement_public': int(sum(vals)),
        'mean': round(sum(vals)/len(vals),2) if vals else 0,
        'median': statistics.median(vals) if vals else 0,
        'max': int(max(vals)) if vals else 0,
        'total_reactions': int(sum(num(r.get('reactions')) for r in rows)),
        'total_comments': int(sum(num(r.get('comments')) for r in rows)),
        'total_shares': int(sum(num(r.get('shares')) for r in rows)),
    }

insight_status = Counter()
for p in posts:
    for metric, item in (p.get('insights') or {}).items():
        insight_status[(metric, item.get('status_code'))] += 1

page_metric_values = {}
for metric, item in data.get('page_insights', {}).items():
    page_metric_values[metric] = {
        'status_code': item.get('status_code'),
        'value': item.get('value'),
        'values': item.get('values', []),
        'error': item.get('error'),
    }

summary = {
    'source': data.get('source'),
    'retrieved_at': data.get('retrieved_at'),
    'posts_returned': len(posts),
    'window': {
        'latest_created_time': max((p['created_time'] for p in posts), default=None),
        'earliest_created_time': min((p['created_time'] for p in posts), default=None),
    },
    'overall': stats(posts),
    'by_format': {k: stats(v) for k,v in sorted(by_format.items())},
    'by_date': {k: stats(v) for k,v in sorted(by_date.items())},
    'top_posts': [
        {
            'rank': i+1,
            'id': p['id'],
            'created_time': p['created_time'],
            'format': p['format_label'],
            'engagement_public': p['engagement_public'],
            'reactions': p.get('reactions'),
            'comments': p.get('comments'),
            'shares': p.get('shares'),
            'message': (p.get('message') or '')[:140].replace('\n',' '),
        }
        for i,p in enumerate(sorted(posts, key=lambda x: x['engagement_public'], reverse=True)[:10])
    ],
    'page_insights': page_metric_values,
    'post_insight_status': {f'{metric}|HTTP_{status}': count for (metric,status),count in sorted(insight_status.items())},
}
OUTPUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))

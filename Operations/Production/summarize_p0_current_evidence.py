import json
from pathlib import Path

src = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-19_P0_17_Agosto_Current_Evidence.jsonl')
out = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-19_P0_17_Agosto_Current_Summary.json')
rows = []
for line in src.read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    d = json.loads(line)
    rows.append({
        'meta_post_id': d.get('id'),
        'created_time': d.get('created_time'),
        'message': d.get('message'),
        'reactions_lifetime': d.get('reactions', {}).get('summary', {}).get('total_count', 0),
        'comments_lifetime': d.get('comments', {}).get('summary', {}).get('total_count', 0),
        'shares_lifetime': d.get('shares', {}).get('count', 0),
        'interactions_observed': (
            d.get('reactions', {}).get('summary', {}).get('total_count', 0)
            + d.get('comments', {}).get('summary', {}).get('total_count', 0)
            + d.get('shares', {}).get('count', 0)
        ),
    })
summary = {
    'experiment_id': 'EXP-2026-08-CAL-01',
    'official_p0_scope': 'five confirmed Facebook posts published 2026-08-17',
    'window_type': 'current lifetime totals observed at extraction time; not exact 24h/72h snapshots',
    'rows': rows,
    'totals': {
        'reactions_lifetime': sum(r['reactions_lifetime'] for r in rows),
        'comments_lifetime': sum(r['comments_lifetime'] for r in rows),
        'shares_lifetime': sum(r['shares_lifetime'] for r in rows),
        'interactions_observed': sum(r['interactions_observed'] for r in rows),
    },
}
out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))

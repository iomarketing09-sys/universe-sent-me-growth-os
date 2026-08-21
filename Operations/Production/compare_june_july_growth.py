from pathlib import Path
import csv, json, math, statistics
from collections import defaultdict, Counter

root = Path('/home/ubuntu/universe-sent-me-growth-os')
source = root / 'Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv'
june_tax = root / 'Operations/Research/2026-08-17_Junio_Analisis_Base.csv'
july_tax = root / 'Operations/Research/2026-08-17_Julio_Analisis_Taxonomia.csv'
out = root / 'Operations/Research/2026-08-20_Comparativo_Crecimiento_Junio_Julio.json'

def read_csv(path):
    with path.open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

rows = [r for r in read_csv(source) if r['month'] in {'2026-06', '2026-07'}]
for r in rows:
    for f in ['reactions','comments','shares','interactions','message_len']:
        r[f] = float(r[f] or 0)
    r['hour_int'] = int(float(r['hour']))
    r['minimal'] = r['minimal_copy_proxy'].lower() == 'true'

summary = {}
for month in ['2026-06','2026-07']:
    rs = [r for r in rows if r['month'] == month]
    def metric(field):
        vals = [r[field] for r in rs]
        return {'total': sum(vals), 'mean': statistics.mean(vals) if vals else 0, 'median': statistics.median(vals) if vals else 0, 'p90': sorted(vals)[max(0, math.ceil(.9*len(vals))-1)] if vals else 0}
    summary[month] = {
        'posts': len(rs),
        'reactions': metric('reactions'),
        'comments': metric('comments'),
        'shares': metric('shares'),
        'interactions': metric('interactions'),
        'minimal_copy': {
            'n': sum(r['minimal'] for r in rs),
            'share_of_posts': sum(r['minimal'] for r in rs)/len(rs) if rs else 0,
            'median_interactions': statistics.median([r['interactions'] for r in rs if r['minimal']]) if any(r['minimal'] for r in rs) else 0,
            'median_shares': statistics.median([r['shares'] for r in rs if r['minimal']]) if any(r['minimal'] for r in rs) else 0,
        },
        'non_minimal_copy': {
            'n': sum(not r['minimal'] for r in rs),
            'share_of_posts': sum(not r['minimal'] for r in rs)/len(rs) if rs else 0,
            'median_interactions': statistics.median([r['interactions'] for r in rs if not r['minimal']]) if any(not r['minimal'] for r in rs) else 0,
            'median_shares': statistics.median([r['shares'] for r in rs if not r['minimal']]) if any(not r['minimal'] for r in rs) else 0,
        },
        'top_posts': [
            {k: r[k] for k in ['id','date','hour','message','interactions','reactions','comments','shares','minimal_copy_proxy']}
            for r in sorted(rs, key=lambda x: (x['interactions'], x['shares']), reverse=True)[:10]
        ],
        'hours': [],
        'weekdays': [],
    }
    by_hour = defaultdict(list)
    for r in rs: by_hour[r['hour_int']].append(r)
    summary[month]['hours'] = [
        {'hour': h, 'posts': len(v), 'mean_interactions': statistics.mean([r['interactions'] for r in v]), 'median_interactions': statistics.median([r['interactions'] for r in v]), 'total_shares': sum(r['shares'] for r in v)}
        for h, v in sorted(by_hour.items(), key=lambda kv: statistics.mean([x['interactions'] for x in kv[1]]), reverse=True)
    ]
    by_day = defaultdict(list)
    for r in rs: by_day[r['weekday']].append(r)
    summary[month]['weekdays'] = [
        {'weekday': d, 'posts': len(v), 'mean_interactions': statistics.mean([r['interactions'] for r in v]), 'median_interactions': statistics.median([r['interactions'] for r in v]), 'total_shares': sum(r['shares'] for r in v)}
        for d, v in sorted(by_day.items(), key=lambda kv: statistics.mean([x['interactions'] for x in kv[1]]), reverse=True)
    ]

# Growth comparisons using the same interactions definition.
def pct(a, b):
    return (b/a - 1) if a else None
summary['comparison'] = {
    'posts_growth_july_vs_june': pct(summary['2026-06']['posts'], summary['2026-07']['posts']),
    'total_interactions_growth_july_vs_june': pct(summary['2026-06']['interactions']['total'], summary['2026-07']['interactions']['total']),
    'median_interactions_change_july_vs_june': pct(summary['2026-06']['interactions']['median'], summary['2026-07']['interactions']['median']),
    'median_shares_change_july_vs_june': pct(summary['2026-06']['shares']['median'], summary['2026-07']['shares']['median']),
    'minimal_share_of_posts_change': summary['2026-07']['minimal_copy']['share_of_posts'] - summary['2026-06']['minimal_copy']['share_of_posts'],
}

# Taxonomy coverage summary; July is only the six reconciled individual top posts.
for label, path in [('june_taxonomy', june_tax), ('july_taxonomy', july_tax)]:
    rs = read_csv(path)
    summary[label] = {
        'rows': len(rs),
        'humor_counts': Counter(r.get('tipo_humor_normalizado','') for r in rs),
        'character_counts': Counter(r.get('personaje_principal_normalizado','') for r in rs),
        'role_counts': Counter(r.get('rol_narrativo','') for r in rs),
        'tagging_counts': Counter(r.get('potencial_etiquetado','') for r in rs),
    }

out.write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=dict), encoding='utf-8')
print(out)
print(json.dumps(summary['comparison'], indent=2, ensure_ascii=False))
for m in ['2026-06','2026-07']:
    print(m, summary[m]['posts'], summary[m]['interactions']['total'], summary[m]['interactions']['median'], summary[m]['shares']['median'], summary[m]['minimal_copy'])

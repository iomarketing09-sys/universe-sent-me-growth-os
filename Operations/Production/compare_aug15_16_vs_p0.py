import json
from pathlib import Path
import statistics

root = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research')
cohort = json.loads((root / '2026-08-20_Cohorte_15_16_Analysis.json').read_text(encoding='utf-8'))
p0 = json.loads((root / '2026-08-19_P0_17_Agosto_Current_Summary.json').read_text(encoding='utf-8'))

def stats(name, data, n):
    t = data['totals']
    return {
        'cohort': name,
        'n': n,
        'reactions': t['reactions_lifetime'] if 'reactions_lifetime' in t else t['reactions'],
        'comments': t['comments_lifetime'] if 'comments_lifetime' in t else t['comments'],
        'shares': t['shares_lifetime'] if 'shares_lifetime' in t else t['shares'],
        'interactions': t['interactions_observed'] if 'interactions_observed' in t else t['interactions'],
        'mean_interactions': (t['interactions_lifetime'] if 'interactions_lifetime' in t else (t['interactions_observed'] if 'interactions_observed' in t else t['interactions'])) / n,
    }

c = stats('Cohorte 15–16', cohort, cohort['n'])
p = stats('P0 17 agosto', p0, len(p0['rows']))
comparison = {
    'cohort': c,
    'p0': p,
    'per_post_ratio_cohort_to_p0': c['mean_interactions'] / p['mean_interactions'],
    'top_cohort_rows': sorted(cohort['rows'], key=lambda r: r['interactions'], reverse=True)[:3],
    'top_p0_rows': sorted(p0['rows'], key=lambda r: r['interactions_observed'], reverse=True)[:3],
}
(root / '2026-08-20_Cohorte_15_16_vs_P0_Comparison.json').write_text(json.dumps(comparison, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(comparison, ensure_ascii=False, indent=2))

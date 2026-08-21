import json
import statistics
from collections import defaultdict
from pathlib import Path

root = Path('/home/ubuntu/universe-sent-me-growth-os')
cut_path = root / 'Operations/Research/2026-08-20_Cohorte_17_30_Current_Cut.json'
out_path = root / 'Operations/Research/2026-08-20_Wilfred_Outlier_Replication_Analysis.json'
data = json.loads(cut_path.read_text(encoding='utf-8'))
rows = data['rows']
wilfred = next(r for r in rows if r.get('publication_id') == 'PUB-FB-17_30-06' or '2608029' in (r.get('asset_ref') or ''))
rest = [r for r in rows if r is not wilfred]
same_slot = [r for r in rows if r['slot_local'] == wilfred['slot_local'] and r is not wilfred]

def agg(items):
    vals = [r['interactions'] for r in items]
    return {
        'n': len(items),
        'interactions': sum(vals),
        'reactions': sum(r['reactions'] for r in items),
        'comments': sum(r['comments'] for r in items),
        'shares': sum(r['shares'] for r in items),
        'mean_interactions': statistics.mean(vals) if vals else 0,
        'median_interactions': statistics.median(vals) if vals else 0,
        'mean_shares': statistics.mean([r['shares'] for r in items]) if items else 0,
        'median_shares': statistics.median([r['shares'] for r in items]) if items else 0,
    }

wilfred_i = wilfred['interactions']
rest_agg = agg(rest)
cohort_agg = agg(rows)
slot_agg = agg(same_slot)
result = {
    'source': str(cut_path.relative_to(root)),
    'snapshot_extraction_time_utc': data.get('extraction_time_utc'),
    'wilfred': {**wilfred, 'share_rate_of_interactions': wilfred['shares'] / wilfred_i if wilfred_i else 0},
    'cohort': cohort_agg,
    'rest_without_wilfred': rest_agg,
    'same_slot_other_images': slot_agg,
    'concentration': {
        'wilfred_share_of_cohort_interactions': wilfred_i / cohort_agg['interactions'] if cohort_agg['interactions'] else 0,
        'wilfred_share_of_cohort_shares': wilfred['shares'] / cohort_agg['shares'] if cohort_agg['shares'] else 0,
        'wilfred_vs_rest_mean_interactions_multiple': wilfred_i / rest_agg['mean_interactions'] if rest_agg['mean_interactions'] else 0,
        'wilfred_vs_rest_median_interactions_multiple': wilfred_i / rest_agg['median_interactions'] if rest_agg['median_interactions'] else 0,
        'wilfred_vs_same_slot_mean_multiple': wilfred_i / slot_agg['mean_interactions'] if slot_agg['mean_interactions'] else 0,
        'rest_share_rate_of_interactions': rest_agg['shares'] / rest_agg['interactions'] if rest_agg['interactions'] else 0,
        'same_slot_share_rate_of_interactions': slot_agg['shares'] / slot_agg['interactions'] if slot_agg['interactions'] else 0,
    },
    'interpretation_guard': 'Observational outlier; no causal attribution to Wilfred, 19:00, one-scene format, or caption without comparable controls.'
}
out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: result[k] for k in ['wilfred','cohort','rest_without_wilfred','same_slot_other_images','concentration']}, ensure_ascii=False, indent=2))

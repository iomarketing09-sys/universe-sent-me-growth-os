from pathlib import Path
import csv, json, statistics

root = Path('/home/ubuntu/universe-sent-me-growth-os')
p = root / 'Operations/Research/2026-08-20_Expansion_Round2_Candidatos.csv'
out = root / 'Operations/Research/2026-08-20_Expansion_Round2_Summary.json'
with p.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

summary = {}
for cell in sorted({r['Cell_Name'] for r in rows}):
    rs = [r for r in rows if r['Cell_Name'] == cell]
    included = [r for r in rs if r['Estado_Candidato'] == 'Current_Comparable']
    def nums(field, source=included):
        return [float(r[field]) for r in source]
    summary[cell] = {
        'rows': len(rs),
        'current_comparable': len(included),
        'candidate_review': sum(r['Estado_Candidato'] == 'Candidate_Review' for r in rs),
        'excluded_or_borderline': sum(r['Estado_Candidato'] in {'Excluded_Not_Comparable', 'Borderline_Not_Comparable'} for r in rs),
        'interactions': nums('Interacciones'),
        'shares': nums('Shares'),
        'median_interactions': statistics.median(nums('Interacciones')) if included else None,
        'median_shares': statistics.median(nums('Shares')) if included else None,
        'caption_treatments': sorted({r['Caption_Treatment'] for r in included}),
        'meta_ids': [r['Meta_ID'] for r in included],
    }
# Explicit comparison to the strict three-panel base.
strict = {'n': 1, 'interactions': [155], 'shares': [19]}
two = [r for r in rows if r['Cell_Name'] == 'Microhistoria secuencial — dos paneles' and r['Estado_Candidato'] == 'Current_Comparable']
summary['comparison_microstory_panel_count'] = {
    'strict_three_panel_n': strict['n'],
    'strict_three_panel_interactions': strict['interactions'],
    'strict_three_panel_shares': strict['shares'],
    'two_panel_n': len(two),
    'two_panel_interactions': [float(r['Interacciones']) for r in two],
    'two_panel_shares': [float(r['Shares']) for r in two],
    'two_panel_median_interactions': statistics.median([float(r['Interacciones']) for r in two]) if two else None,
    'two_panel_median_shares': statistics.median([float(r['Shares']) for r in two]) if two else None,
    'interpretation': 'Descriptive subcell only; do not pool with three-panel microstory until definition is approved.'
}
out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(summary, indent=2, ensure_ascii=False))

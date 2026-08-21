from pathlib import Path
import csv, json
from collections import Counter, defaultdict

root = Path('/home/ubuntu/universe-sent-me-growth-os')
p = root / 'Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv'
out = root / 'Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Summary.json'
with p.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

cells = defaultdict(list)
for r in rows:
    cells[r['Cell_Name']].append(r)
summary = {}
for cell, rs in cells.items():
    current = [r for r in rs if r['Estado_Candidato'] == 'Current_Comparable']
    candidates = [r for r in rs if r['Estado_Candidato'] == 'Candidate_Review']
    summary[cell] = {
        'current_comparable': len(current),
        'candidate_review': len(candidates),
        'borderline_not_comparable': sum(r['Estado_Candidato'] == 'Borderline_Not_Comparable' for r in rs),
        'needed_for_signal_n3': max(0, 3-len(current)),
        'needed_for_operational_n5': max(0, 5-len(current)),
        'current_meta_ids': [r['Meta_ID'] for r in current],
        'candidate_meta_ids': [r['Meta_ID'] for r in candidates],
        'candidate_interactions': [r['Interacciones'] for r in candidates],
    }
out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
for cell, v in summary.items():
    print(cell, v)

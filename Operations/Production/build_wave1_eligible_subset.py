from pathlib import Path
import csv, json
from collections import Counter

root = Path('/home/ubuntu/universe-sent-me-growth-os')
source = root / 'Operations/Research/2026-08-20_Overlay_Wave1_Calendario_17_30.csv'
out_csv = root / 'Operations/Research/2026-08-20_Wave1_Eligible_Operational_Subset.csv'
out_json = root / 'Operations/Research/2026-08-20_Wave1_Eligibility_Summary.json'
with source.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
eligible = [r for r in rows if r['Overlay_Eligibility'] == 'Eligible']
fields = list(rows[0].keys()) + ['Operational_Subset_Status']
with out_csv.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in eligible:
        w.writerow({**r, 'Operational_Subset_Status': 'Eligible_Candidate_Not_Published'})
summary = {
    'source': str(source.relative_to(root)),
    'subset': str(out_csv.relative_to(root)),
    'eligible_rows': len(eligible),
    'excluded_hold_rows': sum(r['Approval_Status'] == 'Approved_Excluded' for r in rows),
    'candidate_review_rows': sum(r['Overlay_Eligibility'] == 'Candidate_Review' for r in rows),
    'family_counts': dict(Counter(r['Family_ID_Final'] for r in eligible)),
    'caption_treatment_counts': dict(Counter(r['Caption_Treatment_Propuesto'] for r in eligible)),
    'publication_authorized': False,
    'calendar_modified': False,
}
out_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(summary, indent=2, ensure_ascii=False))

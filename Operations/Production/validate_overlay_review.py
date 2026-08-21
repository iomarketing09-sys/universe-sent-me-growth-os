from pathlib import Path
import csv, json
from collections import Counter

root = Path('/home/ubuntu/universe-sent-me-growth-os')
source = root / 'Operations/Research/2026-08-20_Overlay_Wave1_Calendario_17_30.csv'
out = root / 'Operations/Research/2026-08-20_Overlay_Wave1_Review_Summary.json'
with source.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
ids = [r['Overlay_ID'] for r in rows]
errors = []
if len(rows) != 15: errors.append(f'expected_15_rows_got_{len(rows)}')
if len(set(ids)) != len(ids): errors.append('duplicate_overlay_id')
for r in rows:
    if r['P0_Eligible'] != 'No': errors.append(f"p0_guard_failed:{r['Overlay_ID']}")
    if r['Affiliate_Attachment'] != 'No': errors.append(f"affiliate_guard_failed:{r['Overlay_ID']}")
    if r['Reuse_Status'] != 'New_Test': errors.append(f"reuse_guard_failed:{r['Overlay_ID']}")
    if r['Overlay_Eligibility'] == 'Hold':
        if r['Approval_Status'] != 'Approved_Excluded': errors.append(f"hold_not_approved_excluded:{r['Overlay_ID']}")
    elif r['Approval_Status'] != 'Pending':
        errors.append(f"approval_state_changed:{r['Overlay_ID']}")
summary = {
    'validation': 'PASS' if not errors else 'FAIL',
    'rows': len(rows),
    'overlay_status_counts': dict(Counter(r['Overlay_Eligibility'] for r in rows)),
    'family_counts': dict(Counter(r['Family_ID_Final'] for r in rows)),
    'risk_counts': dict(Counter(r['Risk_Flag'] for r in rows)),
    'caption_treatment_counts': dict(Counter(r['Caption_Treatment_Propuesto'] for r in rows)),
    'errors': errors,
    'source': str(source.relative_to(root)),
}
out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(summary, indent=2, ensure_ascii=False))

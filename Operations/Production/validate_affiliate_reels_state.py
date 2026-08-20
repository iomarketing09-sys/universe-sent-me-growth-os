import csv
from pathlib import Path

root = Path('/home/ubuntu/universe-sent-me-growth-os')
ledger = list(csv.DictReader((root / 'Operations/Research/Affiliate_Link_Ledger.csv').open(encoding='utf-8')))
pilot = [r for r in ledger if r['Campaign_ID'] == 'USM-AFF-FB20260818-30-P01' and r['Link_ID'].startswith('ML-FB-AFF')]
assignments = list(csv.DictReader((root / 'Operations/Research/Affiliate_Pilot_Assignments.csv').open(encoding='utf-8')))
print('pilot_rows=', len(pilot))
print('pilot_statuses=', sorted(set(r['Status'] for r in pilot)))
print('pilot_native_statuses=', sorted(set(r['Native_Product_Status'] for r in pilot)))
print('assignment_rows=', len(assignments))
print('assignment_statuses=', sorted(set(r['Status'] for r in assignments)))
print('assignment_approvals=', sorted(set(r['Approval_Status'] for r in assignments)))

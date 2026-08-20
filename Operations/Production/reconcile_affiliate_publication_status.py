import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/Affiliate_Link_Ledger.csv')
rows = []
with path.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    rows = list(reader)

pilot_ids = {f'ML-FB-AFF0{i}-' for i in range(1, 10)} | {'ML-FB-AFF10-'}
updated = 0
for r in rows:
    if r['Campaign_ID'] == 'USM-AFF-FB20260818-30-P01' and r['Link_ID'].startswith('ML-FB-AFF'):
        # AFF-01 already has Meta-confirmed attachment; the remaining nine are user-confirmed.
        if r['Native_Product_Status'] in ('', 'Pending') or r['Publication_Status'] in ('', 'Scheduled'):
            r['Native_Product_Status'] = 'Attached_User_Confirmed'
            r['Native_Product_Attached_At'] = '2026-08-20'
            r['Approval_Status'] = 'Approved'
            r['Publication_Status'] = 'Published_User_Confirmed'
            r['Status'] = 'Native_Product_Attached_User_Confirmed'
            note = 'Fernando confirmó que el producto/link fue publicado o adjuntado en Facebook; hora e ID nativo individual pendientes de conciliación.'
            r['Notes'] = (r['Notes'].rstrip('.') + '. ' + note).strip()
            updated += 1

with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
print(f'updated={updated}')

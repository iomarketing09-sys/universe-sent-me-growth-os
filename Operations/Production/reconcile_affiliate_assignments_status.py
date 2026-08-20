import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/Affiliate_Pilot_Assignments.csv')
with path.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    rows = list(reader)
updated = 0
for r in rows:
    if r['Opportunity_ID'].startswith('AFF-'):
        r['Status'] = 'Native_Product_Attached_User_Confirmed'
        r['Approval_Status'] = 'Approved'
        r['Notes'] = 'Fernando confirmó que el producto/link fue publicado o adjuntado en Facebook; hora e ID nativo individual pendientes de conciliación técnica.'
        updated += 1
with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
print(f'updated={updated}')

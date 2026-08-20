#!/usr/bin/env python3
from pathlib import Path
import csv

LEDGER = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/Affiliate_Link_Ledger.csv')
TARGETS = {
    'ML-FB-WIN-2608029-XHP360',
    'ML-FB-WIN-CNT034-LEDNEON',
}

with LEDGER.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

updated = 0
for row in rows:
    if row['Link_ID'] in TARGETS:
        row['Native_Product_Status'] = 'Attached_User_Confirmed'
        row['Approval_Status'] = 'Approved'
        row['Publication_Status'] = 'Published_User_Confirmed'
        row['Status'] = 'Native_Product_Attached_User_Confirmed'
        note = 'Fernando confirmó manualmente la adjunción del producto nativo el 2026-08-20; hora exacta e ID nativo individual pendientes de conciliación.'
        if note not in row['Notes']:
            row['Notes'] = row['Notes'].rstrip() + ' ' + note
        updated += 1

with LEDGER.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

print(f'updated={updated}')

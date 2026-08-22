import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Operations/Research/2026-08-21_Reels_Publication_Inventory.csv'
OUTPUT = ROOT / 'Operations/Research/2026-08-22_Reels_Pending_Asset_Reconciliation_Queue.csv'

with SOURCE.open(encoding='utf-8', newline='') as handle:
    rows = list(csv.DictReader(handle))

pending = []
for row in rows:
    if row.get('Platform') != 'Facebook':
        continue
    if row.get('Asset_Match_Status') not in {'Pending_Drive_or_local_asset_match', ''}:
        continue
    date = row.get('Publication_UTC', '')[:10]
    if not ('2026-05-01' <= date <= '2026-06-30'):
        continue
    try:
        engagement = int(row.get('Engagement') or 0)
    except ValueError:
        engagement = 0
    title = row.get('Title_or_Caption') or ''
    reason = 'High_interaction_priority' if engagement >= 10 else 'Historical_asset_reconciliation'
    if not title:
        reason += '|Caption_empty_visual_review_needed'
    if 'http' in title.lower():
        reason += '|External_URL_editorial_filter'
    pending.append({
        'Reconciliation_Queue_ID': '',
        'Priority_Rank': '',
        'Review_Tier': '',
        'Reel_Record_ID': row.get('Reel_Record_ID'),
        'Platform_Content_ID': row.get('Platform_Content_ID'),
        'Meta_Reel_ID': row.get('Meta_Reel_ID'),
        'Publication_UTC': row.get('Publication_UTC'),
        'Permalink_URL': row.get('Meta_Reel_ID') and f"https://www.facebook.com/reel/{row.get('Meta_Reel_ID')}/" or '',
        'Engagement': engagement,
        'Title_or_Caption': title,
        'Character': row.get('Character'),
        'Current_Asset_Status': 'Pending_Drive_or_local_asset_match',
        'Priority_Reason': reason,
        'Next_Evidence_Source': 'Drive_root_and_subfolders; local/shared project assets; visual review if needed',
        'Decision_Status': 'Queued',
        'Notes': '',
    })

pending.sort(key=lambda x: (-x['Engagement'], x['Publication_UTC']))
for idx, row in enumerate(pending, start=1):
    row['Priority_Rank'] = idx
    row['Reconciliation_Queue_ID'] = f'RAQ-{idx:03d}'
    row['Review_Tier'] = 'Tier_1' if idx <= 15 else 'Tier_2'

fields = list(pending[0].keys()) if pending else []
with OUTPUT.open('w', encoding='utf-8', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(pending)

print({'pending_rows': len(pending), 'tier_1': min(15, len(pending)), 'output': str(OUTPUT)})

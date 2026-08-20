import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/Affiliate_Metrics_Snapshots.csv')
with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
expected = 25
assert len(rows) == 2, len(rows)
assert set(rows[0]) == set(rows[1])
assert len(rows[0]) == expected, len(rows[0])
assert rows[0]['Status'] == 'Recorded'
print('row2_status=', rows[1]['Status'])
print('row2_data_quality=', rows[1]['Data_Quality'])
print('row2_source=', rows[1]['Source'])
print('row2_tag=', rows[1]['ML_Tag'])
assert rows[1]['ML_Tag'] == 'usmfb20260819p01'

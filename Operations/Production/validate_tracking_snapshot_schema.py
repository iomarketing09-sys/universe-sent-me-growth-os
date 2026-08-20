import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/Affiliate_Metrics_Snapshots.csv')
with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
expected = 25
assert len(rows) == 6, len(rows)
assert set(rows[0]) == set(rows[1])
assert len(rows[0]) == expected, len(rows[0])
assert rows[0]['Status'] == 'Recorded'
by_id = {row['Snapshot_ID']: row for row in rows}
assert by_id['MANUAL-20260818-DATE']['Clicks'] == '2'
assert by_id['MANUAL-20260820-7D-AFF07']['Clicks'] == '1'
assert by_id['MANUAL-20260820-7D-REEL']['Status'] == 'Not_Visible_No_Inference'
assert by_id['MANUAL-20260820-7D-REEL']['ML_Tag'] == 'usmfb20260819p01'
print(f'rows={len(rows)} columns={len(rows[0])} reel_status={by_id["MANUAL-20260820-7D-REEL"]["Status"]}')

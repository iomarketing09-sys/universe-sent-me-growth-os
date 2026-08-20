from pathlib import Path

for name in (
    'Operations/Research/Affiliate_Link_Ledger.csv',
    'Operations/Research/Affiliate_Pilot_Assignments.csv',
):
    path = Path('/home/ubuntu/universe-sent-me-growth-os') / name
    raw = path.read_bytes()
    path.write_bytes(raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n'))
    print(path)

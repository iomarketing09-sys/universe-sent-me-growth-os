import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
source = ROOT / 'Operations/Research/2026-08-22_Reels_Top5_Visual_Review_Batch.csv'
out_dir = Path('/home/ubuntu/top5_drive_candidates')
out_dir.mkdir(exist_ok=True)
with source.open(encoding='utf-8', newline='') as handle:
    rows = list(csv.DictReader(handle))
selected = {}
for row in rows:
    selected.setdefault(row['Meta_Post_ID'], row)
results = []
for idx, row in enumerate(selected.values(), start=1):
    ext = '.mp4' if row['Drive_MimeType'].startswith('video/') else '.png'
    output = out_dir / f"{idx:02d}_meta_{row['Meta_Reel_ID']}_{row['Drive_File_Name'][:45].replace('/', '_')}{ext}"
    params = json.dumps({'fileId': row['Drive_File_ID'], 'alt': 'media'})
    result = subprocess.run(['gws', 'drive', 'files', 'get', '--params', params, '--output', str(output)], capture_output=True, text=True)
    results.append({**row, 'download_path': str(output), 'returncode': result.returncode, 'stderr': result.stderr[-500:]})
Path('/home/ubuntu/top5_drive_candidates_manifest.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'selected': len(results), 'downloaded': sum(r['returncode'] == 0 for r in results), 'manifest': '/home/ubuntu/top5_drive_candidates_manifest.json'}, ensure_ascii=False))

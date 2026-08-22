import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
tree = json.loads(Path('/home/ubuntu/drive_reels_tree.json').read_text(encoding='utf-8'))
out_dir = Path('/home/ubuntu/universe_real_batch')
out_dir.mkdir(exist_ok=True)
files = [f for f in tree['files'] if f.get('mimeType') == 'video/mp4' and f.get('name','').startswith('Universe Real - ')]
results = []
for f in sorted(files, key=lambda x: x['name']):
    safe = f['name'].replace('/', '_')
    out = out_dir / safe
    params = json.dumps({'fileId': f['id'], 'alt': 'media'})
    r = subprocess.run(['gws', 'drive', 'files', 'get', '--params', params, '--output', str(out)], capture_output=True, text=True)
    results.append({'id': f['id'], 'name': f['name'], 'createdTime': f.get('createdTime'), 'path': str(out), 'returncode': r.returncode})
Path('/home/ubuntu/universe_real_batch_manifest.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'files_found': len(files), 'downloaded': sum(x['returncode']==0 for x in results), 'manifest': '/home/ubuntu/universe_real_batch_manifest.json'}, ensure_ascii=False))

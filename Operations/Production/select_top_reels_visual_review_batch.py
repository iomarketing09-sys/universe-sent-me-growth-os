import csv
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
queue_path = ROOT / 'Operations/Research/2026-08-22_Reels_Pending_Asset_Reconciliation_Queue.csv'
tree = json.loads(Path('/home/ubuntu/drive_reels_tree.json').read_text(encoding='utf-8'))
with queue_path.open(encoding='utf-8', newline='') as handle:
    queue = list(csv.DictReader(handle))

# One row per Reel, ordered by the priority queue already approved.
unique = {}
for row in queue:
    unique.setdefault(row['Platform_Content_ID'], row)
top = list(unique.values())[:5]

folders = {f.get('id'): f for f in tree['files'] if f.get('mimeType') == 'application/vnd.google-apps.folder'}

def path_for(parents, guard=0):
    if guard > 8 or not parents:
        return ''
    folder = folders.get(parents[0])
    if not folder:
        return ''
    return f"{path_for(folder.get('parents') or [], guard + 1)}/{folder.get('name')}".strip('/')

def parse_dt(s):
    try:
        return datetime.fromisoformat(s.replace('Z', '+00:00'))
    except Exception:
        return None

generic = {'universesentme','universe','sent','reel','real','instagram','facebook','video','png','mp4','aiart','vidareal','relatable','fblifestyle','rockstar'}
def toks(text):
    return {w for w in re.findall(r'[a-záéíóúüñ0-9]+', (text or '').lower()) if len(w) >= 4 and w not in generic}

assets = []
for asset in tree['files']:
    if not (asset.get('mimeType','').startswith('video/') or asset.get('mimeType','').startswith('image/')):
        continue
    asset['folder_path'] = path_for(asset.get('parents') or [])
    assets.append(asset)

rows = []
for p in top:
    pub = parse_dt(p['Publication_UTC'])
    pt = toks(p['Title_or_Caption'])
    scored = []
    for a in assets:
        dates = [parse_dt(a.get('createdTime','')), parse_dt(a.get('modifiedTime',''))]
        dates = [d for d in dates if d]
        delta = min((abs((d - pub).total_seconds()) / 86400 for d in dates), default=999)
        overlap = sorted(pt & toks((a.get('name','') + ' ' + a.get('folder_path',''))))
        type_bonus = 1 if a.get('mimeType','').startswith('video/') else 0
        score = (len(overlap) * 100) + max(0, 20 - min(delta,20)) + type_bonus
        scored.append((score, delta, overlap, a))
    scored.sort(key=lambda x: (-x[0], x[1]))
    for rank, (score, delta, overlap, a) in enumerate(scored[:5], start=1):
        rows.append({
            'Review_Batch': 'TOP5',
            'Meta_Priority_Rank': p['Priority_Rank'],
            'Meta_Post_ID': p['Platform_Content_ID'],
            'Meta_Reel_ID': p['Meta_Reel_ID'],
            'Publication_UTC': p['Publication_UTC'],
            'Engagement': p['Engagement'],
            'Meta_Caption': p['Title_or_Caption'],
            'Candidate_Rank': rank,
            'Drive_File_ID': a.get('id'),
            'Drive_File_Name': a.get('name'),
            'Drive_Folder_Path': a.get('folder_path'),
            'Drive_MimeType': a.get('mimeType'),
            'Drive_Created_UTC': a.get('createdTime'),
            'Drive_Duration_ms': (a.get('videoMediaMetadata') or {}).get('durationMillis'),
            'Date_Delta_Days': round(delta, 2),
            'Meaningful_Token_Overlap': '|'.join(overlap),
            'Triage_Score': round(score, 2),
            'Review_Status': 'Needs_visual_review',
        })

out = ROOT / 'Operations/Research/2026-08-22_Reels_Top5_Visual_Review_Batch.csv'
with out.open('w', encoding='utf-8', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator='\n')
    writer.writeheader(); writer.writerows(rows)
print(json.dumps({'top_reels': len(top), 'candidate_rows': len(rows), 'output': str(out), 'meta_ids': [p['Meta_Reel_ID'] for p in top]}, ensure_ascii=False, indent=2))

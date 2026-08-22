import csv
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREE = json.loads(Path('/home/ubuntu/drive_reels_tree.json').read_text(encoding='utf-8'))
queue_path = ROOT / 'Operations/Research/2026-08-22_Reels_Pending_Asset_Reconciliation_Queue.csv'
with queue_path.open(encoding='utf-8', newline='') as handle:
    pending = list(csv.DictReader(handle))

files = TREE.get('files', [])
folders = {f.get('id'): f for f in files if f.get('mimeType') == 'application/vnd.google-apps.folder'}
folders['1kWkZSbWvMGe0fwXu93UTh1iK6aVfE70a'] = {'name': 'Reels', 'parents': []}

def path_for(parents, guard=0):
    if guard > 8 or not parents:
        return ''
    parent = parents[0]
    folder = folders.get(parent)
    if not folder:
        return ''
    prefix = path_for(folder.get('parents') or [], guard + 1)
    return f"{prefix}/{folder.get('name')}".strip('/')

for f in files:
    f['folder_path'] = path_for(f.get('parents') or [])

assets = [f for f in files if f.get('mimeType', '').startswith('video/') or f.get('mimeType', '').startswith('image/')]
stop = set('de la el los las un una unos unas que por para con sin del al es se me mi yo tu y o a en esto eso esta este como cuando donde muy más mas no si ya vida gente cosas tienes tener hacer hizo hace quien quién dios bien mal todos todo solo otra otro unas uno dos tres'.split())

def tokens(text):
    words = re.findall(r'[a-záéíóúüñ0-9]+', (text or '').lower())
    return {w for w in words if len(w) >= 4 and w not in stop}

def parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace('Z', '+00:00'))
    except Exception:
        return None

rows = []
for p in pending:
    p_tokens = tokens(' '.join([p.get('Title_or_Caption', ''), p.get('Character', '')]))
    pub = parse_dt(p.get('Publication_UTC'))
    scored = []
    for a in assets:
        created = parse_dt(a.get('createdTime'))
        modified = parse_dt(a.get('modifiedTime'))
        candidates_dates = [d for d in (created, modified) if d]
        delta = min((abs((d - pub).total_seconds()) / 86400 for d in candidates_dates), default=999)
        filename_text = ' '.join([a.get('name', ''), a.get('folder_path', '')])
        a_tokens = tokens(filename_text)
        overlap = sorted(p_tokens & a_tokens)
        date_score = max(0, 25 - min(delta, 25)) / 5
        lexical_score = min(20, len(overlap) * 10)
        score = date_score + lexical_score
        if delta <= 10 or overlap:
            scored.append({
                'Queue_ID': p.get('Reconciliation_Queue_ID'),
                'Priority_Rank': p.get('Priority_Rank'),
                'Tier': p.get('Review_Tier'),
                'Meta_Post_ID': p.get('Platform_Content_ID'),
                'Meta_Reel_ID': p.get('Meta_Reel_ID'),
                'Publication_UTC': p.get('Publication_UTC'),
                'Engagement': p.get('Engagement'),
                'Meta_Caption': p.get('Title_or_Caption'),
                'Drive_File_ID': a.get('id'),
                'Drive_File_Name': a.get('name'),
                'Drive_Folder_Path': a.get('folder_path'),
                'Drive_Created_UTC': a.get('createdTime'),
                'Drive_Modified_UTC': a.get('modifiedTime'),
                'Drive_MimeType': a.get('mimeType'),
                'Drive_Duration_ms': (a.get('videoMediaMetadata') or {}).get('durationMillis'),
                'Date_Delta_Days': round(delta, 2),
                'Filename_Token_Overlap': '|'.join(overlap),
                'Triage_Score': round(score, 2),
                'Triage_Status': 'Candidate_Visual_Review' if lexical_score > 0 else 'Date_Proximity_Only',
                'Decision_Status': 'Queued_For_Review',
            })
    scored.sort(key=lambda x: (-x['Triage_Score'], x['Date_Delta_Days']))
    rows.extend(scored[:5])

fields = list(rows[0].keys()) if rows else []
out = ROOT / 'Operations/Research/2026-08-22_Reels_Pending_Drive_Triage.csv'
with out.open('w', encoding='utf-8', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

summary = {
    'pending_reels': len(pending),
    'drive_assets': len(assets),
    'triage_rows': len(rows),
    'visual_review_rows': sum(r['Triage_Status'] == 'Candidate_Visual_Review' for r in rows),
    'date_only_rows': sum(r['Triage_Status'] == 'Date_Proximity_Only' for r in rows),
    'output': str(out),
}
Path('/home/ubuntu/pending_reels_drive_triage_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))

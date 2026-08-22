import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
history_path = ROOT / 'Operations/Research/2026-08-19_Historial_Reels_Consolidado.json'
queue_path = ROOT / 'Operations/Research/2026-08-22_Reels_Pending_Asset_Reconciliation_Queue.csv'
top5_path = ROOT / 'Operations/Research/2026-08-22_Reels_Top5_Visual_Review_Batch.csv'

history = json.loads(history_path.read_text(encoding='utf-8'))
with top5_path.open(encoding='utf-8', newline='') as handle:
    top5 = list(csv.DictReader(handle))
reviewed = {}
for row in top5:
    reviewed.setdefault(row['Meta_Post_ID'], []).append(row)

for r in history.get('records', []):
    pid = r.get('content_id')
    if pid in reviewed:
        candidates = reviewed[pid]
        r['asset_review_status'] = 'No_Match_In_Reviewed_Set'
        r['reconciliation_review_status'] = 'Reviewed_Top5_No_Match'
        r['reviewed_on'] = '2026-08-22'
        r['review_batch_id'] = 'TOP5'
        r['reviewed_drive_candidate_ids'] = sorted({c['Drive_File_ID'] for c in candidates})
        r['reviewed_drive_candidate_count'] = len(candidates)
        r['review_note'] = 'No visual match in the five highest-ranked Drive candidates; global asset match remains pending and no global exclusion is declared.'
history['last_updated'] = '2026-08-22'
history['version'] = '1.9'
history['top5_review_note'] = 'Five high-interaction Facebook Reels were visually reviewed against their top five Drive candidates; all five remain unresolved globally, with no match inferred from date proximity.'
history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

with queue_path.open(encoding='utf-8', newline='') as handle:
    queue = list(csv.DictReader(handle))
for row in queue:
    if row['Platform_Content_ID'] in reviewed:
        row['Decision_Status'] = 'Reviewed_No_Match_In_TOP5'
        row['Notes'] = 'Five Drive candidates visually checked; continue only if a broader Drive/local search is justified.'
fields = list(queue[0].keys())
with queue_path.open('w', encoding='utf-8', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
    writer.writeheader(); writer.writerows(queue)

summary_path = Path('/home/ubuntu/top5_reels_review_summary.json')
summary_path.write_text(json.dumps({
    'review_batch_id': 'TOP5',
    'reviewed_posts': len(reviewed),
    'reviewed_drive_candidates': sum(len(v) for v in reviewed.values()),
    'no_match_in_reviewed_set': len(reviewed),
    'global_asset_status': 'Pending_for_all_five',
    'history_version': history['version'],
    'queue_updated': True,
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print({'reviewed_posts': len(reviewed), 'history_version': history['version'], 'queue_updated': True})

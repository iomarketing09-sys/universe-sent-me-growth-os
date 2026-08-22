import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
history_path=ROOT/'Operations/Research/2026-08-19_Historial_Reels_Consolidado.json'
queue_path=ROOT/'Operations/Research/2026-08-22_Reels_Pending_Asset_Reconciliation_Queue.csv'
review_path=ROOT/'Operations/Research/2026-08-21_Reels_Drive_Meta_Crossmatch_Review.csv'
next_path=ROOT/'Operations/Research/2026-08-22_Reels_Next10_Visual_Review_Batch.csv'

meta_rows=[
('1906363553379974','No_Match_In_Reviewed_Set','Wilfred potion family reviewed; standing Wilfred Reel and crouched potion source are different scenes.'),
('991640670312120','No_Match_In_Reviewed_Set','Catedral image reviewed; street/cathedral, sky, person, and overlay differ from the Reel.'),
('1357137352923823','No_Match_In_Reviewed_Set','Fantasma source reviewed; Reel is a highway POV and not the forest ghost.'),
('26858527637139429','No_Match_In_Reviewed_Set','Fantasma source reviewed; Reel is a blue-sky/cloud meme and not the forest ghost.'),
('1788853558497930','No_Match_In_Reviewed_Set','Universe Real 005 reviewed; Reel is the static fairy/gnome spiritual-friends illustration.'),
('1379496217270226','No_Match_In_Reviewed_Set','Fantasma source reviewed; Reel is the stream/roots scene.'),
('1518053389684402','Match_Visual_Exact','Exact composition match confirmed against Fantasma_tranquilo_con_viento_202605241629.mp4.'),
('1032196252667933','No_Match_In_Reviewed_Set','Universe Real 004 reviewed; Reel is the stream/roots scene.'),
('1408386457716987','No_Match_In_Reviewed_Set','Universe Real 008 reviewed; Reel shows a woman in front of clouds, not a bedroom selfie.'),
('26960899110262609','No_Match_In_Reviewed_Set','Elara/Evan hug source reviewed; Reel is a multi-character campfire gathering.')]
status_by_reel={rid: (status, note) for rid, status, note in meta_rows}

history=json.loads(history_path.read_text(encoding='utf-8'))
for r in history.get('records',[]):
    rid=r.get('platform_reel_id') or r.get('meta_reel_id') or r.get('reel_id')
    if rid not in status_by_reel: continue
    status,note=status_by_reel[rid]
    r['review_batch_id']='NEXT10'; r['reviewed_on']='2026-08-22'; r['asset_review_status']=status; r['reconciliation_review_status']='Reviewed_Exact_Match' if status=='Match_Visual_Exact' else 'Reviewed_No_Match_In_TOP1'
    r['review_note']=note
    if status=='Match_Visual_Exact':
        r['asset_match_status']='Match_Visual_Exact'; r['asset_relationship']='Single_asset_match'; r['drive_file_id']='175XnmOVnBPgVCFlwyDWCZ3jCAmB2MOjO'; r['drive_file_name']='Fantasma_tranquilo_con_viento_202605241629.mp4'; r['asset_review_confidence']='High'
history['last_updated']='2026-08-22'; history['version']='2.0'; history['next10_review_note']='NEXT10 visual review produced one exact Fantasma match and nine no-match results within the primary candidate review set.'
history_path.write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

with queue_path.open(encoding='utf-8',newline='') as h: queue=list(csv.DictReader(h))
for row in queue:
    rid=row['Meta_Reel_ID']
    if rid in status_by_reel:
        status,note=status_by_reel[rid]; row['Decision_Status']='Reviewed_Exact_Match' if status=='Match_Visual_Exact' else 'Reviewed_No_Match_In_NEXT10_Primary'; row['Notes']=note
        if status=='Match_Visual_Exact': row['Current_Asset_Status']='Match_Visual_Exact'; row['Next_Evidence_Source']='Operations/Research/2026-08-21_Reels_Drive_Meta_Crossmatch_Review.csv'
fields=list(queue[0].keys())
with queue_path.open('w',encoding='utf-8',newline='') as h:
    w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(queue)

with review_path.open(encoding='utf-8',newline='') as h: reviews=list(csv.DictReader(h))
existing={r['Review_ID'] for r in reviews}
row={
'Review_ID':'XMR-011','Asset_Drive_ID':'175XnmOVnBPgVCFlwyDWCZ3jCAmB2MOjO','Asset_Filename':'Fantasma_tranquilo_con_viento_202605241629.mp4','Asset_Created_UTC':'2026-05-24T21:29:12.665Z','Source_Analysis':'Direct frame comparison shows the same ghost, round sunglasses, fence, forest composition, camera movement, and palette; Meta adds a different text overlay.','Meta_Candidate_Post_ID':'1036844829507460_122130329817072582','Meta_Reel_ID':'1518053389684402','Meta_Published_UTC':'2026-06-15T04:05:45+0000','Meta_Permalink':'https://www.facebook.com/reel/1518053389684402/','Decision':'Match_Visual_Exact','Confidence':'High','Asset_Relationship':'Single_asset_match','Editorial_Qualification':'Identity_match_only_no_CNT_assignment','Notes':'Exact visual match confirmed by frames at 0.5s and 5s; no new CNT or canonical character assignment created.'}
if row['Review_ID'] not in existing: reviews.append(row)
fields=list(reviews[0].keys())
with review_path.open('w',encoding='utf-8',newline='') as h:
    w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(reviews)

print({'history_version':history['version'],'exact_match':'1518053389684402','next10_no_match_in_primary_set':9,'review_rows':len(reviews)})

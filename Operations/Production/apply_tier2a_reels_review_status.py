import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
history_path=ROOT/'Operations/Research/2026-08-19_Historial_Reels_Consolidado.json'
queue_path=ROOT/'Operations/Research/2026-08-22_Reels_Pending_Asset_Reconciliation_Queue.csv'
review_path=ROOT/'Operations/Research/2026-08-21_Reels_Drive_Meta_Crossmatch_Review.csv'
tier_path=ROOT/'Operations/Research/2026-08-22_Reels_Tier2A_Visual_Review_Batch.csv'

with tier_path.open(encoding='utf-8',newline='') as h: triage=list(csv.DictReader(h))
meta_rows={}
for r in triage: meta_rows.setdefault(r['Meta_Reel_ID'], r)
exact={
 '2159954351459805':('1hduudZ2UhqzrwFVoxs4gJryxPoBAVU1W','Wilfred_and_Elara_cosmic_radio_202606272110.mp4'),
 '1339119487723234':('1ujbbAL9mAm7OCdHrlXeQ8OeIAodzFbZC','Elara_and_Wilfred_dialogue_animation_202606271715.mp4'),
}
statuses={rid:('Match_Visual_Exact' if rid in exact else 'No_Match_In_TIER2A_Primary') for rid in meta_rows}
notes={
 '2159954351459805':'Direct frame comparison confirms the same cosmic radio studio, console, hanging bulbs, Wilfred composition and Elara/Wilfred source sequence; Reel adds dialogue treatment.',
 '1339119487723234':'Direct frame comparison confirms the same radio studio, Elara/Wilfred composition and dialogue sequence; Reel adds text treatment.',
}
for rid,row in meta_rows.items():
 if rid not in notes: notes[rid]=f"Primary Drive candidate reviewed; visual fingerprint differs from the Meta Reel. Global asset match remains pending."

history=json.loads(history_path.read_text(encoding='utf-8')); changed=[]
for r in history.get('records',[]):
 rid=str(r.get('meta_reel_id') or r.get('platform_reel_id') or r.get('reel_id') or '')
 if rid not in statuses: continue
 status=statuses[rid]; r['review_batch_id']='TIER2A'; r['reviewed_on']='2026-08-22'; r['asset_review_status']=status; r['reconciliation_review_status']='Reviewed_Exact_Match' if status=='Match_Visual_Exact' else 'Reviewed_No_Match_In_TIER2A_Primary'; r['review_note']=notes[rid]; r['reviewed_drive_candidate_id']=meta_rows[rid]['Drive_File_ID']; r['reviewed_drive_candidate_name']=meta_rows[rid]['Drive_File_Name']; changed.append(rid)
 if status=='Match_Visual_Exact':
  r['asset_match_status']='Match_Visual_Exact'; r['asset_relationship']='Single_asset_match'; r['drive_file_id'],r['drive_file_name']=exact[rid]; r['asset_review_confidence']='High'
history['last_updated']='2026-08-22'; history['version']='2.1'; history['tier2a_review_note']='TIER2A reviewed 10 Tier 2 historical Reels; two exact Drive matches and eight no-match results within primary candidates.'
history_path.write_text(json.dumps(history,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

with queue_path.open(encoding='utf-8',newline='') as h: queue=list(csv.DictReader(h))
queue=[r for r in queue if r['Meta_Reel_ID'] not in exact]
for r in queue:
 rid=r['Meta_Reel_ID']
 if rid in statuses:
  r['Decision_Status']='Reviewed_No_Match_In_TIER2A_Primary'; r['Notes']=notes[rid]
# preserve order then normalize rank/tier after removing exact matches
queue.sort(key=lambda r:(int(r.get('Priority_Rank') or 9999),r.get('Publication_UTC','')))
for i,r in enumerate(queue,1):
 r['Priority_Rank']=str(i); r['Reconciliation_Queue_ID']=f'RAQ-{i:03d}'; r['Review_Tier']='Tier_1' if i<=15 else 'Tier_2'
fields=list(queue[0].keys())
with queue_path.open('w',encoding='utf-8',newline='') as h:
 w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(queue)

with review_path.open(encoding='utf-8',newline='') as h: reviews=list(csv.DictReader(h))
next_id=12
for rid in meta_rows:
 row=meta_rows[rid]; status=statuses[rid]; asset_id,asset_name=exact[rid] if status=='Match_Visual_Exact' else (row['Drive_File_ID'],row['Drive_File_Name'])
 matches=[x for x in reviews if x.get('Meta_Reel_ID')==rid]
 if matches:
  target=matches[0]; target.update({'Asset_Drive_ID':asset_id,'Asset_Filename':asset_name,'Asset_Created_UTC':row['Drive_Created_UTC'],'Source_Analysis':notes[rid],'Meta_Candidate_Post_ID':row['Meta_Post_ID'],'Meta_Published_UTC':row['Publication_UTC'],'Meta_Permalink':f'https://www.facebook.com/reel/{rid}/','Decision':status,'Confidence':'High' if status=='Match_Visual_Exact' else 'Medium','Asset_Relationship':'Single_asset_match' if status=='Match_Visual_Exact' else 'Not_a_match_in_primary_candidate','Editorial_Qualification':'Identity_match_only_no_CNT_assignment' if status=='Match_Visual_Exact' else 'Pending_other_Drive_or_local_asset_search','Notes':notes[rid]})
 else:
  review_id=f'XMR-{next_id:03d}'; next_id+=1
  reviews.append({'Review_ID':review_id,'Asset_Drive_ID':asset_id,'Asset_Filename':asset_name,'Asset_Created_UTC':row['Drive_Created_UTC'],'Source_Analysis':notes[rid],'Meta_Candidate_Post_ID':row['Meta_Post_ID'],'Meta_Reel_ID':rid,'Meta_Published_UTC':row['Publication_UTC'],'Meta_Permalink':f'https://www.facebook.com/reel/{rid}/','Decision':status,'Confidence':'High' if status=='Match_Visual_Exact' else 'Medium','Asset_Relationship':'Single_asset_match' if status=='Match_Visual_Exact' else 'Not_a_match_in_primary_candidate','Editorial_Qualification':'Identity_match_only_no_CNT_assignment' if status=='Match_Visual_Exact' else 'Pending_other_Drive_or_local_asset_search','Notes':notes[rid]})
fields=list(reviews[0].keys())
with review_path.open('w',encoding='utf-8',newline='') as h:
 w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(reviews)
print({'changed_history_records':changed,'exact_matches':[rid for rid in statuses if statuses[rid]=='Match_Visual_Exact'],'no_match_primary':sum(v=='No_Match_In_TIER2A_Primary' for v in statuses.values()),'queue_rows':len(queue),'review_rows':len(reviews)})

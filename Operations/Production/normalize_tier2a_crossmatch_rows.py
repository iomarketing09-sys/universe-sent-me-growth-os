import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
review_path=ROOT/'Operations/Research/2026-08-21_Reels_Drive_Meta_Crossmatch_Review.csv'
tier_path=ROOT/'Operations/Research/2026-08-22_Reels_Tier2A_Visual_Review_Batch.csv'
with tier_path.open(encoding='utf-8',newline='') as h: triage=list(csv.DictReader(h))
by_reel={}
for r in triage: by_reel.setdefault(r['Meta_Reel_ID'],r)
exact={
 '2159954351459805':('1hduudZ2UhqzrwFVoxs4gJryxPoBAVU1W','Wilfred_and_Elara_cosmic_radio_202606272110.mp4'),
 '1339119487723234':('1ujbbAL9mAm7OCdHrlXeQ8OeIAodzFbZC','Elara_and_Wilfred_dialogue_anima…_202606271715.mp4'),
}
notes={
 '2159954351459805':'Direct frame comparison confirms the same cosmic radio studio, console, hanging bulbs, Wilfred composition and Elara/Wilfred source sequence; Reel adds dialogue treatment.',
 '1339119487723234':'Direct frame comparison confirms the same radio studio, Elara/Wilfred composition and dialogue sequence; Reel adds text treatment.'}
with review_path.open(encoding='utf-8',newline='') as h: reviews=list(csv.DictReader(h))
tier_ids=set(by_reel)
reviews=[r for r in reviews if r.get('Meta_Reel_ID') not in tier_ids]
for i,(rid,meta) in enumerate(by_reel.items(),start=12):
 status='Match_Visual_Exact' if rid in exact else 'No_Match_In_TIER2A_Primary'
 drive_id,drive_name=exact[rid] if rid in exact else (meta['Drive_File_ID'],meta['Drive_File_Name'])
 note=notes.get(rid,'Primary Drive candidate reviewed; visual fingerprint differs from the Meta Reel. Global asset match remains pending.')
 reviews.append({'Review_ID':f'XMR-{i:03d}','Asset_Drive_ID':drive_id,'Asset_Filename':drive_name,'Asset_Created_UTC':meta['Drive_Created_UTC'],'Source_Analysis':note,'Meta_Candidate_Post_ID':meta['Meta_Post_ID'],'Meta_Reel_ID':rid,'Meta_Published_UTC':meta['Publication_UTC'],'Meta_Permalink':f'https://www.facebook.com/reel/{rid}/','Decision':status,'Confidence':'High' if status=='Match_Visual_Exact' else 'Medium','Asset_Relationship':'Single_asset_match' if status=='Match_Visual_Exact' else 'Not_a_match_in_primary_candidate','Editorial_Qualification':'Identity_match_only_no_CNT_assignment' if status=='Match_Visual_Exact' else 'Pending_other_Drive_or_local_asset_search','Notes':note})
fields=list(reviews[0].keys())
with review_path.open('w',encoding='utf-8',newline='') as h:
 w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(reviews)
print({'rows':len(reviews),'tier2a_rows':len(by_reel),'exact_rows':sum(r['Decision']=='Match_Visual_Exact' for r in reviews if r.get('Meta_Reel_ID') in tier_ids)})

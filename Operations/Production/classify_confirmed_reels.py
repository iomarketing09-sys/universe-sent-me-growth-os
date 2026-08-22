import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
inv=ROOT/'Operations/Research/2026-08-21_Reels_Publication_Inventory.csv'
out=ROOT/'Operations/Research/2026-08-22_Reels_Confirmed_Classification.csv'
cross=ROOT/'Operations/Research/2026-08-21_Reels_Drive_Meta_Crossmatch_Review.csv'
with cross.open(encoding='utf-8',newline='') as h: cross_rows=list(csv.DictReader(h))
asset_by_reel={r['Meta_Reel_ID']:r['Asset_Filename'] for r in cross_rows if r.get('Decision')=='Match_Visual_Exact'}
ids={'1877535942934184','2417378928740605','1049041731412120','1518053389684402','2159954351459805','1339119487723234'}
meta={
 '1877535942934184':{'family':'Character_loop_meme','structure':'Animated still loop / character pose','scene':'Fantasma leaning on wooden fence in twilight forest','characters':'Fantasma','motion':'Subtle sheet, cloud and camera movement','caption_function':'External_URL_promotion','clean_comparability':'Exclude_until_external_URL_treatment_coded','asset_reuse_group':'GHOST-FENCE-20260524'},
 '2417378928740605':{'family':'Sequential_visual_reaction','structure':'Two-clip setup → energy reaction','scene':'Man in brown hoodie with glowing rings/energy','characters':'Unknown_human_character','motion':'Physical distress to shocked reaction','caption_function':'Minimal_reaction_caption','clean_comparability':'Conditional_watermark_and_character_treatment_review','asset_reuse_group':'HOODIE-ENERGY-20260613'},
 '1049041731412120':{'family':'Character_POV_reveal','structure':'POV character reveal / suit adjustment → lightning close-up','scene':'Duck in tuxedo against cosmic background','characters':'Duck_unknown_character','motion':'Suit adjustment and lightning reveal','caption_function':'Minimal_character_caption','clean_comparability':'Exclude_until_AI_watermark_and_character_treatment_coded','asset_reuse_group':'DUCK-ARIES-20260630'},
 '1518053389684402':{'family':'Character_loop_meme','structure':'Animated still loop / character pose','scene':'Fantasma leaning on wooden fence in twilight forest','characters':'Fantasma','motion':'Subtle sheet, cloud and camera movement','caption_function':'Minimal_reflection_caption','clean_comparability':'Conditional_same_asset_reuse_not_independent_case','asset_reuse_group':'GHOST-FENCE-20260524'},
 '2159954351459805':{'family':'Dialogue_radio','structure':'Character A statement → Character B reaction/correction','scene':'Cosmic radio studio with console and window','characters':'Wilfred + Elara','motion':'Shot change, lip-sync and hand gesture','caption_function':'Conversational_dialogue','clean_comparability':'Candidate_for_dialogue_family_n2','asset_reuse_group':'RADIO-20260627'},
 '1339119487723234':{'family':'Dialogue_radio','structure':'Astrology warning → misunderstanding → correction','scene':'Cosmic radio studio with console and window','characters':'Elara + Wilfred','motion':'Alternating shots, staff glow and beard gesture','caption_function':'Conversational_dialogue_plus_text_overlay','clean_comparability':'Candidate_for_dialogue_family_n2','asset_reuse_group':'RADIO-20260627'},
}
with inv.open(encoding='utf-8',newline='') as h: rows=list(csv.DictReader(h))
rows=[r for r in rows if r.get('Meta_Reel_ID') in ids]
rows.sort(key=lambda r:r['Publication_UTC'])
fields=['Meta_Reel_ID','Publication_UTC','Engagement','Views','Reach','Metrics_Status','Asset_Filename','Asset_Relationship','Family','Structure','Scene','Characters','Motion','Caption_Function','Clean_Comparability','Asset_Reuse_Group','Experiment_ID','Hypothesis_ID']
out_rows=[]
for r in rows:
 x=meta[r['Meta_Reel_ID']];out_rows.append({'Meta_Reel_ID':r['Meta_Reel_ID'],'Publication_UTC':r['Publication_UTC'],'Engagement':r['Engagement'],'Views':r['Views'],'Reach':r['Reach'],'Metrics_Status':r['Metrics_Status'],'Asset_Filename':asset_by_reel.get(r['Meta_Reel_ID'],r['Meta_Reel_ID']),'Asset_Relationship':r['Asset_Relationship'],'Family':x['family'],'Structure':x['structure'],'Scene':x['scene'],'Characters':x['characters'],'Motion':x['motion'],'Caption_Function':x['caption_function'],'Clean_Comparability':x['clean_comparability'],'Asset_Reuse_Group':x['asset_reuse_group'],'Experiment_ID':r['Experiment_ID'],'Hypothesis_ID':r['Hypothesis_ID']})
with out.open('w',encoding='utf-8',newline='') as h:
 w=csv.DictWriter(h,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(out_rows)
print({'rows':len(out_rows),'families':sorted(set(x['Family'] for x in out_rows)),'output':str(out)})

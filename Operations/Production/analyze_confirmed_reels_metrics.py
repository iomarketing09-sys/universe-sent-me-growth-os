import csv,json,statistics
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
inv=ROOT/'Operations/Research/2026-08-21_Reels_Publication_Inventory.csv'
cls=ROOT/'Operations/Research/2026-08-22_Reels_Confirmed_Classification.csv'
out=ROOT/'Operations/Research/2026-08-22_Reels_Confirmed_Metric_Assessment.json'
with inv.open(encoding='utf-8',newline='') as h: inventory={r['Meta_Reel_ID']:r for r in csv.DictReader(h)}
with cls.open(encoding='utf-8',newline='') as h: classifications={r['Meta_Reel_ID']:r for r in csv.DictReader(h)}
records=[]
for rid,c in classifications.items():
 r=inventory[rid]; status=r['Metrics_Status']; window='Meta_lifetime_interactions' if 'lifetime' in status else 'Meta_current_feed_snapshot_interactions'
 records.append({'Meta_Reel_ID':rid,'Publication_UTC':r['Publication_UTC'],'Engagement':int(r['Engagement']) if r['Engagement'] else None,'Views':int(r['Views']) if r['Views'] else None,'Reach':int(r['Reach']) if r['Reach'] else None,'Metric_Window_Status':window,'Views_Reach_Status':'Missing_in_current_inventory' if not r['Views'] and not r['Reach'] else 'Available','Family':c['Family'],'Asset_Filename':c['Asset_Filename'],'Asset_Reuse_Group':c['Asset_Reuse_Group'],'Clean_Comparability':c['Clean_Comparability'],'Experiment_ID':r['Experiment_ID'],'Hypothesis_ID':r['Hypothesis_ID']})
by=defaultdict(list)
for x in records: by[x['Family']].append(x)
family_summary=[]
for family,items in sorted(by.items()):
 vals=[x['Engagement'] for x in items if x['Engagement'] is not None]
 groups=sorted(set(x['Asset_Reuse_Group'] for x in items))
 assets=sorted(set(x['Asset_Filename'] for x in items))
 windows=sorted(set(x['Metric_Window_Status'] for x in items))
 if family=='Dialogue_radio' and len(items)>=2 and len(assets)>=2 and len(windows)==1: level='Promising_pattern_needs_one_more_case'
 elif family=='Character_loop_meme' and len(groups)==1: level='Reuse_signal_not_independent_comparable'
 else: level='Observed_only_not_verdict'
 family_summary.append({'Family':family,'Posts':len(items),'Distinct_Asset_Reuse_Groups':len(groups),'Distinct_Assets':len(assets),'Asset_Filenames':assets,'Engagement_Values':vals,'Raw_Engagement_Median':statistics.median(vals) if vals else None,'Metric_Window_Statuses':windows,'Views_Reach_Populated':sum(1 for x in items if x['Views'] is not None or x['Reach'] is not None),'Evidence_Level':level})
all_vals=[x['Engagement'] for x in records if x['Engagement'] is not None]
result={'title':'Evaluación de evidencia de métricas de Reels confirmados','purpose':'Separar observaciones de engagement de ventanas y unidades no comparables antes de definir adaptaciones futuras.','status':'Active','created':'2026-08-22','updated':'2026-08-22','version':'1.0','author':'Manus AI','related_documents':['Operations/Research/2026-08-22_Reels_Confirmed_Classification.csv','Operations/Research/2026-08-21_Reels_Publication_Inventory.csv','Operations/Research/2026-08-19_Auditoria_Reels_y_Monetizacion.md','GrowthOS/07_00_Registro_Maestro_Reels.md'],'inventory_scope':{'confirmed_reels':len(records),'raw_engagement_median_non_verdict':statistics.median(all_vals),'views_reach_populated':sum(1 for x in records if x['Views'] is not None or x['Reach'] is not None),'experiment_linked_records':sum(1 for x in records if x['Experiment_ID'] or x['Hypothesis_ID']),'warning':'Los seis registros no tienen views/reach en este corte; el engagement mezcla lifetime y snapshot actual. El valor agregado no es un veredicto multiformato.'},'family_summary':family_summary,'records':records,'recommendation':'Use Dialogue_radio as the first adaptation candidate after adding one more distinct case. Treat Character_loop_meme as reuse evidence only because both publications use the same asset group. Keep Sequential_visual_reaction and Character_POV_reveal as observed examples requiring at least two to four additional comparable cases.'}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print({'records':len(records),'families':family_summary,'output':str(out)})

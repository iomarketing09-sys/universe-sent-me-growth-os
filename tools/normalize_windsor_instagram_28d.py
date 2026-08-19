import json, statistics
from pathlib import Path
from datetime import datetime
SRC=Path('/home/ubuntu/.mcp/tool-results/2026-08-19_02-50-33.317227361_windsor-ai_get_data_17ffd3d0.json')
ROOT=Path('/home/ubuntu/universe-sent-me-growth-os')
OUT=ROOT/'Operations/Research/2026-08-19_Windsor_Instagram_28D_Normalizado.json'
o=json.loads(SRC.read_text())
rows=o['structuredContent']['result']
def val(r,k):
 x=r.get(k)
 return 0.0 if x is None else float(x)
def stats(rs):
 vals=[val(r,'media_engagement') for r in rs]
 return {'n':len(rs),'engagement_total':sum(vals),'engagement_mean':sum(vals)/len(vals) if vals else 0,'engagement_median':statistics.median(vals) if vals else 0,'reach_total':sum(val(r,'media_reach') for r in rs),'views_total':sum(val(r,'media_views') for r in rs),'likes_total':sum(val(r,'media_like_count') for r in rs),'comments_total':sum(val(r,'media_comments_count') for r in rs),'saves_total':sum(val(r,'media_saved') for r in rs),'shares_total':sum(val(r,'media_shares') for r in rs)}
for r in rows:
 r['date_local_guess']=r['timestamp'][:10]
 r['watch_time_avg_seconds']=val(r,'media_reel_avg_watch_time')/1000 if r.get('media_reel_avg_watch_time') is not None else None
print('TOTAL',stats(rows))
for typ in sorted(set(r.get('media_type') for r in rows)):
 rs=[r for r in rows if r.get('media_type')==typ]
 print('TYPE',typ,stats(rs))
for month in ['2026-07','2026-08']:
 rs=[r for r in rows if r['timestamp'].startswith(month)]
 print('MONTH',month,stats(rs))
print('TOP')
for r in sorted(rows,key=lambda x:val(x,'media_engagement'),reverse=True)[:10]:
 print(r['date_local_guess'],r.get('media_type'),int(val(r,'media_engagement')),int(val(r,'media_reach')),int(val(r,'media_views')),r.get('media_caption','')[:90].replace('\n',' '),r.get('media_permalink'))
result={'source':'Windsor.ai','connector':'instagram','account_id':rows[0].get('account_id') if rows else None,'account_name':rows[0].get('account_name') if rows else None,'cut':{'start':'2026-07-22','end':'2026-08-18'},'retrieved_at':'2026-08-19T02:50:32','row_count':len(rows),'rows':rows,'aggregates':{'total':stats(rows), 'by_type':{t:stats([r for r in rows if r.get('media_type')==t]) for t in sorted(set(r.get('media_type') for r in rows))}, 'by_month':{m:stats([r for r in rows if r['timestamp'].startswith(m)]) for m in ['2026-07','2026-08']}}}
OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('OUTPUT',OUT)

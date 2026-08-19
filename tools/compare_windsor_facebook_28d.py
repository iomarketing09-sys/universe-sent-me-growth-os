import json, csv, statistics
from pathlib import Path
from datetime import datetime
SRC=Path('/home/ubuntu/.mcp/tool-results/2026-08-19_02-53-51.368592409_windsor-ai_get_data_86239c2c.json')
ROOT=Path('/home/ubuntu/universe-sent-me-growth-os')
o=json.loads(SRC.read_text()); rows=o['structuredContent']['result']
def f(x): return 0.0 if x is None else float(x)
def stats(rs):
 vals=[f(r.get('post_engagements')) for r in rs]
 return {'n':len(rs),'total':sum(vals),'mean':sum(vals)/len(vals) if vals else 0,'median':statistics.median(vals) if vals else 0,'reactions':sum(f(r.get('post_reactions_total')) for r in rs),'comments':sum(f(r.get('post_comments_total')) for r in rs),'shares':sum(f(r.get('post_activity_by_action_type_share')) for r in rs)}
print('WINDSOR',stats(rows))
for month in ['2026-07','2026-08']:
 rs=[r for r in rows if r.get('date','').startswith(month)]
 print('MONTH',month,stats(rs))
print('TOP')
for r in sorted(rows,key=lambda x:f(x.get('post_engagements')),reverse=True)[:10]: print(r.get('date'),int(f(r.get('post_engagements'))),r.get('post_id'))
# Compare by post id with the historical export's current lifetime interactions.
csv_path=ROOT/'Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv'
with csv_path.open(encoding='utf-8-sig',newline='') as h: old=list(csv.DictReader(h))
oldmap={r['id']:f(r.get('interactions')) for r in old}
matched=[(r['post_id'],f(r.get('post_engagements')),oldmap.get(r['post_id'])) for r in rows if r['post_id'] in oldmap]
diffs=[x for x in matched if abs(x[1]-x[2])>.001]
print('MATCHED',len(matched),'DIFFS',len(diffs))
for x in diffs[:10]: print('DIFF',x)
OUT=ROOT/'Operations/Research/2026-08-19_Windsor_Facebook_Organic_28D_Normalizado.json'
OUT.write_text(json.dumps({'source':'Windsor.ai','connector':'facebook_organic','account_id':'1036844829507460','account_name':'Universe Sent Me','cut':{'start':'2026-07-22','end':'2026-08-18'},'retrieved_at':'2026-08-19T02:53:50','row_count':len(rows),'rows':rows,'aggregates':stats(rows)},ensure_ascii=False,indent=2)+'\n')
print('OUTPUT',OUT)

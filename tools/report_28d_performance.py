from pathlib import Path
import csv,json,statistics
from datetime import date,datetime,timezone
ROOT=Path('/home/ubuntu/universe-sent-me-growth-os'); START=date(2026,7,22); END=date(2026,8,18)
def num(x):
 try:return float(x) if x not in ('',None,'null') else 0.0
 except:return 0.0
def d(x):
 try:return datetime.fromisoformat(str(x).replace('Z','+00:00')).date()
 except:
  try:return datetime.strptime(str(x)[:10],'%Y-%m-%d').date()
  except:return None
def stats(rows):
 vals=[r['interactions'] for r in rows]
 return {'n':len(rows),'total':sum(vals),'median':statistics.median(vals) if vals else 0,'mean':sum(vals)/len(vals) if vals else 0,'p90':sorted(vals)[max(0,int(.9*len(vals))-1)] if vals else 0,'reactions':sum(r['reactions'] for r in rows),'comments':sum(r['comments'] for r in rows),'shares':sum(r['shares'] for r in rows)}
# Facebook page posts from the complete Meta page export.
f=ROOT/'Operations/Research/2026-08-14_Comparativo_Desempeno_Junio_Julio_Agosto_Datos.csv'
with f.open(encoding='utf-8-sig',newline='') as h: raw=list(csv.DictReader(h))
fb=[]
for r in raw:
 dt=d(r.get('local') or r.get('date'))
 if dt and START<=dt<=END:
  fb.append({'date':dt,'id':r['id'],'message':r.get('message',''),'reactions':num(r.get('reactions')),'comments':num(r.get('comments')),'shares':num(r.get('shares')),'interactions':num(r.get('interactions'))})
# Facebook Reels subset from the dedicated audit.
rj=json.load(open(ROOT/'Operations/Research/2026-08-19_Meta_Reels_Audit.json',encoding='utf-8'))
reels=[]
for r in rj.get('video_reels',[]):
 dt=d(r.get('created_time'))
 if dt and START<=dt<=END:
  reactions=num(r.get('reactions')); comments=num(r.get('comments')); shares=num(r.get('shares')); reels.append({'date':dt,'id':r['id'],'message':r.get('message',''),'reactions':reactions,'comments':comments,'shares':shares,'interactions':reactions+comments+shares})
# Instagram rows in the publication log, with explicit status and metrics.
p=ROOT/'Operations/Research/2026-08-15_Publication_Log.csv'
with p.open(encoding='utf-8-sig',newline='') as h: pub=list(csv.DictReader(h))
ig=[]
for r in pub:
 dt=d(r.get('Fecha_Publicacion_Local') or r.get('Fecha_Planeada_Local'))
 if dt and START<=dt<=END and 'Instagram' in (r.get('Plataforma') or ''):
  ig.append(r)
print('CUT',START,END)
print('FACEBOOK_PAGE',stats(fb))
print('FACEBOOK_REELS',stats(reels))
print('INSTAGRAM_LOG_ROWS',len(ig))
for r in ig: print('IG_ROW',r.get('Fecha_Publicacion_Local'),r.get('Estado_Publicacion'),r.get('Eliminada'),r.get('IG_Media_ID'),r.get('Interacciones_24h'),r.get('Interacciones_72h'),r.get('Asset_Ref'))
from collections import defaultdict
for label, rows in [('FB_MONTH', fb), ('REELS_MONTH', reels)]:
 grouped=defaultdict(list)
 for r in rows: grouped[r['date'].strftime('%Y-%m')].append(r)
 for month, group in sorted(grouped.items()): print(label, month, stats(group))
print('FB_TOP10')
for r in sorted(fb,key=lambda x:x['interactions'],reverse=True)[:10]: print(r['date'],int(r['interactions']),int(r['reactions']),int(r['comments']),int(r['shares']),r['id'],r['message'][:90].replace('\n',' '))
print('REELS_TOP')
for r in sorted(reels,key=lambda x:x['interactions'],reverse=True): print(r['date'],int(r['interactions']),int(r['reactions']),int(r['comments']),int(r['shares']),r['message'][:90].replace('\n',' '))

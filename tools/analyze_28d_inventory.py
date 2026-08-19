from pathlib import Path
import csv,json,re
from datetime import date,datetime
ROOT=Path('/home/ubuntu/universe-sent-me-growth-os'); START=date(2026,7,22); END=date(2026,8,18)
def dt(x):
 m=re.search(r'2026[-/]\d{2}[-/]\d{2}',str(x))
 if not m:return None
 try:return datetime.strptime(m.group().replace('/','-'),'%Y-%m-%d').date()
 except:return None
def rd(row):
 for k,v in row.items():
  if any(s in k.lower() for s in ('date','fecha','timestamp','published','created')):
   d=dt(v)
   if d:return d
for p in sorted(ROOT.glob('**/*')):
 if p.is_dir() or '.git' in p.parts or p.suffix.lower() not in ('.csv','.json'):continue
 try:
  if p.suffix.lower()=='.csv':
   with p.open(encoding='utf-8-sig',errors='replace',newline='') as f: rows=list(csv.DictReader(f))
   inside=[r for r in rows if (d:=rd(r)) and START<=d<=END]
   if inside or any('Plataforma' in r for r in rows[:3]):
    plats=sorted({r.get('Plataforma','') for r in inside if r.get('Plataforma')})
    print(p.relative_to(ROOT),'CSV',len(rows),len(inside),','.join(plats))
  else:
   with p.open(encoding='utf-8',errors='replace') as f:o=json.load(f)
   stack=[o]; n=0
   while stack:
    x=stack.pop()
    if isinstance(x,dict):
     if any((d:=dt(v)) and START<=d<=END for k,v in x.items() if any(s in k.lower() for s in ('date','fecha','timestamp','published','created'))):n+=1
     stack.extend(x.values())
    elif isinstance(x,list):stack.extend(x)
   if n or any(s in p.name.lower() for s in ('metric','performance','instagram','facebook','reel','publication','baseline')):print(p.relative_to(ROOT),'JSON',n)
 except Exception as e: print(p.relative_to(ROOT),'ERROR',e)
print('CUT',START,END)

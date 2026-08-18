#!/usr/bin/env python3
"""Run the exact P0 cut for the five confirmed Facebook posts from 17 Aug 2026."""
from __future__ import annotations
import argparse, csv, json, os
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from extract_metrics_24_72 import derive_page_headers, query_lifetime_totals

REPO=Path(os.environ.get('USM_GROWTH_OS_REPO','/home/ubuntu/universe-sent-me-growth-os'))
BASELINE=REPO/'Operations/Research/2026-08-17_P0_Baseline_Ola_Activa.csv'
EXPERIMENT=REPO/'Operations/Research/2026-08-15_ExperimentLog.csv'
EVIDENCE=REPO/'Operations/Research/2026-08-19_P0_Corte_17_Agosto.json'
TZ=ZoneInfo('America/Matamoros')

def read_csv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f); return list(r),list(r.fieldnames)
def write_csv(p,rows,fields):
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)
def parse_dt(s):
 return datetime.fromisoformat(s.replace('Z','+00:00')).astimezone(timezone.utc)
def marker(text,m): return text if m in text else f'{text.rstrip()} {m}'.strip()

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--now'); ap.add_argument('--run-id'); ap.add_argument('--dry-run',action='store_true'); ap.add_argument('--evidence',type=Path,default=EVIDENCE); a=ap.parse_args()
 now=parse_dt(a.now) if a.now else datetime.now(timezone.utc); run=a.run_id or now.strftime('%Y%m%dT%H%M%SZ'); extracted=now.isoformat()
 base,bfields=read_csv(BASELINE); exp,efields=read_csv(EXPERIMENT)
 due=[]
 for row in base:
  published=parse_dt(row['published_at_utc']); age=(now-published).total_seconds()/3600; windows=[]
  if age>=24 and not row.get('interactions_24h','').strip() and '24h_snapshot_unavailable' not in row.get('notes',''): windows.append('24h')
  if age>=72 and not row.get('interactions_72h','').strip() and '72h_snapshot_unavailable' not in row.get('notes',''): windows.append('72h')
  due.append({'publication_id':row['publication_id'],'asset_ref':row['Asset_Ref'],'meta_post_id':row['meta_post_id'],'published_at_local':row['published_at_local'],'age_hours':round(age,3),'due_windows':windows})
 headers=None; page_context=None; responses=[]
 if not a.dry_run:
  token=os.environ.get('META_PAGE_ACCESS_TOKEN')
  if not token: raise SystemExit('META_PAGE_ACCESS_TOKEN required')
  headers,page_context=derive_page_headers(token)
  for c in due:
   if not c['due_windows']: continue
   result=query_lifetime_totals(c['meta_post_id'],headers); c['evidence']=result
   responses.append({'publication_id':c['publication_id'],'asset_ref':c['asset_ref'],'meta_post_id':c['meta_post_id'],**result})
 marker_text=f'[P0-CUT-RUN:{run}] {extracted}'
 did_update=False
 if not a.dry_run and any(c['due_windows'] for c in due):
  did_update=True
  bypub={r['publication_id']:r for r in base}
  bymeta={r.get('Meta_ID',''):r for r in exp}
  for c in due:
   if not c['due_windows']: continue
   note=f"{marker_text}: {','.join(c['due_windows'])} due; " + ' '.join(f'{w}_snapshot_unavailable' for w in c['due_windows']) + '; Meta returned lifetime totals only; exact 24h/72h values not written.'
   r=bypub[c['publication_id']]; r['notes']=marker(r.get('notes',''),note); r['window_status']='Snapshot_Unavailable_Lifetime_Evidence'
   er=bymeta.get(c['meta_post_id'])
   if er is not None:
    er['Conclusion']=marker(er.get('Conclusion',''),note)
    er['Proxima_Accion']=marker(er.get('Proxima_Accion',''),'Do not substitute lifetime totals for exact windows; use observed-cut evidence.')
  write_csv(BASELINE,base,bfields); write_csv(EXPERIMENT,exp,efields)
 result={'extracted_at_utc':extracted,'extracted_at_local':now.astimezone(TZ).isoformat(),'timezone':'America/Matamoros','experiment_id':'EXP-2026-08-CAL-01','target':'five confirmed Facebook posts from 2026-08-17','candidate_count':len(due),'eligible_count':sum(bool(c['due_windows']) for c in due),'exact_window_writes':0,'ledger_updates':did_update,'instagram_touched':False,'content_published':False,'page_context':page_context,'candidates':due,'responses':responses,'status':'dry_run' if a.dry_run else 'extracted_lifetime_only','run_id':run}
 a.evidence.parent.mkdir(parents=True,exist_ok=True); a.evidence.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps({k:result[k] for k in ['extracted_at_utc','candidate_count','eligible_count','exact_window_writes','ledger_updates','status']},ensure_ascii=False)); print('evidence_file='+str(a.evidence))
if __name__=='__main__': main()

#!/usr/bin/env python3
import csv, json, re
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
api=json.loads((ROOT/'Operations/Research/2026-08-23_Facebook_Performance_Meta_API.json').read_text(encoding='utf-8'))
summary=json.loads((ROOT/'Operations/Research/2026-08-23_Facebook_Performance_Summary.json').read_text(encoding='utf-8'))
with (ROOT/'Operations/Research/2026-08-15_Publication_Log.csv').open(encoding='utf-8-sig',newline='') as f: pub=list(csv.DictReader(f))
with (ROOT/'Operations/Research/2026-08-15_ExperimentLog.csv').open(encoding='utf-8-sig',newline='') as f: exp=list(csv.DictReader(f))
with (ROOT/'GrowthOS/Content_Inventory.csv').open(encoding='utf-8-sig',newline='') as f: inv=list(csv.DictReader(f))

# Accept both page_post_id forms used by the ledgers.
def ids(row):
    vals=[]
    for k in ('Meta_Post_ID','Meta_ID','Post_ID','Facebook_Post_ID'):
        if row.get(k): vals.append(row[k].strip())
    return vals
pub_id_set={x for row in pub for x in ids(row)}
exp_id_set={x.strip() for row in exp for x in (row.get('Meta_ID') or '').split('|') if x.strip()}
inv_text=' '.join(' '.join(str(v or '') for v in row.values()) for row in inv)
post_matches=[]
for p in api['posts']:
    pid=p['id']; short=pid.split('_',1)[-1]
    pub_match=pid in pub_id_set or short in pub_id_set
    exp_match=pid in exp_id_set or short in exp_id_set
    post_matches.append({'id':pid,'short_id':short,'publication_log_match':pub_match,'experiment_log_match':exp_match})

recent_exp=[r for r in exp if r.get('Plataforma')=='Facebook' and (r.get('Fecha_Inicio') or '') >= '2026-08-15' and r.get('Estado_Publicacion')=='Publicado']
all_pub_fb=[r for r in pub if r.get('Plataforma') and 'Facebook' in r.get('Plataforma')]
report={
  'api_retrieved_at':api['retrieved_at'],
  'api_post_count':len(api['posts']),
  'api_date_min':summary['window']['earliest_created_time'],
  'api_date_max':summary['window']['latest_created_time'],
  'public_engagement':summary['overall'],
  'shares_share_of_engagement':round(summary['overall']['total_shares']/summary['overall']['total_engagement_public'],4),
  'comments_share_of_engagement':round(summary['overall']['total_comments']/summary['overall']['total_engagement_public'],4),
  'reactions_share_of_engagement':round(summary['overall']['total_reactions']/summary['overall']['total_engagement_public'],4),
  'top1_share':round(summary['top_posts'][0]['engagement_public']/summary['overall']['total_engagement_public'],4),
  'top2_share':round(sum(p['engagement_public'] for p in summary['top_posts'][:2])/summary['overall']['total_engagement_public'],4),
  'recent_posts_in_publication_log':sum(x['publication_log_match'] for x in post_matches),
  'recent_posts_in_experiment_log':sum(x['experiment_log_match'] for x in post_matches),
  'recent_post_matches':post_matches,
  'experiment_log':{
      'rows_total':len(exp), 'facebook_rows':sum(r.get('Plataforma')=='Facebook' for r in exp),
      'recent_published_rows':len(recent_exp),
      'recent_24h_nonempty':sum(bool((r.get('Interacciones_24h') or '').strip()) for r in recent_exp),
      'recent_72h_nonempty':sum(bool((r.get('Interacciones_72h') or '').strip()) for r in recent_exp),
      'recent_verdicts':dict(Counter((r.get('Veredicto') or '<blank>').strip() for r in recent_exp)),
  },
  'publication_log':{
      'rows_total':len(pub),'facebook_rows':len(all_pub_fb),'published_rows':sum(r.get('Estado_Publicacion')=='Publicado' for r in all_pub_fb),
      '24h_nonempty':sum(bool((r.get('Interacciones_24h') or '').strip()) for r in all_pub_fb),
      '72h_nonempty':sum(bool((r.get('Interacciones_72h') or '').strip()) for r in all_pub_fb),
  },
  'normalized_28d_artifact':{'rows':143,'cut_start':'2026-07-22','cut_end':'2026-08-18','retrieved_at':'2026-08-19T16:08:45.687Z'},
}
(ROOT/'Operations/Research/2026-08-23_Facebook_Growth_Integration_Audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in {'recent_post_matches'}},ensure_ascii=False,indent=2))

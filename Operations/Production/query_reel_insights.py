import os,requests,json
from pathlib import Path
BASE='https://graph.facebook.com/v26.0'; PAGE='1036844829507460'
source=json.loads(Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-19_Meta_Reels_Audit.json').read_text())
h={'Authorization':f"Bearer {os.environ['META_PAGE_ACCESS_TOKEN']}"}
a=requests.get(BASE+'/me/accounts',params={'fields':'id,name,access_token','limit':100},headers=h,timeout=30); a.raise_for_status(); page=next(x for x in a.json()['data'] if x['id']==PAGE); ph={'Authorization':f"Bearer {page['access_token']}"}
metrics='post_video_views,post_video_view_time,post_video_avg_time_watched,post_video_complete_views,post_engaged_users,post_reactions_by_type_total,post_comments,post_shares'
rows=[]
for p in source['video_reels']:
 r=requests.get(BASE+'/'+p['id']+'/insights',params={'metric':metrics},headers=ph,timeout=30)
 try: payload=r.json()
 except: payload={'raw':r.text}
 rows.append({'id':p['id'],'created_time':p['created_time'],'permalink_url':p['permalink_url'],'http_status':r.status_code,'data':payload.get('data',[]) if isinstance(payload,dict) else [],'error':payload.get('error') if isinstance(payload,dict) else None})
print('REELS',len(rows),'HTTP_COUNTS', {str(s):sum(x['http_status']==s for x in rows) for s in sorted(set(x['http_status'] for x in rows))})
out=Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-19_Meta_Reel_Insights.json'); out.write_text(json.dumps({'retrieved_at':'2026-08-18T00:00:00Z','metric_request':metrics,'rows':rows},ensure_ascii=False,indent=2)+'\n')
for x in rows: print(x['id'],x['http_status'],len(x['data']), 'error='+str(x['error']) if x['error'] else '')
print('OUTPUT',out)

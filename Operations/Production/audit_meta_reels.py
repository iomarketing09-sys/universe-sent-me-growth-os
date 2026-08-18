import os, requests, json
from pathlib import Path
BASE='https://graph.facebook.com/v26.0'; PAGE='1036844829507460'
h={'Authorization':f"Bearer {os.environ['META_PAGE_ACCESS_TOKEN']}"}
r=requests.get(BASE+'/me/accounts',params={'fields':'id,name,access_token','limit':100},headers=h,timeout=30); r.raise_for_status()
page=next(x for x in r.json()['data'] if x['id']==PAGE); ph={'Authorization':f"Bearer {page['access_token']}"}
params={'fields':'id,created_time,message,permalink_url,attachments{media_type,type,target,url,media},reactions.limit(0).summary(true),comments.limit(0).summary(true),shares','limit':100}
r=requests.get(BASE+f'/{PAGE}/posts',params=params,headers=ph,timeout=60); print('HTTP',r.status_code); r.raise_for_status()
data=r.json().get('data',[])
rows=[]
for p in data:
 att=p.get('attachments',{}).get('data',[]) if isinstance(p.get('attachments'),dict) else []
 types=[]; media=[]
 for a in att:
  types += [str(a.get('media_type','')),str(a.get('type',''))]
  m=a.get('media') or {}; media.append({'media_type':a.get('media_type'),'type':a.get('type'),'url':a.get('url'),'image':m.get('image') if isinstance(m,dict) else None})
 is_video=any('video' in t.lower() or 'reel' in t.lower() for t in types)
 if is_video:
  reactions=((p.get('reactions') or {}).get('summary') or {}).get('total_count')
  comments=((p.get('comments') or {}).get('summary') or {}).get('total_count')
  shares=(p.get('shares') or {}).get('count') if isinstance(p.get('shares'),dict) else None
  rows.append({'id':p.get('id'),'created_time':p.get('created_time'),'permalink_url':p.get('permalink_url'),'message':p.get('message',''),'attachment_types':types,'reactions':reactions,'comments':comments,'shares':shares,'attachments':media})
print('VIDEO_REELS',len(rows))
for x in rows: print(json.dumps({k:x[k] for k in ['id','created_time','permalink_url','message','attachment_types','reactions','comments','shares']},ensure_ascii=False))
out=Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-19_Meta_Reels_Audit.json'); out.write_text(json.dumps({'page_id':PAGE,'page_name':page['name'],'posts_scanned':len(data),'video_reels':rows},ensure_ascii=False,indent=2)+'\n')
print('OUTPUT',out)

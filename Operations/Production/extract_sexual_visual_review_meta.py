import csv,json,os,requests
from datetime import datetime,timezone
from pathlib import Path
root=Path('/home/ubuntu/universe-sent-me-growth-os'); base='https://graph.facebook.com/v26.0'
user=os.environ['META_PAGE_ACCESS_TOKEN']; h={'Authorization':f'Bearer {user}'}
a=requests.get(f'{base}/me/accounts',headers=h,params={'fields':'id,name,access_token,tasks','limit':100},timeout=30); a.raise_for_status()
page=next(x for x in a.json().get('data',[]) if x.get('name')=='Universe Sent Me'); token=page['access_token']
rows=list(csv.DictReader((root/'Operations/Research/2026-08-19_Revision_Visual_Sexualidad_Alto_Rendimiento.csv').open(encoding='utf-8-sig')))
fields='id,created_time,message,full_picture,attachments{media_type,media{image{src,width,height}}}'
batch=[{'method':'GET','relative_url':f"{r['meta_id']}?fields={fields}"} for r in rows]
resp=requests.post(base,headers={'Authorization':f'Bearer {token}'},data={'batch':json.dumps(batch)},timeout=60); resp.raise_for_status()
out={'extracted_at_utc':datetime.now(timezone.utc).isoformat(),'selection_basis':'Top unresolved June cases by performance, excluding prior sexual/acid visual sample; read-only.','selected_rows':rows,'batch_response':resp.json()}
p=root/'Operations/Research/2026-08-19_Revision_Visual_Sexualidad_Alto_Rendimiento_Meta.json'; p.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8'); print({'selected':len(rows),'output':str(p)})

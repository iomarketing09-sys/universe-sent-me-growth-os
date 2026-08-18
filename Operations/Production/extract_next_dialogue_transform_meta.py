import csv, json, os, requests
from datetime import datetime, timezone
from pathlib import Path

root=Path('/home/ubuntu/universe-sent-me-growth-os')
base='https://graph.facebook.com/v26.0'
user=os.environ['META_PAGE_ACCESS_TOKEN']
headers={'Authorization':f'Bearer {user}'}
accounts=requests.get(f'{base}/me/accounts',headers=headers,params={'fields':'id,name,access_token,tasks','limit':100},timeout=30)
accounts.raise_for_status()
page=next(x for x in accounts.json().get('data',[]) if x.get('name')=='Universe Sent Me')
token=page['access_token']
rows=list(csv.DictReader((root/'Operations/Research/2026-08-19_Siguiente_Lote_Candidatos_Dialogo_Transformacion.csv').open(encoding='utf-8-sig')))
selected=rows[:15]
fields='id,created_time,message,full_picture,attachments{media_type,media{image{src,width,height}}}'
batch=[{'method':'GET','relative_url':f"{r['meta_id']}?fields={fields}"} for r in selected]
resp=requests.post(base,headers={'Authorization':f'Bearer {token}'},data={'batch':json.dumps(batch)},timeout=60)
resp.raise_for_status()
out={'extracted_at_utc':datetime.now(timezone.utc).isoformat(),'selection_basis':'Top 15 new candidates after excluding prior dialogue/transform batch; read-only.','selected_queue_rows':selected,'batch_response':resp.json()}
outpath=root/'Operations/Research/2026-08-19_Siguiente_Lote_Dialogo_Transformacion_Meta_Media.json'
outpath.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'selected':len(selected),'output':str(outpath)}))
for row,item in zip(selected,out['batch_response']): print(row['meta_id'],item.get('code'),row.get('interactions'),row.get('shares'),row.get('caption'))

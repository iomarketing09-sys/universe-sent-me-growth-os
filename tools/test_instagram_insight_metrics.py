import os, requests, json
BASE='https://graph.facebook.com/v26.0'
MEDIA_ID='17964221226159563'
TOKEN=os.environ['META_PAGE_ACCESS_TOKEN']
accounts=requests.get(BASE+'/me/accounts',params={'fields':'id,name,access_token','limit':100},headers={'Authorization':f'Bearer {TOKEN}'},timeout=30).json()['data']
page=next(x for x in accounts if x['id']=='1036844829507460')
headers={'Authorization':f"Bearer {page['access_token']}"}
for metric in ['impressions','reach','engagement','saved','video_views','plays','total_interactions']:
 r=requests.get(BASE+'/'+MEDIA_ID+'/insights',params={'metric':metric},headers=headers,timeout=30)
 try:p=r.json()
 except:p={'raw':r.text}
 print(metric,r.status_code,json.dumps(p,ensure_ascii=False))

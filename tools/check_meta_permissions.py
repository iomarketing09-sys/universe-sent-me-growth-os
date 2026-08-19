import os, requests, json
BASE='https://graph.facebook.com/v26.0'
TOKEN=os.environ['META_PAGE_ACCESS_TOKEN']
r=requests.get(BASE+'/me/permissions',headers={'Authorization':f'Bearer {TOKEN}'},timeout=30)
print('HTTP',r.status_code)
print(json.dumps(r.json(),ensure_ascii=False,indent=2))

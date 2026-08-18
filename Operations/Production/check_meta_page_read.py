import os, requests
base='https://graph.facebook.com'
h={'Authorization':f"Bearer {os.environ['META_PAGE_ACCESS_TOKEN']}"}
r=requests.get(base+'/me/accounts',params={'fields':'id,name,access_token','limit':10},headers=h,timeout=30)
r.raise_for_status(); accounts=r.json().get('data',[])
page=next((x for x in accounts if x.get('id')=='1036844829507460'),None)
if not page:
 print('PAGE_NOT_FOUND'); raise SystemExit(2)
ph={'Authorization':f"Bearer {page['access_token']}"}
obj=requests.get(base+'/1036844829507460',params={'fields':'id,name,can_post'},headers=ph,timeout=30)
print('PAGE_OBJECT_STATUS',obj.status_code,obj.json().get('id'),obj.json().get('name'),obj.json().get('can_post'))
feed=requests.get(base+'/1036844829507460/posts',params={'fields':'id,created_time,message,permalink_url','limit':25},headers=ph,timeout=30)
print('PAGE_FEED_STATUS',feed.status_code)
data=feed.json().get('data',[])
print('PAGE_FEED_COUNT',len(data))
for x in data[:10]: print(x.get('id'),x.get('created_time'),(x.get('message') or '')[:80].replace('\n',' '))

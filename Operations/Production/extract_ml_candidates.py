from bs4 import BeautifulSoup
from pathlib import Path
import json, re

html = Path('/home/ubuntu/upload/listado.mercadolibre.com.mx_lentes-de-sol-gato_1787065281826.html').read_text(errors='ignore')
soup = BeautifulSoup(html, 'html.parser')
rows=[]
for a in soup.find_all('a', href=True):
    txt=' '.join(a.get_text(' ', strip=True).split())
    href=a['href']
    if txt and ('gato' in txt.lower() or 'cateye' in txt.lower() or 'joopin' in txt.lower()) and ('mercadolibre.com.mx' in href):
        price=''
        parent=a.parent
        scope=' '.join(parent.get_text(' ', strip=True).split()) if parent else txt
        m=re.search(r'\$\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)', scope)
        if m: price=m.group(1)
        rows.append({'title':txt,'price_visible':price,'url':href})
seen=set(); out=[]
for r in rows:
    key=(r['title'],r['url'])
    if key not in seen:
        seen.add(key); out.append(r)
Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-19_ML_AFF01_Candidates.json').write_text(json.dumps(out[:20],ensure_ascii=False,indent=2))
print(json.dumps(out[:8],ensure_ascii=False,indent=2))

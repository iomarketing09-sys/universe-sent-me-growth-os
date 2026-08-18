from bs4 import BeautifulSoup
from pathlib import Path
import json

src = Path('/home/ubuntu/upload/listado.mercadolibre.com.mx_lentes-de-sol-gato_1787040489569.html')
out = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-19_ML_Search_Lentes_Gato.json')
soup = BeautifulSoup(src.read_text(errors='ignore'), 'html.parser')
rows = []
seen = set()
for a in soup.find_all('a', href=True):
    text = ' '.join(a.get_text(' ', strip=True).split())
    href = a.get('href','')
    if not text or 'mercadolibre' not in href.lower():
        continue
    if not any(token in text.lower() for token in ['lente', 'gafa', 'ojo de gato', 'cateye']):
        continue
    key = (text[:180], href.split('?')[0])
    if key in seen:
        continue
    seen.add(key)
    img = a.find('img')
    image_url = None
    if img:
        for attr in ('src','data-src','data-lazy-src','data-original','srcset'):
            value = img.get(attr)
            if value:
                image_url = value.split(',')[0].strip().split(' ')[0]
                break
    if not image_url:
        for node in a.find_all(['picture','source']):
            for attr in ('srcset','data-srcset'):
                value = node.get(attr)
                if value:
                    image_url = value.split(',')[0].strip().split(' ')[0]
                    break
            if image_url:
                break
    rows.append({'title': text[:240], 'url': href.split('?')[0], 'image_url': image_url})
    if len(rows) >= 30:
        break
out.write_text(json.dumps({'query':'lentes de sol gato','rows':rows}, ensure_ascii=False, indent=2))
print(json.dumps({'count':len(rows),'output':str(out)}, ensure_ascii=False))

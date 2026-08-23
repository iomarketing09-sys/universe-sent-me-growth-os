import csv
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

OUT = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/affiliate_product_candidates.csv')
queries = [
('AFF-13','cubo antiestrés fidget cube'),('AFF-14','lampara luna 3d decorativa'),('AFF-15','lampara calida ambar mesa'),
('AFF-16','mini impresora termica bluetooth'),('AFF-17','taza esmaltada vintage'),('AFF-18','difusor aromas aceites esenciales'),
('AFF-19','gadget inutil divertido escritorio'),('AFF-20','arena cinetica'),('AFF-21','manta suave cozy'),
('AFF-22','letrero neon led frase'),('AFF-23','cojin estetico decorativo'),('AFF-24','lampara de sal'),
('AFF-25','lampara pared resina hada bosque'),('AFF-26','taza grande cafe'),('AFF-27','teclado mecanico compacto'),
('AFF-28','organizador creativo escritorio'),('AFF-29','mini maquina humo fiesta'),('AFF-30','exprimidor manual compacto'),
('AFF-31','tiras led suaves hada'),('AFF-32','cuenco tibetano decorativo'),('AFF-33','shaker licuadora portatil'),
('AFF-34','velas led calidas'),('AFF-35','lampara creativa escritorio'),('AFF-36','mascara led fiesta')]

def fetch(item):
    aid,q=item
    url='https://listado.mercadolibre.com.mx/'+quote(q.replace(' ','-'))
    try:
        r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=(3,8))
        soup=BeautifulSoup(r.text,'html.parser')
        found=[]
        for a in soup.find_all('a',href=True):
            h=a['href'].split('#')[0]
            if re.search(r'/p/MLM\d+|/MLM-\d+-',h) and 'mercadolibre.com.mx' in h and h not in found:
                found.append(h)
        return {'opportunity_id':aid,'query':q,'search_url':url,'candidate_url':found[0] if found else '','status':'ok' if found else 'no_candidate'}
    except Exception as e:
        return {'opportunity_id':aid,'query':q,'search_url':url,'candidate_url':'','status':type(e).__name__}

with ThreadPoolExecutor(max_workers=8) as ex:
    rows=list(ex.map(fetch,queries))
with OUT.open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f'written {len(rows)} rows to {OUT}')

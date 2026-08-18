from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

root = Path('/home/ubuntu/universe-sent-me-growth-os')
img_dir = root / 'Operations/Research/Affiliate_Product_Images'
out = root / 'Operations/Research/2026-08-19_Catalogo_Visual_Afiliados_Facebook.png'
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font_bold_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font = ImageFont.truetype(font_path, 24)
small = ImageFont.truetype(font_path, 18)
bold = ImageFont.truetype(font_bold_path, 26)
items = [
('AFF-01','18 ago · 260644','Lentes ojo de gato','$190–$282 observado','Universe / estilo'),
('AFF-02','19 ago · 260560','Decoración o luces de Fantasma','$138–$239 observado','Fantasma / humor visual'),
('AFF-03','20 ago · 260659','Casa o rascador para gato','$180–$269 observado','Caja / Universe'),
('AFF-04','21 ago · 260635','Lámpara efecto fuego','$100–$300 objetivo','Luz / humor ácido'),
('AFF-05','22 ago · 260510','Soporte para taza y teléfono','$196.54 observado','Taza + chat'),
('AFF-06','24 ago · 260518','Regalo pequeño de pareja','$100–$300 objetivo','Kael / romance'),
('AFF-07','26 ago · 260540','Audífonos o accesorio de lectura','$100–$300 objetivo','Elara / música'),
('AFF-08','28 ago · 260590','Soporte de celular de gatito','$130–$179 observado','Maeve / audio'),
('AFF-09','29 ago · 741','Lámpara de fogata o ambiente','$100–$300 objetivo','Elara + Maeve'),
('AFF-10','30 ago · 260528','Taza o termo de café','$149–$260 objetivo','Universe / buenos días'),
]
files = {f'AFF-{i:02d}': img_dir / f'AFF-{i:02d}_{name}' for i,name in [
(1,'sunglasses.webp'),(2,'ghost_lights.webp'),(3,'cat_house.webp'),(4,'fire_lamp.webp'),(5,'phone_cup_holder.webp'),(6,'rose_gift.webp'),(7,'earbuds.webp'),(8,'cat_phone_holder.webp'),(9,'campfire_lamp.webp'),(10,'coffee_mug.webp')
]}
card_w, card_h = 520, 620
cols, rows = 2, 5
canvas = Image.new('RGB', (cols*card_w, rows*card_h), 'white')
draw = ImageDraw.Draw(canvas)
for idx, (aff, date, title, price, fit) in enumerate(items):
    x, y = (idx % cols)*card_w, (idx // cols)*card_h
    draw.rectangle((x+10,y+10,x+card_w-10,y+card_h-10), outline='#d9d9d9', width=2)
    im = Image.open(files[aff]).convert('RGB')
    im.thumbnail((card_w-40, 390))
    ix = x + (card_w-im.width)//2
    iy = y + 22 + (390-im.height)//2
    canvas.paste(im, (ix, iy))
    draw.text((x+24,y+420), f'{aff} · {date}', fill='#111111', font=bold)
    draw.text((x+24,y+460), title, fill='#222222', font=font)
    draw.text((x+24,y+498), price, fill='#0b5a35', font=small)
    draw.text((x+24,y+532), f'Encaje: {fit}', fill='#444444', font=small)
canvas.save(out, quality=95)
print(out)

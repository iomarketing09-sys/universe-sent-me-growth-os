#!/usr/bin/env python3
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root=Path('Operations/Research')
imgdir=root/'June_Unmatched_Top15_Meta_Images'
out=imgdir/'contact_sheets'; out.mkdir(exist_ok=True)
d=json.loads((root/'2026-08-18_Junio_Unmatched_Top15_Meta_Media.json').read_text(encoding='utf-8'))
rows=[]
for r,item in zip(d['selected_queue_rows'],d['batch_response']):
    pid=r['meta_id']; p=imgdir/f'{pid}.jpg'
    if p.exists(): rows.append((p,r))
font=ImageFont.load_default()
for start in range(0,len(rows),6):
    sheet=Image.new('RGB',(1200,900),'white'); draw=ImageDraw.Draw(sheet)
    for idx,(p,r) in enumerate(rows[start:start+6]):
        im=Image.open(p).convert('RGB'); im.thumbnail((360,380))
        x=20+(idx%3)*390; y=20+(idx//3)*440
        sheet.paste(im,(x+(360-im.width)//2,y))
        label=f"{r['meta_id'].split('_')[-1]} | {r['publication_date_local']} | int {r['interactions']} | sh {r['shares']}"
        draw.text((x,y+390),label,fill='black',font=font)
    target=out/f'unmatched_june_contact_{start//6+1}.jpg'; sheet.save(target,quality=92); print(target)

from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import csv, re

root = Path('/home/ubuntu/universe-sent-me-growth-os')
overlay = root / 'Operations/Research/2026-08-20_Overlay_Wave1_Calendario_17_30.csv'
asset_dir = Path('/home/ubuntu/calendar_visual_review_20260816')
out = root / 'Operations/Research/2026-08-20_Overlay_Wave1_Contact_Sheet.jpg'

with overlay.open(newline='', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

font = ImageFont.load_default()
thumb_w, thumb_h = 420, 390
cols = 3
rows_n = (len(rows) + cols - 1) // cols
sheet = Image.new('RGB', (cols*thumb_w, rows_n*thumb_h), 'white')

def find_asset(ref):
    refnum = ref.split(' - ',1)[0].split('-')[0].strip()
    candidates = list(asset_dir.glob(f'{refnum}__*'))
    return candidates[0] if candidates else None

for idx, row in enumerate(rows):
    x = (idx % cols) * thumb_w
    y = (idx // cols) * thumb_h
    p = find_asset(row['Archivo'])
    if p:
        im = Image.open(p).convert('RGB')
        im.thumbnail((thumb_w-20, thumb_h-80))
        tile = ImageOps.contain(im, (thumb_w-20, thumb_h-80), method=Image.Resampling.LANCZOS)
        sheet.paste(tile, (x+(thumb_w-tile.width)//2, y+5))
    draw = ImageDraw.Draw(sheet)
    label = f"{row['Overlay_ID']} | {row['Fecha']} {row['Hora']}\n{row['Archivo'][:48]}\n{row['Family_ID_Provisional']} | {row['Caption_Treatment_Propuesto']}"
    draw.multiline_text((x+8, y+thumb_h-70), label, fill='black', font=font, spacing=3)
    draw.rectangle((x,y,x+thumb_w-1,y+thumb_h-1), outline='#bdbdbd')

sheet.save(out, quality=92)
print(out)

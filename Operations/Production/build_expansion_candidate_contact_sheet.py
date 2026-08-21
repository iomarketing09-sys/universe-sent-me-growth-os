from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import re

src = Path('/home/ubuntu/june_assets_download')
refs = ['260740','260747','260731','260765','260766','260775','2607780','2607783','2607786','2607787','2607816','2607823','2607824','2607828','2607837','260552']
files = []
for ref in refs:
    matches = sorted(src.glob(f'*_{ref}.*'))
    if matches:
        files.append((ref, matches[0]))

cell_w, cell_h = 420, 460
cols = 4
rows = (len(files) + cols - 1) // cols
sheet = Image.new('RGB', (cols*cell_w, rows*cell_h), 'white')
draw = ImageDraw.Draw(sheet)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
except Exception:
    font = small = None
for i, (ref, path) in enumerate(files):
    x, y = (i % cols)*cell_w, (i // cols)*cell_h
    try:
        im = Image.open(path).convert('RGB')
        thumb = ImageOps.contain(im, (cell_w-20, cell_h-70))
        px = x + (cell_w-thumb.width)//2
        py = y + 35 + (cell_h-70-thumb.height)//2
        sheet.paste(thumb, (px, py))
        draw.text((x+10, y+8), ref, fill='black', font=font)
        draw.text((x+10, y+cell_h-28), path.name[:52], fill='gray', font=small)
    except Exception as e:
        draw.text((x+10, y+8), f'{ref} ERROR', fill='red', font=font)
out = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/2026-08-20_Expansion_Candidate_Contact_Sheet.jpg')
sheet.save(out, quality=92)
print(f'files_included={len(files)} output={out}')

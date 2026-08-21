from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont
import csv

root = Path('/home/ubuntu/universe-sent-me-growth-os')
pool = root / 'Operations/Research/2026-08-18_Junio_Lote_Priorizado_Difusion_Enriquecido.csv'
current = root / 'Operations/Research/2026-08-20_Expansion_Celdas_Comparables_Candidatos.csv'
asset_dir = Path('/home/ubuntu/june_assets_download')
out = root / 'Operations/Research/2026-08-20_Expansion_Round2_Candidate_Contact_Sheet.jpg'

with pool.open(newline='', encoding='utf-8-sig') as f:
    pool_rows = list(csv.DictReader(f))
with current.open(newline='', encoding='utf-8-sig') as f:
    used_ids = {r['Meta_ID'] for r in csv.DictReader(f)}

rows = []
for r in pool_rows:
    if r['meta_id'] in used_ids:
        continue
    ref = r['asset_ref_normalized']
    files = sorted(asset_dir.glob(f'*_{ref}.*'))
    if not files:
        files = sorted(asset_dir.glob(f'*{ref}.*'))
    if files:
        rows.append((ref, r['meta_id'], r['metric_value'], r['shares'], r['filename_or_concept'], files[0]))

cell_w, cell_h = 420, 470
cols = 4
rows_n = (len(rows) + cols - 1) // cols
sheet = Image.new('RGB', (cols*cell_w, rows_n*cell_h), 'white')
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 19)
small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
for i, (ref, mid, interactions, shares, concept, path) in enumerate(rows):
    x, y = (i % cols)*cell_w, (i // cols)*cell_h
    try:
        im = Image.open(path).convert('RGB')
        thumb = ImageOps.contain(im, (cell_w-20, cell_h-105))
        px = x + (cell_w-thumb.width)//2
        py = y + 35 + (cell_h-105-thumb.height)//2
        sheet.paste(thumb, (px, py))
        draw.text((x+10, y+8), f'{ref}  {interactions} int / {shares} sh', fill='black', font=font)
        draw.text((x+10, y+cell_h-62), path.name[:55], fill='gray', font=small)
        draw.text((x+10, y+cell_h-43), concept[:55], fill='gray', font=small)
        draw.text((x+10, y+cell_h-24), mid[-18:], fill='gray', font=small)
    except Exception:
        draw.text((x+10, y+8), f'{ref} ERROR', fill='red', font=font)

sheet.save(out, quality=92)
print(f'candidate_assets={len(rows)} output={out}')

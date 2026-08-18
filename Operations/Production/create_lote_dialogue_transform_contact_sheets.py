from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

root = Path('/home/ubuntu/universe-sent-me-growth-os')
src = root / 'Operations/Research/June_Lote_Dialogo_Transformacion_Images'
out = root / 'Operations/Research/June_Lote_Dialogo_Transformacion_ContactSheets'
out.mkdir(exist_ok=True)
files = sorted(src.glob('*.jpg'))
font = ImageFont.load_default()
for batch_no in range(0, len(files), 4):
    batch = files[batch_no:batch_no+4]
    thumbs = []
    for f in batch:
        im = Image.open(f).convert('RGB')
        im.thumbnail((500, 500))
        canvas = Image.new('RGB', (540, 580), 'white')
        x = (540 - im.width)//2
        canvas.paste(im, (x, 10))
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 525), f.stem, fill='black', font=font)
        thumbs.append(canvas)
    sheet = Image.new('RGB', (1080, 1160), '#dddddd')
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((i%2)*540, (i//2)*580))
    path = out / f'lote_dialogue_transform_contact_{batch_no//4+1}.jpg'
    sheet.save(path, quality=92)
    print(path)

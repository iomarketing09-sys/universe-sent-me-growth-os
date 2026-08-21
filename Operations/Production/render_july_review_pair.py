from pathlib import Path
from PIL import Image, ImageDraw

root = Path('/home/ubuntu/universe-sent-me-growth-os')
meta = root / 'Operations/Research/2026-08-21_Julio_Expansion_Lote01_Meta_Images/1036844829507460_122142624879072582.jpg'
drive = Path('/tmp/usm_july_drive_thumbnails/1yIedBN0HSoESMZMNwUp6Y9hMy-uJSAAd.jpg')
out = root / 'Operations/Research/2026-08-21_Julio_Expansion_Lote01_Review_Pair.jpg'
canvas = Image.new('RGB', (1600, 1000), 'white')
for index, (path, label) in enumerate(((meta, 'Meta'), (drive, 'Drive candidate'))):
    image = Image.open(path).convert('RGB')
    image.thumbnail((760, 880))
    x = 20 + index * 800 + (760 - image.width) // 2
    canvas.paste(image, (x, 50))
    draw = ImageDraw.Draw(canvas)
    draw.text((20 + index * 800, 15), label, fill='black')
canvas.save(out, quality=95)
print(out)

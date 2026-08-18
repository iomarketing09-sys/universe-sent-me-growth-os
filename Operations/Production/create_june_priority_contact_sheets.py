#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

src = Path("Operations/Research/June_Priority_Assets")
out = src / "contact_sheets"
out.mkdir(exist_ok=True)
files = sorted([p for p in src.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"}], key=lambda p: int(''.join(c for c in p.stem if c.isdigit()) or 0))
font = ImageFont.load_default()
for page in range(0, len(files), 6):
    batch = files[page:page+6]
    sheet = Image.new("RGB", (1200, 900), "white")
    draw = ImageDraw.Draw(sheet)
    for idx, path in enumerate(batch):
        im = Image.open(path).convert("RGB")
        im.thumbnail((360, 390))
        x = 20 + (idx % 3) * 390
        y = 30 + (idx // 3) * 430
        sheet.paste(im, (x + (360-im.width)//2, y))
        draw.text((x, y + 395), path.stem, fill="black", font=font)
    target = out / f"june_priority_contact_{page//6+1}.jpg"
    sheet.save(target, quality=92)
    print(target)

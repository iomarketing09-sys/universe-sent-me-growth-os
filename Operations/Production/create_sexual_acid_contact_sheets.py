from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path('/home/ubuntu/universe-sent-me-growth-os'); src=root/'Operations/Research/June_Humor_Sexual_Acido_Images'; out=root/'Operations/Research/June_Humor_Sexual_Acido_ContactSheets'; out.mkdir(exist_ok=True)
files=sorted(src.glob('*.jpg')); font=ImageFont.load_default()
for start in range(0,len(files),4):
 batch=files[start:start+4]; sheet=Image.new('RGB',(1080,1160),'#ddd')
 for i,f in enumerate(batch):
  im=Image.open(f).convert('RGB'); im.thumbnail((500,500)); card=Image.new('RGB',(540,580),'white'); card.paste(im,((540-im.width)//2,10)); ImageDraw.Draw(card).text((10,525),f.stem,fill='black',font=font); sheet.paste(card,((i%2)*540,(i//2)*580))
 p=out/f'humor_sexual_acid_contact_{start//4+1}.jpg'; sheet.save(p,quality=92); print(p)

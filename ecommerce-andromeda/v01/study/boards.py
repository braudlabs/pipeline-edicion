from PIL import Image,ImageDraw
from pathlib import Path
p=Path(__file__).resolve().parent.parent
files=sorted((p/'stills').glob('f*.jpg'));board=Image.new('RGB',(5*216,((len(files)+4)//5)*408),'#18232c');d=ImageDraw.Draw(board)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA');guide=Image.new('RGBA',im.size);g=ImageDraw.Draw(guide)
 # Review guide only, never included in the export; scale .5 frames.
 g.rectangle((0,624,540,960),fill=(240,60,60,58));g.rectangle((0,0,540,135),fill=(240,60,60,32));g.rectangle((32,135,508,624),outline=(40,240,160,190),width=1)
 im=Image.alpha_composite(im,guide).convert('RGB');x=i%5*216;y=i//5*408
 board.paste(im.resize((216,384)),(x,y+24));d.text((x+4,y+4),f.stem,fill='white')
board.save(p/'stills/review-meta-board.jpg',quality=94)

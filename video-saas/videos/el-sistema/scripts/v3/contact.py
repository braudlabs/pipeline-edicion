from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];files=sorted((R/'analysis/v3').glob('frame-*.png'),key=lambda p:float(p.stem.split('-')[-1]));W=1920;tw=480;th=300
im=Image.new('RGB',(W,((len(files)+3)//4)*th),'#0C0C0E');d=ImageDraw.Draw(im);f=ImageFont.truetype('/Users/alejandrorubiocamarero/Library/Fonts/SFPRODISPLAYREGULAR.OTF',22)
for i,p in enumerate(files):
 a=Image.open(p).convert('RGB');a.thumbnail((480,270));x=i%4*tw;y=i//4*th;im.paste(a,(x,y));d.text((x+12,y+275),p.stem.replace('frame-','')+' s',font=f,fill='#FF641A')
im.save(R/'output/v3/Contacto-V3.jpg',quality=94)

import sys,subprocess,tempfile
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
slug,a,b,crop,out=sys.argv[1:];a=int(a);b=int(b);x,y,w,h=map(int,crop.split(','))
with tempfile.TemporaryDirectory() as td:
 subprocess.run(['ffmpeg','-v','error','-i',f'analysis/refs/{slug}.mp4','-vf',f"select=between(n\,{a}\,{b}),crop={w}:{h}:{x}:{y}",'-fps_mode','passthrough',f'{td}/%05d.png'],check=True)
 imgs=[Image.open(p).convert('RGB') for p in sorted(Path(td).glob('*.png'))];cols=max(1,min(3,1590//(w+4)));rows=(len(imgs)+cols-1)//cols
 sheet=Image.new('RGB',(cols*(w+4),rows*(h+28)),(24,24,24));d=ImageDraw.Draw(sheet);font=ImageFont.load_default(size=17)
 for k,im in enumerate(imgs):
  xx=k%cols*(w+4);yy=k//cols*(h+28);d.text((xx,yy),f'f{a+k} · {(a+k)/24:.3f}s',fill='yellow',font=font);sheet.paste(im,(xx,yy+24))
 Path(out).parent.mkdir(parents=True,exist_ok=True);sheet.save(out,quality=94)

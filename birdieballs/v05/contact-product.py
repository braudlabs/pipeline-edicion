from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io
p=Path(__file__).parent
sets={'product':[750,756,757,765,775,790,793,794,800,808]}
for name,frames in sets.items():
 w,h=216,384;cols=6;out=Image.new('RGB',(cols*w,((len(frames)+cols-1)//cols)*(h+24)),'#14261c');d=ImageDraw.Draw(out)
 for i,f in enumerate(frames):
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p/'Birdieballs-20s-V05.mp4'),'-vf',f'select=eq(n\\,{f})','-frames:v','1','-f','image2pipe','-c:v','png','-']);im=Image.open(io.BytesIO(raw));x=i%cols*w;y=i//cols*(h+24);out.paste(im.resize((w,h)),(x,y+24));d.text((x+4,y+4),f'f{f} / {f*1001/60000:.3f}s',fill='white')
 out.save(p/'stills'/('final-'+name+'.jpg'),quality=90);print(name,flush=True)

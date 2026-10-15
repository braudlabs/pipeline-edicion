from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io
p=Path(__file__).parent
sets={'sequence':list(range(0,1175,24))+[1174],'hook':list(range(134,160,3))+[165,175,182],'mask':list(range(560,598,3)),'landscape':[905,920,935,938,941,950,960,970,983,984,995,1003]}
for name,frames in sets.items():
 w,h=216,384;cols=6;out=Image.new('RGB',(cols*w,((len(frames)+cols-1)//cols)*(h+24)),'#14261c');d=ImageDraw.Draw(out)
 for i,f in enumerate(frames):
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p/'Birdieballs-20s-V05.mp4'),'-vf',f'select=eq(n\\,{f})','-frames:v','1','-f','image2pipe','-c:v','png','-']);im=Image.open(io.BytesIO(raw));x=i%cols*w;y=i//cols*(h+24);out.paste(im.resize((w,h)),(x,y+24));d.text((x+4,y+4),f'f{f} / {f*1001/60000:.3f}s',fill='white')
 out.save(p/'stills'/('final-'+name+'.jpg'),quality=90);print(name,flush=True)

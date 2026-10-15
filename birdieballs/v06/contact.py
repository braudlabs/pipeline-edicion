from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io
p=Path(__file__).parent
sets={'tail':[round(t*60000/1001) for t in [19.9,20.3,20.85,21.2,21.48,21.92,22.21,22.65,23.4,23.8,24.4,25.2,25.45,25.82,26.35,26.91,27.65,28.4,29.4,30.7,31.4,32.4,33.2,34.2,34.8,35.8,36.4,37.4]],'color':[928,936,938,941,951,970],'closing':[2117,2140,2165,2185,2205,2230,2265,2277]}
for name,frames in sets.items():
 w,h=216,384;cols=6;out=Image.new('RGB',(cols*w,((len(frames)+cols-1)//cols)*(h+24)),'#14261c');d=ImageDraw.Draw(out)
 for i,f in enumerate(frames):
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p/'Birdieballs-completo-V06.mp4'),'-vf',f'select=eq(n\\,{f})','-frames:v','1','-f','image2pipe','-c:v','png','-']);im=Image.open(io.BytesIO(raw));x=i%cols*w;y=i//cols*(h+24);out.paste(im.resize((w,h)),(x,y+24));d.text((x+4,y+4),f'f{f} / {f*1001/60000:.3f}s',fill='white')
 out.save(p/'stills'/('final-'+name+'.jpg'),quality=90);print(name,flush=True)

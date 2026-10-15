from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess
R=Path(__file__).resolve().parents[1]/'references';f=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',18)
for i,start,end in [(1,3.7,6.0),(2,24.5,28.0),(3,29.5,32.5)]:
 times=[start+j*(end-start)/15 for j in range(16)];im=Image.new('RGB',(1472,952),'#111111');d=ImageDraw.Draw(im)
 for j,t in enumerate(times):
  p=R/f'motion-{i}-{j}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(R/f'ref-{i}.mp4'),'-frames:v','1','-vf','scale=368:207',str(p)],check=True)
  im.paste(Image.open(p),(j%4*368,j//4*238));d.text((j%4*368+10,j//4*238+209),f'{t:.2f}s',font=f,fill='white')
 im.save(R/f'motion-study-{i}.jpg')

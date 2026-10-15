from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;s=p/'Birdieballs-completo-V08.mp4';frames=p/'stills/delivery';frames.mkdir(exist_ok=True)
series={'complete':[1.4,1.8,2.8,3.45,4.05,4.62,5.14,6.35,7.84,8.35,9.65,10.93,11.94,12.54,13.48,14.61,15.54,16.43,17.09,18.94,19.24,20.24,21.11,21.59,22.22,22.87,23.81,24.36,25.38,26.43,27.71,28.53,29.66,30.68,31.52,32.41,33.26,34.24,34.86,35.79,36.48,37.37],
'hook-motion':[2.252,2.285,2.318,2.385,2.452,2.552,2.686,2.85,2.969,3.036],
'solution-motion':[9.309,9.342,9.376,9.409,9.476,9.576,9.676,9.91,9.959,9.976],
'inspection-motion':[21.355,21.422,21.489,21.622,21.755,21.889,22.022,22.155,22.289,22.356],
'continuity':[12.6126,12.6293,13.23,13.2466,15.70,15.84,15.884,15.9,25.558,25.575]}
for name,ts in series.items():
 cols=7 if name=='complete' else 5;w=216;h=384;rows=(len(ts)+cols-1)//cols
 out=Image.new('RGB',(w*cols,(h+24)*rows),(18,28,24));d=ImageDraw.Draw(out)
 for i,t in enumerate(ts):
  f=round(t*60000/1001);dest=frames/f'{f:04d}.jpg'
  if not dest.exists():subprocess.run(['ffmpeg','-v','error','-ss',str(f*1001/60000),'-i',str(s),'-frames:v','1','-vf',f'scale={w}:{h}','-y',str(dest)],check=True)
  x=i%cols*w;y=i//cols*(h+24);out.paste(Image.open(dest),(x,y+24));d.text((x+5,y+6),f'{f} / {f*1001/60000:.3f}s',fill='white')
 out.save(p/'stills'/f'final-{name}.jpg',quality=90)
print('Contacts complete')

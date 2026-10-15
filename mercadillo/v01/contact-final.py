from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess
p=Path(__file__).parent
times=[.2,.7,1.3,2.4,3.6,5.8,7.95,8.8,10.3,12.7,14.1,16.8,19,20.3,21.4,23.4,24.7,26.3,27.8,30.6,33.5,34.8,38.9,39.45,40.9,42.7,44.7,48.75,50.85,51.9,54.2,58.85,60.7,62.8,64.5,65.8,68.6,70.4,71.2,73,74.5,76.8,79.1,81.5,83.3,87.6,88.333]
keyFrames=[0,2,6,13,14,15,16,18,24,27,31,37,41,43,45,186,188,190,207,209,211,214,243,246,295,297,299,302,308,312,1395,1397,1399,1402,1405,1412,1418,1419,1778,1780,1782,1785,1788,1793,1795,1934,1944,1950,1952,1955,1959,1962]
frames=sorted(set([round(t*24) for t in times]+keyFrames))
d=p/'stills/native';d.mkdir(exist_ok=True)
select='+'.join(f'eq(n\\,{f})' for f in frames)
subprocess.run(['ffmpeg','-v','error','-i',str(p/'Mercadillo-agencias-V01.mp4'),'-vf',f'select={select},scale=432:768','-fps_mode','vfr','-q:v','2','-y',str(d/'%04d.jpg')],check=True)
lookup=dict(zip(frames,sorted(d.glob('*.jpg'))));assert len(lookup)==len(frames)
sets={f'complete-{page+1}':[round(t*24) for t in times[page*12:page*12+12]] for page in range((len(times)+11)//12)}
sets['motion']=keyFrames
for name,fs in sets.items():
 w,h=216,384;out=Image.new('RGB',(6*w,((len(fs)+5)//6)*(h+24)),'#17252c');draw=ImageDraw.Draw(out)
 for i,f in enumerate(fs):
  x=i%6*w;y=i//6*(h+24);out.paste(Image.open(lookup[f]).resize((w,h)),(x,y+24));draw.text((x+5,y+4),f'f{f} / {f/24:.3f}s',fill='white')
 out.save(p/'stills'/f'final-{name}.jpg',quality=94)
(p/'stills/native-index.json').write_text(json.dumps({str(k):str(v.relative_to(p)) for k,v in lookup.items()},indent=2));print(len(frames),'native delivery frames extracted')

from pathlib import Path
import subprocess,json,math
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];A=R/'analysis/review';A.mkdir(exist_ok=True)
src=R/'output/AD1-Churros-Cocina-FINAL.mp4'
times=[.3,3.9,4.8,6.9,9.3,10.4,11.4,12.6,14.8,16.8,18.4,20.5,21.9,24.3,26.2,29.9,32.4,33.2,34.6,36.4,37.8,39.5,41.1,42.8,44.1,45.,46.4,49.,50.9,52.7,54.5,56.4,57.9,59.8,61.1,62.5,64.2,65.6,67.3,68.3,69.6,70.7]
def extract(t,out,w=360):subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(src),'-frames:v','1','-vf',f'scale={w}:-2',str(out)],check=True)
def sheet(files,name,cols,w=180,h=320,labels=None):
 im=Image.new('RGB',(cols*w,math.ceil(len(files)/cols)*(h+24)),(20,23,21));d=ImageDraw.Draw(im)
 for i,p in enumerate(files):
  x=i%cols*w;y=i//cols*(h+24);img=Image.open(p).resize((w,h));im.paste(img,(x,y));d.text((x+5,y+h+5),(labels or [p.stem for p in files])[i],fill='white')
 im.save(A/name,quality=93)
files=[]
for i,t in enumerate(times):
 p=A/f'frame-{i:02d}-{t}.jpg';extract(t,p);files.append(p)
sheet(files,'revision-completa.jpg',6,labels=[f'{t:.2f}s' for t in times])
T=json.load(open(R/'src/timeline.json'));start=T['events']['accounts']['from']
for label,frames in [('giro-cuentas',range(62,103,2)),('entrada-subtitulo',range(604,616))]:
 folder=A/label;folder.mkdir(exist_ok=True);files=[]
 for f in frames:
  t=(start+f if label=='giro-cuentas' else f)/48;p=folder/f'{f:04d}.jpg';extract(t,p,270);files.append(p)
 sheet(files,label+'.jpg',7,labels=[f'{f} / 48' for f in frames])
print('Review sheets ready')

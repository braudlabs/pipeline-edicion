from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json
p=Path(__file__).resolve().parent.parent;d=p/'study/final-frames';d.mkdir(exist_ok=True)
seq=[('Contorno / relleno: Andromeda',[114,116,118,120,122,124,126,128],(0,460,540,630)),('Relleno detras del cuerpo: mierda',[420,422,424,426,428,430,432,434],(0,470,540,630)),('Narracion recuperada: sudadera',[1384,1386,1388,1390,1392,1394,1396,1398],(0,290,540,450))]
fs=sorted({f for _,frames,_ in seq for f in frames});expr='+'.join('eq(n\\,%d)'%f for f in fs)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'Andromeda-00-38s-V03-PREVIEW.mp4'),'-vf',f'select={expr},scale=540:960','-fps_mode','passthrough',str(d/'phase-%03d.jpg')],check=True)
lookup={f:d/f'phase-{i+1:03d}.jpg' for i,f in enumerate(fs)};b=Image.new('RGB',(1600,3*220),'#172028');draw=ImageDraw.Draw(b)
for row,(name,frames,crop) in enumerate(seq):
 draw.text((8,row*220+10),name,fill='white')
 for col,f in enumerate(frames):
  im=Image.open(lookup[f]).crop(crop);im=im.resize((198,round(im.height*198/im.width)));x=col*200;y=row*220+52;b.paste(im,(x,y));draw.text((x+6,y+im.height+10),f'{f/48:.3f}s',fill='white')
b.save(p/'study/animation-phases.jpg')
fs=[62,120,199,238,370,461,502,540,586,614,677,727,763,811,859,936,1085,1193,1277,1354,1430,1534,1656,1723,1771,1826];expr='+'.join('eq(n\\,%d)'%f for f in fs)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'Andromeda-00-38s-V03-PREVIEW.mp4'),'-vf',f'select={expr},scale=270:480','-fps_mode','passthrough',str(d/'full-%02d.jpg')],check=True)
b=Image.new('RGB',(1620,5*510),'#172028');draw=ImageDraw.Draw(b)
for i,f in enumerate(fs):
 x=i%6*270;y=i//6*510;b.paste(Image.open(d/f'full-{i+1:02}.jpg'),(x,y+25));draw.text((x+8,y+7),f'{f/48:.2f}s',fill='white')
b.save(p/'study/final-review.jpg')

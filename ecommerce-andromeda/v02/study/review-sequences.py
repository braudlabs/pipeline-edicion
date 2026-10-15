from pathlib import Path
from PIL import Image,ImageDraw
import subprocess
p=Path(__file__).resolve().parent.parent;d=p/'study/phases';d.mkdir(exist_ok=True)
seq=[('Ecommerce / revelado',[26,27,28,29,31,36],(0,470,540,625)),('Andromeda / lateral',[57,58,59,60,63,67],(0,470,540,625)),('Mierda / impacto',[210,211,212,213,216,219],(0,480,540,630)),('Dias / relevo vertical',[262,263,264,265,267,270],(0,460,540,640))]
frames=sorted(set(f for _,fs,_ in seq for f in fs));sel='+'.join('eq(n\\,%d)'%f for f in frames)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'Andromeda-00-38s-V02-PREVIEW.mp4'),'-vf','select='+sel+',scale=540:960','-fps_mode','passthrough',str(d/'%03d.jpg')],check=True)
files={f:d/f'{i+1:03d}.jpg' for i,f in enumerate(frames)}
b=Image.new('RGB',(1440,4*235),'#172128');draw=ImageDraw.Draw(b)
for row,(name,fs,crop) in enumerate(seq):
 draw.text((12,row*235+10),name,fill='white')
 for col,f in enumerate(fs):
  im=Image.open(files[f]).crop(crop);im=im.resize((238,round(im.height*238/im.width)))
  x=col*240;y=row*235+55;b.paste(im,(x,y));draw.text((x+8,y+im.height+12),f'f{f} / {f/24:.3f}s',fill='white')
b.save(p/'study/animation-phases.jpg')
# Full final-video board (not stale pre-render stills)
frames=[31,60,119,185,230,270,406,542,596,638,767,886];sel='+'.join('eq(n\\,%d)'%f for f in frames)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'Andromeda-00-38s-V02-PREVIEW.mp4'),'-vf','select='+sel+',scale=270:480','-fps_mode','passthrough',str(d/'full-%02d.jpg')],check=True)
b=Image.new('RGB',(1080,3*510),'#172128');draw=ImageDraw.Draw(b)
for i,f in enumerate(frames):
 x=i%4*270;y=i//4*510;b.paste(Image.open(d/f'full-{i+1:02d}.jpg'),(x,y+25));draw.text((x+8,y+6),f'{f/24:.2f}s',fill='white')
b.save(p/'study/final-review.jpg')

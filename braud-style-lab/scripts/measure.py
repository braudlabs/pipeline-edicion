from PIL import Image,ImageFilter,ImageDraw
import numpy as np,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def comps(mask):
 ys,xs=np.where(mask);todo=set(zip(xs.tolist(),ys.tolist()));out=[]
 while todo:
  p=todo.pop();q=[p];cc=[p]
  while q:
   x,y=q.pop()
   for d in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
    if d in todo:todo.remove(d);q.append(d);cc.append(d)
  if len(cc)>=3:
   a=np.array(cc);out.append({'x':float(a[:,0].mean()),'y':float(a[:,1].mean()),'area':len(cc),'bbox':[int(a[:,0].min()),int(a[:,1].min()),int(a[:,0].max()+1),int(a[:,1].max()+1)]})
 return out
out={}
for f in [387,390,393,396,399,402,405,408,411,414,417,420,423,426,429,432,438,444,449]:
 a=np.array(Image.open(R/'reference/motion'/f'{f-335:03d}.jpg'))
 mask=(a[:,:,0]>160)&(a[:,:,2]>132)
 er=np.array(Image.fromarray((mask*255).astype('uint8')).filter(ImageFilter.MinFilter(5)))>0
 cc=comps(er);dots=[p for p in cc if 3<=p['area']<=240 and ((p['x']-550)**2+(p['y']-932)**2)>270**2]
 out[f]={'dots':dots,'glyphs':[p for p in cc if p['area']>240]}
 if f==405:
  dots.sort(key=lambda p:math.atan2(p['y']-950,p['x']-540));print('dots',len(dots));print(json.dumps(dots,indent=1))
  im=Image.open(R/'reference/motion'/f'{f-335:03d}.jpg');d=ImageDraw.Draw(im)
  for i,p in enumerate(dots):d.text((p['x']+8,p['y']),str(i),fill='red')
  im.save(R/'analysis/dots-measured.jpg')
(R/'analysis/landmarks.json').write_text(json.dumps(out,indent=2))

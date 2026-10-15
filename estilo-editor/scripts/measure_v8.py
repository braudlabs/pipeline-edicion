#!/usr/bin/env python3
"""Native chroma bounds with threshold sensitivity. NOT recovered alpha/fontSize."""
import json,sys
from pathlib import Path
import numpy as np
from sheet import load_full_run
from common import probe,DATOS
out=DATOS/'revision-v2';info=probe('v8');result=[]
for name,a,b,roi in [('pagar',549,619,(.05,.44,.9,.27)),('Braudd',1652,1725,(.04,.15,.92,.23)),('sirve',3328,3361,(.015,.42,.97,.32))]:
 rows=[];x,y,w,h=roi;X,Y=int(x*1080),int(y*1920)
 for f,img in enumerate(load_full_run('v8',a,b-a+1,info),a):
  im=np.array(img)[Y:int((y+h)*1920),X:int((x+w)*1080)].astype(float);r,g,bl=im.transpose(2,0,1)
  bounds=[]
  for c in [15,30]:
   mask=(g-r>c)&(r-bl>c)&(r>85)&(g>125)
   iy,ix=np.nonzero(mask)
   if len(ix)<25:bounds.append(None);continue
   x0,x1=np.quantile(ix,[.002,.998]);y0,y1=np.quantile(iy,[.002,.998]);bounds.append(dict(x=round(X+x0,2),y=round(Y+y0,2),width=round(x1-x0+1,2),height=round(y1-y0+1,2),cx=round(X+(x0+x1)/2,2),cy=round(Y+(y0+y1)/2,2),pixelCount=len(ix),medianRGB=[round(float(v),1) for v in np.median(im[mask],axis=0)]))
  rows.append(dict(frame=f,threshold15=bounds[0],threshold30=bounds[1]))
 result.append(dict(id=name,slug='v8',range=[a,b],roi=roi,method='Native RGB chroma selection: G-R>c, R-B>c, R>85,G>125; 0.2–99.8 percentile bounds. Thresholds c15/c30.',status='measurement_candidate_requires_mask_review',warnings=['Threshold-dependent ink bounds; not fontSize or source alpha.','Changing compression/background can contaminate bounds.','ROI can clip entry/overshoot.'],rows=rows))
(out/'v8-native-curves.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
for item in result:
 print(item['id'],[(r['frame'],r['threshold30'] and (r['threshold30']['cy'],r['threshold30']['width'],r['threshold30']['height'])) for r in item['rows']][::3])

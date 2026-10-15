#!/usr/bin/env python3
"""Multiple-word shape calibration on unobscured lime hero letters."""
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from common import DATOS,ROOT,probe
from sheet import load_full
from fontfit import fit,CANDIDATES,THIN
out=DATOS/'revision-v2';info=probe('v8');result=[];tiles=[]
for text,frame,roi in [('pagar',590,(110,960,970,1270)),('Braudd',1679,(120,390,960,650))]:
 im=np.asarray(load_full('v8',frame,info),np.int16);x0,y0,x1,y1=roi;im=im[y0:y1,x0:x1];r,g,b=im.transpose(2,0,1)
 m=(g-r>30)&(r-b>30)&(r>85)&(g>125);ys,xs=np.nonzero(m);target=m[ys.min():ys.max()+1,xs.min():xs.max()+1]
 candidates=[]
 for name,path,index,var in THIN+CANDIDATES:
  try:score,data=fit(text,target,path,index,var)
  except Exception:continue
  candidates.append({'font':name,'path':path,'index':index,'iou':score,'size':data['size'],'trackingPx':data['tracking_px'],'trackingPerThousand':data['tracking_milesimas'],'inkWidth':data['w'],'inkHeight':data['h'],'A':data['A'],'B':data['B']})
 candidates.sort(key=lambda x:x['iou'],reverse=True)
 for c in candidates[:3]:
  rgb=np.zeros(c['A'].shape+(3,),np.uint8);rgb[:,:,0]=c['A']*255;rgb[:,:,1]=c['B']*255
  ink=Image.fromarray(rgb);canvas=Image.new('RGB',(max(ink.width,900),ink.height+38),'#182520');canvas.paste(ink,(0,38));ImageDraw.Draw(canvas).text((8,7),f'{text} f{frame} | {c["font"]} | IoU {c["iou"]:.3f} | size {c["size"]} | tracking {c["trackingPx"]:.2f}px',fill='white',font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18));tiles.append(canvas)
 result.append({'text':text,'frame':frame,'roi':roi,'inkSize':[target.shape[1],target.shape[0]],'candidates':[{k:v for k,v in c.items() if k not in ['A','B']} for c in candidates]})
 print(text,[(c['font'],round(c['iou'],3),c['size'],round(c['trackingPx'],2)) for c in candidates[:4]],flush=True)
sheet=Image.new('RGB',(max(im.width for im in tiles),sum(im.height+6 for im in tiles)),'#182520');y=0
for im in tiles:sheet.paste(im,(0,y));y+=im.height+6
sheet.save(ROOT/'analysis/revision-v2/v8/font-calibration.jpg',quality=93)
(out/'v8-font-calibration.json').write_text(json.dumps({'status':'candidate_shape_fits_not_exact_font_identification','method':'Cropped native lime chroma mask; FreeType candidate renders; height search ±4%, tracking fitted to width; IoU on centered ink. Red reference, green candidate, yellow overlap. Native subjects may occlude Braudd, inspect before trusting.','words':result},ensure_ascii=False,indent=2))

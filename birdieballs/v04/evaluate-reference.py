#!/usr/bin/env python3
"""Native decoded reference versus actual Remotion glyph render (calibration test)."""
import json,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np
root=Path(__file__).resolve().parents[2];out=Path(__file__).parent/'reference-test'
manifest=json.loads((root/'estilo-editor/datos/referencias.json').read_text());source=next(x for x in manifest['files'] if x['slug']=='v8')
ages=[2,6,16,26,40,59];roi=(100,890,1000,1320);rows=[];panels=[]
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18)
def mask(im):
 a=np.array(im).astype(np.int16);r,g,b=a[:,:,:3].transpose(2,0,1);return(g-r>30)&(r-b>30)&(r>85)&(g>125)
def bounds(m):
 y,x=np.nonzero(m);return np.array([np.quantile(x,.002),np.quantile(y,.002),np.quantile(x,.998)-np.quantile(x,.002)+1,np.quantile(y,.998)-np.quantile(y,.002)+1])
with tempfile.TemporaryDirectory() as td:
 select='+'.join(f'eq(n\\,{550+a})' for a in ages)
 subprocess.run(['ffmpeg','-v','error','-i',source['available_at'],'-vf','select='+select,'-fps_mode','passthrough','-start_number','0',td+'/%02d.png'],check=True)
 for i,age in enumerate(ages):
  a=Image.open(Path(td)/f'{i:02d}.png').convert('RGB').crop(roi);b=Image.open(out/f'f{age}.png').convert('RGB').crop(roi)
  ma,mb=mask(a),mask(b);ba,bb=bounds(ma),bounds(mb);iou=np.logical_and(ma,mb).sum()/np.logical_or(ma,mb).sum()
  rows.append({'ageSourceFrames':age,'referenceFrame':550+age,'referenceBoundsInROI':ba.tolist(),'renderBoundsInROI':bb.tolist(),'errorXYWHpx':(bb-ba).tolist(),'inkIoU':float(iou)})
  if age in [6,16,40]:
   overlay=np.zeros(ma.shape+(3,),np.uint8);overlay[:,:,0]=ma*255;overlay[:,:,1]=mb*255
   row=Image.new('RGB',(1350,270),'#13221b');d=ImageDraw.Draw(row)
   for j,(img,title) in enumerate([(a,f'Referencia f{550+age}'),(b,f'Reconstrucción edad{age}'),(Image.fromarray(overlay),f'Superposición IoU{iou:.3f}')]):
    d.text((j*450+8,6),title,font=font,fill='white');row.paste(img.resize((450,215)),(j*450,40))
   panels.append(row)
data={'status':'render_calibration_not_cross_video_validation','sourceSha256':source['sha256'],'component':'ReferenceTest in Film.tsx; SFPro Display Regular409px tracking−29.36px, baseline1184, anchor517; measured position fit','rows':rows,'maxAbsPositionErrorPx':max(abs(v) for r in rows for v in r['errorXYWHpx'][:2]),'meanInkIoU':float(np.mean([r['inkIoU'] for r in rows])),'limits':['Six frames calibrate this reconstruction only.','Lime mask threshold is not original alpha.','Ink-height difference is1–4px in five frames and10px at age16; overlays in source may alter lime mask. This test reconstructs the main word only, not the small support layers.','Birdieballs serif, spacing and amplitudes are design adaptations, not replicas of pagar.']}
(out/'comparison.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));sheet=Image.new('RGB',(1350,len(panels)*270))
for i,p in enumerate(panels):sheet.paste(p,(0,i*270))
sheet.save(out/'comparison.jpg',quality=95)
print(json.dumps({k:data[k] for k in ['maxAbsPositionErrorPx','meanInkIoU','rows']},ensure_ascii=False))

from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
R=Path(__file__).resolve().parents[1]
a=np.array(Image.open(R/'reference/motion/109.jpg'));sel=(a[806:1015,130:975,0]>165)&(a[806:1015,130:975,2]>150)
y,x=np.where(sel);target=Image.fromarray((sel[min(y):max(y)+1,min(x):max(x)+1]*255).astype('uint8'));TW,TH=target.size
candidates=[('SFProDisplay-Bold',str(R.parent/'ad1-reedit/assets/Display-Bold.otf'),0),('HelveticaNeue-Bold','/System/Library/Fonts/HelveticaNeue.ttc',1),('HelveticaNeue-CondensedBlack','/System/Library/Fonts/HelveticaNeue.ttc',9),('HelveticaNeue-CondensedBold','/System/Library/Fonts/HelveticaNeue.ttc',4),('Arial-Black','/System/Library/Fonts/Supplemental/Arial Black.ttf',0),('Arial-BoldMT','/System/Library/Fonts/Supplemental/Arial Bold.ttf',0)]
res=[]
for name,p,idx in candidates:
 f=ImageFont.truetype(p,280,index=idx);best=None
 for track in range(-110,6,5):
  out=Image.new('L',(2000,500));d=ImageDraw.Draw(out);xp=70
  for c in 'mínimo':d.text((xp,330),c,font=f,fill=255,anchor='ls');xp+=f.getlength(c)+track*.28
  b=out.getbbox();cut=out.crop(b);fit=cut.resize((TW,TH),Image.Resampling.LANCZOS);X=np.array(fit)>150;Y=np.array(target)>150;iou=(X&Y).sum()/(X|Y).sum()
  if best is None or iou>best['iou']:best={'font':name,'iou':round(float(iou),5),'tracking':track,'sizeFromHeight':280*TH/cut.height,'widthScale':TW/(cut.width*TH/cut.height)};fit.save(R/'analysis'/f'font-{name}.png')
 res.append(best)
res.sort(key=lambda v:-v['iou']);(R/'analysis/font-fit.json').write_text(json.dumps({'referenceBBox':[130+int(min(x)),806+int(min(y)),TW,TH],'results':res},indent=2));print(json.dumps(res,indent=2))
sheet=Image.new('RGB',(900,8*150),'#161b13');d=ImageDraw.Draw(sheet)
for j,n in enumerate(['REFERENCE']+[r['font'] for r in res]):
 im=target if n=='REFERENCE' else Image.open(R/'analysis'/f'font-{n}.png');im.thumbnail((790,120));sheet.paste(im,(55,j*150+24));d.text((15,j*150+4),n,fill='white')
sheet.save(R/'analysis/font-study.jpg',quality=96)

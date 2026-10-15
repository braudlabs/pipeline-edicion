from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path('braud-style-lab');out={}
# Search follows measured word region, away from the radial diagram and small lead-in.
starts={418:1350,419:1280,420:1210,421:1160,422:1120,423:1080,424:1040,425:1010,426:985,427:955,428:935,429:915,430:900,431:881,432:865,433:852,434:840,435:830,436:816,437:805,438:795,439:786,440:780,441:772,442:770,443:769,444:765,445:763,446:761,447:759,448:757,449:755}
for f,yst in starts.items():
 a=np.array(Image.open(R/'reference/motion'/f'{f-335:03d}.jpg'));m=(a[:,:,0]>(130 if f<420 else 165))&(a[:,:,2]>(100 if f<420 else 150));rows=m.sum(axis=1); rr=np.where((rows>160)&(np.arange(1920)>yst))[0]
 if not len(rr):print('MISSING',f);continue
 # longest high-ink row run is the large word body, minus detached diacritics.
 groups=np.split(rr,np.where(np.diff(rr)>1)[0]+1);g=max(groups,key=len);y0,y1=int(g[0]),int(g[-1]);ys,xs=np.where(m[y0:y1+1]);box=[int(min(xs)),y0,int(max(xs)+1),y1+1];out[f]={'bodyBBox':box,'width':box[2]-box[0],'baseline':box[3],'centerX':(box[0]+box[2])/2}
print(json.dumps(out,indent=1));(R/'analysis/minimo-motion.json').write_text(json.dumps(out,indent=2))

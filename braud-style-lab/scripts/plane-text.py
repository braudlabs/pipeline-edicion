from pathlib import Path
import numpy as np,json,math
R=Path('braud-style-lab');data=json.load(open(R/'analysis/camera-tracked.json'));out={}
for fs,v in data.items():
 f=int(fs);H=np.array(v['H']);a=-math.radians(1.2*(f-405));rz=np.array([[math.cos(a),-math.sin(a),0],[math.sin(a),math.cos(a),0],[0,0,1]]);H=H@rz
 F=718.1063;B=np.linalg.inv(np.array([[F,0,540],[0,F,960],[0,0,1]]))@H;s=2/(np.linalg.norm(B[:,0])+np.linalg.norm(B[:,1]));r=np.column_stack([B[:,0]*s,B[:,1]*s,np.cross(B[:,0]*s,B[:,1]*s)]);ang=np.degrees([math.atan2(r[2,1],r[2,2]),math.asin(max(-1,min(1,-r[2,0]))),math.atan2(r[1,0],r[0,0])]);out[f]={'angles':ang.tolist(),'t':v['t'],'H':H.tolist()}
 if f%3==0:print(f,np.round(ang,2))
 if f in [420,426,432,438]:
  from PIL import Image
  # Rectify reference into its scene plane; all coordinates of persistent text should now agree.
  T=np.array([[1,0,-450],[0,1,300],[0,0,1]]);G=H@T;G/=G[2,2];im=Image.open(R/'reference/motion'/f'{f-335:03d}.jpg');im.transform((1100,600),Image.Transform.PERSPECTIVE,G.flatten()[:8],Image.Resampling.BICUBIC).save(R/'analysis'/f'text-plane-{f}.png')
(R/'analysis/plane-motion.json').write_text(json.dumps(out,indent=2))

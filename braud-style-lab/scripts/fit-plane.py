from pathlib import Path
import json,numpy as np,math
R=Path(__file__).resolve().parents[1]
d=json.load(open(R/'analysis/landmarks.json'))['405']['dots'];d.sort(key=lambda p:math.atan2(p['y']-950,p['x']-540));A=[]
for i,p in enumerate(d):
 a=math.pi+i*math.tau/30;x,y=400*math.cos(a),400*math.sin(a);u,v=p['x'],p['y'];A += [[-x,-y,-1,0,0,0,u*x,u*y,u],[0,0,0,-x,-y,-1,v*x,v*y,v]]
_,_,vt=np.linalg.svd(A);H=vt[-1].reshape(3,3);H/=H[2,2];print('H',H)
a=H[:,0];b=H[:,1];cx,cy=540,960;au=a[:2]-np.array([cx,cy])*a[2];bu=b[:2]-np.array([cx,cy])*b[2]
f1=-np.dot(au,bu)/(a[2]*b[2]);f2=-(np.dot(au,au)-np.dot(bu,bu))/(a[2]**2-b[2]**2);print('f1/2',f1,f2,math.sqrt(abs(f1)),math.sqrt(abs(f2)))
f=math.sqrt(abs((f1+f2)/2));K=np.array([[f,0,cx],[0,f,cy],[0,0,1]]);B=np.linalg.inv(K)@H;s=2/(np.linalg.norm(B[:,0])+np.linalg.norm(B[:,1]));rot=np.column_stack([B[:,0]*s,B[:,1]*s,np.cross(B[:,0]*s,B[:,1]*s)]);print('f',f,'rot',rot,'t',B[:,2]*s)
# AE rotations Rx then Ry then Rz, R=Rz Ry Rx
ry=math.asin(-rot[2,0]);rx=math.atan2(rot[2,1],rot[2,2]);rz=math.atan2(rot[1,0],rot[0,0]);print('Euler',np.degrees([rx,ry,rz]))
(R/'analysis/plane-fit.json').write_text(json.dumps({'homography':H.tolist(),'focal':f,'euler':np.degrees([rx,ry,rz]).tolist(),'translation':(B[:,2]*s).tolist()},indent=2))

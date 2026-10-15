from pathlib import Path
import numpy as np,math,json
R=Path('braud-style-lab');F=718.1063;rx,ry,rz=np.radians([-3,-1,0]);RX=np.array([[1,0,0],[0,math.cos(rx),-math.sin(rx)],[0,math.sin(rx),math.cos(rx)]]);RY=np.array([[math.cos(ry),0,math.sin(ry)],[0,1,0],[-math.sin(ry),0,math.cos(ry)]]);ROT=RY@RX
A=[];b=[]
for i,(u,v) in zip([18,17,16,15,14],[[98,366],[263,333],[414,274],[545,187],[647,82]]):
 a=math.radians(180+12*i+1.2*(444-405));xyz=ROT@np.array([400*math.cos(a),400*math.sin(a),0]);x,y,z=xyz
 A.extend([[F,0,-(u-540)],[0,F,-(v-960)]]);b.extend([(u-540)*z-F*x,(v-960)*z-F*y])
t=np.linalg.lstsq(A,b,rcond=None)[0];print(t);(R/'analysis/end-pose.json').write_text(json.dumps({'angles':[-3,-1,0],'t':t.tolist()}))
for i in [18,17,16,15,14]:
 a=math.radians(180+12*i+1.2*(444-405));p=ROT@np.array([400*math.cos(a),400*math.sin(a),0])+t;print(i,[540+F*p[0]/p[2],960+F*p[1]/p[2]])

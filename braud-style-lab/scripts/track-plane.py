exec(open('braud-style-lab/scripts/measure.py').read().split('out={}')[0])
def fit(src,dst):
 A=[]
 for (x,y),(u,v) in zip(src,dst):A += [[-x,-y,-1,0,0,0,u*x,u*y,u],[0,0,0,-x,-y,-1,v*x,v*y,v]]
 _,_,vt=np.linalg.svd(A);H=vt[-1].reshape(3,3);return H/H[2,2]
def proj(H,p):
 a=np.column_stack([p,np.ones(len(p))])@H.T;return a[:,:2]/a[:,2:]
def decomp(H):
 f=718.1063;K=np.array([[f,0,540],[0,f,960],[0,0,1]]);B=np.linalg.inv(K)@H;s=2/(np.linalg.norm(B[:,0])+np.linalg.norm(B[:,1]));rot=np.column_stack([B[:,0]*s,B[:,1]*s,np.cross(B[:,0]*s,B[:,1]*s)]);ry=math.asin(max(-1,min(1,-rot[2,0])));rx=math.atan2(rot[2,1],rot[2,2]);rz=math.atan2(rot[1,0],rot[0,0]);return np.degrees([rx,ry,rz]).tolist(),(B[:,2]*s).tolist()
pts=np.array([[400*math.cos(math.pi+i*math.tau/30),400*math.sin(math.pi+i*math.tau/30)] for i in range(30)])
H=np.array(json.load(open(R/'analysis/plane-fit.json'))['homography']);out={405:{'H':H.tolist(),'angles':decomp(H)[0],'t':decomp(H)[1]}};lastH=H.copy();prevH=H.copy()
# Process one frame at a time so nearest predicted correspondence stays valid.
for f in range(406,450):
 a=np.array(Image.open(R/'reference/motion'/f'{f-335:03d}.jpg'));mask=(a[:,:,0]>145)&(a[:,:,2]>125);er=np.array(Image.fromarray((mask*255).astype('uint8')).filter(ImageFilter.MinFilter(7)))>0
 cc=comps(er);cc=[p for p in cc if 8<=p['area']<=2200 and .3<(p['bbox'][2]-p['bbox'][0])/(p['bbox'][3]-p['bbox'][1])<3 and (p['y']<850 if f>419 else True)]
 pred=proj(lastH,pts)+(proj(lastH,pts)-proj(prevH,pts));src=[];dst=[];used=set()
 for i,(x,y) in enumerate(pred):
  if not(-30<x<1110 and -30<y<1950) or not cc:continue
  ds=[math.hypot(x-p['x'],y-p['y']) if j not in used else 1e6 for j,p in enumerate(cc)];k=int(np.argmin(ds))
  if ds[k]<45:src.append(pts[i]);dst.append([cc[k]['x'],cc[k]['y']]);used.add(k)
 if len(src)>=5:
  H=fit(np.array(src),np.array(dst));err=np.sqrt(np.mean((proj(H,np.array(src))-dst)**2));angles,t=decomp(H);out[f]={'H':H.tolist(),'angles':angles,'t':t,'rmse':err,'n':len(src)};prevH=lastH;lastH=H
 else:print('LOST',f,len(src));break
for f,v in out.items():
 if f%3==0 or f==449:print(f,'n',v.get('n'), 'rmse',round(v.get('rmse',0),2),'r',np.round(v['angles'],2),'t',np.round(v['t'],2))
(R/'analysis/camera-tracked.json').write_text(json.dumps(out,indent=2))

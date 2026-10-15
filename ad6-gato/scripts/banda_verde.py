import subprocess, numpy as np, json
SRC="/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-22-croche-gato/entrega/05-producto.mp4"
W,H=269,482; S=4  # scale back to 1076x1928
raw=subprocess.run(["ffmpeg","-v","error","-i",SRC,"-vf",f"scale={W}:{H}","-pix_fmt","rgb24","-f","rawvideo","-"],capture_output=True).stdout
a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,H,W,3).astype(np.int16)
res=[]
for i in range(a.shape[0]):
    f=a[i]; r,g,b=f[...,0],f[...,1],f[...,2]
    mustard=(r-g>40)&(g-b>35)&(r>70)
    sage=(r-g<26)&(b>24)&(g-b>18)&(r>55)&(r<200)
    for m in (mustard,sage):
        m[:int(H*0.28),:]=False; m[int(H*0.80):,:]=False
    # pouch x-extent from mustard rows that have many pixels
    ys,xs=np.nonzero(mustard)
    px0,px1=(np.percentile(xs,0.5),np.percentile(xs,99.5)) if len(xs)>200 else (0,W)
    sage[:, :int(px0)]=False; sage[:, int(px1)+1:]=False
    rows=sage.sum(axis=1); thr=max(rows.max()*0.45,6)
    good=np.nonzero(rows>thr)[0]
    if len(good)==0: res.append(None); continue
    y0,y1=int(good.min()),int(good.max())
    cols=sage[y0:y1+1].sum(axis=0); cthr=max(cols.max()*0.45,3)
    gc=np.nonzero(cols>cthr)[0]; x0,x1=int(gc.min()),int(gc.max())
    res.append(dict(f=i,t=round(i/24,4),x0=x0*S,x1=(x1+1)*S,y0=y0*S,y1=(y1+1)*S,
                    w=(x1+1-x0)*S,h=(y1+1-y0)*S,cx=round((x0+x1+1)/2*S,1),cy=round((y0+y1+1)/2*S,1),
                    px0=int(px0)*S,px1=int(px1)*S))
for i in range(0,121,10):
    d=res[i]; print("f%3d t=%5.3f  BANDA x %4d-%4d (w %3d, cx %6.1f)  y %4d-%4d (h %3d, cy %6.1f)   bolsa x %4d-%4d"%(
        d['f'],d['t'],d['x0'],d['x1'],d['w'],d['cx'],d['y0'],d['y1'],d['h'],d['cy'],d['px0'],d['px1']))
d0,d1=res[0],res[120]
print("\nescala banda w: %.3f  h: %.3f  (f0->f120)"%(d1['w']/d0['w'], d1['h']/d0['h']))
json.dump(res,open("/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/ad6-gato/analysis/banda-verde.json","w"),indent=0)

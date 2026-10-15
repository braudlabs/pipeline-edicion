"""Pista de la banda verde en coordenadas del MONTAJE RENDERIZADO (1080x1920)."""
import subprocess, numpy as np, json
MOV="/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/ad6-gato/output/ad6-montaje-base.mov"
F0,N=291,96           # plano E
W,H=270,480; S=4.0    # 1/4 de 1080x1920
raw=subprocess.run(["ffmpeg","-v","error","-i",MOV,"-vf",
    f"trim=start_frame={F0}:end_frame={F0+N},scale={W}:{H}","-fps_mode","passthrough",
    "-pix_fmt","rgb24","-f","rawvideo","-"],capture_output=True).stdout
a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,H,W,3).astype(np.int16)
print("fotogramas leidos:",a.shape[0])
res=[]
for i in range(a.shape[0]):
    f=a[i]; r,g,b=f[...,0],f[...,1],f[...,2]
    mustard=(r-g>40)&(g-b>35)&(r>70); mustard[:int(H*.25)]=False; mustard[int(H*.72):]=False
    ys,xs=np.nonzero(mustard)
    # silueta de la bolsa por fila
    px0,px1=np.percentile(xs,0.3),np.percentile(xs,99.7)
    sage=(r-g<26)&(b>24)&(g-b>18)&(r>55)&(r<205)
    sage[:int(H*.25)]=False; sage[int(H*.72):]=False
    sage[:,:int(px0)]=False; sage[:,int(px1)+1:]=False
    rows=sage.sum(axis=1); thr=max(rows.max()*0.5,5)
    good=np.nonzero(rows>thr)[0]; y0,y1=int(good.min()),int(good.max())
    # ancho de la banda: filas del centro de la banda, columnas con sage continuo
    mid=sage[(y0+y1)//2-1:(y0+y1)//2+2].sum(axis=0)
    gc=np.nonzero(mid>=2)[0]
    x0,x1=int(gc.min()),int(gc.max())
    res.append(dict(tl=F0+i, t=round((F0+i)/24,4),
        x0=round(x0*S,1), x1=round((x1+1)*S,1), y0=round(y0*S,1), y1=round((y1+1)*S,1),
        cx=round((x0+x1+1)/2*S,1), cy=round((y0+y1+1)/2*S,1),
        w=round((x1+1-x0)*S,1), h=round((y1+1-y0)*S,1)))
for i in range(0,N,8):
    d=res[i]; print("tl f%3d t=%6.3f  banda x %5.0f-%5.0f (w %5.0f) y %5.0f-%5.0f (h %4.0f)  centro (%5.0f,%5.0f)"%(
        d['tl'],d['t'],d['x0'],d['x1'],d['w'],d['y0'],d['y1'],d['h'],d['cx'],d['cy']))
d=res[-1]; print("tl f%3d t=%6.3f  banda x %5.0f-%5.0f (w %5.0f) y %5.0f-%5.0f (h %4.0f)  centro (%5.0f,%5.0f)"%(
    d['tl'],d['t'],d['x0'],d['x1'],d['w'],d['y0'],d['y1'],d['h'],d['cx'],d['cy']))
print("\nescala de la banda a lo largo del plano E: w x%.3f  h x%.3f"%(res[-1]['w']/res[0]['w'],res[-1]['h']/res[0]['h']))
json.dump(res,open("/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/ad6-gato/analysis/pista-banda-montaje.json","w"),indent=0)

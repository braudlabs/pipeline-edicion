import subprocess, sys, numpy as np, json, os
SRC="/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-22-croche-gato/entrega"
W=134; H=240
out={}
for n in ["01-dormido","02-bolsa","03-carrera","04-cuenco","05-producto"]:
    raw=subprocess.run(["ffmpeg","-v","error","-i",f"{SRC}/{n}.mp4","-vf",f"scale={W}:{H}",
        "-pix_fmt","gray","-f","rawvideo","-"],capture_output=True).stdout
    a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,H,W).astype(np.float32)
    nf=a.shape[0]
    d=np.abs(np.diff(a,axis=0)).mean(axis=(1,2))
    out[n]={"frames":nf,"diff":[round(float(x),3) for x in d]}
    print(f"=== {n}  {nf} frames ===")
    # print per-frame diff with frame index and time
    peak=float(d.max()); 
    for i,v in enumerate(d):
        t=(i+1)/24.0
        bar="#"*int(v/peak*50)
        print(f"  f{i+1:3d} t={t:5.3f}  {v:6.2f} {bar}")
json.dump(out,open("/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/ad6-gato/analysis/motion.json","w"))

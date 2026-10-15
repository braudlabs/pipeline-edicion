import subprocess, numpy as np
SRC="/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-22-croche-gato/entrega/03-carrera.mp4"
W,H=134,240
raw=subprocess.run(["ffmpeg","-v","error","-i",SRC,"-vf",f"scale={W}:{H}","-pix_fmt","gray","-f","rawvideo","-"],capture_output=True).stdout
a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,H,W).astype(np.float32)
# candidate OUT frame (last frame shown) in 40..70 ; candidate IN frame in 60..80
best=[]
for o in range(40,75):
    for i in range(o+1,82):
        d=np.abs(a[o+1]-a[i]).mean()   # continuity: frame after out vs the in-frame
        best.append((d,o,i,(i-o-1)/24.0))
best.sort()
print("mejores empalmes ocultos (out=ultimo fotograma mostrado, in=primero del siguiente trozo):")
for d,o,i,sk in best[:15]:
    print("  out f%3d (t=%5.3f) -> in f%3d (t=%5.3f)  salta %5.3fs  dif=%.3f"%(o,o/24,i,i/24,sk,d))
print()
print("referencia: dif media entre fotogramas consecutivos en la zona muerta:",
      round(float(np.abs(np.diff(a[50:75],axis=0)).mean()),3))

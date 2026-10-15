import subprocess, numpy as np
SRC="/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-22-croche-gato/entrega/05-producto.mp4"
W,H=269,482
raw=subprocess.run(["ffmpeg","-v","error","-i",SRC,"-vf",f"scale={W}:{H}","-pix_fmt","rgb24","-f","rawvideo","-"],capture_output=True).stdout
a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,H,W,3).astype(np.int16)
for fi in (0,60,120):
    f=a[fi]
    print(f"--- frame {fi} : vertical scan at x=134 (centre) , full-res y = row*4 ---")
    for row in range(int(H*0.30),int(H*0.78),4):
        px=f[row,128:142].mean(axis=0)
        r,g,b=px
        tag=""
        if g>r-10 and g>b+6: tag="  <-- GREENISH"
        print("  y=%4d  rgb=(%3d,%3d,%3d)%s"%(row*4,r,g,b,tag))

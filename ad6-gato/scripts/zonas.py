import subprocess, numpy as np, json
SRC="/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-22-croche-gato/entrega"
# shot: (archivo, primer fotograma fuente, n fotogramas)
SHOTS={"A":("01-dormido",69,52),"B":("02-bolsa",10,36),"C":("03-carrera",0,90),
       "D1":("04-cuenco",0,52),"D2":("04-cuenco",52,61),"E":("05-producto",0,96)}
W,H=134,240
cache={}
def load(n):
    if n in cache: return cache[n]
    raw=subprocess.run(["ffmpeg","-v","error","-i",f"{SRC}/{n}.mp4","-vf",f"scale={W}:{H}",
        "-pix_fmt","gray","-f","rawvideo","-"],capture_output=True).stdout
    cache[n]=np.frombuffer(raw,dtype=np.uint8).reshape(-1,H,W).astype(np.float32)
    return cache[n]
bands=[(0.06,0.14,"06-14 (cabecera)"),(0.62,0.70,"62-70"),(0.70,0.78,"70-78"),
       (0.76,0.84,"76-84"),(0.82,0.90,"82-90"),(0.86,0.94,"86-94"),(0.90,0.97,"90-97")]
out={}
for k,(n,f0,nf) in SHOTS.items():
    a=load(n)[f0:f0+nf]
    print(f"=== PLANO {k}  ({n} f{f0}..{f0+nf-1}) ===")
    out[k]={}
    for y0,y1,lab in bands:
        r=a[:,int(H*y0):int(H*y1), int(W*0.10):int(W*0.90)]
        mean=r.mean(); sd=r.std(); p5,p95=np.percentile(r,[5,95])
        # estabilidad temporal: cuanto cambia el brillo medio de la banda a lo largo del plano
        tv=r.mean(axis=(1,2)); drift=tv.max()-tv.min()
        # "actividad": movimiento dentro de la banda
        act=np.abs(np.diff(r,axis=0)).mean()
        print("  y %-18s L=%5.1f  sd=%4.1f  p5=%5.1f p95=%5.1f  deriva=%4.1f  mov=%4.2f"%(lab,mean,sd,p5,p95,drift,act))
        out[k][lab]=dict(L=round(float(mean),1),sd=round(float(sd),1),p5=round(float(p5),1),
                         p95=round(float(p95),1),drift=round(float(drift),1),act=round(float(act),2))
json.dump(out,open("/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/ad6-gato/analysis/zonas.json","w"),indent=1)

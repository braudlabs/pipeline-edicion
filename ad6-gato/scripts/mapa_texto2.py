import subprocess, numpy as np, json
SRC="/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-22-croche-gato/entrega"
SHOTS={"A":("01-dormido",69,52),"B":("02-bolsa",10,36),"C":("03-carrera",0,90),
       "D1":("04-cuenco",0,52),"D2":("04-cuenco",52,61),"E":("05-producto",0,96)}
W,H=270,484   # ~1/4 de 1076x1928 -> 1 px = 4 px reales
BLUR=5        # ~20 px reales ~= grosor de trazo de un subtitulo de 60 px de altura de caja
cache={}
def load(n):
    if n not in cache:
        raw=subprocess.run(["ffmpeg","-v","error","-i",f"{SRC}/{n}.mp4",
            "-vf",f"scale={W}:{H},boxblur={BLUR}:1","-pix_fmt","gray","-f","rawvideo","-"],capture_output=True).stdout
        cache[n]=np.frombuffer(raw,dtype=np.uint8).reshape(-1,H,W).astype(np.float32)
    return cache[n]
def lin(s):
    s=np.asarray(s,dtype=np.float64)/255.0
    return np.where(s<=0.04045, s/12.92, ((s+0.055)/1.055)**2.4)
TD=lin(58.0); TL=lin(243.0)
XW={"centro-76":(0.12,0.88),"centro-56":(0.22,0.78),"izq-52":(0.08,0.60),"der-52":(0.40,0.92)}
res={}
print("contraste PEOR CASO (p2/p98 del fondo DESENFOCADO a escala de trazo). objetivo >=4.5, aceptable >=3.0\n")
for k,(n,f0,nf) in SHOTS.items():
    a=load(n)[f0:f0+nf]; res[k]={}
    print(f"══ PLANO {k} ({n}) ══")
    for xn,(x0,x1) in XW.items():
        best=[]
        for top in range(58,96,2):
            r=a[:,int(H*top/100):int(H*(top+6)/100), int(W*x0):int(W*x1)]
            p2,p98=np.percentile(r,[2,98])
            cd=(lin(p2)+0.05)/(TD+0.05); cl=(TL+0.05)/(lin(p98)+0.05)
            best.append((max(cd,cl),top,r.mean(),p2,p98,cd,cl,float(np.abs(np.diff(r,axis=0)).mean())))
        best.sort(reverse=True)
        s=best[0]
        print("  %-11s mejor y=%2d-%2d  L=%5.1f p2=%5.1f p98=%5.1f  c_oscuro=%4.2f c_claro=%4.2f mov=%4.2f"%(
              xn,s[1],s[1]+6,s[2],s[3],s[4],s[5],s[6],s[7]))
        res[k][xn]=dict(y0=s[1],y1=s[1]+6,L=round(s[2],1),p2=round(s[3],1),p98=round(s[4],1),
                        c_dark=round(s[5],2),c_light=round(s[6],2),act=round(s[7],2))
    print()
json.dump(res,open("/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/ad6-gato/analysis/mapa-texto2.json","w"),indent=1)

import subprocess, numpy as np, json
SRC="/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-22-croche-gato/entrega"
SHOTS={"A":("01-dormido",69,52),"B":("02-bolsa",10,36),"C":("03-carrera",0,90),
       "D1":("04-cuenco",0,52),"D2":("04-cuenco",52,61),"E":("05-producto",0,96)}
W,H=134,240
cache={}
def load(n):
    if n not in cache:
        raw=subprocess.run(["ffmpeg","-v","error","-i",f"{SRC}/{n}.mp4","-vf",f"scale={W}:{H}",
            "-pix_fmt","gray","-f","rawvideo","-"],capture_output=True).stdout
        cache[n]=np.frombuffer(raw,dtype=np.uint8).reshape(-1,H,W).astype(np.float32)
    return cache[n]
def lin(s):
    s=s/255.0
    return np.where(s<=0.04045, s/12.92, ((s+0.055)/1.055)**2.4)
TXT_DARK=lin(np.array([58.0]))[0]   # #3A2A1E aprox -> usar canal medio
TXT_LIGHT=lin(np.array([243.0]))[0]
print("Ltexto oscuro=%.4f  Ltexto claro=%.4f\n"%(TXT_DARK,TXT_LIGHT))
res={}
for k,(n,f0,nf) in SHOTS.items():
    a=load(n)[f0:f0+nf]
    print(f"══ PLANO {k} ({n} f{f0}..{f0+nf-1}) — contraste PEOR CASO de una caja de texto (x 12-88%) ══")
    print("   banda y%%      Lmed  p2    p98   c_oscuro  c_claro   mov")
    res[k]=[]
    for top in range(58,95,3):
        y0,y1=top/100.0,(top+7)/100.0
        r=a[:,int(H*y0):int(H*y1), int(W*0.12):int(W*0.88)]
        p2,p98=np.percentile(r,[2,98])
        Lp2,Lp98=lin(np.array([p2]))[0],lin(np.array([p98]))[0]
        c_dark=(Lp2+0.05)/(TXT_DARK+0.05)       # peor caso: fondo mas oscuro que aparece
        c_light=(TXT_LIGHT+0.05)/(Lp98+0.05)    # peor caso: fondo mas claro que aparece
        act=np.abs(np.diff(r,axis=0)).mean()
        flag=""
        if c_dark>=4.5: flag+=" OSCURO-OK"
        elif c_dark>=3.0: flag+=" oscuro-limite"
        if c_light>=4.5: flag+=" CLARO-OK"
        elif c_light>=3.0: flag+=" claro-limite"
        print("   %2d-%2d      %5.1f %5.1f %5.1f    %5.2f    %5.2f   %5.2f %s"%(top,top+7,r.mean(),p2,p98,c_dark,c_light,act,flag))
        res[k].append(dict(y0=top,y1=top+7,L=round(float(r.mean()),1),p2=round(float(p2),1),
            p98=round(float(p98),1),c_dark=round(float(c_dark),2),c_light=round(float(c_light),2),act=round(float(act),2)))
    print()
json.dump(res,open("/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/ad6-gato/analysis/mapa-texto.json","w"),indent=1)

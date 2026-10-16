"""Espectrogramas propios (mid y side) con rejilla de fotogramas. Uso: aud.py t0 t1 salida.png [side|mid|both]"""
import sys, wave, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
WAV='analysis/audio/v3-ia-cara.wav'
def load():
    w=wave.open(WAV); n=w.getnframes(); sr=w.getframerate()
    x=np.frombuffer(w.readframes(n),dtype=np.int16).reshape(-1,2).astype(np.float32)/32768
    return x,sr
def stft(x,sr,t0,t1,nfft=2048,hop=220):
    a=max(0,int(t0*sr)-nfft); b=min(len(x),int(t1*sr)+nfft)
    seg=x[a:b]; win=np.hanning(nfft)
    idx=np.arange(0,len(seg)-nfft,hop)
    S=np.stack([np.abs(np.fft.rfft(seg[i:i+nfft]*win)) for i in idx],1)
    times=(a+idx+nfft/2)/sr
    freqs=np.fft.rfftfreq(nfft,1/sr)
    return S,times,freqs
def render(S,times,freqs,t0,t1,W=1500,H=380,fmin=40,fmax=16000,dbmin=-80,dbmax=-10,title=""):
    db=20*np.log10(S/ (2048/4) +1e-9)
    # eje log de frecuencia
    fy=np.geomspace(fmin,fmax,H)[::-1]
    fi=np.clip(np.searchsorted(freqs,fy),0,len(freqs)-1)
    tx=np.linspace(t0,t1,W)
    ti=np.clip(np.searchsorted(times,tx),0,len(times)-1)
    img=db[fi][:,ti]
    v=np.clip((img-dbmin)/(dbmax-dbmin),0,1)
    # paleta tipo magma simple
    r=np.clip(v*2.2,0,1); g=np.clip(v*2.2-0.9,0,1); b=np.clip(np.where(v<0.45,v*1.6,0.72-(v-0.45)*1.0),0,1)
    rgb=(np.dstack([r,g,b])*255).astype(np.uint8)
    I=Image.fromarray(rgb)
    C=Image.new("RGB",(W+60,H+46),(16,16,16)); C.paste(I,(60,22))
    d=ImageDraw.Draw(C)
    try: f=ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc",13)
    except Exception: f=ImageFont.load_default()
    d.text((62,3),title,fill=(230,230,230),font=f)
    for hz in (50,100,200,500,1000,2000,5000,10000):
        y=22+int(np.argmin(np.abs(fy-hz)))
        d.line([(55,y),(60,y)],fill=(200,200,200)); d.text((2,y-7),f"{hz}",fill=(200,200,200),font=f)
    # rejilla de fotogramas (24 fps)
    f0=int(np.ceil(t0*24)); f1=int(np.floor(t1*24))
    step=1 if (f1-f0)<=60 else (2 if (f1-f0)<=120 else 6)
    for fr in range(f0,f1+1):
        x=60+int((fr/24-t0)/(t1-t0)*W)
        if fr%step==0:
            major=(fr%6==0) if step<6 else True
            d.line([(x,22+H),(x,22+H+(8 if major else 4))],fill=(255,220,90))
            if major or step==1 and (f1-f0)<=30:
                d.text((x-12,22+H+9),f"f{fr}",fill=(255,220,90),font=f)
            if major:
                for yy in range(22,22+H,6): C.putpixel((min(x,W+59),yy),(120,120,120))
    return C
def words(t0,t1):
    try:
        w=json.load(open('datos/v3-ia-cara/words.json'))
        ws=w if isinstance(w,list) else w.get('words',[])
        return [(x.get('start',x.get('t0')),x.get('end',x.get('t1')),x.get('word',x.get('w',''))) for x in ws if x.get('start',x.get('t0'))<t1 and x.get('end',x.get('t1'))>t0]
    except Exception as e:
        return []
if __name__=="__main__":
    t0=float(sys.argv[1]); t1=float(sys.argv[2]); out=sys.argv[3]; mode=sys.argv[4] if len(sys.argv)>4 else "both"
    x,sr=load()
    mid=(x[:,0]+x[:,1])/2; side=(x[:,0]-x[:,1])/2
    panels=[]
    if mode in("mid","both"):
        S,T,F=stft(mid,sr,t0,t1); panels.append(render(S,T,F,t0,t1,title=f"MID (L+R)  {t0:.2f}-{t1:.2f}s"))
    if mode in("side","both"):
        S,T,F=stft(side,sr,t0,t1); panels.append(render(S,T,F,t0,t1,dbmin=-95,dbmax=-30,title=f"SIDE (L-R): sin voz centrada  {t0:.2f}-{t1:.2f}s"))
    Wd=panels[0].width; Ht=sum(p.height for p in panels)+24
    C=Image.new("RGB",(Wd,Ht),(16,16,16)); y=0
    for p in panels: C.paste(p,(0,y)); y+=p.height
    d=ImageDraw.Draw(C)
    try: f=ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc",13)
    except Exception: f=ImageFont.load_default()
    for (a,b,wd) in words(t0,t1):
        xa=60+int((a-t0)/(t1-t0)*1500)
        if xa>=60: d.line([(xa,y),(xa,y+8)],fill=(120,200,255)); d.text((xa+2,y+6),str(wd),fill=(120,200,255),font=f)
    C.save(out); print(out,C.size)

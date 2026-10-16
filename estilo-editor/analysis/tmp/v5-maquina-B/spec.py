#!/usr/bin/env python3
"""Espectrograma propio de alta resolución temporal, con marcas de fotograma.
  spec.py t0 t1 salida.png [--fmax 12000] [--marks 988,1012] [--words]
"""
import sys, wave, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT='/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/estilo-editor'
FPS=30000/1001
def load():
    w=wave.open(ROOT+'/analysis/audio/v5-maquina.wav')
    sr=w.getframerate(); n=w.getnframes(); ch=w.getnchannels()
    x=np.frombuffer(w.readframes(n),np.int16).astype(np.float32)/32768
    if ch>1: x=x.reshape(-1,ch).mean(axis=1)
    return x,sr
def main():
    t0=float(sys.argv[1]); t1=float(sys.argv[2]); out=sys.argv[3]
    marks=[]; fmax=12000; words=False
    a=sys.argv[4:]
    i=0
    while i<len(a):
        if a[i]=='--marks': marks=[int(v) for v in a[i+1].split(',')]; i+=2
        elif a[i]=='--fmax': fmax=float(a[i+1]); i+=2
        elif a[i]=='--words': words=True; i+=1
        else: i+=1
    x,sr=load()
    N=2048; hop=int(sr*(t1-t0)/1480)
    hop=max(32,hop)
    win=np.hanning(N)
    s0=int(t0*sr); s1=int(t1*sr)
    cols=[]
    for s in range(s0,s1,hop):
        seg=x[max(0,s-N//2):s+N//2]
        if len(seg)<N: seg=np.pad(seg,(0,N-len(seg)))
        cols.append(np.abs(np.fft.rfft(seg*win)))
    S=np.array(cols).T  # freq x time
    freqs=np.fft.rfftfreq(N,1/sr)
    Hh=520
    # eje log 40..fmax
    fl=np.exp(np.linspace(np.log(40),np.log(fmax),Hh))
    idx=np.clip(np.searchsorted(freqs,fl),1,len(freqs)-1)
    # promedio por banda
    img=np.zeros((Hh,S.shape[1]),np.float32)
    for k in range(Hh):
        lo=idx[k-1] if k>0 else idx[k]-1
        hi=max(idx[k],lo+1)
        img[k]=S[lo:hi].max(axis=0)
    db=20*np.log10(img/(N/4)+1e-9)
    lo_db,hi_db=-95.0,-15.0
    v=np.clip((db-lo_db)/(hi_db-lo_db),0,1)[::-1]
    cp=np.array([[0,0,0],[40,10,80],[130,30,120],[220,80,60],[250,180,40],[255,255,200]],np.float32)
    pos=np.linspace(0,1,len(cp))
    rgb=np.dstack([np.interp(v,pos,cp[:,c]) for c in range(3)]).astype(np.uint8)
    top=64
    im=Image.new('RGB',(rgb.shape[1]+60,Hh+top+22),(16,16,16))
    im.paste(Image.fromarray(rgb),(60,top))
    d=ImageDraw.Draw(im); font=ImageFont.load_default(size=11)
    for f in (50,100,200,500,1000,2000,5000,10000):
        if f<fmax:
            y=top+Hh-1-int(np.log(f/40)/np.log(fmax/40)*(Hh-1))
            d.line([(54,y),(60,y)],fill=(200,200,200)); d.text((2,y-6),f'{f}',fill=(200,200,200),font=font)
    W=rgb.shape[1]
    def X(t): return 60+(t-t0)/(t1-t0)*W
    # fotogramas
    f_a=int(np.ceil(t0*FPS)); f_b=int(t1*FPS)
    for f in range(f_a,f_b+1):
        x_=X(f/FPS)
        if f%5==0:
            d.line([(x_,top-10),(x_,top)],fill=(160,160,160))
            if f%10==0: d.text((x_-12,top-24),f'f{f}',fill=(160,160,160),font=font)
        else:
            d.line([(x_,top-4),(x_,top)],fill=(90,90,90))
    for f in marks:
        x_=X(f/FPS); d.line([(x_,top-10),(x_,top+Hh)],fill=(255,60,60))
        d.text((x_+2,top+2),f'f{f}',fill=(255,90,90),font=font)
    if words:
        ws=json.load(open(ROOT+'/datos/v5-maquina/words.json'))['words']
        for w in ws:
            if t0<=w['t0']<=t1:
                x_=X(w['t0']); d.line([(x_,2),(x_,top-26)],fill=(90,170,255)); d.text((x_+2,2+12*(ws.index(w)%2)),w['w'],fill=(120,190,255),font=font)
    # segundos
    t=np.ceil(t0*10)/10
    while t<=t1:
        x_=X(t)
        if abs(t-round(t))<1e-6:
            d.text((x_-8,top+Hh+4),f'{t:.0f}s',fill=(220,220,220),font=font); d.line([(x_,top+Hh),(x_,top+Hh+4)],fill=(220,220,220))
        elif abs(t*2-round(t*2))<1e-6:
            d.text((x_-10,top+Hh+4),f'{t:.1f}',fill=(150,150,150),font=font)
        t=round(t+0.1,1)
    im.save(out); print(out, im.size)
main()

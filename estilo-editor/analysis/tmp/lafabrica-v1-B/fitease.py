import json, math, sys
import numpy as np
cum=json.load(open('analysis/tmp/lafabrica-v1-B/cumscale.json'))
# curva media (escala relativa al primer fotograma), usando lupa como base (75 pasos)
L=np.array(cum['lupa']); S=np.exp(L)
k=np.arange(len(S))
def bez(t,x1,y1,x2,y2):
    # resuelve x(u)=t por bisección vectorizada
    t=np.clip(t,0,1)
    lo=np.zeros_like(t); hi=np.ones_like(t)
    for _ in range(40):
        u=(lo+hi)/2
        x=3*(1-u)**2*u*x1+3*(1-u)*u**2*x2+u**3
        lo=np.where(x<t,u,lo); hi=np.where(x>=t,u,hi)
    u=(lo+hi)/2
    return 3*(1-u)**2*u*y1+3*(1-u)*u**2*y2+u**3
def err(model):
    return float(np.sqrt(((model-S)**2).mean()))
rng=np.random.default_rng(1)
best=None
# familias
def fam_bez(p):
    x1,y1,x2,y2,T,S0,Send=p
    return S0+(Send-S0)*bez(k/T,x1,y1,x2,y2)
def fam_pow(p):
    n,T,S0,Send=p
    t=np.clip(k/T,0,1); return S0+(Send-S0)*(1-(1-t)**n)
def fam_expo(p):
    c,T,S0,Send=p
    t=np.clip(k/T,0,1); return S0+(Send-S0)*(1-np.exp(-c*t))/(1-np.exp(-c))
def search(f,lo,hi,n=60000,rounds=6):
    lo=np.array(lo,float); hi=np.array(hi,float)
    bestp=None;beste=9
    for r in range(rounds):
        P=rng.uniform(lo,hi,size=(n if r==0 else n//4,len(lo)))
        for p in P:
            e=err(f(p))
            if e<beste: beste=e;bestp=p
        span=(hi-lo)*0.35
        lo=np.maximum(lo,bestp-span/2); hi=np.minimum(hi,bestp+span/2)
    return bestp,beste
p,e=search(fam_pow,[1,40,0.99,0.80],[12,400,1.01,0.86],n=20000)
print('potencia  1-(1-t)^n : n=%.3f T=%.1f S0=%.4f Send=%.4f  rms=%.5f'%(*p,e))
p,e=search(fam_expo,[0.5,40,0.99,0.80],[12,400,1.01,0.86],n=20000)
print('expo  (1-e^-ct)/(1-e^-c): c=%.3f T=%.1f S0=%.4f Send=%.4f  rms=%.5f'%(*p,e))
p,e=search(fam_bez,[0,0,0,0.5,60,0.995,0.83],[0.5,1.2,1,1.0,200,1.005,0.86],n=6000)
print('bezier: x1=%.3f y1=%.3f x2=%.3f y2=%.3f T=%.1f S0=%.4f Send=%.4f rms=%.5f'%(*p,e))
m=fam_bez(p)
print('k obs modelo')
for i in [0,1,2,3,4,5,6,8,10,12,16,20,24,30,36,48,56,64,75]:
    print(i, f"{S[i]:.4f} {m[i]:.4f}")

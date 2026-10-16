import json, math, sys
import numpy as np
cum=json.load(open('analysis/tmp/lafabrica-v1-B/cumscale.json'))
L=np.array(cum['lupa']); S=np.exp(L)
k=np.arange(len(S))
def bez(t,x1,y1,x2,y2):
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
rng=np.random.default_rng(2)
def search(f,lo,hi,n=6000,rounds=7):
    lo=np.array(lo,float); hi=np.array(hi,float)
    bestp=None;beste=9
    for r in range(rounds):
        P=rng.uniform(lo,hi,size=(n if r==0 else n//3,len(lo)))
        for p in P:
            e=err(f(p))
            if e<beste: beste=e;bestp=p
        span=(hi-lo)*0.4
        lo=np.maximum(lo,bestp-span/2); hi=np.minimum(hi,bestp+span/2)
    return bestp,beste
def fam(p):
    x1,y1,x2,y2,T,k0,S0,Send=p
    return S0+(Send-S0)*bez((k+k0)/T,x1,y1,x2,y2)
p,e=search(fam,[0,0,0,0.5,60,0,0.99,0.83],[0.5,1.2,1,1.0,200,2,1.03,0.86])
print('bezier+offset: x1=%.3f y1=%.3f x2=%.3f y2=%.3f T=%.1f k0=%.2f S0=%.4f Send=%.4f rms=%.5f  S0/Send=%.4f'%(*p,e,p[6]/p[7]))
# familia: suma de exponenciales
def fam2(p):
    a,t1,t2,S0,Send=p
    return Send+(S0-Send)*(a*np.exp(-k/t1)+(1-a)*np.exp(-k/t2))
p2,e2=search(fam2,[0,0.5,5,0.99,0.83],[1,10,60,1.01,0.86],n=20000)
print('2 exponenciales: a=%.3f tau1=%.2f tau2=%.2f S0=%.4f Send=%.4f rms=%.5f'%(*p2,e2))
# familia: 1/(1+k/c)^n (hiperbólica)
def fam3(p):
    c,n,S0,Send=p
    return Send+(S0-Send)*(1+k/c)**(-n)
p3,e3=search(fam3,[0.5,0.3,0.99,0.80],[80,8,1.01,0.86],n=20000)
print('hiperbólica (1+k/c)^-n: c=%.2f n=%.2f S0=%.4f Send=%.4f rms=%.5f'%(*p3,e3))
# ¿es exponencial en log con spring? prueba: ley de potencia en t con T fijo
for nm,pp,ff in [('bez',p,fam),('2exp',p2,fam2),('hip',p3,fam3)]:
    m=ff(pp)
    print(nm,' '.join(f"{i}:{(m[i]-S[i])*1e4:+.0f}" for i in [0,1,2,3,4,5,6,8,10,12,16,20,24,30,36,48,56,64,75]))

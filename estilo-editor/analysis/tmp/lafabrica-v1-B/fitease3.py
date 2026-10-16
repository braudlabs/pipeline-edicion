import json, math, sys
import numpy as np
tab=json.load(open('analysis/tmp/lafabrica-v1-B/Z_table.json'))
k=np.arange(76); S=np.array([tab[str(i)] for i in range(76)])
def bez(t,x1,y1,x2,y2):
    t=np.clip(t,0,1)
    lo=np.zeros_like(t); hi=np.ones_like(t)
    for _ in range(40):
        u=(lo+hi)/2
        x=3*(1-u)**2*u*x1+3*(1-u)*u**2*x2+u**3
        lo=np.where(x<t,u,lo); hi=np.where(x>=t,u,hi)
    u=(lo+hi)/2
    return 3*(1-u)**2*u*y1+3*(1-u)*u**2*y2+u**3
def err(model): return float(np.sqrt(((model-S)**2).mean()))
rng=np.random.default_rng(3)
def search(f,lo,hi,n=6000,rounds=8):
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
# A: bezier libre, sin desfase
def famA(p):
    x1,y1,x2,y2,T,S0,Send=p
    return S0+(Send-S0)*bez(k/T,x1,y1,x2,y2)
pA,eA=search(famA,[0,0,0,0.5,70,1.17,0.97],[0.5,1.2,1,1.0,200,1.21,1.005])
print('A bezier: cubic-bezier(%.3f,%.3f,%.3f,%.3f) T=%.1f f  Z0=%.4f Zfin=%.4f rms=%.5f'%(*pA,eA))
# B: bezier con llegada plana y2=1, x1=0
def famB(p):
    y1,x2,T,S0,Send=p
    return S0+(Send-S0)*bez(k/T,0.0,y1,x2,1.0)
pB,eB=search(famB,[0,0,70,1.17,0.97],[1.2,1,200,1.22,1.005],n=8000)
print('B bezier(0,y1,x2,1): y1=%.3f x2=%.3f T=%.1f Z0=%.4f Zfin=%.4f rms=%.5f'%(*pB,eB))
# C: 2 exponenciales
def famC(p):
    a,t1,t2,S0,Send=p
    return Send+(S0-Send)*(a*np.exp(-k/t1)+(1-a)*np.exp(-k/t2))
pC,eC=search(famC,[0,0.5,5,1.17,0.95],[1,10,80,1.21,1.005],n=20000)
print('C 2 exp: a=%.3f tau1=%.2f tau2=%.2f Z0=%.4f Zfin=%.4f rms=%.5f'%(*pC,eC))
# D: potencia con T libre:  Z = Zfin + (Z0-Zfin)*(1-t)^n
def famD(p):
    n,T,S0,Send=p
    t=np.clip(k/T,0,1); return Send+(S0-Send)*(1-t)**n
pD,eD=search(famD,[1,60,1.17,0.95],[12,400,1.21,1.005],n=20000)
print('D potencia (1-t)^n: n=%.3f T=%.1f Z0=%.4f Zfin=%.4f rms=%.5f'%(*pD,eD))
# E: expo estándar: Z=Zfin+(Z0-Zfin)*2^(-10 k/T)
def famE(p):
    T,S0,Send=p
    return Send+(S0-Send)*2.0**(-10*k/T)
pE,eE=search(famE,[30,1.17,0.95],[600,1.21,1.005],n=20000)
print('E expoOut 2^(-10t): T=%.1f Z0=%.4f Zfin=%.4f rms=%.5f'%(*pE,eE))
for nm,pp,ff in [('A',pA,famA),('B',pB,famB),('C',pC,famC),('D',pD,famD),('E',pE,famE)]:
    m=ff(pp)
    print(nm,' '.join(f"{i}:{(m[i]-S[i])*1e4:+.0f}" for i in [0,1,2,3,4,5,6,8,10,12,16,20,24,30,36,48,56,64,75]))

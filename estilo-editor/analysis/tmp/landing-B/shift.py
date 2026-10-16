#!/usr/bin/env python3
"""Desplazamiento (correlación de fase, subpíxel) de un ROI entre un fotograma de referencia y otros.
uso: shift.py ref f1,f2,... x0,y0,x1,y1 [x0,y0,x1,y1 ...]"""
import sys
import numpy as np
sys.path.insert(0,'scripts')
from common import probe
from sheet import load_full
info=probe('landing')
ref=int(sys.argv[1]); fs=[int(v) for v in sys.argv[2].split(',')]
rois=[[int(q) for q in s.split(',')] for s in sys.argv[3:]]
def gray(f):
    return np.asarray(load_full('landing',f,info),np.float32).mean(axis=2)
def pc(a,b):
    a=a-a.mean(); b=b-b.mean()
    wy=np.hanning(a.shape[0])[:,None]; wx=np.hanning(a.shape[1])[None,:]
    A=np.fft.fft2(a*wy*wx); B=np.fft.fft2(b*wy*wx)
    R=A*np.conj(B); R/=np.abs(R)+1e-9
    r=np.fft.ifft2(R).real
    py,px=np.unravel_index(np.argmax(r),r.shape)
    def sub(v,p,n):
        l=v[(p-1)%n]; c=v[p]; rr=v[(p+1)%n]
        den=(l-2*c+rr)
        return 0 if den==0 else 0.5*(l-rr)/den
    dy=py+sub(r[:,px],py,r.shape[0]); dx=px+sub(r[py,:],px,r.shape[1])
    if dy>r.shape[0]/2: dy-=r.shape[0]
    if dx>r.shape[1]/2: dx-=r.shape[1]
    return dx,dy,r.max()
G=gray(ref)
for f in fs:
    g=gray(f)
    out=[]
    for (x0,y0,x1,y1) in rois:
        dx,dy,pk=pc(g[y0:y1,x0:x1],G[y0:y1,x0:x1])
        out.append(f'dx={dx:+.2f} dy={dy:+.2f} pk={pk:.2f}')
    print(f, ' | '.join(out))

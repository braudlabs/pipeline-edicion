#!/usr/bin/env python3
"""Tramos de columnas/filas con tinta en un ROI. uso: cols.py f x0 y0 x1 y1 thr gap [mode]  (mode: white=min canal>=thr ; dark=max canal<=thr)"""
import sys
import numpy as np
sys.path.insert(0,'scripts')
from common import probe
from sheet import load_full
f=int(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]; thr=float(sys.argv[6]); gap=int(sys.argv[7])
mode=sys.argv[8] if len(sys.argv)>8 else 'white'
im=np.asarray(load_full('landing',f,probe('landing')),np.float32)
A=im.min(axis=2) if mode=='white' else im.max(axis=2)
R=A[y0:y1,x0:x1]
M=(R>=thr) if mode=='white' else (R<=thr)
def runs(v,gap):
    idx=np.nonzero(v>0)[0]
    if len(idx)==0: return []
    out=[];s=idx[0];p=idx[0]
    for i in idx[1:]:
        if i>p+gap: out.append((s,p)); s=i
        p=i
    out.append((s,p)); return out
print('columnas:', [(x0+s,x0+e,e-s+1) for s,e in runs(M.sum(axis=0),gap)])
print('filas:', [(y0+s,y0+e,e-s+1) for s,e in runs(M.sum(axis=1),1)])

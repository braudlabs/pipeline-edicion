#!/usr/bin/env python3
"""Grosor de trazo: moda de las longitudes de tramos horizontales de tinta en un ROI. uso: stroke.py f x0 y0 x1 y1 thr"""
import sys
import numpy as np
from collections import Counter
sys.path.insert(0,'scripts')
from common import probe
from sheet import load_full
f=int(sys.argv[1]); x0,y0,x1,y1=[int(v) for v in sys.argv[2:6]]; thr=float(sys.argv[6])
A=np.asarray(load_full('landing',f,probe('landing')),np.float32).min(axis=2)[y0:y1,x0:x1]
M=A>=thr
c=Counter()
for r in M:
    idx=np.nonzero(r)[0]
    if len(idx)==0: continue
    s=idx[0];p=idx[0]
    for i in idx[1:]:
        if i>p+1: c[p-s+1]+=1; s=i
        p=i
    c[p-s+1]+=1
tot=sum(c.values())
print(f'f{f} roi {x0},{y0},{x1},{y1} thr {thr}: tramos={tot}  histograma (long:n):', sorted(c.items())[:16])
vals=[k for k,v in c.items() for _ in range(v)]
print('  mediana', np.median(vals), ' moda', c.most_common(3))
ys,xs=np.nonzero(M); print('  caja', x0+xs.min(), y0+ys.min(), x0+xs.max(), y0+ys.max())

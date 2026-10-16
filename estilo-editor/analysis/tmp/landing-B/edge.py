#!/usr/bin/env python3
"""Perfil horizontal de un borde vertical: anchura 10-90 % del flanco. uso: edge.py ref A B y0 y1 x0 x1 [lado: R|L]"""
import sys
import numpy as np
sys.path.insert(0,'scripts')
from common import probe
from sheet import load_full, load_full_run
info=probe('landing')
ref,a,b,y0,y1,x0,x1=[int(v) for v in sys.argv[1:8]]
side=sys.argv[8] if len(sys.argv)>8 else 'R'
R=np.asarray(load_full('landing',ref,info),np.float32).mean(axis=2)
for k,im in enumerate(load_full_run('landing',a,b-a+1,info)):
    A=np.asarray(im,np.float32).mean(axis=2)
    p=(A-R)[y0:y1,x0:x1].mean(axis=0)
    if side=='L': p=p[::-1]
    # flanco de bajada desde meseta (izq) a 0 (der)
    top=np.percentile(p,95); 
    if top<5: print(a+k,'-'); continue
    n=p/top
    # primer x (desde la derecha) donde supera 0.1, 0.5 y 0.9
    def last_above(t):
        idx=np.nonzero(n>=t)[0]
        return idx.max() if len(idx) else -1
    i10,i50,i90=last_above(0.1),last_above(0.5),last_above(0.9)
    conv=(lambda i: x0+i) if side=='R' else (lambda i: x1-1-i)
    print(a+k, f'meseta={top:.0f} x10={conv(i10)} x50={conv(i50)} x90={conv(i90)} ancho10-90={abs(i10-i90)}')

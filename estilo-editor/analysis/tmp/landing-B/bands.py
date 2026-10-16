#!/usr/bin/env python3
"""Opacidad aparente por bandas verticales: p97 de (fotograma - ref) por banda, normalizado al valor del fotograma 'fin'.
uso: bands.py ref fin A B y0 y1 x0 x1 paso"""
import sys
import numpy as np
sys.path.insert(0,'scripts')
from common import probe
from sheet import load_full, load_full_run
info=probe('landing')
ref,fin,a,b,y0,y1,x0,x1,st=[int(v) for v in sys.argv[1:10]]
R=np.asarray(load_full('landing',ref,info),np.float32).mean(axis=2)
F=np.asarray(load_full('landing',fin,info),np.float32).mean(axis=2)
xs=list(range(x0,x1,st))
fin_v=[np.percentile((F-R)[y0:y1,x:x+st],97) for x in xs]
print('bandas x:', xs)
print('fin   ', ' '.join(f'{v:5.0f}' for v in fin_v))
imgs=load_full_run('landing',a,b-a+1,info)
for k,im in enumerate(imgs):
    A=np.asarray(im,np.float32).mean(axis=2)
    v=[np.percentile((A-R)[y0:y1,x:x+st],97) for x in xs]
    print(a+k, ' '.join(f'{100*q/max(w,1):5.0f}' for q,w in zip(v,fin_v)))

#!/usr/bin/env python3
"""Caja de lo que cambia respecto a un fotograma de referencia. uso: diffbox.py ref A B thr x0,y0,x1,y1 [más rois]
imprime por ROI: x0 y0 x1 y1 area dif_media(sobre máscara) dif_p95"""
import sys
import numpy as np
sys.path.insert(0,'scripts')
from common import probe
from sheet import load_full, load_full_run
info=probe('landing')
ref=int(sys.argv[1]); a,b=int(sys.argv[2]),int(sys.argv[3]); thr=float(sys.argv[4])
rois=[[int(q) for q in s.split(',')] for s in sys.argv[5:]]
R=np.asarray(load_full('landing',ref,info),np.float32)
imgs=load_full_run('landing',a,b-a+1,info)
for k,im in enumerate(imgs):
    A=np.asarray(im,np.float32)
    D=(A-R).mean(axis=2)  # con signo: positivo = más claro
    out=[]
    for (x0,y0,x1,y1) in rois:
        d=D[y0:y1,x0:x1]; M=d>=thr
        if M.sum()<20: out.append('-'); continue
        ys,xs=np.nonzero(M)
        cx0,cx1=np.percentile(xs,[0.3,99.7]); cy0,cy1=np.percentile(ys,[0.3,99.7])
        out.append(f'{x0+cx0:.0f} {y0+cy0:.0f} {x0+cx1:.0f} {y0+cy1:.0f} a={int(M.sum())} m={d[M].mean():.1f} p95={np.percentile(d[M],95):.1f}')
    print(a+k,' | '.join(out))

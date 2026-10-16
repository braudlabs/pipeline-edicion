#!/usr/bin/env python3
"""Caja de tinta por ROI y fotograma. uso: rois.py A B thr mode name=x0,y0,x1,y1 ...   mode white|dark|bgdiff"""
import sys
import numpy as np
sys.path.insert(0,'scripts')
from common import probe
from sheet import load_full_run
a,b=int(sys.argv[1]),int(sys.argv[2]); thr=float(sys.argv[3]); mode=sys.argv[4]
regs=[]
for s in sys.argv[5:]:
    n,v=s.split('='); regs.append((n,[int(q) for q in v.split(',')]))
imgs=load_full_run('landing',a,b-a+1,probe('landing'))
print('f\t'+'\t'.join(f'{n}: x0 y0 x1 y1 w h area lum' for n,_ in regs))
for k,im in enumerate(imgs):
    A=np.asarray(im,np.float32)
    L=A.min(axis=2) if mode=='white' else A.max(axis=2)
    row=[]
    for n,(x0,y0,x1,y1) in regs:
        R=L[y0:y1,x0:x1]
        M=(R>=thr) if mode=='white' else (R<=thr)
        if M.sum()<6: row.append('-'); continue
        ys,xs=np.nonzero(M)
        row.append(f'{x0+xs.min()} {y0+ys.min()} {x0+xs.max()} {y0+ys.max()} {xs.max()-xs.min()+1} {ys.max()-ys.min()+1} {int(M.sum())} {R[M].mean():.0f}')
    print(f'{a+k}\t'+'\t| '.join(row))

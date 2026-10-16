#!/usr/bin/env python3
"""Luminancia media (parches 21x21) en puntos fijos a lo largo de fotogramas. uso: lum.py A B paso x,y ..."""
import sys
import numpy as np
sys.path.insert(0,'scripts')
from common import probe
from sheet import load_full_run
info=probe('landing')
a,b,st=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
pts=[[int(q) for q in s.split(',')] for s in sys.argv[4:]]
imgs=load_full_run('landing',a,b-a+1,info)
print('f\t'+'\t'.join(f'({x},{y})' for x,y in pts))
for k in range(0,len(imgs),st):
    A=np.asarray(imgs[k],np.float32)
    row=[]
    for x,y in pts:
        c=A[y-10:y+11,x-10:x+11].reshape(-1,3).mean(axis=0)
        row.append(f'{c[0]:.0f},{c[1]:.0f},{c[2]:.0f}')
    print(f'{a+k}\t'+'\t'.join(row))

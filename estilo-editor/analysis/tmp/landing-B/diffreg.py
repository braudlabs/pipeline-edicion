#!/usr/bin/env python3
"""MAD entre fotogramas consecutivos por regiones (nativas). uso: diffreg.py A B name=x,y,w,h ..."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, 'scripts')
from common import probe
from sheet import load_full_run
slug='landing'
a,b=int(sys.argv[1]),int(sys.argv[2])
regs=[]
for s in sys.argv[3:]:
    n,v=s.split('=')
    regs.append((n,[float(q) for q in v.split(',')]))
info=probe(slug)
imgs=load_full_run(slug,a-1,b-a+2,info)
arr=[np.asarray(im,np.float32) for im in imgs]
H,W=arr[0].shape[:2]
print('f\t'+'\t'.join(n for n,_ in regs))
for k in range(1,len(arr)):
    row=[]
    for n,(x,y,w,h) in regs:
        X0,Y0,X1,Y1=int(x*W),int(y*H),int((x+w)*W),int((y+h)*H)
        d=np.abs(arr[k][Y0:Y1,X0:X1]-arr[k-1][Y0:Y1,X0:X1]).mean()
        row.append(f'{d:.2f}')
    print(f'{a-1+k}\t'+'\t'.join(row))

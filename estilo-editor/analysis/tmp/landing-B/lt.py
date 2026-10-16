import sys
import numpy as np
sys.path.insert(0,'scripts')
from common import probe
from sheet import load_full_run
info=probe('landing')
a,b=736,773
imgs=load_full_run('landing',a,b-a+1,info)
def runs(v,thr):
    idx=np.nonzero(v>=thr)[0]
    if len(idx)==0: return []
    out=[];s=idx[0];p=idx[0]
    for i in idx[1:]:
        if i>p+1: out.append((s,p)); s=i
        p=i
    out.append((s,p)); return out
A=np.asarray(imgs[0],np.float32).min(axis=2)
reg=A[780:1000,0:820]
rows=(reg>=170).sum(axis=1)
print('f736 filas con tinta (y, n):')
for (s,e) in runs(rows,3): print('  y',780+s,780+e,'max n',rows[s:e+1].max())
# linea: fila con más tinta
yl=780+int(np.argmax(rows)); print('fila de la linea',yl, rows.max())
for y in range(yl-3,yl+4):
    r=A[y,0:900]; xs=np.nonzero(r>=150)[0]
    print(y, xs.min() if len(xs) else None, xs.max() if len(xs) else None, len(xs), r[xs].mean() if len(xs) else 0)

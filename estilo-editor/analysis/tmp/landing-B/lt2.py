import sys
import numpy as np
sys.path.insert(0,'scripts')
from common import probe
from sheet import load_full_run
info=probe('landing')
a,b=730,774
imgs=load_full_run('landing',a,b-a+1,info)
def bbox(M,thr,x0,y0):
    m=M>=thr
    if m.sum()<8: return None
    ys,xs=np.nonzero(m)
    return (x0+xs.min(),y0+ys.min(),x0+xs.max(),y0+ys.max(),int(m.sum()),float(M[m].mean()))
print('f  | linea: x0 x1 (fila926, thr120) maxlum | nombre bbox (thr150) area lum | 2a linea bbox area lum')
for k,im in enumerate(imgs):
    f=a+k
    A=np.asarray(im,np.float32).min(axis=2)
    # linea: busca en filas 900..935 la fila con el tramo más largo >=120
    best=None
    for y in range(895,940):
        r=A[y,60:1300]; xs=np.nonzero(r>=120)[0]
        if len(xs)>40:
            # tramo contiguo mas largo
            d=np.diff(xs); brk=np.nonzero(d>3)[0]
            st=np.concatenate([[0],brk+1]); en=np.concatenate([brk,[len(xs)-1]])
            L=(xs[en]-xs[st]); j=int(np.argmax(L))
            if best is None or L[j]>best[0]: best=(int(L[j]),y,60+int(xs[st[j]]),60+int(xs[en[j]]),float(r[xs[st[j]]:xs[en[j]]+1].mean()))
    nb=bbox(A[800:922,60:500],150,60,800)
    sb=bbox(A[932:985,60:900],140,60,932)
    print(f, '|', best, '|', nb, '|', sb)

import numpy as np
from nm import nelder_mead
from fit2 import bez, dy, n
def mk(fix):
    def model(p, n):
        D, N, n0, x1, y1, x2 = fix(p)
        t = np.clip((n - n0)/N, 0, 1)
        return D*(1 - bez(t, np.clip(x1, 0, 1), y1, np.clip(x2, 0, 1), 1.0))
    return model
cases = {
 "P1=(0,0); D,N,n0,x2": (lambda p: (p[0], p[1], p[2], 0, 0, p[3]), [50, 50, 0.5, 0.1]),
 "P1=(1/6,1/6); D,N,n0,x2": (lambda p: (p[0], p[1], p[2], 1/6, 1/6, p[3]), [50, 50, 0.5, 0.1]),
 "P1=(x1,x1); D,N,n0,x1,x2": (lambda p: (p[0], p[1], p[2], p[3], p[3], p[4]), [50, 50, 0.5, 0.05, 0.1]),
 "D=50,N=50; n0,x1,y1,x2": (lambda p: (50, 50, p[0], p[1], p[2], p[3]), [0.5, 0.05, 0.16, 0.07]),
 "D=50,N=50,n0=0.5; x1,y1,x2": (lambda p: (50, 50, 0.5, p[0], p[1], p[2]), [0.05, 0.16, 0.07]),
 "D=50; N,n0,x1,y1,x2": (lambda p: (50, p[0], p[1], p[2], p[3], p[4]), [50, 0.5, 0.05, 0.16, 0.07]),
 "D=50,N=50,P1=(0,0); n0,x2": (lambda p: (50, 50, p[0], 0, 0, p[1]), [0.5, 0.07]),
 "D=50, P1=(0,0); N,n0,x2": (lambda p: (50, p[0], p[1], 0, 0, p[2]), [50, 0.5, 0.07]),
}
for name, (fix, p0) in cases.items():
    m = mk(fix)
    best = None
    for jit in (1.0, 0.7, 1.3):
        x, v = nelder_mead(lambda p: np.sum((m(p, n) - dy)**2), [q*jit if i > 2 else q for i, q in enumerate(p0)])
        if best is None or v < best[1]: best = (x, v)
    x, v = best
    print(f"{name}: {np.round(x,3)}  -> params {np.round(fix(x),3)}  rms={np.sqrt(v/len(n)):.3f}")

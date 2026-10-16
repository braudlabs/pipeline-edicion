import sys
import numpy as np
from tools import frames
a, b = 33, 60
fr = frames(a, b)
print("f\tthr\ttop3\ttop0\tleft3\tright0\tbot3izq")
for k, im in enumerate(fr):
    f = a + k
    c = im.astype(np.float32).min(axis=2)
    for thr in (165, 235):
        m = c >= thr
        # tope del 3: columnas 180-330 ; tope del 0: columnas 700-880 (lejos del pelo)
        def top(x0, x1, y0=100, y1=700):
            col = m[y0:y1, x0:x1].sum(axis=1)
            idx = np.nonzero(col >= 0.5 * (x1 - x0))[0]
            return y0 + idx.min() if len(idx) else -1
        def left(y0, y1, x0=60, x1=500):
            row = m[y0:y1, x0:x1].sum(axis=0)
            idx = np.nonzero(row >= 0.5 * (y1 - y0))[0]
            return x0 + idx.min() if len(idx) else -1
        def right(y0, y1, x0=600, x1=1040):
            row = m[y0:y1, x0:x1].sum(axis=0)
            idx = np.nonzero(row >= 0.5 * (y1 - y0))[0]
            return x0 + idx.max() if len(idx) else -1
        def bottom(x0, x1, y0=400, y1=900):
            col = m[y0:y1, x0:x1].sum(axis=1)
            idx = np.nonzero(col >= 0.5 * (x1 - x0))[0]
            return y0 + idx.max() if len(idx) else -1
        print(f"{f}\t{thr}\t{top(230,330)}\t{top(730,850)}\t{left(560,640)}\t{right(380,480)}\t{bottom(200,280)}")

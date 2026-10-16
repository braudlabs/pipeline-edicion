import numpy as np
from la import *
F = frames(300, 430)
prev = None
def reg(f, x0, x1): return luma(F[f])[425:505, x0:x1]
out = []
for f in range(301, 431):
    d1 = np.abs(reg(f, 155, 230) - reg(f-1, 155, 230)).mean()
    d2 = np.abs(reg(f, 232, 305) - reg(f-1, 232, 305)).mean()
    m1 = reg(f, 155, 230).max(); m2 = reg(f, 232, 305).max()
    # centroide vertical de tinta (>60)
    def cen(R):
        m = R > 60
        if m.sum() < 10: return float('nan'), 0
        ys, xs = np.nonzero(m); return ys.mean() + 425, int(m.sum())
    c1, a1 = cen(reg(f, 155, 230)); c2, a2 = cen(reg(f, 232, 305))
    out.append(f"f{f}: dif i1={d1:5.2f} i2={d2:5.2f}  max {m1:3.0f}/{m2:3.0f}  cy {c1:6.1f}/{c2:6.1f}  área {a1}/{a2}")
print("\n".join(out))

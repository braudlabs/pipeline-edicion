import numpy as np
from la import *
F = frames(380, 430)
# fondo: mediana por fila de una zona vecina sin rótulo no sirve (plano con degradado); usar f430 (sin rótulos) como referencia
R = luma(F[430])
def cen(f, x0, x1, yA, yB, thr=10):
    d = (luma(F[f]) - R)[yA:yB, x0:x1 + 1]
    m = d > thr
    if m.sum() < 6: return np.nan, 0.0
    w = np.where(m, d, 0)
    return (w.sum(1) * np.arange(yA, yB)).sum() / w.sum(), float(np.percentile(d[m], 99))
base = {}
print("f     encia.(x455-545) dy/brillo")
c0, b0 = cen(382, 455, 545, 440, 640)
dys = {}
for f in range(382, 428):
    c, b = cen(f, 455, 545, 440, 640)
    dys[f] = c - c0 if not np.isnan(c) else np.nan
    print(f"f{f}: dy={c - c0:+7.2f}  brillo={b/b0*100:5.1f}%")
np.save(OUT / "exit_dy.npy", np.array([dys[f] for f in range(382, 428)]))

"""Frase 3: ajuste por palabra con fondo estimado por mediana de columna (hay cortes de plano por debajo)."""
import sys
import numpy as np
from la import *
from nm import nelder_mead
from fit2 import bez
BEZ = (0.048, 0.158, 0.073, 1.0)
F = frames(206, 345)
def dmap(f, x0, x1, yA=380, yB=720):
    L = luma(F[f])[yA:yB, x0:x1 + 1]
    return L - np.median(L, axis=0, keepdims=True), yA
def centroid(f, x0, x1, ya, yb, thr=10):
    d, off = dmap(f, x0, x1)
    d = d[ya - off: yb - off]
    m = d > thr
    if m.sum() < 8: return np.nan, 0.0
    w = np.where(m, d, 0)
    return (w.sum(1) * np.arange(ya, yb)).sum() / w.sum(), float(np.percentile(d[m], 99))
def fitword(name, a, b, x0, x1, ya, yb, show=False):
    rows = [(f,) + centroid(f, x0, x1, ya, yb) for f in range(a, b + 1)]
    rows = [r for r in rows if not np.isnan(r[1])]
    fs = np.array([r[0] for r in rows], float); cy = np.array([r[1] for r in rows]); br = np.array([r[2] for r in rows])
    def model(p):
        t = np.clip((fs - p[0]) / p[1], 0, 1)
        return p[3] + p[2] * (1 - bez(t, *BEZ))
    best = None
    for N_init in (50, 65, 80):
        x, v = nelder_mead(lambda p: np.sum((model(p) - cy) ** 2), [fs[0] - 0.5, N_init, 50.0, cy[-1]], step=[0.5, 8, 2, 1])
        if best is None or v < best[1]: best = (x, v)
    x, v = best
    print(f"{name:13s} visible desde f{int(fs[0])} | inicio f{x[0]:.2f} N={x[1]:.1f} D={x[2]:.1f} final_y={x[3]:.1f} rms={np.sqrt(v/len(fs)):.2f} (fin f{x[0]+x[1]:.1f}) brillo final {br[-5:].mean():.0f}")
    if show:
        print("   " + "  ".join(f"f{int(f)}:{c-x[3]:+.1f}/{b/br[-5:].mean()*100:.0f}%" for f, c, b in rows))
    return x
if __name__ == "__main__":
    show = len(sys.argv) > 1
    # línea 1: asentada y 517..554 ; entra desde +50 -> ventana 505..612 (la línea 2 aún no está hasta f233)
    fitword("Ponte", 209, 232, 163, 267, 500, 615, show)
    fitword("auriculares", 221, 232, 269, 451, 500, 615, show)
    fitword("auriculares*", 221, 300, 346, 451, 500, 566, show)   # tras f233 restringir a zona sin línea 2?  (x346-451 sí tiene 'experiencia')
    fitword("y", 233, 330, 160, 186, 566, 690, show)
    fitword("disfruta", 245, 330, 188, 310, 566, 690, show)
    fitword("la", 257, 330, 314, 341, 566, 690, show)
    fitword("experiencia.", 269, 345, 344, 545, 566, 690, show)

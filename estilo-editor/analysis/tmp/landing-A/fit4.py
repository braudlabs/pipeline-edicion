"""Ajusta el inicio de cada palabra con la curva hallada (bezier fijo), usando el centroide subpíxel."""
import sys
import numpy as np
from la import *
from nm import nelder_mead
from fit2 import bez
BEZ = (0.048, 0.158, 0.073, 1.0); D0 = 50.25; N0 = 50.45
_cache = {}
def fr(a, b):
    key = (a, b)
    if key not in _cache: _cache[key] = frames(a, b)
    return _cache[key]
def centroid(Ld, x0, x1, yA, yB, thr=10):
    d = Ld[yA:yB, x0:x1 + 1]; m = d > thr
    if m.sum() < 8: return np.nan, 0.0, 0.0
    w = np.where(m, d, 0)
    return (w.sum(1) * np.arange(yA, yB)).sum() / w.sum(), float(np.percentile(d[m], 99)), float(w.sum())
def word(name, ref, a, b, x0, x1, yA, yB, fin, yAf=None, yBf=None, show=True, thr=10):
    R = luma(frames(ref, ref)[ref]); F = fr(a, b)
    Ff = fr(fin, fin + 3)
    cf = np.mean([centroid(luma(Ff[f]) - R, x0, x1, yAf or yA, yBf or yB, thr)[0] for f in Ff])
    bf = np.mean([centroid(luma(Ff[f]) - R, x0, x1, yAf or yA, yBf or yB, thr)[1] for f in Ff])
    rows = []
    for f in range(a, b + 1):
        cy, br, sm = centroid(luma(F[f]) - R, x0, x1, yA, yB, thr)
        rows.append((f, cy - cf, br / bf))
    fs = np.array([r[0] for r in rows if not np.isnan(r[1])], float); dy = np.array([r[1] for r in rows if not np.isnan(r[1])])
    first = int(fs[0]) if len(fs) else None
    def model(p):
        t = np.clip((fs - p[0]) / N0, 0, 1)
        return p[1] * (1 - bez(t, *BEZ))
    x, v = nelder_mead(lambda p: np.sum((model(p) - dy) ** 2), [first - 0.5, D0], step=[0.5, 2.0])
    xs, vs = nelder_mead(lambda p: np.sum((model([p[0], D0]) - dy) ** 2), [first - 0.5], step=[0.5])
    print(f"{name:13s} 1.er fotograma visible f{first}  inicio ajustado f{x[0]:.2f} (D libre={x[1]:.1f}px, rms {np.sqrt(v/len(fs)):.2f}) | con D=50,25: inicio f{xs[0]:.2f} rms {np.sqrt(vs/len(fs)):.2f} | centroide final y={cf:.1f}")
    if show:
        print("   " + "  ".join(f"f{int(f)}:{d:+.1f}/{b*100:.0f}%" for (f, d, b) in rows if not np.isnan(d))[:1500])
    return x[0], xs[0]
if __name__ == "__main__":
    which = sys.argv[1]
    if which == "p1":
        for nm_, x0, x1 in (("Gracias", 180, 314), ("por", 316, 378), ("reservar.", 380, 524)):
            word(nm_, 8, 9, 85, x0, x1, 440, 660, 80, show=False)
    if which == "p2":
        word("T(e)", 8, 86, 123, 145, 176, 440, 660, 196, 440, 548, show=False)
        for nm_, x0, x1 in (("dejamos", 202, 355), ("un", 357, 405), ("mensaje", 408, 560)):
            word(nm_, 8, 90, 123, x0, x1, 440, 660, 196, 440, 548, show=False)
        for nm_, x0, x1 in (("de", 146, 200), ("los", 202, 251), ("fundadores.", 252, 460)):
            word(nm_, 8, 120, 200, x0, x1, 548, 700, 196, show=False)

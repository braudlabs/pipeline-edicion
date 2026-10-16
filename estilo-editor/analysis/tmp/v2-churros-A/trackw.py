"""Sigue una palabra por correlación con su plantilla (máscara de tinta blanca en un fotograma de referencia).
track(ref, box, frames, sx, sy) -> lista (f, dx, dy, score, nivel_dentro, nivel_fuera)"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from lib import fr

def template(ref, box, thr=236, sat=12, pad=6):
    x0, y0, x1, y1 = box
    A = fr(ref)[y0 - pad:y1 + pad + 1, x0 - pad:x1 + pad + 1]
    g = A.min(axis=2)
    M = (g >= thr) & ((A.max(axis=2) - g) <= sat)
    return M, (x0 - pad, y0 - pad)

def track(ref, box, frames, sx=(-40, 40), sy=(-60, 100), step=1, thr=236, sat=12, verbose=True, label=""):
    M, (ox, oy) = template(ref, box, thr, sat)
    h, w = M.shape
    # anillo exterior: dilatación simple de la máscara
    out = []
    for n in frames:
        G = fr(n).min(axis=2)
        best = None
        for dy in range(sy[0], sy[1] + 1, step):
            yy = oy + dy
            if yy < 0 or yy + h > G.shape[0]: continue
            for dx in range(sx[0], sx[1] + 1, step):
                xx = ox + dx
                if xx < 0 or xx + w > G.shape[1]: continue
                S = G[yy:yy + h, xx:xx + w]
                sc = S[M].mean() - S[~M].mean()
                if best is None or sc > best[0]:
                    best = (sc, dx, dy, float(np.median(S[M])), float(np.median(S[~M])), float(np.percentile(S[M], 20)))
        out.append((n,) + best)
        if verbose:
            sc, dx, dy, inn, outv, p20 = best
            print(f"  {label} f{n}: dx {dx:+4d} dy {dy:+4d}  score {sc:6.1f}  dentro med {inn:5.1f} p20 {p20:5.1f}  fuera med {outv:5.1f}")
    return out

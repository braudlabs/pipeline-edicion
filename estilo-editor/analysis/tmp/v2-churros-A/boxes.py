"""Detecta recuadros finos (líneas claras de 1-3 px, horizontales y verticales) en un fotograma.
uso: boxes.py f0 f1 [thr]"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from lib import fr

def segs(resp, thr, minlen, axis):
    """tramos largos de respuesta de línea. axis=1: horizontales (recorre filas)."""
    out = []
    R = resp if axis == 1 else resp.T
    B = R > thr
    for y in range(B.shape[0]):
        row = B[y]
        if row.sum() < minlen: continue
        idx = np.nonzero(row)[0]
        s = idx[0]; p = idx[0]; gaps = 0
        run = [s]
        for i in idx[1:]:
            if i - p > 6:
                if p - s + 1 >= minlen: out.append((y, s, p, float(R[y, s:p + 1].mean())))
                s = i
            p = i
        if p - s + 1 >= minlen: out.append((y, s, p, float(R[y, s:p + 1].mean())))
    return out

def merge(sg, tol=3):
    """une tramos en filas contiguas con extensión parecida."""
    sg = sorted(sg); out = []
    for y, a, b, v in sg:
        for m in out:
            if abs(m[0] - y) <= tol and min(b, m[2]) - max(a, m[1]) > 0.5 * min(b - a, m[2] - m[1]):
                if v > m[3]: m[0] = y
                m[1] = min(m[1], a); m[2] = max(m[2], b); m[3] = max(m[3], v); break
        else:
            out.append([y, a, b, v])
    return out

def detect(n, thr=7.0, minlen=70):
    A = fr(n); L = A.mean(axis=2)
    # respuesta de línea horizontal: más claro que 3 px arriba y abajo
    rh = np.zeros_like(L); rv = np.zeros_like(L)
    rh[3:-3] = L[3:-3] - np.maximum(L[:-6], L[6:])
    rv[:, 3:-3] = L[:, 3:-3] - np.maximum(L[:, :-6], L[:, 6:])
    H = merge(segs(rh, thr, minlen, 1)); V = merge(segs(rv, thr, minlen, 0))
    return H, V

def boxes(n, thr=7.0, minlen=70):
    H, V = detect(n, thr, minlen)
    res = []
    # empareja dos horizontales con extensión x parecida y dos verticales en sus extremos
    for i in range(len(H)):
        for j in range(i + 1, len(H)):
            y0, a0, b0, _ = H[i]; y1, a1, b1, _ = H[j]
            if y1 - y0 < 40: continue
            if abs(a0 - a1) > 14 or abs(b0 - b1) > 14: continue
            w = max(b0, b1) - min(a0, a1); h = y1 - y0
            if not (0.5 < w / h < 2.2): continue
            # verticales cerca de los extremos
            lv = [v for v in V if abs(v[0] - min(a0, a1)) <= 8 and v[1] < y1 and v[2] > y0]
            rvv = [v for v in V if abs(v[0] - max(b0, b1)) <= 8 and v[1] < y1 and v[2] > y0]
            res.append((min(a0, a1), y0, max(b0, b1), y1, len(lv) > 0, len(rvv) > 0))
    return res, H, V

if __name__ == "__main__":
    f0, f1 = int(sys.argv[1]), int(sys.argv[2])
    thr = float(sys.argv[3]) if len(sys.argv) > 3 else 7.0
    for n in range(f0, f1 + 1):
        bx, H, V = boxes(n, thr)
        s = "  ".join(f"[x {a}-{c} y {b}-{d} {c-a}x{d-b}{'' if (l and r) else ' (sin vert.)'}]" for a, b, c, d, l, r in bx)
        print(f"f{n}: {len(H)} h, {len(V)} v  ->  {s if s else '—'}")

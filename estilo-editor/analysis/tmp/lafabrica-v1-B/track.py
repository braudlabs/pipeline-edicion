"""Estimación de escala + traslación global entre dos fotogramas por emparejado de parches (NCC) y ajuste robusto.
x' = s*(x-cx)+cx+tx ; y' = s*(y-cy)+cy+ty   (cx,cy = centro del fotograma)
"""
import sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from m import gray

def ncc_best(I, T):
    """I ventana de búsqueda (H,W), T plantilla (h,w). Devuelve (dy,dx,score) de la mejor posición (esquina sup-izq)."""
    h, w = T.shape
    H, W = I.shape
    Tz = T - T.mean()
    tn = np.sqrt((Tz ** 2).sum())
    if tn < 1e-3:
        return None
    F = np.fft.rfft2(I, s=(H, W))
    G = np.fft.rfft2(Tz[::-1, ::-1], s=(H, W))
    cc = np.fft.irfft2(F * G, s=(H, W))[h - 1:, w - 1:]
    # sumas locales
    c1 = np.zeros((H + 1, W + 1)); c1[1:, 1:] = I.cumsum(0).cumsum(1)
    c2 = np.zeros((H + 1, W + 1)); c2[1:, 1:] = (I ** 2).cumsum(0).cumsum(1)
    S1 = c1[h:, w:] - c1[:-h, w:] - c1[h:, :-w] + c1[:-h, :-w]
    S2 = c2[h:, w:] - c2[:-h, w:] - c2[h:, :-w] + c2[:-h, :-w]
    var = np.maximum(S2 - S1 ** 2 / (h * w), 1e-6)
    cc = cc[:var.shape[0], :var.shape[1]]
    ncc = cc / (tn * np.sqrt(var))
    k = np.argmax(ncc)
    y, x = divmod(k, ncc.shape[1])
    sc = ncc[y, x]
    # subpíxel parabólico
    def sub(a, b, c):
        d = (a - 2 * b + c)
        return 0.0 if abs(d) < 1e-9 else 0.5 * (a - c) / d
    oy = sub(ncc[y - 1, x], sc, ncc[y + 1, x]) if 0 < y < ncc.shape[0] - 1 else 0.0
    ox = sub(ncc[y, x - 1], sc, ncc[y, x + 1]) if 0 < x < ncc.shape[1] - 1 else 0.0
    return y + oy, x + ox, sc

def sim(a, b, ps=64, sr=48, step=90, excl=None, minstd=6.0, roi=None, verbose=False):
    """Transformación de a -> b. excl: lista de cajas (x0,y0,x1,y1) a excluir en a. roi: caja a usar."""
    A = gray(a) if isinstance(a, int) else a
    B = gray(b) if isinstance(b, int) else b
    H, W = A.shape
    pts = []
    x0r, y0r, x1r, y1r = roi if roi else (0, 0, W, H)
    for y in range(max(sr, y0r), min(H - ps - sr, y1r - ps), step):
        for x in range(max(sr, x0r), min(W - ps - sr, x1r - ps), step):
            if excl and any(ex0 - ps < x < ex1 and ey0 - ps < y < ey1 for ex0, ey0, ex1, ey1 in excl):
                continue
            T = A[y:y + ps, x:x + ps]
            if T.std() < minstd:
                continue
            I = B[y - sr:y + ps + sr, x - sr:x + ps + sr]
            r = ncc_best(I, T)
            if r is None or r[2] < 0.6:
                continue
            dy, dx = r[0] - sr, r[1] - sr
            if abs(dy) >= sr - 1 or abs(dx) >= sr - 1:
                continue
            pts.append((x + ps / 2, y + ps / 2, dx, dy, r[2]))
    if len(pts) < 6:
        return None
    P = np.array(pts)
    cx, cy = W / 2, H / 2
    X = np.concatenate([P[:, 0] - cx, P[:, 1] - cy])
    D = np.concatenate([P[:, 2], P[:, 3]])
    n = len(P)
    Mx = np.concatenate([np.ones(n), np.zeros(n)])
    My = np.concatenate([np.zeros(n), np.ones(n)])
    keep = np.ones(2 * n, bool)
    for it in range(6):
        Am = np.stack([X[keep], Mx[keep], My[keep]], 1)
        sol, *_ = np.linalg.lstsq(Am, D[keep], rcond=None)
        res = D - (X * sol[0] + Mx * sol[1] + My * sol[2])
        r2 = np.abs(res[:n]) + np.abs(res[n:])
        thr = max(1.0, np.median(r2[keep[:n]]) * 2.5)
        kp = r2 < thr
        keep = np.concatenate([kp, kp])
    return dict(s=1 + sol[0], tx=sol[1], ty=sol[2], n=int(kp.sum()), ntot=n, res=float(np.median(r2[kp])))

if __name__ == '__main__':
    a, b = int(sys.argv[1]), int(sys.argv[2])
    print(sim(a, b))


def scaled_gray(n, r):
    """Fotograma n reescalado por r alrededor del centro, mismo lienzo (relleno con NaN->media)."""
    from PIL import Image
    g = gray(n)
    H, W = g.shape
    im = Image.fromarray(g.astype(np.float32), mode='F')
    w2, h2 = int(round(W * r)), int(round(H * r))
    im2 = im.resize((w2, h2), Image.LANCZOS)
    out = np.full((H, W), float(g.mean()), np.float32)
    a2 = np.asarray(im2)
    if r <= 1:
        x0, y0 = (W - w2) // 2, (H - h2) // 2
        out[y0:y0 + h2, x0:x0 + w2] = a2
        box = (x0, y0, x0 + w2, y0 + h2)
    else:
        x0, y0 = (w2 - W) // 2, (h2 - H) // 2
        out[:] = a2[y0:y0 + H, x0:x0 + W]
        box = (0, 0, W, H)
    return out, box, (w2 / W, h2 / H)

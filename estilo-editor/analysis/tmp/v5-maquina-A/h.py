"""Utilidades de medida para v5-maquina-A (solo lectura de fotogramas nativos)."""
import numpy as np
from PIL import Image
S = '/private/tmp/claude-501/-Users-alejandrorubiocamarero-Documents-ChatGPT-editor/1f516058-b06c-4444-a7f3-77af77afb931/scratchpad/v5A/full/'
FPS = 30000 / 1001
_cache = {}

def rgb(n):
    if n not in _cache:
        if len(_cache) > 60:
            _cache.pop(next(iter(_cache)))
        _cache[n] = np.asarray(Image.open(S + f'{n:05d}.jpg').convert('RGB'), np.float32)
    return _cache[n]

def luma(n):
    a = rgb(n)
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]

def down(a, k):
    H, W = a.shape[:2]
    H2, W2 = H // k * k, W // k * k
    a = a[:H2, :W2]
    if a.ndim == 2:
        return a.reshape(H2 // k, k, W2 // k, k).mean(axis=(1, 3))
    return a.reshape(H2 // k, k, W2 // k, k, a.shape[2]).mean(axis=(1, 3))

def bilinear(img, x, y):
    H, W = img.shape
    x0 = np.clip(np.floor(x).astype(int), 0, W - 2); y0 = np.clip(np.floor(y).astype(int), 0, H - 2)
    fx = np.clip(x - x0, 0, 1); fy = np.clip(y - y0, 0, 1)
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)

def align(I0, I1, mask=None, iters=40, p0=(0.0, 0.0, 0.0)):
    """Halla s,tx,ty tales que I1(x) ~ I0(c + s*(x-c) + t).  Devuelve (s, tx, ty, rms).
    Es decir: un punto x de I1 corresponde al punto c+s(x-c)+t de I0.  Si I1 es un alejamiento
    (zoom out) de I0, s>1.  Coordenadas en px de la imagen dada."""
    H, W = I0.shape
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = (W - 1) / 2, (H - 1) / 2
    gy, gx = np.gradient(I0)
    a, tx, ty = p0
    m = np.ones_like(I0, bool) if mask is None else mask
    for _ in range(iters):
        X = cx + (1 + a) * (xs - cx) + tx
        Y = cy + (1 + a) * (ys - cy) + ty
        inb = (X >= 1) & (X <= W - 2) & (Y >= 1) & (Y <= H - 2) & m
        w = bilinear(I0, X, Y); r = (I1 - w)
        Gx = bilinear(gx, X, Y); Gy = bilinear(gy, X, Y)
        J = np.stack([Gx * (xs - cx) + Gy * (ys - cy), Gx, Gy], -1)[inb]
        rr = r[inb]
        # robusto: recorta residuos grandes
        thr = np.percentile(np.abs(rr), 85) + 1e-3
        k = np.abs(rr) <= thr
        A = J[k].T @ J[k]; b = J[k].T @ rr[k]
        d = np.linalg.solve(A + 1e-6 * np.eye(3), b)
        a += d[0]; tx += d[1]; ty += d[2]
        if abs(d[0]) < 1e-7 and abs(d[1]) < 1e-4 and abs(d[2]) < 1e-4:
            break
    return 1 + a, tx, ty, float(np.sqrt((rr[k] ** 2).mean()))

def t(n):
    return n / FPS

def boxblur(a, r):
    """Desenfoque de caja separable de radio r (ventana 2r+1) con bordes reflejados."""
    k = 2 * r + 1
    p = np.pad(a, ((r, r), (r, r)), mode='reflect')
    c = np.cumsum(p, axis=0); c = np.vstack([np.zeros((1, c.shape[1]), c.dtype), c])
    v = (c[k:] - c[:-k]) / k
    c = np.cumsum(v, axis=1); c = np.hstack([np.zeros((c.shape[0], 1), c.dtype), c])
    return (c[:, k:] - c[:, :-k]) / k

def hp(n, k=2, r=12):
    """Luma a 1/k con paso alto y normalización local (insensible a cambios de brillo/contraste)."""
    a = down(luma(n), k).astype(np.float64)
    m = boxblur(a, r)
    s = np.sqrt(np.maximum(boxblur((a - m) ** 2, r), 1.0))
    return ((a - m) / (s + 4.0)).astype(np.float32)

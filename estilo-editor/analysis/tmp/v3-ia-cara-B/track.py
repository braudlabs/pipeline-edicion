"""Seguimiento de escala+traslación del fondo por NCC (numpy puro) para medir zooms digitales.
track(ref, frames, roi, scales): roi en px nativos del fotograma de referencia. Devuelve por fotograma (s, dx, dy, ncc):
el parche de ref, escalado por s, aparece en el fotograma n desplazado (dx,dy) respecto a su posición en ref."""
import sys
import numpy as np
from PIL import Image
sys.path.insert(0, 'analysis/tmp/v3-ia-cara-B')
import h

def gray(n, q):
    I = h.im(n).convert("L")
    return I.resize((1080 // q, 1920 // q), Image.BOX)

def ncc_map(img, tpl):
    """NCC de tpl (zero-mean) sobre img mediante FFT; devuelve mapa 'valid'."""
    H, W = img.shape; th, tw = tpl.shape
    t = tpl - tpl.mean()
    tn = np.sqrt((t ** 2).sum()) + 1e-6
    F = np.fft.rfft2(img, (H, W)); G = np.fft.rfft2(t[::-1, ::-1], (H, W))
    cc = np.fft.irfft2(F * G, (H, W))[th - 1:, tw - 1:]
    # energía local
    ii = np.pad(np.cumsum(np.cumsum(img, 0), 1), ((1, 0), (1, 0)))
    ii2 = np.pad(np.cumsum(np.cumsum(img ** 2, 0), 1), ((1, 0), (1, 0)))
    s1 = ii[th:, tw:] - ii[:-th, tw:] - ii[th:, :-tw] + ii[:-th, :-tw]
    s2 = ii2[th:, tw:] - ii2[:-th, tw:] - ii2[th:, :-tw] + ii2[:-th, :-tw]
    var = np.clip(s2 - s1 ** 2 / (th * tw), 1e-6, None)
    return cc[:var.shape[0], :var.shape[1]] / (np.sqrt(var) * tn)

def track(ref, frames, roi, scales, q=3, win=None):
    x0, y0, x1, y1 = [v // q for v in roi]
    R = gray(ref, q)
    T0 = R.crop((x0, y0, x1, y1))
    out = {}
    for n in frames:
        img = np.asarray(gray(n, q), np.float32)
        best = None
        for s in scales:
            tw, th = max(8, round((x1 - x0) * s)), max(8, round((y1 - y0) * s))
            tpl = np.asarray(T0.resize((tw, th), Image.BICUBIC), np.float32)
            if th >= img.shape[0] or tw >= img.shape[1]:
                continue
            m = ncc_map(img, tpl)
            if win:  # limitar la búsqueda a un entorno (px nativos) de la posición de referencia
                yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
                mask = (abs(xx - x0) <= win // q) & (abs(yy - y0) <= win // q)
                m = np.where(mask, m, -1)
            iy, ix = np.unravel_index(np.argmax(m), m.shape)
            v = m[iy, ix]
            if best is None or v > best[3]:
                # centro del parche encontrado
                cx = (ix + tw / 2) * q; cy = (iy + th / 2) * q
                best = (s, cx, cy, v)
        out[n] = best
    return out

if __name__ == "__main__":
    ref = int(sys.argv[1]); a = int(sys.argv[2]); b = int(sys.argv[3])
    roi = [int(v) for v in sys.argv[4].split(",")]
    smin, smax, sstep = [float(v) for v in sys.argv[5].split(",")]
    scales = np.arange(smin, smax + 1e-9, sstep)
    win = int(sys.argv[6]) if len(sys.argv) > 6 else None
    r = track(ref, range(a, b + 1), roi, scales, win=win)
    rcx = (roi[0] + roi[2]) / 2; rcy = (roi[1] + roi[3]) / 2
    print(f"# ref f{ref} roi {roi} centro ref ({rcx:.0f},{rcy:.0f})")
    for n in sorted(r):
        s, cx, cy, v = r[n]
        print(f"{n}\ts={s:.3f}\tcentro=({cx:.0f},{cy:.0f})\tncc={v:.3f}")

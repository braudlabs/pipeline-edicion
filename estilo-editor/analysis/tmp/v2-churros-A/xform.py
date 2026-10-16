"""Estima escala+traslación entre dos fotogramas (similaridad sin rotación) por correlación de fase,
usando solo una banda vertical del fotograma (para no medir los rótulos, que están fijos).
uso: xform.py A B [y0 y1] [pair]   (y0,y1 normalizados; por defecto 0 0.40)"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
FULL = Path(__file__).parent / "full"
SW, SH = 360, 640

def gray(n):
    return Image.open(FULL / f"f{n:05d}.jpg").convert("L").resize((SW, SH), Image.BILINEAR)

def grad(a):
    gx = np.zeros_like(a); gy = np.zeros_like(a)
    gx[:, 1:-1] = a[:, 2:] - a[:, :-2]; gy[1:-1] = a[2:] - a[:-2]
    return np.hypot(gx, gy)

def pc(a, b):
    win = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1])).astype(np.float32)
    Fa = np.fft.rfft2(a * win); Fb = np.fft.rfft2(b * win)
    R = Fa * np.conj(Fb); R /= np.abs(R) + 1e-6
    r = np.fft.irfft2(R, s=a.shape)
    i = np.unravel_index(np.argmax(r), r.shape)
    dy, dx = i
    if dy > a.shape[0] // 2: dy -= a.shape[0]
    if dx > a.shape[1] // 2: dx -= a.shape[1]
    return float(r[i]), dx, dy

def scaled(im, s):
    cx, cy = SW / 2, SH / 2
    return im.transform((SW, SH), Image.AFFINE, (1 / s, 0, cx - cx / s, 0, 1 / s, cy - cy / s), Image.BILINEAR)

def est(na, nb, band=(0.0, 0.40), scales=None, fine=True):
    r0, r1 = int(band[0] * SH), int(band[1] * SH)
    A = grad(np.asarray(gray(na), np.float32))[r0:r1]; imB = gray(nb)
    best = None
    scales = scales if scales is not None else np.arange(0.80, 1.2501, 0.01)
    for s in scales:
        p, dx, dy = pc(A, grad(np.asarray(scaled(imB, s), np.float32))[r0:r1])
        if best is None or p > best[0]: best = (p, s, dx, dy)
    if fine:
        s0 = best[1]
        for s in np.arange(s0 - 0.009, s0 + 0.0091, 0.001):
            p2, dx2, dy2 = pc(A, grad(np.asarray(scaled(imB, s), np.float32))[r0:r1])
            if p2 > best[0]: best = (p2, s, dx2, dy2)
    p, s, dx, dy = best
    # B escalado por s y desplazado (dx,dy) coincide con A  =>  el contenido de B respecto de A: escala 1/s
    k = 1080 / SW
    return p, 1 / s, -dx * k / s, -dy * k / s

if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    rest = sys.argv[3:]
    pair = "pair" in rest
    nums = [float(v) for v in rest if v != "pair"]
    band = (nums[0], nums[1]) if len(nums) >= 2 else (0.0, 0.40)
    if pair:
        p, s, dx, dy = est(a, b, band)
        print(f"f{a}->f{b}: pico {p:.3f} escala x{s:.4f} dx {dx:+.1f}px dy {dy:+.1f}px (banda {band})")
    else:
        for n in range(a, b):
            p, s, dx, dy = est(n, n + 1, band, np.arange(0.92, 1.0801, 0.01))
            flag = "" if (abs(s - 1) < 0.004 and abs(dx) < 7 and abs(dy) < 7 and p > 0.15) else "  <<<"
            print(f"f{n}->f{n+1}: pico {p:.3f} escala x{s:.4f} dx {dx:+.1f} dy {dy:+.1f}{flag}")

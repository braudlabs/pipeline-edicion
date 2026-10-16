#!/usr/bin/env python3
"""Ajusta una sombra paralela gaussiana: oscurecimiento = k * blur_sigma(máscara desplazada (ox,oy)).
  shadowfit.py A B x0 y0 x1 y1 [thr]
A = fotograma sin rótulo, B = con rótulo, mismo fondo.
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from lib import frames, gray
A, B, X0, Y0, X1, Y1 = [int(v) for v in sys.argv[1:7]]
thr = float(sys.argv[7]) if len(sys.argv) > 7 else 240
lo, hi = min(A, B), max(A, B)
F = frames(lo, hi).astype(np.float32)
a = gray(F[A - lo])[Y0:Y1, X0:X1]
b = gray(F[B - lo])[Y0:Y1, X0:X1]
mB = (F[B - lo].min(axis=2) >= thr)[Y0:Y1, X0:X1]
mA = (F[A - lo].min(axis=2) >= thr)[Y0:Y1, X0:X1]
m = (mB & ~mA).astype(np.float32)
def dil(z, n):
    for _ in range(n):
        e = z.copy(); e[1:, :] |= z[:-1, :]; e[:-1, :] |= z[1:, :]; e[:, 1:] |= z[:, :-1]; e[:, :-1] |= z[:, 1:]; z = e
    return z
near = dil(mB | mA, 3)
valid = (~near) & (a > 40) & (a < 235)
dark = 1 - b / np.maximum(a, 1)          # oscurecimiento observado
H, W = m.shape
fy = np.fft.fftfreq(H)[:, None]; fx = np.fft.rfftfreq(W)[None, :]
Mf = np.fft.rfft2(m)
best = None
for sigma in (12, 16, 20, 24, 28, 32, 36, 40, 46, 52):
    G = np.exp(-2 * (np.pi ** 2) * (sigma ** 2) * (fx ** 2 + fy ** 2))
    for oy in range(0, 61, 4):
        for ox in range(-8, 61, 4):
            ph = np.exp(-2j * np.pi * (fx * ox + fy * oy))
            s = np.fft.irfft2(Mf * G * ph, s=m.shape)
            sv = s[valid]; dv = dark[valid]
            k = float((sv * dv).sum() / max((sv * sv).sum(), 1e-9))
            e = float(np.sqrt(np.mean((k * sv - dv) ** 2)))
            if best is None or e < best[0]:
                best = (e, sigma, ox, oy, k)
e, sigma, ox, oy, k = best
print(f"mejor: sigma={sigma}px  desplazamiento=({ox:+d},{oy:+d})px  opacidad k={k:.3f}  rms={e:.4f}  (n={int(valid.sum())})")
# vecindad del óptimo
for sg in (sigma - 2, sigma, sigma + 2):
    if sg <= 0: continue
    G = np.exp(-2 * (np.pi ** 2) * (sg ** 2) * (fx ** 2 + fy ** 2))
    for (dx, dy) in ((ox, oy), (0, 0), (ox, 0), (0, oy)):
        ph = np.exp(-2j * np.pi * (fx * dx + fy * dy))
        s = np.fft.irfft2(Mf * G * ph, s=m.shape)
        sv = s[valid]; dv = dark[valid]
        kk = float((sv * dv).sum() / max((sv * sv).sum(), 1e-9))
        print(f"  sigma={sg} o=({dx:+d},{dy:+d}) k={kk:.3f} rms={float(np.sqrt(np.mean((kk*sv-dv)**2))):.4f}")

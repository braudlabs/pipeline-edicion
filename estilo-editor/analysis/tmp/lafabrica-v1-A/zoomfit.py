#!/usr/bin/env python3
"""Ajusta escala (alrededor de un centro) y traslación entre dos fotogramas: B ≈ escala(A).
  zoomfit.py fA fB [y0 y1] -> mejor escala y desplazamiento por búsqueda (MAD mínima) en media resolución.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from common import probe
from sheet import load_full
slug = "lafabrica-v1"; info = probe(slug)
fa, fb = int(sys.argv[1]), int(sys.argv[2])
y0, y1 = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, 1920)
x0, x1 = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (0, 1080)
A = load_full(slug, fa, info).convert("L"); B = load_full(slug, fb, info).convert("L")
W, H = A.size
Bn = np.asarray(B, np.float32)
def warp(s, tx, ty):
    # salida(x,y) = A(cx + (x-cx-tx)/s, cy + (y-cy-ty)/s)
    cx, cy = W / 2, H / 2
    a = 1 / s
    return np.asarray(A.transform((W, H), Image.AFFINE, (a, 0, cx - a * (cx + tx), 0, a, cy - a * (cy + ty)), resample=Image.BILINEAR), np.float32)
def cost(s, tx, ty):
    Wp = warp(s, tx, ty)
    m = 40
    return float(np.abs(Wp[y0 + m:y1 - m, x0 + m:x1 - m] - Bn[y0 + m:y1 - m, x0 + m:x1 - m]).mean())
best = (cost(1, 0, 0), 1.0, 0.0, 0.0)
base = best[0]
step_s, step_t = 0.004, 4.0
s, tx, ty = 1.0, 0.0, 0.0
for it in range(6):
    improved = True
    while improved:
        improved = False
        for ds, dx, dy in [(step_s, 0, 0), (-step_s, 0, 0), (0, step_t, 0), (0, -step_t, 0), (0, 0, step_t), (0, 0, -step_t)]:
            c = cost(s + ds, tx + dx, ty + dy)
            if c < best[0] - 1e-4:
                best = (c, s + ds, tx + dx, ty + dy); s, tx, ty = best[1:]; improved = True
    step_s /= 2; step_t /= 2
print(f"f{fa}->f{fb}: MAD sin ajustar {base:.2f} -> ajustada {best[0]:.2f}  escala {best[1]:.4f}  dx {best[2]:+.2f} dy {best[3]:+.2f}")

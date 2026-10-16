#!/usr/bin/env python3
"""Ajuste de escala (alrededor del centro del fotograma) + traslación entre pares de fotogramas.

  zf.py "137:138,138:139" x0,y0,x1,y1 [--mask "x0,y0,x1,y1;..."]
B ≈ escala(A, s) desplazada (dx, dy). Busca el mínimo de la diferencia absoluta media en la región
(en píxeles del original). Sirve para separar el zoom aplicado por el editor (afecta igual a metraje
y rótulos, y existe aunque el metraje esté congelado) del movimiento propio del metraje.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from common import probe  # noqa: E402
from sheet import load_full  # noqa: E402

slug = "lafabrica-v1"
info = probe(slug)
cache = {}


def frame(n):
    if n not in cache:
        cache[n] = load_full(slug, n, info).convert("L")
    return cache[n]


def fit(fa, fb, roi, masks=()):
    A, B = frame(fa), frame(fb)
    W, H = A.size
    x0, y0, x1, y1 = roi
    Bn = np.asarray(B, np.float32)[y0:y1, x0:x1]
    keep = np.ones(Bn.shape, bool)
    for (mx0, my0, mx1, my1) in masks:
        keep[max(0, my0 - y0):max(0, my1 - y0), max(0, mx0 - x0):max(0, mx1 - x0)] = False

    def cost(s, tx, ty):
        cx, cy = W / 2, H / 2
        a = 1 / s
        Wp = np.asarray(A.transform((W, H), Image.AFFINE, (a, 0, cx - a * (cx + tx), 0, a, cy - a * (cy + ty)),
                                    resample=Image.BILINEAR), np.float32)[y0:y1, x0:x1]
        return float(np.abs(Wp - Bn)[keep].mean())

    base = cost(1, 0, 0)
    best = (base, 1.0, 0.0, 0.0)
    s, tx, ty = 1.0, 0.0, 0.0
    step_s, step_t = 0.004, 4.0
    for _ in range(7):
        improved = True
        while improved:
            improved = False
            for ds, dx, dy in [(step_s, 0, 0), (-step_s, 0, 0), (0, step_t, 0), (0, -step_t, 0), (0, 0, step_t), (0, 0, -step_t)]:
                c = cost(s + ds, tx + dx, ty + dy)
                if c < best[0] - 1e-4:
                    best = (c, s + ds, tx + dx, ty + dy)
                    s, tx, ty = best[1:]
                    improved = True
        step_s /= 2
        step_t /= 2
    return base, best


def main():
    pairs = [tuple(int(v) for v in p.split(":")) for p in sys.argv[1].split(",")]
    roi = tuple(int(v) for v in sys.argv[2].split(",")) if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else (40, 40, 1040, 1880)
    masks = []
    if "--mask" in sys.argv:
        masks = [tuple(int(v) for v in m.split(",")) for m in sys.argv[sys.argv.index("--mask") + 1].split(";")]
    for fa, fb in pairs:
        base, best = fit(fa, fb, roi, masks)
        n = fb - fa
        print(f"f{fa}->f{fb}: MAD {base:.2f} -> {best[0]:.2f}  escala {best[1]:.4f} ({(best[1] ** (1 / n) - 1) * 100:+.3f} %/f)  dx {best[2]:+.2f} dy {best[3]:+.2f}")


if __name__ == "__main__":
    main()

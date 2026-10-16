#!/usr/bin/env python3
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from common import probe
from sheet import load_full_run
slug = "lafabrica-v1"; info = probe(slug)
a, b = int(sys.argv[1]), int(sys.argv[2])
imgs = load_full_run(slug, a, b - a + 1, info)
prev = None
for k, im in enumerate(imgs):
    A = np.asarray(im, np.float32)
    R, G, B = A[..., 0], A[..., 1], A[..., 2]
    # objeto: gris/negro neutro (no azul) dentro de la zona central
    sub = A[600:1320, 180:900]
    r, g, bl = sub[..., 0], sub[..., 1], sub[..., 2]
    neutral = (np.abs(r - bl) < 22) & (np.abs(r - g) < 18)
    dark = neutral & (r < 175)
    ys, xs = np.nonzero(dark)
    if len(xs) < 80:
        print(f"f{a+k}: -"); continue
    cx, cy = xs.mean(), ys.mean()
    C = np.cov(np.vstack([xs - cx, ys - cy]))
    w, v = np.linalg.eigh(C)
    ax = v[:, 1]
    ang = np.degrees(np.arctan2(-ax[1], ax[0]))  # ángulo sobre la horizontal (y hacia arriba)
    if ang < -90: ang += 180
    if ang > 90: ang -= 180
    x0, x1 = np.percentile(xs, [1, 99]); y0, y1 = np.percentile(ys, [1, 99])
    print(f"f{a+k}: área {len(xs):6d}  centro ({180+cx:.0f},{600+cy:.0f})  caja {x1-x0:.0f}x{y1-y0:.0f}  eje mayor {ang:+.1f}°  σ {np.sqrt(w[1]):.0f}/{np.sqrt(w[0]):.0f}")

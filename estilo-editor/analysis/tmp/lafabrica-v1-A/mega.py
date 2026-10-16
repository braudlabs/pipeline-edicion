#!/usr/bin/env python3
"""Escena del megáfono (f102-f136): disco blanco y dos líneas de texto crema, fotograma a fotograma."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from common import probe
from sheet import load_full_run
slug = "lafabrica-v1"; info = probe(slug)
a, b = int(sys.argv[1]), int(sys.argv[2])
imgs = load_full_run(slug, a, b - a + 1, info)

def runs(v, gap=10):
    idx = np.nonzero(v)[0]
    if len(idx) == 0:
        return []
    sp = np.split(idx, np.nonzero(np.diff(idx) > gap)[0] + 1)
    return [(int(s[0]), int(s[-1])) for s in sp]

for k, im in enumerate(imgs):
    A = np.asarray(im, np.float32)
    R, G, B = A[..., 0], A[..., 1], A[..., 2]
    mn = A.min(axis=2)
    # disco: blanco neutro
    disc = (mn > 150) & (np.abs(R - B) < 10)
    # extensión horizontal del disco en la fila central y vertical en la columna central (desde fuera)
    row = disc[940:1000].sum(axis=0) > 30
    col = disc[:, 150:930].sum(axis=1) > 60
    xs = np.nonzero(row)[0]; ys = np.nonzero(col)[0]
    if len(xs) and len(ys):
        dx0, dx1, dy0, dy1 = xs[0], xs[-1], ys[0], ys[-1]
        dtxt = f"disco x {dx0}-{dx1} (Ø{dx1-dx0+1}) y {dy0}-{dy1} (Ø{dy1-dy0+1}) c=({(dx0+dx1)/2:.0f},{(dy0+dy1)/2:.0f})"
    else:
        dtxt = "disco -"
    cream = (np.minimum(R, G) > 120) & ((R + G) / 2 - B > 10)
    out = []
    for name, (y0, y1) in {"L1": (560, 800), "L2": (1120, 1360)}.items():
        M = cream[y0:y1]
        if M.sum() < 40:
            out.append(f"{name} -"); continue
        yy, xx = np.nonzero(M)
        cols = M.sum(axis=0) >= 2
        ws = runs(cols, gap=14)
        pk = float(np.percentile(A[y0:y1][M].sum(axis=1), 95)) / 3
        out.append(f"{name} x {xx.min()}-{xx.max()} y {y0+yy.min()}-{y0+yy.max()} nivel {pk:.0f} tramos " + " ".join(f"[{s}-{e}]" for s, e in ws))
    print(f"f{a+k}: {dtxt} | " + " | ".join(out))

#!/usr/bin/env python3
"""Medidas propias del revisor v1-pagado-C (solo lectura del vídeo; escribe solo por stdout).

  ink.py --range A:B --roi x,y,w,h [--thr 240] [--final F --bgref F0] [--px]

Por fotograma: caja de los píxeles con canal mínimo >= thr (tinta blanca), área, y si se dan
--final y --bgref, la opacidad estimada alfa = (I_f - I_bg) / (I_final - I_bg) sobre el núcleo
de la tinta del fotograma --final (máscara erosionada). Vale para rótulos que no se mueven.
--roi en fracción 0..1 salvo con --px (píxeles x,y,w,h).
"""
import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from common import probe, t_of  # noqa: E402
from sheet import load_full_run, load_full  # noqa: E402

SLUG = "v1-pagado"


def erode(m, n=2):
    for _ in range(n):
        k = m.copy()
        k[1:] &= m[:-1]
        k[:-1] &= m[1:]
        k[:, 1:] &= m[:, :-1]
        k[:, :-1] &= m[:, 1:]
        m = k
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--range", required=True)
    ap.add_argument("--roi", default="0,0,1,1")
    ap.add_argument("--px", action="store_true")
    ap.add_argument("--thr", type=float, default=240)
    ap.add_argument("--final", type=int)
    ap.add_argument("--bgref", type=int)
    ap.add_argument("--erode", type=int, default=2)
    a = ap.parse_args()
    info = probe(SLUG)
    f0, f1 = [int(v) for v in a.range.split(":")[:2]]
    lo = min([f0] + [v for v in (a.final, a.bgref) if v is not None])
    hi = max([f1] + [v for v in (a.final, a.bgref) if v is not None])
    imgs = load_full_run(SLUG, lo, hi - lo + 1, info)
    get = lambda f: np.asarray(imgs[f - lo], np.float32)
    W, H = imgs[0].size
    x, y, w, h = [float(v) for v in a.roi.split(",")]
    if a.px:
        X0, Y0, X1, Y1 = int(x), int(y), int(x + w), int(y + h)
    else:
        X0, Y0, X1, Y1 = int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)
    core = None
    if a.final is not None:
        F = get(a.final)[Y0:Y1, X0:X1]
        core = erode(F.min(axis=2) >= a.thr, a.erode)
        If = F.mean(axis=2)[core].mean() if core.any() else 0
        Ib = get(a.bgref)[Y0:Y1, X0:X1].mean(axis=2)[core].mean() if (a.bgref is not None and core.any()) else 0
        print(f"# núcleo de tinta en f{a.final}: {int(core.sum())} px; I_final={If:.1f} I_fondo(f{a.bgref})={Ib:.1f}")
    print(f"# región px [{X0},{Y0}]-[{X1},{Y1}] thr={a.thr}")
    print("f\tt\tx0\ty0\tx1\ty1\tcx\tcy\tancho\talto\tarea\talfa")
    for f in range(f0, f1 + 1):
        A = get(f)[Y0:Y1, X0:X1]
        d = A.min(axis=2)
        mask = d >= a.thr
        alfa = ""
        if core is not None and core.any():
            I = A.mean(axis=2)[core].mean()
            alfa = f"{(I - Ib) / max(1e-6, (If - Ib)):.3f}"
        if mask.sum() < 30:
            print(f"{f}\t{t_of(f, info):.3f}\t-\t-\t-\t-\t-\t-\t-\t-\t{int(mask.sum())}\t{alfa}")
            continue
        ys, xs = np.nonzero(mask)
        bx0, bx1 = np.percentile(xs, [0.3, 99.7])
        by0, by1 = np.percentile(ys, [0.3, 99.7])
        print(f"{f}\t{t_of(f, info):.3f}\t{X0 + bx0:.0f}\t{Y0 + by0:.0f}\t{X0 + bx1:.0f}\t{Y0 + by1:.0f}\t"
              f"{X0 + (bx0 + bx1) / 2:.1f}\t{Y0 + (by0 + by1) / 2:.1f}\t{bx1 - bx0:.0f}\t{by1 - by0:.0f}\t{int(mask.sum())}\t{alfa}")


if __name__ == "__main__":
    main()

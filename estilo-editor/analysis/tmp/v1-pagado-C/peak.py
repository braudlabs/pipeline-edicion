#!/usr/bin/env python3
"""peak.py --range A:B --roi x,y,w,h(px) [--bg F]
Por fotograma: percentiles del canal mínimo en la región (p50 p90 p98 p99.5) y, con --bg F,
alfa estimada = (p99.5_f - B)/(255 - B), con B = p50 de la región en el fotograma F sin rótulo.
Además caja de los píxeles >= mitad de camino entre B y p99.5 (sigue al rótulo mientras funde).
"""
import argparse, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from common import probe, t_of
from sheet import load_full_run
SLUG = "v1-pagado"
ap = argparse.ArgumentParser()
ap.add_argument("--range", required=True)
ap.add_argument("--roi", required=True)
ap.add_argument("--bg", type=int)
ap.add_argument("--bgval", type=float)
ap.add_argument("--slug", default=SLUG)
a = ap.parse_args()
info = probe(a.slug)
f0, f1 = [int(v) for v in a.range.split(":")[:2]]
lo = min(f0, a.bg) if a.bg is not None else f0
imgs = load_full_run(a.slug, lo, f1 - lo + 1, info)
x, y, w, h = [int(float(v)) for v in a.roi.split(",")]
B = None
if a.bg is not None:
    Bg = np.asarray(imgs[a.bg - lo], np.float32)[y:y+h, x:x+w].min(axis=2)
    B = float(np.percentile(Bg, 50))
    print(f"# fondo f{a.bg}: p50={B:.0f} p90={np.percentile(Bg,90):.0f} p99.5={np.percentile(Bg,99.5):.0f}")
if a.bgval is not None:
    B = a.bgval
print("f\tt\tp50\tp90\tp98\tp99.5\talfa\tx0\ty0\tx1\ty1\tcx\tcy\tw\th")
for f in range(f0, f1 + 1):
    A = np.asarray(imgs[f - lo], np.float32)[y:y+h, x:x+w].min(axis=2)
    p50, p90, p98, p995 = np.percentile(A, [50, 90, 98, 99.5])
    al = ""
    box = "\t-\t-\t-\t-\t-\t-\t-\t-"
    if B is not None:
        alv = (p995 - B) / (255 - B)
        al = f"{alv:.2f}"
        if alv > 0.12:
            thr = B + 0.6 * (p995 - B)
            m = A >= thr
            if m.sum() > 30:
                ys, xs = np.nonzero(m)
                bx0, bx1 = np.percentile(xs, [0.5, 99.5]); by0, by1 = np.percentile(ys, [0.5, 99.5])
                box = f"\t{x+bx0:.0f}\t{y+by0:.0f}\t{x+bx1:.0f}\t{y+by1:.0f}\t{x+(bx0+bx1)/2:.1f}\t{y+(by0+by1)/2:.1f}\t{bx1-bx0:.0f}\t{by1-by0:.0f}"
    print(f"{f}\t{t_of(f, info):.3f}\t{p50:.0f}\t{p90:.0f}\t{p98:.0f}\t{p995:.0f}\t{al}{box}")

#!/usr/bin/env python3
"""Mide a resolución nativa, fotograma a fotograma, una caja estimada de la tinta de un rótulo.

  inkbox.py <slug> --range A:B --roi x,y,w,h [--mode bg|white|color] [--color R,G,B] [--thr N]

  --roi    región de búsqueda, normalizada 0..1 (x, y, ancho, alto)
  --mode   bg     fondo plano: es tinta lo que se aparta del color de fondo (mediana del borde de la región)
           white  texto blanco sobre imagen: es tinta lo que supera el umbral de blanco
           color  es tinta lo que se acerca al color dado
Sale una línea por fotograma: caja x0 y0 x1 y1, centro, ancho, alto, área de tinta y
«fuerza»: white usa media normalizada 0..1; bg usa percentil 90 de distancia
RGB/255 y puede alcanzar √3. No mide alpha. Caja por percentiles 0.2–99.8%,
condicionada por ROI/umbral; ruido, fondo móvil y clipping pueden contaminarla.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import probe, t_of  # noqa: E402
from sheet import load_full_run  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--range", required=True)
    ap.add_argument("--roi", default="0,0,1,1")
    ap.add_argument("--mode", default="bg", choices=["bg", "white", "color"])
    ap.add_argument("--color")
    ap.add_argument("--thr", type=float)
    a = ap.parse_args()
    info = probe(a.slug)
    f0, f1 = [int(v) for v in a.range.split(":")[:2]]
    x, y, w, h = [float(v) for v in a.roi.split(",")]
    imgs = load_full_run(a.slug, f0, f1 - f0 + 1, info)
    W, H = imgs[0].size
    X0, Y0, X1, Y1 = int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)
    print(f"# {a.slug} f{f0}-f{f1}  región px [{X0},{Y0}]-[{X1},{Y1}]  modo {a.mode}")
    print("f\tt\tx0\ty0\tx1\ty1\tcx\tcy\tancho\talto\tarea\tfuerza")
    for k, im in enumerate(imgs):
        A = np.asarray(im, np.float32)[Y0:Y1, X0:X1]
        if a.mode == "white":
            thr = a.thr or 225
            d = A.min(axis=2)
            mask = d >= thr
            strength = (d[mask].mean() - thr) / (255 - thr) if mask.any() else 0
        else:
            if a.mode == "bg":
                border = np.concatenate([A[:6].reshape(-1, 3), A[-6:].reshape(-1, 3), A[:, :6].reshape(-1, 3), A[:, -6:].reshape(-1, 3)])
                ref = np.median(border, axis=0)
                d = np.sqrt(((A - ref) ** 2).sum(axis=2))
                thr = a.thr or 40
                mask = d >= thr
            else:
                ref = np.array([float(v) for v in a.color.split(",")], np.float32)
                d = np.sqrt(((A - ref) ** 2).sum(axis=2))
                thr = a.thr or 60
                mask = d <= thr
                d = 255 - d
            strength = float(np.percentile(d[mask], 90)) / 255 if mask.any() else 0
        f = f0 + k
        if mask.sum() < 30:
            print(f"{f}\t{t_of(f, info):.4f}\t-\t-\t-\t-\t-\t-\t-\t-\t{int(mask.sum())}\t0")
            continue
        ys, xs = np.nonzero(mask)
        # recorta el 0,2 % extremo para que una mota suelta no mueva la caja
        bx0, bx1 = np.percentile(xs, [0.2, 99.8])
        by0, by1 = np.percentile(ys, [0.2, 99.8])
        print(f"{f}\t{t_of(f, info):.4f}\t{X0 + bx0:.0f}\t{Y0 + by0:.0f}\t{X0 + bx1:.0f}\t{Y0 + by1:.0f}\t"
              f"{X0 + (bx0 + bx1) / 2:.1f}\t{Y0 + (by0 + by1) / 2:.1f}\t{bx1 - bx0:.0f}\t{by1 - by0:.0f}\t{int(mask.sum())}\t{strength:.3f}")


if __name__ == "__main__":
    main()

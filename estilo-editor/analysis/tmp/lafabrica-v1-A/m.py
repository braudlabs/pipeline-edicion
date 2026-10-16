#!/usr/bin/env python3
"""Medidas auxiliares del tramo lafabrica-v1-A (solo numpy + PIL).

  m.py edge  <slug> A:B --roi x,y,w,h [--frac 0.5] [--dark]
      Por fotograma: nivel de fondo, pico de blanco, caja de la tinta con umbral adaptativo
      (fondo + frac*(pico-fondo)), nitidez (gradiente p99 normalizado) y área.
  m.py track <slug> A:B --pts "x,y;x,y" [--half 28] [--rad 26] [--ref A]
      Sigue puntos del metraje por SSD (plantilla del fotograma anterior). Imprime x,y por
      fotograma y la distancia entre los dos primeros puntos (escala relativa).
  m.py lum   <slug> A:B --roi x,y,w,h
      Luminancia media y mediana de la región por fotograma (para oscurecimientos y destellos).
  m.py diff  <slug> A:B [--roi x,y,w,h]
      Diferencia absoluta media con el fotograma anterior (para repetidos y cadencia).
  m.py prof  <slug> F --roi x,y,w,h [--axis y] [--frac 0.5]
      Perfil de tinta por filas (o columnas): tramos con tinta, para medir altura de x, trazos, etc.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from common import probe, t_of  # noqa: E402
from sheet import load_full_run  # noqa: E402


def frames(slug, a, b, info, chunk=24):
    f = a
    while f <= b:
        n = min(chunk, b - f + 1)
        imgs = load_full_run(slug, f, n, info)
        for k, im in enumerate(imgs):
            yield f + k, np.asarray(im, np.float32)
        f += n


def roi_px(roi, W, H):
    x, y, w, h = [float(v) for v in roi.split(",")]
    return int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)


def lum(A):
    return 0.299 * A[..., 0] + 0.587 * A[..., 1] + 0.114 * A[..., 2]


def cmd_edge(a):
    info = probe(a.slug)
    f0, f1 = [int(v) for v in a.range.split(":")]
    print("f\tt\tfondo\tpico\tx0\ty0\tx1\ty1\tcx\tcy\tancho\talto\tarea\tnitidez")
    for f, A in frames(a.slug, f0, f1, info):
        H, W = A.shape[:2]
        X0, Y0, X1, Y1 = roi_px(a.roi, W, H)
        R = A[Y0:Y1, X0:X1]
        d = R.min(axis=2) if not a.dark else 255 - R.max(axis=2)
        bg = float(np.median(d))
        pk = float(np.percentile(d, 99.7))
        thr = bg + a.frac * (pk - bg)
        mask = d >= thr
        L = lum(R)
        gx = np.abs(np.diff(L, axis=1))
        sharp = float(np.percentile(gx, 99.5)) / max(1.0, pk - bg)
        if mask.sum() < 30 or pk - bg < 12:
            print(f"{f}\t{t_of(f, info):.3f}\t{bg:.0f}\t{pk:.0f}\t-\t-\t-\t-\t-\t-\t-\t-\t{int(mask.sum())}\t{sharp:.3f}")
            continue
        ys, xs = np.nonzero(mask)
        bx0, bx1 = np.percentile(xs, [0.2, 99.8])
        by0, by1 = np.percentile(ys, [0.2, 99.8])
        print(f"{f}\t{t_of(f, info):.3f}\t{bg:.0f}\t{pk:.0f}\t{X0 + bx0:.0f}\t{Y0 + by0:.0f}\t{X0 + bx1:.0f}\t{Y0 + by1:.0f}\t"
              f"{X0 + (bx0 + bx1) / 2:.1f}\t{Y0 + (by0 + by1) / 2:.1f}\t{bx1 - bx0:.0f}\t{by1 - by0:.0f}\t{int(mask.sum())}\t{sharp:.3f}")


def cmd_track(a):
    info = probe(a.slug)
    f0, f1 = [int(v) for v in a.range.split(":")]
    pts = [[float(v) for v in p.split(",")] for p in a.pts.split(";")]
    h, r = a.half, a.rad
    prev = None
    d0 = None
    print("f\tt\t" + "\t".join(f"x{i}\ty{i}\terr{i}" for i in range(len(pts))) + "\tdist\tescala")
    for f, A in frames(a.slug, f0, f1, info):
        G = lum(A)
        H, W = G.shape
        row = []
        if prev is not None:
            for i, (px, py) in enumerate(pts):
                px, py = int(round(px)), int(round(py))
                tx0, ty0 = max(0, px - h), max(0, py - h)
                T = prev[ty0:py + h, tx0:px + h]
                th, tw = T.shape
                best = (1e18, 0, 0)
                Tm = T - T.mean()
                for dy in range(-r, r + 1, 1):
                    yy = ty0 + dy
                    if yy < 0 or yy + th > H:
                        continue
                    for dx in range(-r, r + 1, 1):
                        xx = tx0 + dx
                        if xx < 0 or xx + tw > W:
                            continue
                        C = G[yy:yy + th, xx:xx + tw]
                        e = float(((C - C.mean() - Tm) ** 2).mean())
                        if e < best[0]:
                            best = (e, dx, dy)
                pts[i] = [pts[i][0] + best[1], pts[i][1] + best[2]]
                row.append(f"{pts[i][0]:.0f}\t{pts[i][1]:.0f}\t{best[0]:.0f}")
        else:
            for i, (px, py) in enumerate(pts):
                row.append(f"{px:.0f}\t{py:.0f}\t0")
        dist = float(np.hypot(pts[0][0] - pts[1][0], pts[0][1] - pts[1][1])) if len(pts) > 1 else 0
        if d0 is None:
            d0 = dist or 1
        print(f"{f}\t{t_of(f, info):.3f}\t" + "\t".join(row) + f"\t{dist:.1f}\t{dist / d0:.4f}")
        prev = G


def cmd_lum(a):
    info = probe(a.slug)
    f0, f1 = [int(v) for v in a.range.split(":")]
    print("f\tt\tmedia\tmediana\tp05\tp95\tR\tG\tB")
    for f, A in frames(a.slug, f0, f1, info):
        H, W = A.shape[:2]
        X0, Y0, X1, Y1 = roi_px(a.roi, W, H)
        R = A[Y0:Y1, X0:X1]
        L = lum(R)
        m = R.reshape(-1, 3).mean(axis=0)
        print(f"{f}\t{t_of(f, info):.3f}\t{L.mean():.1f}\t{np.median(L):.1f}\t{np.percentile(L, 5):.1f}\t{np.percentile(L, 95):.1f}\t{m[0]:.0f}\t{m[1]:.0f}\t{m[2]:.0f}")


def cmd_diff(a):
    info = probe(a.slug)
    f0, f1 = [int(v) for v in a.range.split(":")]
    prev = None
    print("f\tt\tmad")
    for f, A in frames(a.slug, f0, f1, info):
        H, W = A.shape[:2]
        X0, Y0, X1, Y1 = roi_px(a.roi, W, H)
        R = lum(A[Y0:Y1, X0:X1])
        if prev is not None:
            print(f"{f}\t{t_of(f, info):.3f}\t{np.abs(R - prev).mean():.2f}")
        prev = R


def runs(v):
    out, start = [], None
    for i, b in enumerate(v):
        if b and start is None:
            start = i
        if not b and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(v) - 1))
    return out


def cmd_prof(a):
    info = probe(a.slug)
    f = int(a.range)
    for _, A in frames(a.slug, f, f, info):
        H, W = A.shape[:2]
        X0, Y0, X1, Y1 = roi_px(a.roi, W, H)
        R = A[Y0:Y1, X0:X1]
        d = R.min(axis=2) if not a.dark else 255 - R.max(axis=2)
        bg = float(np.median(d))
        pk = float(np.percentile(d, 99.7))
        thr = bg + a.frac * (pk - bg)
        mask = d >= thr
        ax = 1 if a.axis == "y" else 0
        cnt = mask.sum(axis=ax)
        off = Y0 if a.axis == "y" else X0
        print(f"# f{f} fondo {bg:.0f} pico {pk:.0f} umbral {thr:.0f}; tramos con tinta a lo largo de {a.axis} (inicio-fin px, tamaño, tinta máx)")
        for s, e in runs(cnt >= a.minink):
            print(f"{off + s}\t{off + e}\t{e - s + 1}\t{int(cnt[s:e + 1].max())}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["edge", "track", "lum", "diff", "prof"])
    ap.add_argument("slug")
    ap.add_argument("range")
    ap.add_argument("--roi", default="0,0,1,1")
    ap.add_argument("--frac", type=float, default=0.5)
    ap.add_argument("--dark", action="store_true")
    ap.add_argument("--pts")
    ap.add_argument("--half", type=int, default=28)
    ap.add_argument("--rad", type=int, default=26)
    ap.add_argument("--axis", default="y")
    ap.add_argument("--minink", type=int, default=3)
    a = ap.parse_args()
    {"edge": cmd_edge, "track": cmd_track, "lum": cmd_lum, "diff": cmd_diff, "prof": cmd_prof}[a.cmd](a)


if __name__ == "__main__":
    main()

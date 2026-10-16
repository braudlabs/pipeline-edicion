#!/usr/bin/env python3
"""Seguimiento subpíxel de un rótulo por correlación normalizada (NCC) con una plantilla binaria.

  track.py A B --ref F --box x0,y0,x1,y1 [--thr 240] [--sx 140] [--sy 30] [--scales 0.94:1.06:0.01]
               [--bg FRAME] [--slug v6-ads90-rev] [--mode white|color --color R,G,B --cthr 60]
               [--sig 0,2,4,8] [--split x1,x2,...]

  --ref    fotograma en el que el rótulo está completo y opaco (de ahí sale la plantilla)
  --box    caja (px del original) que contiene el rótulo en el fotograma de referencia
  --bg     fotograma sin el rótulo con el mismo fondo (para estimar la opacidad por mezcla)
  --split  cortes en x (px, en coordenadas del fotograma de referencia) para medir la opacidad por tramos (palabras)

Sale por fotograma: dx, dy (desplazamiento respecto a la referencia), escala, NCC, opacidad estimada
(dentro frente a anillo exterior) y, si hay --bg, opacidad por mezcla con el fondo.
"""
import argparse

import numpy as np
from PIL import Image, ImageFilter

from lib import run, arr, luma, info, t_of


def box_sums(P, h, w):
    """Suma y suma de cuadrados de P en ventanas h×w (posiciones válidas)."""
    def integ(A):
        S = np.zeros((A.shape[0] + 1, A.shape[1] + 1), np.float64)
        S[1:, 1:] = A.cumsum(0).cumsum(1)
        return S
    S1 = integ(P)
    S2 = integ(P * P)
    def win(S):
        return S[h:, w:] - S[:-h, w:] - S[h:, :-w] + S[:-h, :-w]
    return win(S1), win(S2)


def ncc_map(P, T):
    """NCC de la plantilla T (float, cualquier rango) sobre el parche P. Devuelve mapa (H-h+1, W-w+1)."""
    H, W = P.shape
    h, w = T.shape
    T0 = T - T.mean()
    tn = np.sqrt((T0 * T0).sum())
    F = np.fft.rfft2(P, s=(H, W))
    G = np.fft.rfft2(T0, s=(H, W))
    c = np.fft.irfft2(F * np.conj(G), s=(H, W))[: H - h + 1, : W - w + 1]
    s1, s2 = box_sums(P.astype(np.float64), h, w)
    var = np.maximum(s2 - s1 * s1 / (h * w), 1e-6)
    return c / (tn * np.sqrt(var))


def subpix(m, iy, ix):
    def par(a, b, c):
        d = a - 2 * b + c
        return 0.0 if abs(d) < 1e-12 else 0.5 * (a - c) / d
    oy = par(m[iy - 1, ix], m[iy, ix], m[iy + 1, ix]) if 0 < iy < m.shape[0] - 1 else 0.0
    ox = par(m[iy, ix - 1], m[iy, ix], m[iy, ix + 1]) if 0 < ix < m.shape[1] - 1 else 0.0
    return iy + oy, ix + ox


def resize_mask(M, s):
    h, w = M.shape
    im = Image.fromarray((M * 255).astype(np.uint8))
    nh, nw = max(2, round(h * s)), max(2, round(w * s))
    return np.asarray(im.resize((nw, nh), Image.BICUBIC), np.float32) / 255.0, nh / h, nw / w


def blur_mask(M, sig):
    if sig <= 0:
        return M
    im = Image.fromarray((M * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(sig)), np.float32) / 255.0


def morph(M, r, op):
    im = Image.fromarray((M > 0.5).astype(np.uint8) * 255)
    k = 2 * r + 1
    im = im.filter(ImageFilter.MaxFilter(k) if op == "dil" else ImageFilter.MinFilter(k))
    return np.asarray(im) > 127


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a", type=int)
    ap.add_argument("b", type=int)
    ap.add_argument("--ref", type=int, required=True)
    ap.add_argument("--box", required=True)
    ap.add_argument("--thr", type=float, default=240)
    ap.add_argument("--sx", type=int, default=140)
    ap.add_argument("--sy", type=int, default=30)
    ap.add_argument("--scales", default="1:1:1")
    ap.add_argument("--bg", type=int)
    ap.add_argument("--slug", default="v6-ads90-rev")
    ap.add_argument("--mode", default="white")
    ap.add_argument("--color")
    ap.add_argument("--cthr", type=float, default=60)
    ap.add_argument("--sig", default="0")
    ap.add_argument("--split")
    ap.add_argument("--savemask")
    ap.add_argument("--gamma", action="store_true", help="con --bg: alfa en código y en luz lineal, por brillo del fondo")
    a = ap.parse_args()

    x0, y0, x1, y1 = [int(v) for v in a.box.split(",")]
    inf = info(a.slug)
    ref = arr(run(a.ref, a.ref, a.slug)[0])
    R = ref[y0:y1, x0:x1]
    if a.mode == "white":
        M = (R.min(axis=2) >= a.thr).astype(np.float32)
    else:
        col = np.array([float(v) for v in a.color.split(",")], np.float32)
        M = (np.sqrt(((R - col) ** 2).sum(axis=2)) <= a.cthr).astype(np.float32)
    ys, xs = np.nonzero(M)
    # recorta la plantilla a la tinta
    ty0, ty1, tx0, tx1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    M = M[ty0:ty1, tx0:tx1]
    bx0, by0 = x0 + tx0, y0 + ty0          # esquina de la tinta en la referencia
    h, w = M.shape
    print(f"# plantilla f{a.ref}: tinta x {bx0}-{bx0 + w - 1}  y {by0}-{by0 + h - 1}  ({w}x{h} px)  área {int(M.sum())}")
    if a.savemask:
        Image.fromarray((M * 255).astype(np.uint8)).save(a.savemask)

    s0, s1, ds = [float(v) for v in a.scales.split(":")]
    scales = [1.0] if s0 == s1 else list(np.arange(s0, s1 + 1e-9, ds))
    sigs = [float(v) for v in a.sig.split(",")]
    bg = arr(run(a.bg, a.bg, a.slug)[0]) if a.bg is not None else None
    splits = [int(v) for v in a.split.split(",")] if a.split else []

    inner = morph(M, 2, "ero")
    ring = morph(M, 9, "dil") & ~morph(M, 4, "dil")
    pad = 12
    Mp = np.pad(M, pad)
    ring = morph(Mp, 9, "dil") & ~morph(Mp, 4, "dil")
    innerp = np.pad(inner, pad)

    frames = run(a.a, a.b, a.slug)
    Hh, Ww = ref.shape[:2]
    hdr = "f\tt\tdx\tdy\tx0\tcx\tescala\tsigma\tncc\talfa_anillo"
    if bg is not None:
        hdr += "\talfa_fondo"
        if a.gamma:
            hdr += "\tosc(cod/lin)\tmed(cod/lin)\tclaro(cod/lin)"
    for k in range(len(splits) + 1 if splits else 0):
        hdr += f"\talfa_t{k}"
    print(hdr)
    for i, im in enumerate(frames):
        f = a.a + i
        A = arr(im)
        L = luma(A)
        best = None
        for s in scales:
            Ms, sy_, sx_ = resize_mask(M, s) if s != 1.0 else (M, 1.0, 1.0)
            hs, ws = Ms.shape
            # la escala se aplica respecto al centro de la tinta
            cx_ref, cy_ref = bx0 + w / 2, by0 + h / 2
            ex0 = int(round(cx_ref - ws / 2)) - a.sx
            ey0 = int(round(cy_ref - hs / 2)) - a.sy
            px0, py0 = max(0, ex0), max(0, ey0)
            px1, py1 = min(Ww, ex0 + ws + 2 * a.sx), min(Hh, ey0 + hs + 2 * a.sy)
            P = L[py0:py1, px0:px1]
            if P.shape[0] <= hs or P.shape[1] <= ws:
                continue
            for sg in sigs:
                Tm = blur_mask(Ms, sg)
                m = ncc_map(P, Tm)
                iy, ix = np.unravel_index(np.argmax(m), m.shape)
                v = m[iy, ix]
                if best is None or v > best[0]:
                    fy, fx = subpix(m, iy, ix)
                    # posición de la esquina de la plantilla escalada → centro
                    cx = px0 + fx + ws / 2
                    cy = py0 + fy + hs / 2
                    best = (v, s, sg, cx - cx_ref, cy - cy_ref, cx)
        v, s, sg, dx, dy, cx = best
        # opacidad: dentro frente a anillo, con la plantilla desplazada (sin escala)
        ox, oy = int(round(dx)), int(round(dy))
        yy0, xx0 = by0 + oy - pad, bx0 + ox - pad
        sub = A[max(0, yy0): yy0 + h + 2 * pad, max(0, xx0): xx0 + w + 2 * pad]
        cut_y, cut_x = max(0, -yy0), max(0, -xx0)
        inn = innerp[cut_y: cut_y + sub.shape[0], cut_x: cut_x + sub.shape[1]]
        rg = ring[cut_y: cut_y + sub.shape[0], cut_x: cut_x + sub.shape[1]]
        mn = sub.min(axis=2)
        alfa = float("nan")
        if inn.any() and rg.any():
            mi, mo = mn[inn].mean(), mn[rg].mean()
            alfa = (mi - mo) / max(1.0, 255 - mo)
        line = f"{f}\t{t_of(f, inf):.4f}\t{dx:+.2f}\t{dy:+.2f}\t{bx0 + dx:.1f}\t{cx:.1f}\t{s:.3f}\t{sg:g}\t{v:.3f}\t{alfa:.3f}"
        if bg is not None:
            bsub = bg[max(0, yy0): yy0 + h + 2 * pad, max(0, xx0): xx0 + w + 2 * pad]
            num = (sub - bsub)[inn]
            den = (255.0 - bsub)[inn]
            ok = den > 40
            ab = float((num[ok] * den[ok]).sum() / (den[ok] * den[ok]).sum()) if ok.any() else float("nan")
            line += f"\t{ab:.3f}"
            if a.gamma:
                def lin(v):
                    v = v / 255.0
                    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)
                Ig, Bg = sub.mean(axis=2)[inn], bsub.mean(axis=2)[inn]
                for lo, hi in ((0, 60), (60, 130), (130, 200)):
                    g = (Bg >= lo) & (Bg < hi)
                    if g.sum() < 200:
                        line += "\t  -    -  "
                        continue
                    ac = np.median((Ig[g] - Bg[g]) / (255 - Bg[g]))
                    al = np.median((lin(Ig[g]) - lin(Bg[g])) / (1 - lin(Bg[g])))
                    line += f"\t{ac:.3f}/{al:.3f}"
        if splits:
            edges = [bx0] + splits + [bx0 + w]
            for k in range(len(edges) - 1):
                c0 = edges[k] - bx0 + pad
                c1 = edges[k + 1] - bx0 + pad
                sel = np.zeros_like(inn)
                sel[:, max(0, c0 - cut_x): max(0, c1 - cut_x)] = True
                ii, rr = inn & sel, rg & sel
                if ii.any() and rr.any():
                    mi, mo = mn[ii].mean(), mn[rr].mean()
                    line += f"\t{(mi - mo) / max(1.0, 255 - mo):.3f}"
                else:
                    line += "\tnan"
        print(line)


if __name__ == "__main__":
    main()

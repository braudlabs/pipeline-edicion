#!/usr/bin/env python3
"""Movimiento global entre fotogramas consecutivos (escala + traslación) por correlación de fase en bloques.

  gmotion.py A B [--roi x,y,w,h] [--bs 128] [--ref K]

Para cada par (f-1, f) calcula el desplazamiento subpíxel de una rejilla de bloques y ajusta
  d(x) = t + (s-1)·(x - c)      (c = centro del fotograma)
de forma robusta (mediana iterada). Imprime por fotograma: ds (% de cambio de escala), tx, ty (px),
nº de bloques válidos, y la escala y traslación acumuladas desde A.
Con --ref K compara cada fotograma con el fotograma fijo K en vez de con el anterior.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from lib import frames, gray, W, H  # noqa: E402


def phase_shift(a, b, win):
    """Desplazamiento (dx, dy) que lleva a -> b, subpíxel, y calidad del pico."""
    A = np.fft.rfft2((a - a.mean()) * win)
    B = np.fft.rfft2((b - b.mean()) * win)
    R = np.conj(A) * B
    R /= np.abs(R) + 1e-6
    r = np.fft.irfft2(R, s=a.shape)
    n0, n1 = r.shape
    k = np.argmax(r)
    py, px = divmod(k, n1)
    peak = r[py, px]

    def sub(v_m, v_0, v_p):
        d = v_m - 2 * v_0 + v_p
        return 0.0 if abs(d) < 1e-9 else 0.5 * (v_m - v_p) / d

    oy = sub(r[(py - 1) % n0, px], peak, r[(py + 1) % n0, px])
    ox = sub(r[py, (px - 1) % n1], peak, r[py, (px + 1) % n1])
    dy = py + oy
    dx = px + ox
    if dy > n0 / 2:
        dy -= n0
    if dx > n1 / 2:
        dx -= n1
    return dx, dy, float(peak)


def fit(pts, d, q):
    """Ajuste robusto d = t + k·(p - c). Devuelve k (=s-1), tx, ty, n."""
    c = np.array([W / 2, H / 2])
    P = pts - c
    ok = q > max(0.04, np.percentile(q, 30))
    for _ in range(6):
        if ok.sum() < 6:
            break
        X = P[ok]
        D = d[ok]
        # mínimos cuadrados: [dx;dy] = [1 0 px; 0 1 py] [tx ty k]
        Amat = np.zeros((2 * len(X), 3))
        Amat[0::2, 0] = 1
        Amat[0::2, 2] = X[:, 0]
        Amat[1::2, 1] = 1
        Amat[1::2, 2] = X[:, 1]
        sol, *_ = np.linalg.lstsq(Amat, D.reshape(-1), rcond=None)
        tx, ty, k = sol
        res = np.hypot(d[:, 0] - (tx + k * P[:, 0]), d[:, 1] - (ty + k * P[:, 1]))
        thr = max(0.35, 2.5 * np.median(res[ok]))
        new = (res < thr) & (q > 0.04)
        if (new == ok).all():
            break
        ok = new
    return k, tx, ty, int(ok.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a", type=int)
    ap.add_argument("b", type=int)
    ap.add_argument("--roi", default="0,0,1,1")
    ap.add_argument("--bs", type=int, default=128)
    ap.add_argument("--step", type=int, default=0)
    ap.add_argument("--ref", type=int, default=None)
    a = ap.parse_args()
    x, y, w, h = [float(v) for v in a.roi.split(",")]
    X0, Y0, X1, Y1 = int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)
    bs = a.bs
    step = a.step or bs
    F = frames(a.a if a.ref is None else min(a.a, a.ref), a.b)
    base = a.a if a.ref is None else min(a.a, a.ref)
    G = [gray(f) for f in F]
    win = np.outer(np.hanning(bs), np.hanning(bs)).astype(np.float32)
    cells = [(xx, yy) for yy in range(Y0, Y1 - bs + 1, step) for xx in range(X0, X1 - bs + 1, step)]
    pts = np.array([[xx + bs / 2, yy + bs / 2] for xx, yy in cells])
    print("f\tds%\ttx\tty\tn\tS_acum\tTX_acum\tTY_acum\tmad")
    S, TX, TY = 1.0, 0.0, 0.0
    for f in range(a.a + (1 if a.ref is None else 0), a.b + 1):
        g1 = G[f - base]
        g0 = G[(f - 1 - base) if a.ref is None else (a.ref - base)]
        d = np.zeros((len(cells), 2))
        q = np.zeros(len(cells))
        for i, (xx, yy) in enumerate(cells):
            dx, dy, pk = phase_shift(g0[yy:yy + bs, xx:xx + bs], g1[yy:yy + bs, xx:xx + bs], win)
            d[i] = (dx, dy)
            q[i] = pk
        k, tx, ty, n = fit(pts, d, q)
        mad = float(np.abs(g1 - g0).mean())
        if a.ref is None:
            S *= (1 + k)
            TX = TX * (1 + k) + tx
            TY = TY * (1 + k) + ty
            print(f"{f}\t{k * 100:+.3f}\t{tx:+.2f}\t{ty:+.2f}\t{n}\t{S:.4f}\t{TX:+.1f}\t{TY:+.1f}\t{mad:.2f}")
        else:
            print(f"{f}\t{k * 100:+.3f}\t{tx:+.2f}\t{ty:+.2f}\t{n}\t{1 + k:.4f}\t{tx:+.1f}\t{ty:+.1f}\t{mad:.2f}")


if __name__ == "__main__":
    main()

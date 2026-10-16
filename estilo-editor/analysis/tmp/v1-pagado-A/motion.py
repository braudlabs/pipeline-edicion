#!/usr/bin/env python3
"""motion.py A B salida.json: transformación de semejanza (escala+traslación+giro) entre fotogramas consecutivos.
Emparejado por bloques (SAD) a media resolución + ajuste robusto. d = a*(p-c) + r*perp(p-c) + t."""
import json, sys
import numpy as np
from tools import frames, W, H

R, P = 8, 30


def half(im):
    g = im.astype(np.float32).mean(axis=2)
    return g.reshape(H // 2, 2, W // 2, 2).mean(axis=(1, 3))


def match(A, B):
    h, w = A.shape
    core = A[R:h - R, R:w - R]
    nh, nw = core.shape[0] // P, core.shape[1] // P
    core = core[:nh * P, :nw * P]
    costs = np.empty((2 * R + 1, 2 * R + 1, nh, nw), np.float32)
    for iy, dy in enumerate(range(-R, R + 1)):
        for ix, dx in enumerate(range(-R, R + 1)):
            diff = np.abs(core - B[R + dy:R + dy + nh * P, R + dx:R + dx + nw * P])
            costs[iy, ix] = diff.reshape(nh, P, nw, P).sum(axis=(1, 3))
    flat = costs.reshape(-1, nh, nw)
    k = flat.argmin(axis=0)
    iy, ix = np.divmod(k, 2 * R + 1)
    cmin = flat.min(axis=0)
    cmean = flat.mean(axis=0)
    tex = core.reshape(nh, P, nw, P).std(axis=(1, 3))
    dx = ix.astype(np.float32) - R
    dy = iy.astype(np.float32) - R
    # refinamiento parabólico
    for j in range(nh):
        for i in range(nw):
            y, x = iy[j, i], ix[j, i]
            if 0 < x < 2 * R:
                l, c, r = costs[y, x - 1, j, i], costs[y, x, j, i], costs[y, x + 1, j, i]
                den = l - 2 * c + r
                if den > 1e-6:
                    dx[j, i] += 0.5 * (l - r) / den
            if 0 < y < 2 * R:
                u, c, d = costs[y - 1, x, j, i], costs[y, x, j, i], costs[y + 1, x, j, i]
                den = u - 2 * c + d
                if den > 1e-6:
                    dy[j, i] += 0.5 * (u - d) / den
    ys = (np.arange(nh) * P + R + P / 2)[:, None] * np.ones((1, nw))
    xs = np.ones((nh, 1)) * (np.arange(nw) * P + R + P / 2)[None, :]
    edge = (ix == 0) | (ix == 2 * R) | (iy == 0) | (iy == 2 * R)
    return xs, ys, dx, dy, tex, cmin / (P * P), cmean / (P * P), edge


def fit(xs, ys, dx, dy, tex, cmin, cmean, edge, h, w):
    ok = (tex > 5) & (~edge) & (cmin < 0.6 * cmean)
    n = int(ok.sum())
    if n < 12:
        return None
    px, py = xs[ok] - w / 2, ys[ok] - h / 2
    ux, uy = dx[ok], dy[ok]
    # incógnitas: a, r, tx, ty ;  ux = a*px - r*py + tx ; uy = a*py + r*px + ty
    A = np.zeros((2 * n, 4))
    A[:n, 0], A[:n, 1], A[:n, 2] = px, -py, 1
    A[n:, 0], A[n:, 1], A[n:, 3] = py, px, 1
    b = np.concatenate([ux, uy])
    wgt = np.ones(2 * n)
    for _ in range(12):
        sol, *_ = np.linalg.lstsq(A * wgt[:, None], b * wgt, rcond=None)
        res = A @ sol - b
        rr = np.sqrt(res[:n] ** 2 + res[n:] ** 2)
        sig = max(0.15, 1.4826 * np.median(rr))
        w1 = 1 / (1 + (rr / (2 * sig)) ** 2)
        wgt = np.concatenate([w1, w1])
    inl = float((rr < 2.5 * sig).mean())
    return dict(a=float(sol[0]), r=float(sol[1]), tx=float(sol[2]) * 2, ty=float(sol[3]) * 2,
                n=n, inl=round(inl, 3), sig=round(float(sig) * 2, 3))


def main():
    a, b, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    res = []
    prev = None
    CH = 40
    f = a
    while f <= b:
        e = min(b, f + CH - 1)
        for k, im in enumerate(frames(f, e)):
            g = half(im)
            if prev is not None:
                m = match(prev, g)
                r = fit(*m, *g.shape)
                d = float(np.abs(g - prev).mean())
                row = dict(f=f + k, mad=round(d, 3))
                if r:
                    row.update(r)
                res.append(row)
            prev = g
        f = e + 1
        print(f"hasta f{e}", file=sys.stderr, flush=True)
    json.dump(res, open(out, "w"))


main()

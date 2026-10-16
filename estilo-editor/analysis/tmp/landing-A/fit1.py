"""Centroide subpíxel y brillo por palabra; ajuste exponencial."""
import sys
import numpy as np
from la import *
def track(a, b, ref, x0, x1, yA, yB, thr=10):
    R = luma(frames(ref, ref)[ref]); F = frames(a, b)
    rows = []
    for f in range(a, b + 1):
        d = (luma(F[f]) - R)[yA:yB, x0:x1 + 1]
        m = d > thr
        if m.sum() < 8: rows.append((f, np.nan, 0, 0)); continue
        w = np.where(m, d, 0)
        cy = (w.sum(1) * np.arange(yA, yB)).sum() / w.sum()
        rows.append((f, cy, float(np.percentile(d[m], 99)), float(w.sum())))
    return rows
def report(name, rows, tail=8):
    fin_cy = np.nanmean([r[1] for r in rows[-tail:]]); fin_b = np.mean([r[2] for r in rows[-tail:]]); fin_s = np.mean([r[3] for r in rows[-tail:]])
    print(f"## {name}: centroide final y={fin_cy:.2f}  brillo final={fin_b:.0f}  suma final={fin_s:.0f}")
    xs, ys = [], []
    line = []
    for f, cy, b, s in rows:
        if np.isnan(cy): continue
        off = cy - fin_cy
        line.append(f"f{f}: dy={off:+6.2f}px  brillo={b/fin_b*100:5.1f}%  suma={s/fin_s*100:5.1f}%")
        if off > 1.5: xs.append(f); ys.append(np.log(off))
    print("\n".join(line))
    if len(xs) > 4:
        k, c = np.polyfit(xs, ys, 1)
        f0 = xs[0]
        print(f"ajuste dy = {np.exp(c + k*f0):.1f}·exp({k:.4f}·(f-{f0}))  -> semivida {np.log(2)/-k:.2f} f, constante {1/-k:.2f} f; D extrapolado a f{f0-1}: {np.exp(c+k*(f0-1)):.1f}px")
if __name__ == "__main__":
    name = sys.argv[1]; a, b, ref, x0, x1, yA, yB = [int(v) for v in sys.argv[2:9]]
    report(name, track(a, b, ref, x0, x1, yA, yB))

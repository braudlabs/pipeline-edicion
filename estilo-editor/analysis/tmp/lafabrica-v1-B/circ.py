import sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from m import load

def boxsum(M, k):
    c = np.zeros((M.shape[0] + 1, M.shape[1] + 1)); c[1:, 1:] = M.cumsum(0).cumsum(1)
    r = k // 2
    H, W = M.shape
    out = np.zeros_like(M, dtype=np.float64)
    y0 = np.clip(np.arange(H) - r, 0, H); y1 = np.clip(np.arange(H) + r + 1, 0, H)
    x0 = np.clip(np.arange(W) - r, 0, W); x1 = np.clip(np.arange(W) + r + 1, 0, W)
    return c[y1][:, x1] - c[y0][:, x1] - c[y1][:, x0] + c[y0][:, x0]

def bluemask(A):
    R, G, B = A[..., 0], A[..., 1], A[..., 2]
    return (B > 130) & (R < 120) & (B - R > 55)

def kasa(xs, ys):
    A = np.stack([xs, ys, np.ones_like(xs)], 1)
    b = xs ** 2 + ys ** 2
    sol, *_ = np.linalg.lstsq(A, b, rcond=None)
    cx, cy = sol[0] / 2, sol[1] / 2
    r = np.sqrt(sol[2] + cx ** 2 + cy ** 2)
    return cx, cy, r

def circle(n, half='lower', bm=bluemask, ek=11):
    A = load(n)
    M = bm(A)
    if M.sum() < 200:
        return None
    E = boxsum(M.astype(np.float64), ek) >= ek * ek * 0.98
    if E.sum() < 20:
        E = M
    ys, xs = np.nonzero(E)
    cx, cy = xs.mean(), ys.mean()
    r = max(8.0, np.sqrt(E.sum() / np.pi))
    for it in range(6):
        px, py = [], []
        rows = range(int(cy + 0.05 * r), int(cy + 0.93 * r)) if half == 'lower' else range(int(cy - 0.93 * r), int(cy - 0.05 * r))
        for y in rows:
            if y < 0 or y >= M.shape[0]:
                continue
            xa, xb = int(max(0, cx - 1.25 * r)), int(min(M.shape[1], cx + 1.25 * r))
            row = M[y, xa:xb]
            idx = np.nonzero(row)[0]
            if len(idx) < 3:
                continue
            px += [xa + idx[0], xa + idx[-1]]; py += [y, y]
        if len(px) < 10:
            return None
        cx, cy, r = kasa(np.array(px, float), np.array(py, float))
    return cx, cy, r

if __name__ == '__main__':
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for n in range(a, b + 1):
        c = circle(n)
        print(n, None if c is None else f"cx={c[0]:.1f} cy={c[1]:.1f} r={c[2]:.1f}")

"""Ajuste de curvas de animación: cubic-bezier(x1,y1,x2,y2) y familias simples."""
import numpy as np


def bez(x, x1, y1, x2, y2):
    """Easing cubic-bezier evaluado en x (array 0..1)."""
    x = np.clip(np.asarray(x, float), 0, 1)
    lo = np.zeros_like(x)
    hi = np.ones_like(x)
    for _ in range(40):
        u = (lo + hi) / 2
        bx = 3 * (1 - u) ** 2 * u * x1 + 3 * (1 - u) * u ** 2 * x2 + u ** 3
        hi = np.where(bx > x, u, hi)
        lo = np.where(bx <= x, u, lo)
    u = (lo + hi) / 2
    return 3 * (1 - u) ** 2 * u * y1 + 3 * (1 - u) * u ** 2 * y2 + u ** 3


def fit_bezier(t, p, T, iters=4000, seed=0, y_free=False):
    """p = progreso medido 0..1 en t (fotogramas), duración T. Devuelve (rms, x1,y1,x2,y2)."""
    rng = np.random.default_rng(seed)
    best = None
    cur = np.array([0.1, 0.6, 0.3, 1.0])
    step = 0.3
    def err(q):
        return float(np.sqrt(np.mean((bez(t / T, *q) - p) ** 2)))
    e = err(cur)
    for i in range(iters):
        q = cur + rng.normal(0, step, 4)
        q[0] = np.clip(q[0], 0, 1)
        q[2] = np.clip(q[2], 0, 1)
        if not y_free:
            q[1] = np.clip(q[1], 0, 1)
            q[3] = np.clip(q[3], 0, 1)
        e2 = err(q)
        if e2 < e:
            cur, e = q, e2
        if i % 500 == 499:
            step *= 0.6
    return e, cur

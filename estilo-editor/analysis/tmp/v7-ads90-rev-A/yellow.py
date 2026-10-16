import sys; sys.path.insert(0,'analysis/tmp/v7-ads90-rev-A')
from h import *
F = frames('v7-ads90-rev', 0, 45)
print('f\tn\tcx\tcy\tang\tlargo\talto\tmeanRGB')
for n in range(0, 46):
    A = F[n].astype(np.float32)
    # amarillo: R alto, G alto, B bajo
    m = (A[...,0] > 200) & (A[...,1] > 190) & (A[...,2] < 110)
    m[:, 700:] = False; m[:400] = False; m[1000:] = False
    ys, xs = np.nonzero(m)
    if len(xs) < 50:
        print(n, len(xs), '-'); continue
    pts = np.stack([xs, ys], 1).astype(np.float64)
    c = pts.mean(0)
    u, s, vt = np.linalg.svd(pts - c, full_matrices=False)
    ax = vt[0]
    if ax[0] < 0: ax = -ax
    ang = np.degrees(np.arctan2(ax[1], ax[0]))
    pr = (pts - c) @ ax
    pe = (pts - c) @ np.array([-ax[1], ax[0]])
    L = np.percentile(pr, 99.9) - np.percentile(pr, 0.1)
    Hh = np.percentile(pe, 99.9) - np.percentile(pe, 0.1)
    col = A[m].mean(0)
    # centro de caja orientada
    cc = c + ax * (np.percentile(pr, 99.9) + np.percentile(pr, 0.1)) / 2 + np.array([-ax[1], ax[0]]) * (np.percentile(pe, 99.9) + np.percentile(pe, 0.1)) / 2
    print(f'{n}\t{len(xs)}\t{cc[0]:.1f}\t{cc[1]:.1f}\t{ang:.2f}\t{L:.0f}\t{Hh:.0f}\t{col[0]:.0f},{col[1]:.0f},{col[2]:.0f}')

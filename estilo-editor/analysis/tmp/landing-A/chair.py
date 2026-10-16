import numpy as np
from la import *
def shift(A, B, maxs=12):
    """desplazamiento entero (dx,dy) de B respecto de A que minimiza la diferencia"""
    best = None
    h, w = A.shape
    for dy in range(-maxs, maxs + 1):
        for dx in range(-maxs, maxs + 1):
            a = A[maxs:h - maxs, maxs:w - maxs]
            b = B[maxs + dy:h - maxs + dy, maxs + dx:w - maxs + dx]
            e = np.mean((a - b) ** 2)
            if best is None or e < best[0]: best = (e, dx, dy)
    return best
for (fa, others, roi) in ((312, (340, 380, 420, 460, 500, 506), (1500, 900, 1920, 1080)), (572, (600, 640, 680, 720, 728, 748), (1500, 900, 1920, 1080)),
                          (2, (40, 80, 120, 160, 200, 213), (600, 60, 1300, 220)), (216, (240, 270, 300, 306), (500, 20, 1400, 160))):
    A = luma(frames(fa, fa)[fa])[roi[1]:roi[3], roi[0]:roi[2]]
    print(f"ref f{fa} roi {roi}: contraste (std) {A.std():.1f}")
    for fb in others:
        B = luma(frames(fb, fb)[fb])[roi[1]:roi[3], roi[0]:roi[2]]
        e, dx, dy = shift(A, B)
        e0 = np.mean((A[12:-12, 12:-12] - B[12:-12, 12:-12]) ** 2)
        print(f"   f{fb}: desplazamiento óptimo dx={dx:+d} dy={dy:+d}  (error {e:.1f}; sin desplazar {e0:.1f})")

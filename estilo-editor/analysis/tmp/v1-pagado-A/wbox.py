#!/usr/bin/env python3
"""wbox.py A B x0 y0 x1 y1 [thr] [keepborder]: caja de tinta blanca en región px, sin componentes que tocan el borde."""
import sys
import numpy as np
from tools import frames, drop_border, bbox, white_mask
a, b = int(sys.argv[1]), int(sys.argv[2])
X0, Y0, X1, Y1 = [int(v) for v in sys.argv[3:7]]
thr = int(sys.argv[7]) if len(sys.argv) > 7 else 235
keep = len(sys.argv) > 8
print("f\tx0\ty0\tx1\ty1\tcx\tcy\tw\th\tarea")
for k, im in enumerate(frames(a, b)):
    m = white_mask(im[Y0:Y1, X0:X1], thr)
    if not keep:
        m = drop_border(m)
    bb = bbox(m)
    if bb is None:
        print(f"{a+k}\t-\t-\t-\t-\t-\t-\t-\t-\t{int(m.sum())}")
        continue
    x0, y0, x1, y1 = bb
    print(f"{a+k}\t{X0+x0:.0f}\t{Y0+y0:.0f}\t{X0+x1:.0f}\t{Y0+y1:.0f}\t{X0+(x0+x1)/2:.1f}\t{Y0+(y0+y1)/2:.1f}\t{x1-x0+1:.0f}\t{y1-y0+1:.0f}\t{int(m.sum())}")

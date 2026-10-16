#!/usr/bin/env python3
"""pairscale.py fA fB [R]: escala/traslación entre dos fotogramas no consecutivos por bloques (media resolución)."""
import sys
import numpy as np
from tools import frames, W, H
import motion_lib as ml
fa, fb = int(sys.argv[1]), int(sys.argv[2])
R = int(sys.argv[3]) if len(sys.argv) > 3 else 20
A = ml.half(frames(fa, fa)[0]); B = ml.half(frames(fb, fb)[0])
m = ml.match(A, B, R=R, P=30)
r = ml.fit(*m, *A.shape, R=R)
print(f"f{fa}->f{fb}: escala {1 + r['a']:.4f} (a={r['a']*100:+.2f}%) giro {r['r']*1000:+.1f} mrad  t=({r['tx']:+.1f},{r['ty']:+.1f}) px  n={r['n']} inl={r['inl']} sig={r['sig']}")

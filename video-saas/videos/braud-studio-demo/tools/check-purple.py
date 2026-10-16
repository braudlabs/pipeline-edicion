#!/usr/bin/env python3
"""Busca la sudadera morada vetada (veto de Ale, 15/10) en un render.

Muestrea el vídeo a 4 fps y cuenta los píxeles morados saturados (el estampado del monstruo).
Lista los tramos con más de `--px` píxeles en un fotograma de 640×360. Los retratos diminutos
del perchero dan menos de ~200 px; un plano en el que se reconoce la sudadera pasa de 300.
Uso: python3 -I tools/check-purple.py out/BRAUD-Studio-Demo-Avance06.mp4 [--px 300]
Sale con código 1 si algún tramo supera el umbral.
"""
import subprocess
import sys

import numpy as np

path = sys.argv[1]
limit = int(sys.argv[sys.argv.index('--px') + 1]) if '--px' in sys.argv else 300
W, H = 640, 360
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'fps=4,scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
hits, i = [], 0
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3:
        break
    f = np.frombuffer(b, dtype=np.uint8).reshape(H, W, 3).astype(np.float32) / 255
    r, g, bl = f[..., 0], f[..., 1], f[..., 2]
    s = (f.max(-1) - f.min(-1)) / (f.max(-1) + 1e-6)
    purple = (bl > 0.30) & (r > 0.20) & (g < 0.55 * bl) & (r < 1.15 * bl) & (r > 0.40 * bl) & (s > 0.40)
    n = int(purple.sum())
    if n > 40:
        hits.append((i / 4, n))
    i += 1
spans = []
for t, n in hits:
    if spans and t - spans[-1][1] <= 0.3:
        spans[-1][1], spans[-1][2] = t, max(spans[-1][2], n)
    else:
        spans.append([t, t, n])
bad = [x for x in spans if x[2] > limit]
for a, b, m in spans:
    print(f"{'FALLA' if m > limit else 'ok   '} {a:6.2f}–{b:6.2f} s  máx. {m} px")
print(f'{i} fotogramas · {len(spans)} tramos con morado · {len(bad)} por encima de {limit} px')
sys.exit(1 if bad else 0)

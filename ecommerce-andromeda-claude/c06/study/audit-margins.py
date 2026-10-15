#!/usr/bin/env python3
"""Márgenes reales de los rótulos (C05): lee study/audit-captions.mp4 (solo rótulos sobre negro,
540×960) y lista los tramos donde la tinta sale de x 100–980 (coordenadas de 1080). Escribe
study/audit-margins.json. Uso: python3 study/audit-margins.py"""
import json
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
W, H, K = 540, 960, 2  # escala 0,5
raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(HERE / 'audit-captions.mp4'), '-f', 'rawvideo', '-pix_fmt', 'gray', '-'])
F = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
rows = []
for i, f in enumerate(F):
    cols = np.nonzero((f > 70).sum(0) >= 2)[0]
    if len(cols):
        rows.append((i, int(cols[0]) * K, int(cols[-1] + 1) * K))
bad = [(i, a, b) for i, a, b in rows if a < 100 or b > 980]
spans = []
for i, a, b in bad:
    if spans and i - spans[-1]['to'] <= 1:
        s = spans[-1]
        s['to'] = i
        s['min_x'] = min(s['min_x'], a)
        s['max_x'] = max(s['max_x'], b)
    else:
        spans.append({'from': i, 'to': i, 'min_x': a, 'max_x': b})
out = {'frames': len(F), 'frames_with_text': len(rows), 'frames_outside_100_980': len(bad), 'spans': spans}
(HERE / 'audit-margins.json').write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ('frames', 'frames_with_text', 'frames_outside_100_980')}))
for s in spans:
    print(f"f{s['from']}–{s['to']}: x {s['min_x']}–{s['max_x']}")

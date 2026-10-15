#!/usr/bin/env python3
"""Track the two blue selection handles; never interpret crop width as font scale."""
import json
import subprocess
import numpy as np
from common import DATOS, src

A, B = 168, 327
W, H, Y = 1080, 390, 525
proc = subprocess.Popen([
    'ffmpeg', '-v', 'error', '-i', str(src('v8')), '-vf',
    f'select=between(n\\,{A}\\,{B}),crop={W}:{H}:0:{Y}',
    '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'
], stdout=subprocess.PIPE)

def read_exact(n):
    chunks, size = [], 0
    while size < n:
        chunk = proc.stdout.read(n - size)
        if not chunk:
            raise RuntimeError(f'Incomplete native frame: {size}/{n}')
        chunks.append(chunk)
        size += len(chunk)
    return b''.join(chunks)

rows = []
for frame in range(A, B + 1):
    rgb = np.frombuffer(read_exact(W * H * 3), dtype=np.uint8).reshape(H, W, 3).astype(np.int16)
    r, g, b = rgb.transpose(2, 0, 1)
    row = {'frame': frame}
    for threshold in [50, 70]:
        mask = (b - r > 80) & (b - g > threshold) & (b > 150) & (r < 110)
        points = []
        for label, lo, hi in [('upperLeft', 530, 615), ('lowerRight', 830, 910)]:
            yy, xx = np.nonzero(mask[lo - Y:hi - Y])
            count = len(xx)
            points.append({'handle': label, 'pixelCount': count,
                           'x': round(float(np.median(xx)), 3) if count else None,
                           'y': round(float(np.median(yy)) + lo, 3) if count else None,
                           'reliable': count > 1500})
        row[f'threshold{threshold}'] = {
            'handles': points,
            'separationX': round(points[1]['x'] - points[0]['x'], 3)
                if all(p['reliable'] for p in points) else None,
            'midpointX': round((points[1]['x'] + points[0]['x']) / 2, 3)
                if all(p['reliable'] for p in points) else None,
        }
    rows.append(row)
if proc.stdout.read(1):
    raise RuntimeError('Unexpected extra native frame')
assert proc.wait() == 0
result = {
    'slug': 'v8', 'range': [A, B], 'fps': {'num': 60000, 'den': 1001},
    'method': 'Native RGB, blue chroma selection in two fixed handle bands; median x/y; B-R>80, B-G>50/70, B>150, R<110. Reliable if >1500 pixels per handle.',
    'warnings': ['Handle spacing is not fontSize, text width or recovered mask alpha.',
                 'Handle circles and attached strokes affect medians; compare both thresholds.',
                 'The midpoint is screen-space, not a tracked scene anchor.',
                 'Native visual review distinguishes clipping from horizontal scaling.'],
    'rows': rows
}
output = DATOS / 'revision-v2/v8-selector-curves.json'
output.write_text(json.dumps(result, ensure_ascii=False, indent=2))
for f in [173, 180, 190, 200, 220, 230, 232, 235, 240, 245, 250, 254, 256, 258, 260, 265, 270, 280, 290, 300, 326, 327]:
    row = rows[f-A]['threshold70']
    print(f, row['separationX'], row['midpointX'], [p['pixelCount'] for p in row['handles']])

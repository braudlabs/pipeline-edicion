"""Color medio (5x5) en varios puntos a lo largo de un rango: pts.py A B x,y x,y ... [--slug s]"""
import sys
import numpy as np
from lib import run, arr
args = [a for a in sys.argv[1:]]
slug = 'v6-ads90-rev'
if '--slug' in args:
    i = args.index('--slug'); slug = args[i + 1]; del args[i:i + 2]
a, b = int(args[0]), int(args[1])
P = [tuple(int(v) for v in p.split(',')) for p in args[2:]]
ims = run(a, b, slug)
print('f\t' + '\t'.join(f'({x},{y})' for x, y in P))
for k, im in enumerate(ims):
    A = arr(im)
    out = []
    for x, y in P:
        c = A[y - 2:y + 3, x - 2:x + 3].reshape(-1, 3).mean(axis=0)
        out.append(f'{c[0]:.0f},{c[1]:.0f},{c[2]:.0f}')
    print(f'{a + k}\t' + '\t'.join(out))

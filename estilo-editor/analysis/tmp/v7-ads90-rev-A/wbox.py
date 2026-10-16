import sys; sys.path.insert(0,'analysis/tmp/v7-ads90-rev-A')
from h import *
slug, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
thr = int(sys.argv[4]) if len(sys.argv) > 4 else 250
roi = [float(v) for v in sys.argv[5].split(',')] if len(sys.argv) > 5 else [0.0, 0.40, 1.0, 0.22]
F = frames(slug, a, b)
H, W = F[a].shape[:2]
X0, Y0, X1, Y1 = int(roi[0]*W), int(roi[1]*H), int((roi[0]+roi[2])*W), int((roi[1]+roi[3])*H)
print('f\tn\tx0\ty0\tx1\ty1\tcx\tcy\tw\th')
for n in range(a, b+1):
    A = F[n][Y0:Y1, X0:X1]
    m = A.min(axis=2) >= thr
    bb = bbox(m, 0.0)
    if bb is None:
        print(n, int(m.sum()), '-'); continue
    x0,y0,x1,y1 = bb
    print(f'{n}\t{int(m.sum())}\t{X0+x0:.0f}\t{Y0+y0:.0f}\t{X0+x1:.0f}\t{Y0+y1:.0f}\t{X0+(x0+x1)/2:.1f}\t{Y0+(y0+y1)/2:.1f}\t{x1-x0+1:.0f}\t{y1-y0+1:.0f}')

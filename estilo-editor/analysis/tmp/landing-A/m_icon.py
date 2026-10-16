import numpy as np
from la import *
np.set_printoptions(linewidth=220, suppress=True)
F = frames(206, 420)
ref = luma(F[208])  # con frase 2 aún; zona de iconos (y<490) sin texto de la frase 2? la frase 2 ocupa y 494..588
def D(f): return luma(F[f]) - luma(F[206])
# geometria con f400 (todo asentado, plano 3)... los iconos están sobre el fondo; usar umbral absoluto de luma
L = luma(F[400]).copy()
roi = L[420:500, 150:330]
m = roi > 110
ys, xs = np.nonzero(m)
print("tinta iconos f400: x %d..%d y %d..%d" % (xs.min()+150, xs.max()+150, ys.min()+420, ys.max()+420))
cols = m.sum(0); 
runs=[]; on=False
for x in range(len(cols)):
    if cols[x] and not on: on=True; s=x
    if not cols[x] and on: on=False; runs.append((s+150, x-1+150))
print("tramos x:", runs)
def fitcircle(mask, x_off, y_off):
    ys, xs = np.nonzero(mask)
    A = np.c_[2*xs, 2*ys, np.ones(len(xs))]; b = xs**2 + ys**2
    cx, cy, c = np.linalg.lstsq(A, b, rcond=None)[0]
    r = np.sqrt(c + cx**2 + cy**2)
    return cx + x_off, cy + y_off, r
for name, (xa, xb) in {"icono1": (150, 232), "icono2": (232, 330)}.items():
    sub = L[420:505, xa:xb] > 110
    ys, xs = np.nonzero(sub)
    print(name, "caja x %d..%d y %d..%d  (ancho %d alto %d)" % (xs.min()+xa, xs.max()+xa, ys.min()+420, ys.max()+420, xs.max()-xs.min()+1, ys.max()-ys.min()+1))
    # anillo: pixeles lejos del centro de la caja
    cx0 = (xs.min()+xs.max())/2; cy0 = (ys.min()+ys.max())/2
    rr = np.hypot(xs-cx0, ys-cy0)
    ring = rr > rr.max()*0.85
    mk = np.zeros_like(sub); mk[ys[ring], xs[ring]] = True
    cx, cy, r = fitcircle(mk, xa, 420)
    print("   círculo: centro (%.1f, %.1f) radio %.1f  -> diámetro exterior ~%d px" % (cx, cy, r, xs.max()-xs.min()+1))
    # perfil radial para grosor del trazo
    yy, xx = np.mgrid[420:505, xa:xb]
    rad = np.hypot(xx-cx, yy-cy)
    prof = [(rr_, float(L[420:505, xa:xb][(rad>=rr_-0.5)&(rad<rr_+0.5)].mean())) for rr_ in np.arange(r-5, r+5.5, 1)]
    print("   perfil radial (r, luma media):", [(round(a,1), round(b)) for a,b in prof])

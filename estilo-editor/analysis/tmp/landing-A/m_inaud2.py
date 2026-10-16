import numpy as np
from la import *
F = frames(84, 89)
A = F[86].astype(np.float32); B = F[87].astype(np.float32)
# zona de caja sin texto: regresión box = a*c + (1-a)*bg
ys, xs = np.mgrid[793:858, 824:1097]
a_ = A[793:858, 824:1097].reshape(-1, 3); b_ = B[793:858, 824:1097].reshape(-1, 3)
# excluir texto amarillo (saturado)
sat = a_.max(1) - a_.min(1)
m = sat < 6
print("pix sin texto", m.sum(), "de", len(m))
for c in range(3):
    x = b_[m, c]; y = a_[m, c]
    k, n = np.polyfit(x, y, 1)
    print("canal", c, "pendiente(1-a)=%.3f  ordenada=%.2f -> alfa=%.3f color=%.1f" % (k, n, 1 - k, n / (1 - k)), " bg medio %.1f  caja media %.1f" % (x.mean(), y.mean()))
# color del texto: percentil alto de amarillo
T = F[86].astype(np.float32)[793:858, 824:1097].reshape(-1, 3)
yel = (T[:, 0] > 200) & (T[:, 1] > 200) & (T[:, 2] < 120)
print("pix amarillos", yel.sum(), "media", T[yel].mean(0).round(1), "p90 por canal", np.percentile(T[yel], 90, axis=0).round(1), "min B", T[yel][:, 2].min())
core = (T[:, 0] > 235) & (T[:, 1] > 235) & (T[:, 2] < 60)
print("núcleo", core.sum(), T[core].mean(0).round(1))
# caja exacta del texto amarillo
full = F[86].astype(np.float32)
Y = (full[..., 0] > 150) & (full[..., 1] > 150) & (full[..., 2] < 140) & (full[..., 0] - full[..., 2] > 60)
Y[:700] = False; Y[900:] = False; Y[:, :700] = False; Y[:, 1250:] = False
yy, xx = np.nonzero(Y)
print("tinta amarilla: x %d..%d  y %d..%d  ancho %d alto %d  centro %.1f,%.1f" % (xx.min(), xx.max(), yy.min(), yy.max(), xx.max() - xx.min() + 1, yy.max() - yy.min() + 1, (xx.min() + xx.max()) / 2, (yy.min() + yy.max()) / 2))
# perfil de columnas para ver letras
cols = Y.sum(0)
runs = []; on = False
for x in range(700, 1250):
    if cols[x] > 0 and not on: on = True; s = x
    if cols[x] == 0 and on: on = False; runs.append((s, x - 1))
print("tramos de tinta en x:", runs)
rows = Y.sum(1)
print("filas con tinta:", [(y, int(rows[y])) for y in range(790, 862) if rows[y] > 0][:80])
# borde de la caja con precisión: diferencia f86-f87
D = np.abs(luma(A) - luma(B))
box = D > 5
yy, xx = np.nonzero(box[700:900, 700:1250])
print("caja por diferencia f86-f87: x %d..%d y %d..%d" % (xx.min() + 700, xx.max() + 700, yy.min() + 700, yy.max() + 700))
for y in (789, 790, 791, 792, 793, 857, 858, 859, 860, 861):
    print("fila", y, "dif media en caja", round(float(D[y, 830:1090].mean()), 2))
for x in (819, 820, 821, 822, 823, 824, 1096, 1097, 1098, 1099, 1100, 1101):
    print("col", x, "dif media", round(float(D[795:855, x].mean()), 2))

import numpy as np
from la import *
F = frames(0, 2)
A = F[0].astype(np.float32)
# perfil horizontal en y=822 (centro del rótulo) y vertical en x=960
np.set_printoptions(linewidth=250, suppress=True)
print("fila y=800 (dentro de caja, encima del texto?) x 800..1130 paso 5")
for y in (776, 780, 784, 788, 792, 800, 822, 850, 856, 860, 864, 868):
    row = A[y, 800:1130:6]
    print(y, " ".join(f"{int(r[0]):3d},{int(r[1]):3d},{int(r[2]):3d}" for r in row[:28]))
L = luma(A)
# caja gris: buscar borde por gradiente a lo largo de columnas en x 800..1130, y 760..890
sub = L[760:890, 790:1140]
print("media por fila (y):")
for y in range(760, 890, 2):
    print(y, round(float(L[y, 800:1130].mean()), 1), round(float(np.median(L[y, 800:1130])), 1))
print("mediana por columna (x) en y 790..855:")
for x in range(800, 1130, 4):
    print(x, round(float(np.median(L[790:856, x])), 1), end=" | ")

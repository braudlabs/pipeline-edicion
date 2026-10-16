"""Color, tinta y sombra del subtítulo amarillo usando la diferencia rev − original."""
import numpy as np
from lib import run, arr
from PIL import Image
for f, name in ((965, 'quiero'), (983, 'un'), (1000, 'UGC'), (1050, 'de'), (1060, 'este'), (1070, 'avatar'), (1080, 'avatar(teclado)')):
    R = arr(run(f, f, 'v6-ads90-rev')[0]); O = arr(run(f, f, 'v6-ads90')[0])
    d = R - O
    ad = np.abs(d).max(axis=2)
    # núcleo amarillo: muy distinto del original y con B bajo
    core = (R[..., 2] < 60) & (R[..., 0] > 235) & (R[..., 1] > 225)
    ys, xs = np.nonzero(core)
    col = np.median(R[core], axis=0)
    p10 = np.percentile(R[core], 10, axis=0); p90 = np.percentile(R[core], 90, axis=0)
    print(f"f{f} {name}: núcleo {core.sum()} px  caja x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}  ({xs.max()-xs.min()+1}x{ys.max()-ys.min()+1})  centro {(xs.min()+xs.max())/2:.1f},{(ys.min()+ys.max())/2:.1f}  color mediana rgb({col[0]:.0f},{col[1]:.0f},{col[2]:.0f}) p10 {p10.round()} p90 {p90.round()}")
    # sombra: píxeles que la revisión oscurece respecto al original, fuera del núcleo
    dark = (d.sum(axis=2) < -18) & ~core
    if dark.sum() > 50:
        ys2, xs2 = np.nonzero(dark)
        x0, x1 = np.percentile(xs2, [1, 99]); y0, y1 = np.percentile(ys2, [1, 99])
        ratio = (R[dark].sum(axis=1) / np.maximum(1, O[dark].sum(axis=1)))
        print(f"      sombra: {dark.sum()} px  caja x {x0:.0f}-{x1:.0f} y {y0:.0f}-{y1:.0f}  oscurecimiento mediano ×{np.median(ratio):.2f}  mínimo ×{np.percentile(ratio,2):.2f}")

"""Genera las dos texturas del fondo verde como PNG deterministas.

En AE son efectos procedurales (ADBE Fractal Noise y ADBE Noise2) sobre sólidos
grises al 50 %. Aquí se reconstruyen con el mismo modelo — ruido fractal de varias
octavas estirado en horizontal, y ruido monocromo recortado — y se congelan en un
PNG para que el render de Remotion sea determinista.
"""
from pathlib import Path
import numpy as np
from PIL import Image

R = Path(__file__).resolve().parents[1]
W, H = 1080, 1920
rng = np.random.default_rng(20260916)


def value_noise(w, h, cells_x, cells_y):
    """Ruido de valor con interpolación suave, equivalente a una octava de AE."""
    gx, gy = int(cells_x) + 2, int(cells_y) + 2
    g = rng.random((gy, gx))
    ys = np.linspace(0, gy - 2, h)
    xs = np.linspace(0, gx - 2, w)
    y0, x0 = np.floor(ys).astype(int), np.floor(xs).astype(int)
    fy, fx = ys - y0, xs - x0
    sy = (fy * fy * (3 - 2 * fy))[:, None]          # smoothstep
    sx = (fx * fx * (3 - 2 * fx))[None, :]
    a = g[np.ix_(y0, x0)]
    b = g[np.ix_(y0, x0 + 1)]
    c = g[np.ix_(y0 + 1, x0)]
    d = g[np.ix_(y0 + 1, x0 + 1)]
    return (a * (1 - sx) + b * sx) * (1 - sy) + (c * (1 - sx) + d * sx) * sy


def fiber(scale_x=500, scale_y=160, complexity=8, contrast=70):
    """Fractal Noise estirado: fibra horizontal suave."""
    out = np.zeros((H, W))
    amp, total = 1.0, 0.0
    for octave in range(int(complexity)):
        f = 2 ** octave
        out += amp * value_noise(W, H, W / scale_x * 100 * f / 100, H / scale_y * 100 * f / 100)
        total += amp
        amp *= 0.5
    out /= total
    out = (out - out.mean()) * (contrast / 100 * 2.2) + 0.5   # contraste de AE
    return np.clip(out, 0, 1)


def grain(amount=40):
    """Noise monocromo recortado, como ADBE Noise2 con «usar color» desactivado."""
    n = rng.normal(0.5, amount / 100 * 0.45, (H, W))
    return np.clip(n, 0, 1)


for name, data in [('textura-fibra', fiber()), ('grano-fino', grain())]:
    a = (data * 255).round().astype(np.uint8)
    p = R / 'public/textures' / f'{name}.png'
    p.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(a, mode='L').convert('RGB').save(p, optimize=True)
    print(f'{p.relative_to(R)}  {a.shape[1]}x{a.shape[0]}  media={a.mean():.1f}')

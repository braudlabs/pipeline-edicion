"""Compara fotogramas de la recreación con la imagen entregada de V8.

Usa el PNG nativo que renderizó After Effects cuando existe —sin compresión— y,
si no, extrae el fotograma exacto de AD3-Pipeline-V8.mp4.

Uso: python3 scripts/compare.py <f1> [f2 ...]
"""
from pathlib import Path
import subprocess
import sys
import numpy as np
from PIL import Image

R = Path(__file__).resolve().parents[1]
AD3 = R.parent
V8 = AD3 / 'v8/output/AD3-Pipeline-V8.mp4'
NATIVE = AD3 / 'v7/analysis'
REF = R / 'analysis/ref'
OUT = R / 'analysis/still'
CMP = R / 'analysis/compare'
# El mp4 entregado es la imagen de referencia; los PNG nativos solo como apoyo.
USE_NATIVE = False
for d in (REF, CMP):
    d.mkdir(parents=True, exist_ok=True)


def reference(frame: int):
    """PNG nativo de AE si lo hay; si no, el fotograma exacto del máster."""
    if USE_NATIVE:
        native = NATIVE / f'native-{frame}.png'
        if native.exists():
            return native, 'AE nativo'
    p = REF / f'{frame}.png'
    if not p.exists():
        subprocess.run(
            ['ffmpeg', '-v', 'error', '-y', '-i', str(V8),
             '-vf', f"select='eq(n\\,{frame})'", '-frames:v', '1',
             '-fps_mode', 'passthrough', '-pix_fmt', 'rgb24', str(p)], check=True)
    return p, 'mp4'


def soften(a: np.ndarray, r: int = 4) -> np.ndarray:
    """Desenfoque de caja: descarta el grano y deja la estructura."""
    out = a.astype(np.float32)
    for axis in (0, 1):
        c = np.cumsum(np.pad(out, [(r, r) if i == axis else (0, 0) for i in range(3)],
                             mode='edge'), axis=axis)
        n = 2 * r + 1
        sl = [slice(None)] * 3
        sl[axis] = slice(n, None)
        hi = c[tuple(sl)]
        sl[axis] = slice(0, -n)
        lo = c[tuple(sl)]
        out = (hi - lo) / n
    return out


def main(frames):
    # `estructura` compara tras desenfocar: el grano es ruido procedural y nunca
    # coincide píxel a píxel, pero la geometría y los tiempos sí deben hacerlo.
    print(f'{"frame":>6} {"origen":>10} {"bruto":>7} {"estructura":>11} {"p99":>6}   veredicto')
    worst = 0.0
    for f in frames:
        ref, kind = reference(f)
        a = np.asarray(Image.open(ref).convert('RGB'), dtype=np.int16)
        mine = OUT / f'AD3-V8-{f}.png'
        if not mine.exists():
            print(f'{f:>6}   falta {mine.name}')
            continue
        b = np.asarray(Image.open(mine).convert('RGB'), dtype=np.int16)
        d = np.abs(a - b)
        ds = np.abs(soften(a) - soften(b))
        mean, struct, p99 = d.mean(), ds.mean(), np.percentile(ds, 99)
        worst = max(worst, struct)
        verdict = ('igual' if struct < 2 else 'muy cerca' if struct < 4
                   else 'cerca' if struct < 8 else 'DIFIERE')
        print(f'{f:>6} {kind:>10} {mean:7.2f} {struct:11.2f} {p99:6.1f}   {verdict}')

        h = a.shape[0]
        gap = np.full((h, 8, 3), 255)
        strip = np.concatenate([a, gap, b, gap, np.clip(d * 4, 0, 255)], axis=1)
        Image.fromarray(strip.astype(np.uint8)).save(CMP / f'{f}.png')
    print(f'\npeor estructura: {worst:.2f}')


if __name__ == '__main__':
    main([int(x) for x in sys.argv[1:]] or [1962])

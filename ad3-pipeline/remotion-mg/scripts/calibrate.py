"""Ajusta la distancia de la cámara por defecto de After Effects.

AE proyecta las capas 3D desde una cámara implícita cuya distancia depende de las
dimensiones de la comp. En vez de suponer la fórmula, se barre un rango y se elige
el valor que menos se aleja del render entregado en los dos planos con rotación
en X/Y: el recorrido por el sistema (comp 04) y el plano de pistas (comp 01).
"""
from pathlib import Path
import subprocess
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare import reference, soften   # noqa: E402

R = Path(__file__).resolve().parents[1]
CAL = R / 'analysis/calib'
CAL.mkdir(parents=True, exist_ok=True)

FRAMES = [660, 760, 800, 1600]
VALUES = [int(v) for v in (sys.argv[1:] or
                           [800, 1000, 1200, 1400, 1500, 1600, 1800, 2000, 2400])]

refs = {f: np.asarray(Image.open(reference(f)[0]).convert('RGB'), dtype=np.int16) for f in FRAMES}
soft_refs = {f: soften(refs[f]) for f in FRAMES}

print(f'{"cámara":>8}  ' + '  '.join(f'{f:>7}' for f in FRAMES) + f'  {"media":>7}')
best = (None, 1e9)
for v in VALUES:
    env = {**__import__('os').environ, 'REMOTION_CAMERA': str(v)}
    subprocess.run(
        ['node', 'scripts/still.mjs', 'AD3-V8', ','.join(map(str, FRAMES)),
         'analysis/calib', f'-c{v}'],
        cwd=R, env=env, check=True, capture_output=True)
    scores = []
    for f in FRAMES:
        b = np.asarray(Image.open(CAL / f'AD3-V8-{f}-c{v}.png').convert('RGB'), dtype=np.int16)
        scores.append(float(np.abs(soft_refs[f] - soften(b)).mean()))
    avg = sum(scores) / len(scores)
    print(f'{v:>8}  ' + '  '.join(f'{s:7.2f}' for s in scores) + f'  {avg:7.2f}')
    if avg < best[1]:
        best = (v, avg)

print(f'\nmejor: {best[0]}  (media {best[1]:.2f})')

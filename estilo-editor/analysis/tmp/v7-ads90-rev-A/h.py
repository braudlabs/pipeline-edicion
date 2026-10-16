"""Utilidades locales del revisor v7-ads90-rev-A (solo lectura del vídeo, caché en scratchpad)."""
import subprocess, sys, os
from pathlib import Path
import numpy as np
from PIL import Image
ROOT = Path('/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/estilo-editor')
sys.path.insert(0, str(ROOT / 'scripts'))
from common import probe, src  # noqa
CACHE = Path('/private/tmp/claude-501/-Users-alejandrorubiocamarero-Documents-ChatGPT-editor/1f516058-b06c-4444-a7f3-77af77afb931/scratchpad/v7A')

def frames(slug, a, b):
    """dict n -> ndarray uint8 HxWx3, fotogramas a..b incluidos (caché PNG en scratchpad)."""
    info = probe(slug)
    d = CACHE / slug
    d.mkdir(parents=True, exist_ok=True)
    need = [n for n in range(a, b + 1) if not (d / f'{n:05d}.png').exists()]
    if need:
        n0, n1 = need[0], need[-1]
        t = max(0.0, (n0 - 0.5) * info['fps_den'] / info['fps_num'])
        tmp = d / f'_tmp_{os.getpid()}'
        tmp.mkdir(exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.6f}', '-i', str(src(slug)), '-frames:v', str(n1 - n0 + 1),
                        '-fps_mode', 'passthrough', '-start_number', '0', f'{tmp}/%05d.png'], check=True)
        for p in sorted(tmp.glob('*.png')):
            k = int(p.stem)
            p.rename(d / f'{n0 + k:05d}.png')
        tmp.rmdir()
    return {n: np.asarray(Image.open(d / f'{n:05d}.png').convert('RGB')) for n in range(a, b + 1)}

def white_mask(A, thr=225):
    return A.min(axis=2) >= thr

def bbox(mask, pct=0.2):
    ys, xs = np.nonzero(mask)
    if len(xs) < 30:
        return None
    x0, x1 = np.percentile(xs, [pct, 100 - pct]); y0, y1 = np.percentile(ys, [pct, 100 - pct])
    return x0, y0, x1, y1

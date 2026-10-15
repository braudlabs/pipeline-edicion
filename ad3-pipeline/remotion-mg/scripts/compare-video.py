"""Compara el vídeo renderizado con el entregado, fotograma a fotograma.

A diferencia de `compare.py`, que mide PNG sueltos, esto mide la cadena completa
—render, codificación y todo— contra `AD3-Pipeline-V8.mp4`.

Uso: python3 scripts/compare-video.py [paso]
"""
from pathlib import Path
import subprocess
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare import soften   # noqa: E402

R = Path(__file__).resolve().parents[1]
MINE = R / 'output/AD3-V8.mp4'
V8 = R.parent / 'v8/output/AD3-Pipeline-V8.mp4'
W, H = 1080, 1920
STEP = int(sys.argv[1]) if len(sys.argv) > 1 else 24


def frames(path: Path, step: int):
    """Descodifica uno de cada `step` fotogramas en crudo."""
    p = subprocess.Popen(
        ['ffmpeg', '-v', 'error', '-i', str(path),
         '-vf', f"select='not(mod(n\\,{step}))'", '-fps_mode', 'passthrough',
         '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
        stdout=subprocess.PIPE)
    size = W * H * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    p.stdout.close()
    p.wait()


def main():
    if not MINE.exists():
        sys.exit(f'falta {MINE}; ejecuta npm run render')
    scores = []
    worst = []
    for i, (a, b) in enumerate(zip(frames(V8, STEP), frames(MINE, STEP))):
        n = i * STEP
        s = float(np.abs(soften(a.astype(np.int16)) - soften(b.astype(np.int16))).mean())
        scores.append(s)
        worst.append((s, n))
    scores = np.array(scores)
    worst.sort(reverse=True)
    print(f'{len(scores)} fotogramas comparados (1 de cada {STEP})')
    print(f'  media   {scores.mean():6.2f}')
    print(f'  mediana {np.median(scores):6.2f}')
    print(f'  p90     {np.percentile(scores, 90):6.2f}')
    print(f'  máximo  {scores.max():6.2f}')
    print(f'  por debajo de 6: {int((scores < 6).sum())} de {len(scores)}')
    print('\n  peores:', '  '.join(f'f{n}={s:.1f}' for s, n in worst[:8]))


if __name__ == '__main__':
    main()

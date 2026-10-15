"""Mezcla de audio del anuncio de creatina.

La locución no se corta en ningún momento: 01, 02 y 03 son un plano continuo
partido en tres generaciones, así que sus audios se pegan sin hueco ni solape.
Los dos macros van encima de la imagen, pero su pista queda muda o muy por
debajo — nunca por encima de la voz.

No hay música: solo su voz y el ambiente de la cocina.
"""
from pathlib import Path
import json
import subprocess
import numpy as np

R = Path(__file__).resolve().parents[1]
SRC = Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/'
           'cliente/creativos/2026-09-21-escaparate-web/entrega/02-creatina')
SR = 48000
FPS = 48
T = json.load(open(R / 'remotion/src/timeline.json'))
TOTAL = T['duration']

# El brief autoriza colar el sonido de los macros por debajo de la voz. Se deja
# en un pico de −18 dBFS, que es audible como textura y no compite con ella.
MACROS_DB = -18.0
MACROS = [
    ('04-macro-polvo.mp4', 510, 116),
    ('05-macro-guardar.mp4', 652, 60),
]


def load(name: str) -> np.ndarray:
    """Descodifica el audio de un clip a mono float32 a 48 kHz."""
    raw = subprocess.run(
        ['ffmpeg', '-v', 'error', '-i', str(SRC / name), '-vn',
         '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def place(bed: np.ndarray, sig: np.ndarray, at_frame: int, frames: int,
          src_frame: int = 0, gain: float = 1.0):
    a = round(at_frame / FPS * SR)
    s = round(src_frame / FPS * SR)
    n = round(frames / FPS * SR)
    part = sig[s:s + n]
    if len(part) < n:
        part = np.pad(part, (0, n - len(part)))
    bed[a:a + n] += part * gain


bed = np.zeros(round(TOTAL / FPS * SR), np.float32)

# --- voz, los tres tramos pegados
for seg in T['audio']:
    place(bed, load(seg['src']), seg['masterFrom'], seg['duration'], seg['sourceFrom'])

# --- textura de los macros, por debajo
for name, at, frames in MACROS:
    sig = load(name)
    peak = float(np.abs(sig).max()) or 1.0
    gain = (10 ** (MACROS_DB / 20)) / peak
    place(bed, sig, at, frames, 0, gain)

# --- rampas de entrada y salida, para que no chasquee
ramp = int(0.012 * SR)
bed[:ramp] *= np.linspace(0, 1, ramp)
bed[-ramp:] *= np.linspace(1, 0, ramp)

out = R / 'assets/Voz-Creatina.wav'
out.parent.mkdir(exist_ok=True)
tmp = R / 'analysis/voz-cruda.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR),
                '-ac', '1', '-i', '-', '-ac', '2', '-c:a', 'pcm_s16le', str(tmp)],
               input=bed.tobytes(), check=True)

# Máster cerca de −14 LUFS, como el resto de la serie.
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(tmp),
                '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                '-ar', str(SR), '-ac', '2', '-c:a', 'pcm_s16le', str(out)], check=True)

probe = subprocess.run(
    ['ffmpeg', '-hide_banner', '-i', str(out), '-af', 'volumedetect', '-f', 'null', '-'],
    capture_output=True, text=True).stderr
levels = [l.split(':')[-1].strip() for l in probe.splitlines()
          if 'mean_volume' in l or 'max_volume' in l]
dur = round(len(bed) / SR, 4)
print(f'{out.relative_to(R)}  {dur} s  ({TOTAL} fotogramas a {FPS} fps)')
print('  niveles:', ' / '.join(levels))
print(f'  macros a {MACROS_DB} dBFS de pico, por debajo de la voz')

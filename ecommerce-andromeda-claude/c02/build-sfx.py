"""Pista de acentos ligados a construcciones tipográficas concretas (no a cada corte).

Fuente de los samples: biblioteca ya usada en el proyecto (mercadillo/v03/assets), copiada a
public/assets/audio/sfx. Ganancias bajas bajo la voz; pista separada y desactivable en
src/data/audio.json. Propuesta del agente, pendiente de escucha de Ale.

Uso: python3 ecommerce-andromeda-claude/c02/build-sfx.py
"""
import json
import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent / 'mercadillo/v03/assets'
DST = HERE / 'public/assets/audio/sfx'
OUT = HERE / 'public/assets/audio/stems/sfx-captions.wav'
SR = 48000
FPS = 24
FRAMES = 920

WORDS = json.loads((HERE / 'src/data/words.json').read_text())['words']
wf = lambda i: int(np.floor(WORDS[i]['start'] * FPS + 1e-6))
# «CAÍDO»: caída con g = 9 px/f² desde y=462 hasta el canto y=760 (Scene03.tsx)
landing = wf(66) + float(np.sqrt(2 * (760 - 462) / 9))
close_start = wf(100) - round((266 - 230) / 59.94005994005994 * FPS)
reopen = close_start + (258 - 230) / 59.94005994005994 * FPS

EVENTS = [
    {'id': 'caido-aterriza', 'file': 'impact-bass-1.mp3', 'frame': landing, 'gain': 0.10, 'maxSeconds': 0.42, 'why': '«CAÍDO» cae y toca el canto de las pantallas'},
    {'id': 'seleccion-problema', 'file': 'click-soft.mp3', 'frame': wf(83), 'gain': 0.30, 'maxSeconds': 0.35, 'why': 'selección de «tu problema» (tiradores)'},
    {'id': 'reabre-solucion', 'file': 'click-soft.mp3', 'frame': reopen, 'gain': 0.36, 'maxSeconds': 0.35, 'why': 'la ventana reabre con «la solución»'},
    {'id': 'cinco', 'file': 'pop.mp3', 'frame': wf(110), 'gain': 0.38, 'maxSeconds': 0.5, 'why': '«5» se posa'},
]


def decode(path: Path) -> np.ndarray:
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-'])
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def main():
    DST.mkdir(parents=True, exist_ok=True)
    mix = np.zeros((round(FRAMES * SR / FPS), 2), np.float32)
    report = []
    for e in EVENTS:
        src = SRC / e['file']
        shutil.copy2(src, DST / e['file'])
        x = decode(src)[: int(e['maxSeconds'] * SR)] * e['gain']
        fade = min(len(x), int(0.06 * SR))
        x[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)[:, None]
        a = int(round(e['frame'] / FPS * SR))
        b = min(len(mix), a + len(x))
        mix[a:b] += x[: b - a]
        report.append({**e, 'seconds': round(e['frame'] / FPS, 4), 'peakDb': round(float(20 * np.log10(np.abs(x).max() + 1e-9)), 2)})
    pcm = (np.clip(mix, -1, 1) * 32767).round().astype('<i2')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    (HERE / 'study/sfx-build.json').write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()

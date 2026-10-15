"""Stems de C01 a 48 kHz, cortes exactos por fotograma (24 fps, OUT exclusivo).

- narrador.wav      NARRADOR_COMPLETO_ORIGINAL.mp3 desde 0, sin retiming ni cambios de timbre.
- native-XX.wav     audio nativo de cada clip en su tramo exacto [IN, OUT) con microfundidos
                    de 8 ms. Incluye el HOOK NATIVO (voz generada sincronizada «Más anuncios.
                    Más.» + ambiente) por instrucción directa de Ale; no se usa el stem externo
                    del azul ni la cama provisional del clip 04.
- La ganancia se aplica en Remotion (audio.json) para que siga siendo editable.
- Música: pista vacía, pendiente de Ale.

Uso: python3 ecommerce-andromeda-claude/c02/build-audio.py
"""
import json
import subprocess
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
A = HERE / 'public/assets'
OUT = A / 'audio/stems'
SR = 48000
FPS = 24
FADE = int(0.008 * SR)
TIMELINE = json.loads((HERE / 'src/data/timeline.json').read_text())
RENDER_FRAMES = TIMELINE['renderedFrames']


def decode(path: Path, channels=2) -> np.ndarray:
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ar', str(SR), '-ac', str(channels), '-'])
    return np.frombuffer(raw, np.float32).reshape(-1, channels).copy()


def write(path: Path, x: np.ndarray):
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(x, -1, 1) * 32767).round().astype('<i2')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def fades(x: np.ndarray, n=FADE) -> np.ndarray:
    n = min(n, len(x) // 2)
    ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
    x[:n] *= ramp
    x[-n:] *= ramp[::-1]
    return x


def samples(frames: int) -> int:
    return round(frames * SR / FPS)


def main():
    report = {'sampleRate': SR, 'fps': FPS, 'segments': []}
    narr = decode(A / 'audio/NARRADOR_COMPLETO_ORIGINAL.mp3')
    seg = narr[: samples(RENDER_FRAMES)].copy()
    seg[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR), dtype=np.float32)[:, None]
    write(OUT / 'narrador.wav', seg)
    write(OUT / 'narrador-completo.wav', narr)
    report['narrador'] = {'file': 'audio/stems/narrador.wav', 'start': 0, 'seconds': len(seg) / SR, 'fullSeconds': len(narr) / SR}

    for s in TIMELINE['scenes']:
        clip = HERE / 'public' / s['asset']
        x = decode(clip)
        a, b = samples(s['srcIn']), samples(s['srcIn'] + s['dur'])
        part = x[a:b].copy()
        if len(part) < b - a:
            part = np.vstack([part, np.zeros((b - a - len(part), 2), np.float32)])
        part = fades(part)
        name = f"native-{s['id']}.wav"
        write(OUT / name, part)
        report['segments'].append({'scene': s['id'], 'file': f'audio/stems/{name}', 'recordFrom': s['from'], 'frames': s['dur'],
                                   'sourceInFrames': s['srcIn'], 'samples': len(part), 'peakDb': round(float(20 * np.log10(np.abs(part).max() + 1e-9)), 2)})
    (HERE / 'study/audio-build.json').write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()

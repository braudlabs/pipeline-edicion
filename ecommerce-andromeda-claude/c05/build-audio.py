"""Stems de C04 a 48 kHz, cortes exactos por fotograma (24 fps, OUT exclusivo). 17 unidades, 2050 f.

- narrador.wav      NARRADOR_COMPLETO_ORIGINAL.mp3 entero (0 – 85,39425 s): sin retiming, sin recorte, sin
                    fundidos ni cambios de timbre. WAV de 32 bits flotante, estéreo con la misma conversión
                    de ffmpeg (-ac 2) que usaron C01–C03 y el ensamble del director, de modo que es la
                    decodificación del mp3 muestra por muestra (error máx. 0). El mp3 es mono: ese
                    -ac 2 reparte la señal con -3 dB por canal, igual que en el preview del director.
- native-XX.wav     audio nativo de cada clip en su tramo exacto [IN, OUT) con microfundidos de 8 ms.
                    Incluye el HOOK NATIVO (voz generada sincronizada «Más anuncios. Más.» + ambiente)
                    por instrucción directa de Ale; no se usa el stem externo del azul ni la cama del 04.
                    Si la fuente trae menos audio que vídeo (12: 32 ms), el resto es silencio y el
                    microfundido de salida se aplica al final del audio real, no al del silencio.
- Medición          sonoridad integrada (LUFS), LRA, pico real y de muestra de cada stem →
                    study/audio-build.json. Sirve para fijar las ganancias de src/data/audio.json.
- La ganancia se aplica en Remotion (audio.json) para que siga siendo editable.
- Música: pista vacía, pendiente (la integrará otra persona).

Uso: python3 ecommerce-andromeda-claude/c04/build-audio.py
"""
import json
import re
import struct
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


def write_pcm16(path: Path, x: np.ndarray):
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(x, -1, 1) * 32767).round().astype('<i2')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def write_f32(path: Path, x: np.ndarray):
    """WAV IEEE float de 32 bits (formato 3): conserva las muestras decodificadas sin cuantizar."""
    path.parent.mkdir(parents=True, exist_ok=True)
    n, ch = x.shape
    data = x.astype('<f4').tobytes()
    fmt = struct.pack('<HHIIHHH', 3, ch, SR, SR * ch * 4, ch * 4, 32, 0)
    body = b'WAVE' + b'fmt ' + struct.pack('<I', len(fmt)) + fmt + b'fact' + struct.pack('<II', 4, n) + b'data' + struct.pack('<I', len(data)) + data
    path.write_bytes(b'RIFF' + struct.pack('<I', len(body)) + body)


def fades(x: np.ndarray, real: int, n=FADE) -> np.ndarray:
    """Microfundido de entrada y de salida; la salida termina en la última muestra de audio real."""
    n = min(n, real // 2)
    ramp = np.linspace(0, 1, n, dtype=np.float32)[:, None]
    x[:n] *= ramp
    x[real - n: real] *= ramp[::-1]
    return x


def samples(frames: int) -> int:
    return round(frames * SR / FPS)


def loudness(path: Path) -> dict:
    """EBU R128 con ffmpeg: I (LUFS), LRA (LU) y pico real (dBTP)."""
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-v', 'info', '-i', str(path), '-af', 'ebur128=peak=true:framelog=quiet', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    summary = err[err.rfind('Summary:'):]
    num = lambda m: None if m is None or 'inf' in m.group(1) else float(m.group(1))
    return {
        'lufs': num(re.search(r'I:\s+(-?[\d.]+|-?inf)\s+LUFS', summary)),
        'lra': num(re.search(r'LRA:\s+(-?[\d.]+|-?inf)\s+LU', summary)),
        'truePeakDb': num(re.search(r'Peak:\s+(-?[\d.]+|-?inf)\s+dBFS', summary)),
    }


def db(v: float) -> float:
    return round(float(20 * np.log10(v + 1e-9)), 2)


def main():
    report = {'sampleRate': SR, 'fps': FPS, 'renderedFrames': RENDER_FRAMES, 'segments': []}

    # Narrador: completo, tal cual sale del mp3 (mismo -ac 2 que C03).
    src = A / 'audio/NARRADOR_COMPLETO_ORIGINAL.mp3'
    narr = decode(src)
    mono = decode(src, channels=1)
    write_f32(OUT / 'narrador.wav', narr)
    back = decode(OUT / 'narrador.wav')
    assert back.shape == narr.shape and np.array_equal(back, narr), 'el stem del narrador no es idéntico a la decodificación'
    report['narrador'] = {
        'file': 'audio/stems/narrador.wav', 'start': 0, 'format': 'WAV float32 estéreo 48 kHz',
        'samples': len(narr), 'seconds': len(narr) / SR, 'sourceSeconds': TIMELINE['narratorSeconds'],
        'maxAbsErrorVsDecode': float(np.abs(back - narr).max()),
        'dualMonoDownmixVsMono': float(np.abs(narr[:, 0] - mono[:, 0] * np.float32(np.sqrt(0.5))).max()),
        'peakDb': db(np.abs(narr).max()), **loudness(OUT / 'narrador.wav'),
    }
    assert len(narr) >= samples(int(TIMELINE['narratorFrames'])), 'el narrador no cubre su duración'

    for s in TIMELINE['scenes']:
        clip = HERE / 'public' / s['asset']
        x = decode(clip)
        a, b = samples(s['srcIn']), samples(s['srcIn'] + s['dur'])
        part = x[a:b].copy()
        real = len(part)
        if real < b - a:
            part = np.vstack([part, np.zeros((b - a - real, 2), np.float32)])
        part = fades(part, real)
        name = f"native-{s['id']}.wav"
        write_pcm16(OUT / name, part)
        report['segments'].append({'scene': s['id'], 'file': f'audio/stems/{name}', 'recordFrom': s['from'], 'frames': s['dur'],
                                   'sourceInFrames': s['srcIn'], 'samples': len(part), 'paddedSamples': len(part) - real,
                                   'peakDb': db(np.abs(part).max()), **loudness(OUT / name)})
    (HERE / 'study').mkdir(exist_ok=True)
    (HERE / 'study/audio-build.json').write_text(json.dumps(report, indent=1, ensure_ascii=False))
    n = report['narrador']
    print(f"narrador.wav  {n['seconds']:.5f} s  {n['samples']} muestras  error máx. {n['maxAbsErrorVsDecode']}  {n['lufs']} LUFS  pico {n['peakDb']} dBFS")
    for r in report['segments']:
        print(f"native-{r['scene']:16s} from {r['recordFrom']:4d} {r['frames']:3d} f  {r['samples']:6d} muestras (+{r['paddedSamples']} silencio)  I {r['lufs']} LUFS  LRA {r['lra']}  TP {r['truePeakDb']}  pico {r['peakDb']} dBFS")


if __name__ == '__main__':
    main()

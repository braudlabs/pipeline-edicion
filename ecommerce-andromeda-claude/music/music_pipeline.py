#!/usr/bin/env python3
"""Banda sonora comedy-funk de 85,400 s para Ecommerce Andrómeda con ElevenLabs Music.

Modos:
  --dry-run   Construye y valida el plan, escribe composition_plan.json y cue_timeline.json,
              comprueba dependencias y clave (sin mostrarla) y estima el coste. No gasta créditos.
  --generate  Lanza UNA generación pagada (music_v2_5 + composition_plan). Exige
              --approve-cost y no sobrescribe una toma existente salvo --new-take.
  --conform   Monta la toma a 48 kHz y EXACTAMENTE 85,400 s sin estirar el tiempo: con --edits
              coloca cada sección de la toma con su ataque en el cue (empalmes dentro de las
              paradas naturales), añade notas sueltas de la propia toma donde el guion pide un
              comentario grave, aplica ganancia y paso bajo por cue con microfundidos que no
              desplazan los límites, verifica y escribe final_soundtrack_85_4s.wav y timing_report.json.

Documentación consultada (2026-10-14):
  https://elevenlabs.io/docs/api-reference/music/compose
  https://elevenlabs.io/docs/eleven-api/guides/how-to/music/composition-plans
La API acepta para music_v2/v2_5 `composition_plan.chunks[]` con text, duration_ms
(3000–120000), positive_styles, negative_styles y context_adherence (low|medium|high). En v2
las duraciones de los chunks se respetan siempre. `force_instrumental` solo vale en modo prompt:
aquí lo instrumental se impone con texto y estilos.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
API_URL = 'https://api.elevenlabs.io/v1/music'
MODEL_ID = 'music_v2_5'
OUTPUT_FORMAT = 'mp3_48000_320'  # 48 kHz: sin remuestrear al conformar
SEED = 85402  # toma 3 (toma 1: 85400 en take1/; toma 2: 85401 en take2/)
SR = 48000
TARGET_MS = 85400
TARGET_SAMPLES = TARGET_MS * SR // 1000  # 4.099.200
PRICE_PER_MIN_USD = 0.150  # https://elevenlabs.io/pricing/api (Eleven Music, API, 2026-10-14)

F_PLAN = HERE / 'composition_plan.json'
F_CUES = HERE / 'cue_timeline.json'
F_ORIG = HERE / 'original_music.mp3'
F_META = HERE / 'generation_meta.json'
F_FINAL = HERE / 'final_soundtrack_85_4s.wav'
F_REPORT = HERE / 'timing_report.json'

# ───────────────────────── Identidad musical ─────────────────────────
# Plan 3 (15/10/2026). Ale sobre la toma 2: «no me gusta nada, es como que frena mucho a la
# mitad». La toma 2 paraba al final de casi cada compás (cada cambio de sección y estilos como
# «caper», «staccato», «stabs», «awkward replies») y el montaje añadía silencios. Ahora: groove
# continuo de principio a fin, cinco secciones (menos cambios = menos paradas antes de cada
# tiempo fuerte) y la intensidad cambia por instrumentos, nunca cortando.
NEG_BASE = [
    'vocals', 'singing', 'voice', 'choir', 'whispering', 'spoken word', 'rap', 'scat singing',
    'humming', 'vocal chops', 'laughter', 'crowd noise', 'EDM', 'riser', 'build-up swell',
    'trailer drums', 'orchestral hit', 'circus music', 'kazoo', 'slide whistle', 'cartoon sound effects',
    'sentimental melody', 'stop-time', 'band stops', 'breaks', 'breakdown', 'pauses', 'silence', 'dead air',
    'staccato stops', 'fermata', 'dropout', 'ritardando', 'rubato', 'tempo change', 'stop-start pattern',
]
CORE = [
    'upbeat comedy funk', '122 BPM', 'E minor', 'continuous driving groove', 'groove never stops',
    'steady sixteenth-note hi-hats', 'rolling syncopated electric bass', 'tight kick and snare backbeat',
    'muted funk guitar', 'clavinet', 'catchy three-note nagging bass motif', 'playful', 'bouncy',
    'constant forward momentum', 'instrumental',
]


def chunk(name, start, end, directions, positive, negative_extra, adherence):
    return {
        'name': name,
        'start_s': start,
        'end_s': end,
        'text': '\n'.join([f'[{name}]'] + [f'{{{d}}}' for d in directions]),
        'duration_ms': round((end - start) * 1000),
        'positive_styles': positive,
        'negative_styles': NEG_BASE + negative_extra,
        'context_adherence': adherence,
    }


# Cinco secciones en los grandes cambios del vídeo (cortes de 32,583, 51,542, 66,042 y 78,320);
# suman 85.400 ms. Las tomas 1 y 2 usaron las 15 de la spec (ver take1/ y take2/).
EXPECTED_CHUNKS = 5
CHUNKS = [
    chunk('Cheeky Groove', 0.000, 32.583, [
        'catchy bouncy comedy funk groove from the very first beat, full energy',
        'a nagging three-note bass motif loops over a steady sixteenth-note hi-hat groove',
        'muted guitar and clavinet keep the rhythm moving without ever stopping',
    ], CORE + ['instant start', 'cheeky', 'mischievous', 'punchy premium mix'],
        ['intro swell', 'fade in', 'slow start', 'suspense', 'ambient intro'], 'high'),
    chunk('The Machine Works', 32.583, 51.542, [
        'the same groove gets brighter and fuller',
        'confident interlocking guitar, clavinet and electric piano over the same bass motif',
        'steady unstoppable momentum with an uncluttered, airy arrangement',
    ], CORE + ['brighter', 'fuller arrangement', 'confident', 'satisfying', 'clever'],
        ['triumphant anthem', 'corporate', 'lead melody', 'solo'], 'high'),
    chunk('Warm and Human', 51.542, 66.042, [
        'the same groove continues, lighter and warmer',
        'rounded bass, electric piano and soft rim clicks keep the pulse going',
        'calm and confident, still moving forward',
    ], ['upbeat comedy funk', '122 BPM', 'E minor', 'continuous groove', 'groove never stops', 'steady pulse',
        'rounded electric bass', 'warm electric piano', 'soft rim clicks', 'light hi-hats', 'same bass motif',
        'warm', 'lighter arrangement', 'confident', 'instrumental'],
        ['ballad', 'sad', 'loud drums', 'aggressive'], 'high'),
    chunk('Everything at Once', 66.042, 78.320, [
        'full band, busier and more playful: rapid guitar chops, bass runs, clavinet and punchy drums',
        'then the opening riff comes back in a cheeky variation',
        'friendly confident groove that keeps rolling',
    ], CORE + ['busier', 'energetic', 'full band', 'opening riff reprise', 'friendly'],
        ['drop', 'dubstep', 'loudness wall', 'hard sell anthem'], 'high'),
    chunk('Back to Work', 78.320, 85.400, [
        'the groove continues, softer and warm',
        'the punchy riff returns for the last two seconds',
        'it ends on one short low bass and kick hit on the final beat',
    ], ['upbeat comedy funk', '122 BPM', 'E minor', 'continuous groove', 'warm electric piano', 'soft bass',
        'steady pulse', 'punchy riff reprise', 'final low bass hit', 'instrumental'],
        ['long outro', 'fade out', 'early ending', 'giant final impact', 'ringing cymbal tail'], 'high'),
]

# ───────────────────────── Cue timeline completo ─────────────────────────
# Tratamiento por cue sobre la música YA MONTADA (tiempo de vídeo):
#   gain_db: número, rampa [a, b] o 'mute' (silencio musical; en el vídeo quedan voz, tela y ambiente).
#   lowpass_hz: paso bajo fijo o escalones [[t, Hz], ...] activos desde t (retirada progresiva).
#   treat_from: el tratamiento empieza antes que el cue porque el ataque del compás siguiente cae
#   dentro de la parada previa; se documenta y no cambia el límite perceptivo.
# Un paso bajo apaga brillo (charles, púas, ataque de caja), NO separa instrumentos: bombo y bajo
# siguen. expect: 'built' = tramo construido con material de la propia toma (notas sueltas) sobre silencio.
CUES = [
    {'start': 0.000, 'end': 1.970, 'name': 'explosive opening', 'gain_db': 0, 'expect': 'full'},
    {'start': 1.970, 'end': 4.850, 'name': 'whisper (near silence)', 'gain_db': -26, 'lowpass_hz': 400, 'treat_from': 1.950,
     'expect': 'post', 'why': 'solo queda un bajo tenue; el ataque del compás 2 empieza en 1,952, dentro de la parada'},
    {'start': 4.850, 'end': 5.417, 'name': 'frightened reaction (one low note)', 'gain_db': 'mute', 'expect': 'built'},
    {'start': 5.417, 'end': 14.583, 'name': 'endless waiting (groove returns)', 'gain_db': 0, 'expect': 'full'},
    {'start': 14.583, 'end': 18.750, 'name': 'absurd queue ticket', 'gain_db': 0, 'expect': 'full'},
    {'start': 18.750, 'end': 23.000, 'name': 'old ads fail (progressive removal)', 'gain_db': [0, -5],
     'lowpass_hz': [[19.187, 3500], [20.171, 1200], [21.154, 450], [22.138, 250]], 'expect': 'decreasing',
     'why': 'una sustracción por tiempo fuerte: brillo → ataques → teclados; queda el bajo solo'},
    {'start': 23.000, 'end': 25.417, 'name': 'again?! (motif restarts)', 'gain_db': 0, 'expect': 'full'},
    {'start': 25.417, 'end': 29.050, 'name': 'subject change (polite minimal)', 'gain_db': -4, 'lowpass_hz': 5000, 'expect': 'reduced'},
    {'start': 29.050, 'end': 30.920, 'name': 'hoodie reveal (hard dropout)', 'gain_db': 'mute', 'expect': 'built'},
    {'start': 30.920, 'end': 32.583, 'name': 'the idea (pickup)', 'gain_db': 0, 'expect': 'present'},
    {'start': 32.583, 'end': 42.583, 'name': 'the machine works (full re-entry)', 'gain_db': 0, 'expect': 'full'},
    {'start': 42.583, 'end': 50.400, 'name': 'more ad variations', 'gain_db': 0, 'expect': 'full'},
    {'start': 50.400, 'end': 51.542, 'name': 'owner says yes (resolution)', 'gain_db': -6, 'expect': 'present'},
    {'start': 51.542, 'end': 55.833, 'name': 'bad ideas warning (stripped)', 'gain_db': 'mute', 'expect': 'built'},
    {'start': 55.833, 'end': 61.583, 'name': 'competent humans (warm funk)', 'gain_db': 0, 'expect': 'full'},
    {'start': 61.583, 'end': 66.042, 'name': 'human creative judgment (reduced)', 'gain_db': -8, 'lowpass_hz': 1200, 'expect': 'reduced'},
    {'start': 66.042, 'end': 70.042, 'name': 'ads everywhere (4 s burst)', 'gain_db': 0, 'expect': 'full'},
    {'start': 70.042, 'end': 74.417, 'name': 'the reveal (hesitation + riff)', 'gain_db': 0, 'expect': 'present'},
    {'start': 74.417, 'end': 78.320, 'name': 'call invitation', 'gain_db': 0, 'expect': 'full'},
    {'start': 78.320, 'end': 82.958, 'name': 'honest fit / no-fit (quiet)', 'gain_db': -6, 'lowpass_hz': 1500, 'expect': 'reduced'},
    {'start': 82.958, 'end': 84.800, 'name': 'back to work (riff returns)', 'gain_db': 0, 'expect': 'full'},
    {'start': 84.800, 'end': 85.400, 'name': 'final low button + decay', 'gain_db': 0, 'expect': 'decay'},
]
KEY_POINTS = [1.970, 4.850, 5.417, 18.750, 23.000, 29.050, 29.700, 30.920, 32.583, 50.400, 51.542,
              61.583, 66.042, 70.042, 78.320, 82.958, 84.800, 85.400]
RAMP_S = 0.008  # microfundido anticlic: termina exactamente en el límite, en ambos sentidos


# ───────────────────────── Validación ─────────────────────────
def validate():
    errors = []
    if len(CHUNKS) != EXPECTED_CHUNKS:
        errors.append(f'se esperaban {EXPECTED_CHUNKS} chunks, hay {len(CHUNKS)}')
    total = sum(c['duration_ms'] for c in CHUNKS)
    if total != TARGET_MS:
        errors.append(f'la suma de duraciones es {total} ms, no {TARGET_MS}')
    prev_end = 0.0
    for i, c in enumerate(CHUNKS, 1):
        if not 3000 <= c['duration_ms'] <= 120000:
            errors.append(f'chunk {i} fuera de 3000–120000 ms: {c["duration_ms"]}')
        if abs(c['start_s'] - prev_end) > 1e-9:
            errors.append(f'chunk {i} no empieza donde acaba el anterior')
        prev_end = c['end_s']
        if not c['positive_styles'] or len(c['positive_styles']) > 50 or len(c['negative_styles']) > 50:
            errors.append(f'chunk {i}: estilos vacíos o más de 50')
        if c['context_adherence'] not in ('low', 'medium', 'high'):
            errors.append(f'chunk {i}: context_adherence no válido')
        if any(not s.isascii() for s in c['positive_styles'] + c['negative_styles']):
            errors.append(f'chunk {i}: estilos fuera de ASCII (deben ir en inglés)')
        lines = c['text'].split('\n')
        if len(lines) > 30 or any(len(l) > 200 for l in lines):
            errors.append(f'chunk {i}: texto con más de 30 líneas o líneas de más de 200 caracteres')
        if re.search(r'\b(sing|sings|singing|singer|vocal|vocals|lyric|lyrics|voice|choir)\b', c['text'].lower()):
            errors.append(f'chunk {i}: el texto sugiere voz')
    times = [0.0] + [c['end'] for c in CUES]
    if times != sorted(times) or times[0] != 0.0 or abs(times[-1] - TARGET_MS / 1000) > 1e-9:
        errors.append('los cues no están ordenados o no cubren 0–85,400 s')
    for a, b in zip(CUES, CUES[1:]):
        if abs(a['end'] - b['start']) > 1e-9:
            errors.append(f'hueco o solape entre cues en {a["end"]}')
    if sorted(KEY_POINTS) != KEY_POINTS or KEY_POINTS[0] < 0 or KEY_POINTS[-1] > TARGET_MS / 1000:
        errors.append('puntos clave desordenados o fuera de rango')
    if TARGET_SAMPLES != 4_099_200:
        errors.append('número de muestras objetivo incorrecto')
    return errors


def payload():
    return {
        'model_id': MODEL_ID,
        'composition_plan': {'chunks': [{k: c[k] for k in ('text', 'duration_ms', 'positive_styles', 'negative_styles', 'context_adherence')} for c in CHUNKS]},
        'seed': SEED,
        'store_for_inpainting': True,
    }


def load_key():
    if os.environ.get('ELEVENLABS_API_KEY'):
        return os.environ['ELEVENLABS_API_KEY']
    for env in (HERE / '.env', HERE.parent / '.env', HERE.parent.parent / '.env'):
        if env.exists():
            for line in env.read_text().splitlines():
                if line.strip().startswith('ELEVENLABS_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"').strip("'")
    return None


def write_plan_files():
    F_PLAN.write_text(json.dumps(payload(), indent=2, ensure_ascii=False))
    F_CUES.write_text(json.dumps({
        'target_seconds': TARGET_MS / 1000, 'sample_rate': SR, 'target_samples': TARGET_SAMPLES,
        'chunks': [{k: c[k] for k in ('name', 'start_s', 'end_s', 'duration_ms', 'context_adherence')} for c in CHUNKS],
        'cues': CUES, 'key_points': KEY_POINTS, 'ramp_seconds': RAMP_S,
        'note': 'Tiempos absolutos desde el inicio del vídeo. gain_db y lowpass_hz se aplican a la mezcla completa ya montada: no separan instrumentos.',
    }, indent=2, ensure_ascii=False))


# ───────────────────────── Modos ─────────────────────────
def dry_run():
    errors = validate()
    write_plan_files()
    body = json.dumps(payload()).encode()
    deps = {tool: subprocess.run(['which', tool], capture_output=True).returncode == 0 for tool in ('ffmpeg', 'ffprobe')}
    key = load_key()
    minutes = TARGET_MS / 60000
    print(json.dumps({
        'schema_ok': not errors, 'errors': errors,
        'chunks': len(CHUNKS), 'total_ms': sum(c['duration_ms'] for c in CHUNKS),
        'request': {'method': 'POST', 'url': f'{API_URL}?output_format={OUTPUT_FORMAT}', 'headers': ['xi-api-key: <ELEVENLABS_API_KEY>', 'Content-Type: application/json'],
                    'body_bytes': len(body), 'model_id': MODEL_ID, 'seed': SEED, 'store_for_inpainting': True},
        'dependencies': deps, 'api_key_present': bool(key),
        'cost_estimate_usd': {'prorated': round(minutes * PRICE_PER_MIN_USD, 3), 'if_rounded_up_to_minutes': round(-(-TARGET_MS // 60000) * PRICE_PER_MIN_USD, 3),
                              'source': 'https://elevenlabs.io/pricing/api — Eleven Music $0.150/min; la página no aclara redondeo ni precio por modelo'},
        'files_written': [F_PLAN.name, F_CUES.name],
    }, indent=2, ensure_ascii=False))
    return 0 if not errors and all(deps.values()) else 1


def generate(args):
    errors = validate()
    if errors:
        print('Plan no válido:', errors)
        return 1
    if not args.approve_cost:
        print('Generación pagada bloqueada: añade --approve-cost tras aprobar el coste del --dry-run.')
        return 2
    key = load_key()
    if not key:
        print('Falta ELEVENLABS_API_KEY (variable de entorno o .env en esta carpeta).')
        return 2
    out = F_ORIG
    if out.exists():
        if not args.new_take:
            print(f'{out.name} ya existe: no se repite una generación pagada sin --new-take.')
            return 2
        n = 2
        while (HERE / f'original_music_take{n}.mp3').exists():
            n += 1
        out = HERE / f'original_music_take{n}.mp3'
    write_plan_files()
    req = urllib.request.Request(f'{API_URL}?output_format={OUTPUT_FORMAT}', data=json.dumps(payload()).encode(), method='POST',
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            headers = dict(resp.headers.items())
            with open(out, 'wb') as f:
                while True:
                    block = resp.read(65536)
                    if not block:
                        break
                    f.write(block)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors='replace')[:4000]
        print(f'Error HTTP {e.code}: {detail}')
        F_META.write_text(json.dumps({'error': e.code, 'detail': detail}, indent=2, ensure_ascii=False))
        return 3
    safe_headers = {k: v for k, v in headers.items() if 'key' not in k.lower() and 'auth' not in k.lower()}
    F_META.write_text(json.dumps({'file': out.name, 'model_id': MODEL_ID, 'output_format': OUTPUT_FORMAT, 'seed': SEED,
                                  'response_headers': safe_headers}, indent=2, ensure_ascii=False))
    print(f'Generado {out.name} ({out.stat().st_size} bytes). Cabeceras (incluye el id de la canción) en {F_META.name}.')
    return 0


def ffprobe_duration(path: Path) -> float:
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)])
    return float(out.strip())


def decode(path: Path) -> np.ndarray:
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'])
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def jsonable(o):
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError(type(o).__name__)


def db(x):
    return 20 * np.log10(max(float(x), 1e-12))


def rms(x):
    return float(np.sqrt(np.mean(np.square(x)))) if len(x) else 0.0


def loudness_lufs(x: np.ndarray) -> float:
    tmp = HERE / '.lufs_tmp.wav'
    write_wav(tmp, x, bits=16)
    out = subprocess.run(['ffmpeg', '-nostats', '-i', str(tmp), '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    tmp.unlink(missing_ok=True)
    vals = [l for l in out.splitlines() if l.strip().startswith('I:')]
    return float(vals[-1].split()[1]) if vals else float('nan')


def write_wav(path: Path, x: np.ndarray, bits=24):
    x = np.clip(x, -1.0, 1.0 - 1e-7)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(bits // 8)
        w.setframerate(SR)
        if bits == 16:
            w.writeframes((x * 32767).round().astype('<i2').tobytes())
        else:
            ints = (x * 8388607).round().astype('<i4')
            b = ints.reshape(-1, 1).view(np.uint8).reshape(-1, 4)[:, :3]
            w.writeframes(b.tobytes())


def treated_cues(ed: dict) -> list:
    """Cues con el tratamiento de la toma: `cue_treatment` del JSON de montaje sustituye la
    ganancia/filtro por defecto de CUES (p. ej. la toma 3 no lleva silencios). null = quitar."""
    t = ed.get('cue_treatment')
    if not t:
        return CUES
    out = []
    for c in CUES:
        c2 = dict(c)
        for k, v in {**t.get('default', {}), **t.get(c['name'], {})}.items():
            if v is None:
                c2.pop(k, None)
            else:
                c2[k] = v
        out.append(c2)
    return out


def gain_envelope(n: int, cues: list = CUES) -> tuple[np.ndarray, list]:
    """Automatización por cue en tiempo de vídeo. Cada cambio se suaviza en RAMP_S y termina
    exactamente en su límite: el nuevo nivel rige desde el límite, que no se desplaza."""
    g_db = np.zeros(n)
    applied = []
    for c in cues:
        a, b = int(round(c.get('treat_from', c['start']) * SR)), int(round(c['end'] * SR))
        v = c['gain_db']
        if v == 'mute':
            g_db[a:b] = -120.0
        elif isinstance(v, list):  # rampa progresiva (retirada de energía)
            g_db[a:b] = np.linspace(v[0], v[1], b - a)
        else:
            g_db[a:b] = v
        applied.append({'cue': c['name'], 'start': c['start'], 'end': c['end'], 'gain_db': v,
                        'lowpass_hz': c.get('lowpass_hz'), 'treat_from': c.get('treat_from')})
    g = 10 ** (g_db / 20)
    r = int(RAMP_S * SR)
    for e in sorted({int(round(c.get('treat_from', c['start']) * SR)) for c in cues if c['start'] > 0}):
        s0 = max(1, e - r)
        if abs(g[e] - g[s0 - 1]) > 1e-9:
            g[s0:e] = np.linspace(g[s0 - 1], g[e], e - s0, endpoint=False)
    return g, applied


def lowpass_fft(sig: np.ndarray, fc: float, order: int = 4) -> np.ndarray:
    """Paso bajo de fase cero (magnitud Butterworth) para fragmentos cortos."""
    pad = int(0.05 * SR)
    buf = np.zeros((len(sig) + 2 * pad, sig.shape[1]))
    buf[pad:pad + len(sig)] = sig
    f = np.fft.rfftfreq(len(buf), 1 / SR)
    h = 1 / np.sqrt(1 + (f / fc) ** (2 * order))
    return np.fft.irfft(np.fft.rfft(buf, axis=0) * h[:, None], len(buf), axis=0)[pad:pad + len(sig)]


def cutoff_at(c):
    """Corte del paso bajo de un cue en el instante t (None = sin filtro)."""
    lp = c.get('lowpass_hz')
    if lp is None:
        return None
    if isinstance(lp, (int, float)):
        return lambda t: float(lp)
    steps = sorted(lp)
    return lambda t: next((float(hz) for t0, hz in reversed(steps) if t >= t0), None)


def lowpass_region(y: np.ndarray, a: int, b: int, fc_at, n: int = 2048):
    """Paso bajo variable (STFT Hann·Hann al 75 %) en [a, b) de la pista montada. Lo que suena desde
    b se excluye del análisis para que el filtro no arrastre el ataque de la sección siguiente."""
    hop = n // 4
    lo = max(0, a - 2 * n)
    block = y[lo:b].astype(np.float64)
    L = len(block)
    buf = np.zeros((L + 2 * n, 2))
    buf[n:n + L] = block
    w = np.hanning(n + 1)[:-1]
    f = np.fft.rfftfreq(n, 1 / SR)
    out = np.zeros_like(buf)
    norm = np.zeros(len(buf))
    for s in range(0, len(buf) - n + 1, hop):
        t = (lo - n + s + n // 2) / SR
        fc = fc_at(t) if a / SR <= t < b / SR else None
        fr = buf[s:s + n] * w[:, None]
        if fc:
            fr = np.fft.irfft(np.fft.rfft(fr, axis=0) * (1 / np.sqrt(1 + (f / fc) ** 8))[:, None], n, axis=0)
        out[s:s + n] += fr * w[:, None]
        norm[s:s + n] += w ** 2
    res = out[n:n + L] / np.maximum(norm[n:n + L], 1e-12)[:, None]
    k0 = max(0, (a - n) - lo)  # antes de aquí la máscara vale 1 y la reconstrucción es exacta
    y[lo + k0:b] = res[k0:].astype(np.float32)


def render_edl(x: np.ndarray, ed: dict) -> tuple[np.ndarray, list]:
    """Coloca cada segmento de la toma en su posición de vídeo (copia de muestras, sin estirar)."""
    out = np.zeros((TARGET_SAMPLES, 2), np.float32)
    rep = []
    prev = None
    for s in ed['segments']:
        a, b = s['src']
        shift = s['anchor'][1] - s['anchor'][0] if 'anchor' in s else s['shift']
        ia, ib = int(round(a * SR)), int(round(b * SR))
        d = int(round((a + shift) * SR))
        piece = x[ia:ib].copy()
        fi = int(round(s.get('fade_in_ms', 3) * SR / 1000))
        fo = int(round(s.get('fade_out_ms', 3) * SR / 1000))
        if fi:
            piece[:fi] *= np.linspace(0, 1, fi, endpoint=False, dtype=np.float32)[:, None]
        if fo:
            piece[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)[:, None]
        lo, hi = max(0, d), min(TARGET_SAMPLES, d + len(piece))
        out[lo:hi] += piece[lo - d:hi - d]
        item = {'id': s['id'], 'src': [a, b], 'dst': [round(a + shift, 4), round(b + shift, 4)], 'shift_s': round(shift, 4)}
        if 'anchor' in s:
            item['anchor'] = {'src_onset': s['anchor'][0], 'cue': s['anchor'][1]}
        if prev is not None:
            item['time_change_at_joint_s'] = round(shift - prev, 4)  # + silencio añadido en la parada, − quitado
        item['why'] = s.get('why')
        prev = shift
        rep.append(item)
    return out, rep


def add_notes(y: np.ndarray, x: np.ndarray, notes: list) -> list:
    """Notas sueltas tomadas de la propia toma (paso bajo y envolvente seca), en tiempo de vídeo."""
    rep = []
    pre = int(0.002 * SR)
    for n in notes:
        on = int(round(n['src'] * SR))
        snip = lowpass_fft(x[on - pre:on + int(round(n['dur'] * SR))].astype(np.float64), n['lowpass_hz'])
        t = (np.arange(len(snip)) - pre) / SR
        hold = n.get('hold_ms', 40) / 1000
        tau = max(1e-3, (n['dur'] - hold) / np.log(1000))  # −60 dB al final de la nota
        env = np.clip((t + pre / SR) / (pre / SR), 0, 1)
        env = np.where(t > hold, np.exp(-(t - hold) / tau), env)
        snip *= (env * 10 ** (n['gain_db'] / 20))[:, None]
        d = int(round(n['dst'] * SR)) - pre
        y[d:d + len(snip)] += snip.astype(np.float32)
        rep.append({k: n[k] for k in ('id', 'src', 'dst', 'dur', 'lowpass_hz', 'gain_db', 'why') if k in n})
    return rep


def joint_click(sig: np.ndarray, t: float) -> tuple[float, float]:
    """Salto máximo de muestra en ±1,5 ms del empalme frente al percentil 99 de su entorno (±60 ms)."""
    m = sig.mean(1).astype(np.float64)
    i, w, ctx = int(round(t * SR)), int(0.0015 * SR), int(0.06 * SR)
    d = np.abs(np.diff(m[max(0, i - ctx):i + ctx]))
    c = min(i, ctx)
    ratio = 20 * np.log10((d[max(0, c - w):c + w].max() + 1e-9) / (np.percentile(d, 99) + 1e-9))
    lvl = db(rms(m[max(0, i - w):i + w]))
    return round(float(ratio), 1), round(float(lvl), 1)


def conform(args):
    src = HERE / args.source if args.source else F_ORIG
    if not src.exists():
        print(f'No existe {src.name}: genera primero (--generate).')
        return 2
    report = {'source': src.name, 'target_seconds': TARGET_MS / 1000, 'target_samples': TARGET_SAMPLES, 'sample_rate': SR,
              'deviations': [], 'needs_listening': [], 'checks': []}
    dur = ffprobe_duration(src)
    report['source_duration_ffprobe_s'] = dur
    x = decode(src)
    report['decoded_samples'] = len(x)
    # Silencio digital inicial (retardo del codificador): se recorta; la música debe empezar en 0.
    thr = 10 ** (-70 / 20)
    nz = np.nonzero(np.max(np.abs(x), axis=1) > thr)[0]
    lead = int(nz[0]) if len(nz) else 0
    report['leading_digital_silence_ms'] = round(lead / SR * 1000, 2)
    if lead > int(0.12 * SR):
        report['deviations'].append(f'silencio inicial de {lead / SR:.3f} s en la generación: la música no empieza en 0')
    x = x[lead:] if lead <= int(0.12 * SR) else x
    diff = len(x) - TARGET_SAMPLES
    report['length_difference_ms'] = round(diff / SR * 1000, 2)
    ed = json.loads((HERE / args.edits).read_text()) if args.edits else {}
    if ed.get('segments'):
        need = max(s['src'][1] for s in ed['segments'])
        if need * SR > len(x):
            report['deviations'].append(f'la EDL pide material hasta {need:.3f} s y la toma dura {len(x) / SR:.3f} s')
            F_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=jsonable))
            print(report['deviations'][-1])
            return 4
        y0, segs = render_edl(x, ed)
        report['edl'] = segs
        report['edits_file'] = args.edits
        report['edits_note'] = ed.get('note')
        report['deviations'].append(f'montaje por segmentos: la duración la fija la timeline (85,400 s); la toma recortada dura '
                                    f'{len(x) / SR:.3f} s y sus últimos {(len(x) / SR) - need:.3f} s (silencio tras el remate) no se usan')
        report['deviations'] += ed.get('floating', [])
    else:
        tol = int(0.120 * SR)
        if abs(diff) > tol and not args.allow_mismatch:
            report['deviations'].append(f'duración generada {len(x) / SR:.3f} s frente a 85,400 s: diferencia mayor que 120 ms. '
                                        'No se estira ni se trunca: regenerar o hacer inpainting del chunk final (ver README).')
            F_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=jsonable))
            print(json.dumps(report, indent=2, ensure_ascii=False, default=jsonable))
            return 4
        if diff > 0:
            report['deviations'].append(f'sobran {diff / SR * 1000:.1f} ms tras el final: se recortan después del decaimiento con fundido de 40 ms que termina en 85,400')
            x = x[:TARGET_SAMPLES]
        elif diff < 0:
            report['deviations'].append(f'faltan {-diff / SR * 1000:.1f} ms: se completa con silencio tras el decaimiento')
            x = np.vstack([x, np.zeros((-diff, 2), np.float32)])
        y0 = x.copy()
        # Ediciones antiguas (v1): mover una frase entera, nunca estirar.
        report['editorial_moves'] = []
        for mv in ed.get('moves', []):
            a = int(round(mv['from_s'] * SR))
            sh = int(round(mv['shift_s'] * SR))
            fade = max(1, int(mv.get('fade_ms', 5) * SR / 1000))
            tail = y0[a:].copy()
            y0[a:] = 0.0
            y0[a - fade:a] *= np.linspace(1, 0, fade, dtype=np.float32)[:, None]
            tail[:fade] *= np.linspace(0, 1, fade, dtype=np.float32)[:, None]
            room = len(y0) - (a + sh)
            y0[a + sh:] += tail[:room]
            report['editorial_moves'].append({**mv, 'samples_moved': int(min(len(tail), room))})
    # Medición por cue de la música montada (antes de tratar) para comprobar dropouts/arreglos.
    measured = []
    for c in CUES:
        a, b = int(c['start'] * SR), int(c['end'] * SR)
        measured.append({'cue': c['name'], 'start': c['start'], 'end': c['end'], 'expect': c['expect'], 'rms_dbfs': round(db(rms(y0[a:b])), 2)})
    full = [m['rms_dbfs'] for m in measured if m['expect'] == 'full']
    ref = float(np.median(full)) if full else -20.0
    for m in measured:
        rel = m['rms_dbfs'] - ref
        m['relative_to_groove_db'] = round(rel, 2)
        if m['expect'] == 'post':
            m['note'] = 'caída creada en posproducción (ganancia + paso bajo)'
        if m['expect'] == 'built':
            m['note'] = 'tramo construido: silencio musical + notas sueltas de la propia toma (ver notes)'
        if m['expect'] == 'reduced' and rel > -4:
            report['needs_listening'].append(f'{m["cue"]}: la generación no reduce el arreglo ({rel:.1f} dB); lo hacen ganancia y paso bajo')
        if m['expect'] == 'full' and rel < -8:
            report['needs_listening'].append(f'{m["cue"]}: groove más débil de lo previsto ({rel:.1f} dB)')
    report['measured_generation'] = measured
    # Tratamientos por cue: paso bajo, ganancia y, después, las notas construidas.
    y = y0.copy()
    cues = treated_cues(ed)
    for c in cues:
        fc = cutoff_at(c)
        if fc:
            lowpass_region(y, int(round(c.get('treat_from', c['start']) * SR)), int(round(c['end'] * SR)), fc)
    g, applied = gain_envelope(len(y), cues)
    y *= g[:, None].astype(np.float32)
    report['notes'] = add_notes(y, x, ed.get('notes', []))
    # Final: decaimiento natural tras 84,800 y fundido de 40 ms que termina exactamente en 85,400.
    f = int(0.040 * SR)
    y[-f:] *= np.linspace(1, 0, f, dtype=np.float32)[:, None]
    # Nivel de la pista de música (la mezcla con la voz se decide en el montaje).
    lufs = loudness_lufs(y)
    target_lufs = -16.0
    gain = 10 ** ((target_lufs - lufs) / 20) if np.isfinite(lufs) else 1.0
    peak = float(np.max(np.abs(y))) * gain
    if peak > 10 ** (-1 / 20):
        gain *= 10 ** (-1 / 20) / peak
    y *= gain
    report['loudness'] = {'measured_lufs_before': round(lufs, 2), 'target_lufs': target_lufs, 'applied_gain_db': round(db(gain), 2),
                          'peak_dbfs_after': round(db(np.max(np.abs(y))), 2), 'note': 'nivel de la pista aislada; ducking bajo la voz en el montaje'}
    report['applied_treatment'] = applied
    write_wav(F_FINAL, y.astype(np.float32), bits=24)
    # Verificación
    with wave.open(str(F_FINAL)) as w:
        frames, rate, ch = w.getnframes(), w.getframerate(), w.getnchannels()
    report['checks'] += [
        {'check': 'muestras por canal = 4.099.200 a 48 kHz', 'ok': frames == TARGET_SAMPLES and rate == SR and ch == 2, 'value': [frames, rate, ch]},
        {'check': 'arranca en el tiempo cero (primeros 20 ms con señal)', 'ok': db(rms(y[: int(0.02 * SR)])) > -50, 'value': round(db(rms(y[: int(0.02 * SR)])), 1)},
        {'check': 'remate final presente (84,60–84,95 s)', 'ok': db(rms(y[int(84.6 * SR): int(84.95 * SR)])) > -45, 'value': round(db(rms(y[int(84.6 * SR): int(84.95 * SR)])), 1)},
        {'check': 'termina sin clic en 85,400 (última muestra ≈ 0 y sin saltos en los últimos 10 ms)',
         'ok': float(np.max(np.abs(y[-1]))) < 1e-3 and float(np.max(np.abs(np.diff(y[-int(0.010 * SR):], axis=0)))) < 0.05},
        {'check': 'sin silencio inicial no deseado', 'ok': report['leading_digital_silence_ms'] <= 120},
        {'check': 'sin outro duplicado o alargado (duración exacta)', 'ok': frames == TARGET_SAMPLES},
    ]
    if ed.get('segments'):
        hits = []
        mo, ms = y.mean(1).astype(np.float64), x.mean(1).astype(np.float64)
        span, lag = int(0.060 * SR), int(0.010 * SR)
        for s in report['edl']:
            if 'anchor' not in s:
                continue
            cue, so = s['anchor']['cue'], s['anchor']['src_onset']
            # Desfase real entre máster y toma justo después del cue (correlación cruzada ±10 ms).
            o = mo[int(round(cue * SR)):int(round(cue * SR)) + span]
            r = ms[int(round(so * SR)) - lag:int(round(so * SR)) + span + lag]
            cc = np.correlate(r, o, 'valid')
            hits.append({'segment': s['id'], 'cue': cue, 'lag_samples': int(np.argmax(cc)) - lag})
        report['checks'].append({'check': 'cada entrada anclada cae en su cue (desfase máster–toma = 0 ± 1 muestra)',
                                 'ok': all(abs(h['lag_samples']) <= 1 for h in hits), 'value': hits})
        joints = []
        for s in report['edl']:
            for t in s['dst']:
                if 0.01 < t < TARGET_MS / 1000 - 0.01:
                    ratio, lvl = joint_click(y, t)
                    joints.append({'segment': s['id'], 't': t, 'jump_vs_context_db': ratio, 'level_dbfs': lvl, 'ok': ratio < 6 or lvl < -55})
        report['checks'].append({'check': 'empalmes sin clic (salto ≤ +6 dB sobre su entorno o en silencio)',
                                 'ok': all(j['ok'] for j in joints), 'value': [j for j in joints if not j['ok']] or 'todos limpios'})
        iso = []
        for n in report['notes']:
            d = n['dst']
            on, before = db(rms(y[int(d * SR): int((d + 0.12) * SR)])), db(rms(y[int((d - 0.25) * SR): int((d - 0.03) * SR)]))
            isolated = next((m.get('isolated', True) for m in ed.get('notes', []) if m['id'] == n['id']), True)
            iso.append({'note': n['id'], 't': d, 'note_dbfs': round(on, 1), 'before_dbfs': round(before, 1),
                        'ok': on > -45 and (on - before >= 15 if isolated else on - before >= 6)})
        report['checks'].append({'check': 'notas construidas presentes y destacadas (≥ 15 dB sobre silencio; ≥ 6 dB tras música)', 'ok': all(i['ok'] for i in iso), 'value': iso})
    report['key_points'] = [{'t': p, 'rms_dbfs_80ms_after': round(db(rms(y[int(p * SR): int(p * SR) + int(0.08 * SR)])), 1)} for p in KEY_POINTS if p < TARGET_MS / 1000]
    report['needs_listening'] += ed.get('needs_listening', [
        'Motivo de tres notas y respuestas del fagot: no verificable automáticamente',
        'Retirada progresiva guitarra → batería → teclados (18,75–23,00): la ganancia no separa instrumentos'])
    for c in report['checks']:
        c['ok'] = bool(c['ok'])
    report['all_checks_ok'] = all(c['ok'] for c in report['checks'])
    F_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=jsonable))
    print(json.dumps({k: report[k] for k in ('source_duration_ffprobe_s', 'length_difference_ms', 'deviations', 'needs_listening', 'checks', 'all_checks_ok')}, indent=2, ensure_ascii=False, default=jsonable))
    return 0 if report['all_checks_ok'] else 5


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    m = ap.add_mutually_exclusive_group(required=True)
    m.add_argument('--dry-run', action='store_true')
    m.add_argument('--generate', action='store_true')
    m.add_argument('--conform', action='store_true')
    ap.add_argument('--approve-cost', action='store_true', help='confirma el coste estimado (obligatorio para --generate)')
    ap.add_argument('--new-take', action='store_true', help='permite otra generación pagada sin sobrescribir la anterior')
    ap.add_argument('--source', help='toma a conformar (por defecto original_music.mp3)')
    ap.add_argument('--allow-mismatch', action='store_true', help='conformar aunque la duración difiera más de 120 ms (solo tras revisar)')
    ap.add_argument('--edits', help='JSON de montaje de la toma: segmentos colocados en el tiempo del vídeo y notas sueltas (sin estirar)')
    a = ap.parse_args()
    if a.dry_run:
        return dry_run()
    if a.generate:
        return generate(a)
    return conform(a)


if __name__ == '__main__':
    sys.exit(main())

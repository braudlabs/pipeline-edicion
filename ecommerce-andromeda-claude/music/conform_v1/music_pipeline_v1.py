#!/usr/bin/env python3
"""Banda sonora comedy-funk de 85,400 s para Ecommerce Andrómeda con ElevenLabs Music.

Modos:
  --dry-run   Construye y valida el plan, escribe composition_plan.json y cue_timeline.json,
              comprueba dependencias y clave (sin mostrarla) y estima el coste. No gasta créditos.
  --generate  Lanza UNA generación pagada (music_v2_5 + composition_plan). Exige
              --approve-cost y no sobrescribe una toma existente salvo --new-take.
  --conform   Ajusta la toma a 48 kHz y EXACTAMENTE 85,400 s sin estirar el tiempo, aplica la
              automatización de ganancia por cue con microfundidos, verifica y escribe
              final_soundtrack_85_4s.wav y timing_report.json.

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
SEED = 85401  # toma 2 (la toma 1 usó 85400: ver take1/)
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
NEG_BASE = [
    'vocals', 'singing', 'voice', 'choir', 'whispering', 'spoken word', 'rap', 'scat singing',
    'humming', 'vocal chops', 'laughter', 'crowd noise', 'EDM', 'riser', 'build-up swell',
    'trailer drums', 'orchestral hit', 'huge cinematic impact', 'circus music', 'kazoo',
    'slide whistle', 'boing', 'cartoon sound effects', 'sentimental melody', 'generic corporate funk',
    # Toma 1: el modelo convirtió «hard stop / near silence» en paradas cada compás y silencios
    # largos. Las caídas exactas se hacen ahora en posproducción; la música se pide continua.
    'silence', 'long pauses', 'stop-start pattern', 'breaks between bars', 'dead air',
]
CORE = [
    'aggressive comedy funk', 'cinematic funk caper', '122 BPM', 'E minor',
    'fat gritty syncopated electric bass', 'tight dry kick and snappy snare', 'tight hi-hats and rim clicks',
    'sharp muted wah funk guitar scratches', 'percussive rhythmic clavinet', 'staccato piano accents',
    'sneaky pizzicato strings', 'awkward low bassoon replies', 'three-note nagging bass motif', 'instrumental',
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


# Tabla de la especificación (15 chunks, suman 85.400 ms).
# Plan 2: la generación aporta un groove CONTINUO con su arreglo (más lleno o más ligero, qué
# instrumentos entran o salen, motivo y fagot); las caídas al casi silencio en 1,970, 29,050,
# 51,542… y el corte final se hacen en posproducción, al milisegundo. En la toma 1 las palabras
# «stop», «silence» y «dropout» del primer chunk se volvieron la identidad de toda la pieza.
CHUNKS = [
    chunk('Cold Open', 0.000, 5.417, [
        'full-band syncopated funk riff hits on the very first beat at full energy',
        'driving groove keeps going with the nagging three-note bass motif',
        'a short awkward low bassoon reply at the end of the phrase',
    ], CORE + ['brazen', 'mischievous', 'punchy premium mix', 'instant start at full energy', 'continuous driving groove'],
        ['intro swell', 'fade in', 'ambient pad intro', 'suspense', 'slow start'], 'high'),
    chunk('Endless Waiting', 5.417, 14.583, [
        'the full funk groove drives on',
        'nagging repetitive bass hook with clockwork precision',
        'muted guitar scratches and clavinet answers',
        'awkward low bassoon complaints between phrases',
    ], ['comedy funk', '122 BPM', 'E minor', 'fat syncopated bass hook', 'repetitive nagging motif', 'tight dry drums',
        'muted funk guitar scratches', 'clavinet', 'low bassoon complaints', 'clockwork rhythmic precision', 'catchy',
        'continuous groove', 'instrumental'],
        ['suspense', 'tension drones', 'slow'], 'high'),
    chunk('Absurd Ticket', 14.583, 18.750, [
        'same groove with more rhythmic activity',
        'fast staccato clavinet and piano tumble over the beat',
    ], ['comedy funk', '122 BPM', 'same tempo', 'busier rhythmic subdivisions', 'staccato clavinet runs',
        'staccato piano tumble', 'tight drums', 'fat bass', 'continuous groove', 'instrumental'],
        ['tempo change', 'accelerando'], 'high'),
    chunk('Old Ads Fail', 18.750, 23.000, [
        'the arrangement thins out step by step',
        'the guitar leaves, then the drums leave, then the keys leave',
        'only the nagging bass motif is left playing, softer',
    ], ['comedy funk', '122 BPM', 'arrangement thinning out', 'instruments leaving one by one', 'deflating',
        'solo bass motif at the end', 'deadpan', 'instrumental'],
        ['crescendo', 'build-up', 'full band at the end', 'dramatic'], 'medium'),
    chunk('Again and Polite Interlude', 23.000, 29.050, [
        'the opening bass motif starts again, stubborn repetition, full groove',
        'one irritated low bassoon answer',
        'then a polite minimalist funk vamp with soft bass, light drums and small harmonic accents',
    ], ['comedy funk', '122 BPM', 'E minor', 'stubborn repeated motif', 'low bassoon answer', 'deadpan',
        'polite minimalist funk vamp', 'soft bass', 'light drums', 'small harmonic accents', 'awkward anticipation', 'instrumental'],
        ['impact', 'crescendo'], 'high'),
    chunk('Hoodie Reveal', 29.050, 32.583, [
        'very light bass and clavinet vamp, quiet and tense',
        'one low bassoon note',
        'quick sharp funky bass and clavinet pickup leading into a big groove',
    ], ['comedy funk', '122 BPM', 'light quiet vamp', 'single low bassoon note', 'sharp funky pickup',
        'clavinet and bass motif', 'instrumental'],
        ['cymbal crash', 'whistle', 'sting', 'pad'], 'medium'),
    chunk('The Machine Works', 32.583, 42.583, [
        'major full-band funk re-entry on the downbeat',
        'powerful crisp bass and drum pocket',
        'interlocking muted guitar, clavinet and staccato piano',
        'tidy, clever, confident and playful, leaving room for narration',
    ], ['comedy funk', 'cinematic funk caper', '122 BPM', 'E minor', 'powerful bass and drum pocket', 'interlocking muted guitar',
        'clavinet', 'staccato piano', 'satisfying', 'confident', 'playful', 'tight arrangement', 'continuous groove', 'instrumental'],
        ['triumphant anthem', 'corporate', 'overly busy', 'lead melody'], 'high'),
    chunk('More Variations', 42.583, 50.400, [
        'controlled increase in rhythmic complexity',
        'eager looping bass motif with clever guitar answers',
        'clavinet syncopation, energetic and satisfying',
    ], ['comedy funk', '122 BPM', 'looping bass motif', 'guitar call and response', 'clavinet syncopation',
        'energetic', 'increasing complexity', 'tight drums', 'continuous groove', 'instrumental'],
        ['lead melody', 'solo', 'loud cymbals'], 'high'),
    chunk('Yes Then Bad Ideas', 50.400, 55.833, [
        'a small satisfying chord resolution',
        'then an awkward sparse bass line with soft low bassoon notes and no drums',
        'a descending two-note bassoon comment',
    ], ['comedy funk', '122 BPM', 'short harmonic resolution', 'awkward sparse bass line', 'no drums',
        'soft low bassoon', 'descending two-note bassoon', 'deadpan', 'instrumental'],
        ['big hit', 'impact', 'drum beat'], 'medium'),
    chunk('Competent Humans', 55.833, 61.583, [
        'warm rhythmic funk groove returns',
        'rounded bass, electric piano and softer guitar',
        'same motif, more mature and assured',
    ], ['warm funk', '122 BPM', 'E minor', 'rounded bass', 'electric piano', 'soft muted guitar', 'same motif matured',
        'assured', 'charming', 'subtly funny', 'continuous groove', 'instrumental'],
        ['aggressive', 'loud drums'], 'high'),
    chunk('Human Judgment', 61.583, 66.042, [
        'warm electric piano chords playing continuously',
        'soft steady bass line and light rim clicks',
        'confident and calm under the narration',
    ], ['warm electric piano chords', 'soft steady bass line', 'light rim clicks', 'stable harmony', 'confident', 'calm',
        '122 BPM', 'continuous', 'instrumental'],
        ['sentimental strings', 'busy drums', 'piano ballad'], 'medium'),
    chunk('Ads Everywhere', 66.042, 70.042, [
        'four seconds of controlled comedic chaos',
        'rapid interlocking guitar chops, bass runs, clavinet, staccato piano and punchy drums',
        'bassoon chasing the rhythm',
    ], ['comedy funk', '122 BPM', 'frantic but controlled', 'rapid guitar chops', 'bass runs', 'clavinet', 'staccato piano',
        'punchy drums', 'bassoon runs', 'high rhythmic activity', 'instrumental'],
        ['drop', 'dubstep', 'loudness wall'], 'medium'),
    chunk('The Reveal', 70.042, 74.417, [
        'a brief questioning bass and clavinet phrase',
        'the opening funk riff returns with the full band in a cheeky knowing variation',
    ], ['comedy funk', '122 BPM', 'E minor', 'questioning phrase', 'opening riff reprise', 'cheeky', 'knowing', 'fat bass',
        'clavinet', 'full band', 'instrumental'],
        ['wink sound effect', 'sting'], 'high'),
    chunk('Call Invitation', 74.417, 78.320, [
        'solid memorable friendly funk groove',
        'confident, approachable and slightly mischievous',
    ], ['comedy funk', '122 BPM', 'solid groove', 'friendly', 'approachable', 'confident', 'slightly mischievous',
        'tight drums', 'fat bass', 'continuous groove', 'instrumental'],
        ['hard sell anthem', 'escalation', 'crescendo'], 'high'),
    chunk('Honest Fit and Back to Work', 78.320, 85.400, [
        'warm electric piano and soft bass with a light steady groove, grounded and direct',
        'the punchy full-band caper funk riff returns for the last two seconds',
        'the very last beat is one punchy low bass and kick hit',
    ], ['warm electric piano', 'soft bass', 'light steady groove', 'grounded', 'trustworthy', 'punchy funk riff reprise',
        'full band at the very end', 'final low bass hit', '122 BPM', 'instrumental'],
        ['long outro', 'fade out', 'early ending', 'giant final impact', 'ringing cymbal tail'], 'medium'),
]

# ───────────────────────── Cue timeline completo ─────────────────────────
# gain_db: automatización aplicada sobre la mezcla generada (no separa instrumentos).
# expect: lo que la generación debería contener; se mide y, si no se puede verificar, se marca
# para escucha.
CUES = [
    {'start': 0.000, 'end': 1.970, 'name': 'explosive opening', 'gain_db': 0, 'expect': 'full'},
    {'start': 1.970, 'end': 4.850, 'name': 'whisper (near silence)', 'gain_db': -24, 'expect': 'post'},
    {'start': 4.850, 'end': 5.417, 'name': 'frightened reaction (one low note)', 'gain_db': -10, 'expect': 'post'},
    {'start': 5.417, 'end': 14.583, 'name': 'endless waiting (groove returns)', 'gain_db': 0, 'expect': 'full'},
    {'start': 14.583, 'end': 18.750, 'name': 'absurd queue ticket', 'gain_db': 0, 'expect': 'full'},
    {'start': 18.750, 'end': 23.000, 'name': 'old ads fail (progressive removal)', 'gain_db': [0, -5], 'expect': 'decreasing'},
    {'start': 23.000, 'end': 25.417, 'name': 'again?! (motif restarts)', 'gain_db': 0, 'expect': 'full'},
    {'start': 25.417, 'end': 29.050, 'name': 'subject change (polite minimal)', 'gain_db': -3, 'expect': 'reduced'},
    {'start': 29.050, 'end': 30.920, 'name': 'hoodie reveal (hard dropout)', 'gain_db': -30, 'expect': 'post',
     'keep': {'start': 29.600, 'end': 29.950, 'gain_db': -6, 'why': 'tiny low comment ~29.700'}},
    {'start': 30.920, 'end': 32.583, 'name': 'the idea (pickup)', 'gain_db': 0, 'expect': 'present'},
    {'start': 32.583, 'end': 42.583, 'name': 'the machine works (full re-entry)', 'gain_db': 0, 'expect': 'full'},
    {'start': 42.583, 'end': 50.400, 'name': 'more ad variations', 'gain_db': 0, 'expect': 'full'},
    {'start': 50.400, 'end': 51.542, 'name': 'owner says yes (resolution)', 'gain_db': -2, 'expect': 'present'},
    {'start': 51.542, 'end': 55.833, 'name': 'bad ideas warning (stripped)', 'gain_db': -10, 'expect': 'sparse'},
    {'start': 55.833, 'end': 61.583, 'name': 'competent humans (warm funk)', 'gain_db': 0, 'expect': 'full'},
    {'start': 61.583, 'end': 66.042, 'name': 'human creative judgment (reduced)', 'gain_db': -8, 'expect': 'reduced'},
    {'start': 66.042, 'end': 70.042, 'name': 'ads everywhere (4 s burst)', 'gain_db': 0, 'expect': 'full'},
    {'start': 70.042, 'end': 74.417, 'name': 'the reveal (hesitation + riff)', 'gain_db': 0, 'expect': 'present'},
    {'start': 74.417, 'end': 78.320, 'name': 'call invitation', 'gain_db': 0, 'expect': 'full'},
    {'start': 78.320, 'end': 82.958, 'name': 'honest fit / no-fit (quiet)', 'gain_db': -6, 'expect': 'reduced'},
    {'start': 82.958, 'end': 84.800, 'name': 'back to work (riff returns)', 'gain_db': 0, 'expect': 'full'},
    {'start': 84.800, 'end': 85.400, 'name': 'final low button + decay', 'gain_db': 0, 'expect': 'decay'},
]
KEY_POINTS = [1.970, 4.850, 5.417, 18.750, 23.000, 29.050, 29.700, 30.920, 32.583, 50.400, 51.542,
              61.583, 66.042, 70.042, 78.320, 82.958, 84.800, 85.400]
RAMP_S = 0.008  # microfundido anticlic: termina en el límite (bajadas) o empieza en él (subidas)


# ───────────────────────── Validación ─────────────────────────
def validate():
    errors = []
    if len(CHUNKS) != 15:
        errors.append(f'se esperaban 15 chunks, hay {len(CHUNKS)}')
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
        'note': 'Tiempos absolutos desde el inicio del vídeo. gain_db se aplica a la mezcla completa: no separa instrumentos.',
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


def gain_envelope(n: int) -> tuple[np.ndarray, list]:
    """Automatización por cue, con microfundidos que no desplazan los límites."""
    t = np.arange(n) / SR
    g_db = np.zeros(n)
    applied = []
    for c in CUES:
        a, b = int(round(c['start'] * SR)), int(round(c['end'] * SR))
        if isinstance(c['gain_db'], list):  # rampa progresiva (retirada de energía)
            g_db[a:b] = np.linspace(c['gain_db'][0], c['gain_db'][1], b - a)
        else:
            g_db[a:b] = c['gain_db']
        if 'keep' in c:
            ka, kb = int(round(c['keep']['start'] * SR)), int(round(c['keep']['end'] * SR))
            g_db[ka:kb] = c['keep']['gain_db']
        applied.append({'cue': c['name'], 'start': c['start'], 'end': c['end'], 'gain_db': c['gain_db'], 'keep': c.get('keep')})
    g = 10 ** (g_db / 20)
    # Microfundidos: cada cambio de ganancia se suaviza en RAMP_S. Las bajadas terminan en el
    # límite (el silencio empieza exactamente en él); las subidas empiezan en el límite.
    r = int(RAMP_S * SR)
    edges = np.nonzero(np.abs(np.diff(g)) > 1e-6)[0] + 1
    for e in edges:
        lo, hi = g[e - 1], g[e]
        if hi < lo:
            s0 = max(0, e - r)
            g[s0:e] = np.linspace(lo, hi, e - s0, endpoint=False)
        else:
            s1 = min(n, e + r)
            g[e:s1] = np.linspace(lo, hi, s1 - e, endpoint=False)
    return g, applied


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
    # Ediciones de montaje declaradas por toma (mover una frase entera, nunca estirar).
    if args.edits:
        ed = json.loads((HERE / args.edits).read_text())
        report['editorial_moves'] = []
        for mv in ed.get('moves', []):
            a = int(round(mv['from_s'] * SR))
            sh = int(round(mv['shift_s'] * SR))
            fade = max(1, int(mv.get('fade_ms', 5) * SR / 1000))
            tail = x[a:].copy()
            x[a:] = 0.0
            x[a - fade:a] *= np.linspace(1, 0, fade, dtype=np.float32)[:, None]
            tail[:fade] *= np.linspace(0, 1, fade, dtype=np.float32)[:, None]
            dst = a + sh
            room = len(x) - dst
            x[dst:] += tail[:room]
            report['editorial_moves'].append({**mv, 'samples_moved': int(min(len(tail), room)), 'dropped_after_end_ms': round(max(0, len(tail) - room) / SR * 1000, 1)})
        report['edits_file'] = args.edits
        report['edits_note'] = ed.get('note')
    original = x.copy()
    # Medición por cue de la generación (antes de automatizar) para comprobar dropouts/arreglos.
    measured = []
    for c in CUES:
        a, b = int(c['start'] * SR), int(c['end'] * SR)
        measured.append({'cue': c['name'], 'start': c['start'], 'end': c['end'], 'expect': c['expect'], 'rms_dbfs': round(db(rms(original[a:b])), 2)})
    full = [m['rms_dbfs'] for m in measured if m['expect'] == 'full']
    ref = float(np.median(full)) if full else -20.0
    for m in measured:
        rel = m['rms_dbfs'] - ref
        m['relative_to_groove_db'] = round(rel, 2)
        if m['expect'] == 'post':
            m['note'] = 'caída creada en posproducción sobre la mezcla completa (plan 2)'
        if m['expect'] == 'dropout' and rel > -12:
            report['needs_listening'].append(f'{m["cue"]}: la generación no baja lo suficiente ({rel:.1f} dB); la automatización lo fuerza en la mezcla completa')
        if m['expect'] in ('sparse', 'reduced') and rel > -4:
            report['needs_listening'].append(f'{m["cue"]}: la generación no reduce el arreglo ({rel:.1f} dB); solo la ganancia lo hace')
        if m['expect'] == 'full' and rel < -8:
            report['needs_listening'].append(f'{m["cue"]}: groove más débil de lo previsto ({rel:.1f} dB)')
    report['measured_generation'] = measured
    g, applied = gain_envelope(len(x))
    y = x * g[:, None]
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
    report['applied_gain_automation'] = applied
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
    report['key_points'] = [{'t': p, 'rms_dbfs_80ms_after': round(db(rms(y[int(p * SR): int(p * SR) + int(0.08 * SR)])), 1)} for p in KEY_POINTS if p < TARGET_MS / 1000]
    report['needs_listening'] += ['Motivo de tres notas y respuestas del fagot: no verificable automáticamente',
                                  'Retirada progresiva guitarra → batería → teclados (18,75–23,00): la ganancia no separa instrumentos']
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
    ap.add_argument('--edits', help='JSON de ediciones de montaje de la toma (mover frases sin estirar)')
    a = ap.parse_args()
    if a.dry_run:
        return dry_run()
    if a.generate:
        return generate(a)
    return conform(a)


if __name__ == '__main__':
    sys.exit(main())

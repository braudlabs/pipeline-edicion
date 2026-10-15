"""Comprobaciones ejecutables de C02. No certifican gusto, lipsync perceptivo ni escucha.

1. Montaje: 920 f contiguos, IN/OUT y offsets idénticos al CSV de la entrega (ticket +12 f).
2. Audio: narrador = NARRADOR_COMPLETO_ORIGINAL desde 0; hook = audio nativo del clip 00 en
   sus mismas muestras (sin stem externo del azul ni cama del 04); ambientes en su IN exacto;
   música desactivada.
3. Cobertura: toda palabra 0–118 del narrador (hasta «dará») tiene rótulo, salvo el gag de la
   sudadera (89–95), suprimido por instrucción de Ale; el blanco y negro cubre ese intervalo.
4. Máster (si existe): 1080×1920, 24 fps, 920 f, AAC 48 kHz y desfase 0 frente a la mezcla
   de referencia reconstruida desde los stems en 6 ventanas.

Uso: python3 ecommerce-andromeda-claude/c02/verify.py
"""
import csv
import json
import re
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PUB = HERE / 'public'
SR = 48000
FPS = 24
report = {'checks': [], 'ok': True}


def check(name, ok, detail=None):
    report['checks'].append({'name': name, 'ok': bool(ok), 'detail': detail})
    report['ok'] &= bool(ok)
    print(('OK  ' if ok else 'FAIL'), name, '' if detail is None else detail)


def decode(path, channels=2, ss=None, t=None):
    cmd = ['ffmpeg', '-v', 'error'] + (['-ss', str(ss)] if ss is not None else []) + (['-t', str(t)] if t is not None else []) + ['-i', str(path), '-f', 'f32le', '-ar', str(SR), '-ac', str(channels), '-']
    return np.frombuffer(subprocess.check_output(cmd), np.float32).reshape(-1, channels)


# 1 · montaje frente al CSV
tl = json.loads((HERE / 'src/data/timeline.json').read_text())
rows = list(csv.DictReader(open(HERE / 'source-notes/cortes-exactos-24fps.csv')))
pos = 0
for s, r in zip(tl['scenes'], rows):
    rin = round(float(r['master_IN_seg']) * FPS)
    rout = round(float(r['master_OUT_seg_exclusivo']) * FPS)
    sin = round(float(r['source_IN_seg']) * FPS)
    check(f"corte {s['id']}", s['from'] == rin == pos and s['from'] + s['dur'] == rout and s['srcIn'] == sin, {'from': s['from'], 'dur': s['dur'], 'srcIn': s['srcIn'], 'csv': [rin, rout, sin]})
    pos = rout
check('920 fotogramas contiguos', pos == 920 == tl['renderedFrames'])

# 2 · audio
audio = json.loads((HERE / 'src/data/audio.json').read_text())
ids = {t['id']: t for t in audio['tracks']}
check('sin stem externo del azul', not any('AZUL' in (t.get('src') or '') for t in audio['tracks']))
check('música desactivada', ids['musica'].get('enabled') is False and ids['musica']['src'] is None)
narr_stem = decode(PUB / 'assets/audio/stems/narrador.wav')
narr_src = decode(PUB / 'assets/audio/NARRADOR_COMPLETO_ORIGINAL.mp3')[: len(narr_stem)]
body = slice(0, len(narr_stem) - int(0.02 * SR))
check('narrador desde 0 sin retiming', np.abs(narr_stem[body] - narr_src[body]).max() < 1e-4, float(np.abs(narr_stem[body] - narr_src[body]).max()))
for s in tl['scenes']:
    stem = decode(PUB / f"assets/audio/stems/native-{s['id']}.wav")
    src = decode(PUB / s['asset'])
    a = round(s['srcIn'] * SR / FPS)
    ref = src[a: a + len(stem)]
    inner = slice(int(0.01 * SR), len(stem) - int(0.01 * SR))
    err = float(np.abs(stem[inner] - ref[inner]).max())
    check(f"audio nativo {s['id']} en su IN", err < 1e-4 and len(stem) == round(s['dur'] * SR / FPS), {'maxErr': err, 'samples': len(stem)})
check('hook con audio nativo', ids['hook-nativo']['src'].endswith('native-00_hook.wav') and ids['hook-nativo']['from'] == 0)

# 3 · cobertura de palabras en los rótulos
src_text = '\n'.join(p.read_text() for p in (HERE / 'src/captions').glob('*.tsx') if 'Descartado' not in p.name)
film = (HERE / 'src/Film.tsx').read_text()
hook = 'HookA' if '<HookA />' in film else None
used = set(int(m) for m in re.findall(r'wf\((\d+)\)', src_text))
# El aparte vertical del gag existe como estudio descartado: no cuenta como cobertura.
aside = re.search(r'export const AsideDescartado[\s\S]*?\n};', src_text)
if aside:
    used -= set(int(m) for m in re.findall(r'wf\((\d+)\)', aside.group(0))) - set(int(m) for m in re.findall(r'wf\((\d+)\)', src_text.replace(aside.group(0), '')))
gag = set(range(89, 96))
missing = [i for i in range(0, 119) if i not in used and i not in gag]
check('hook = variante A aprobada', hook == 'HookA')
check('cobertura 0–118 salvo gag', not missing, {'faltan': missing})
spine = (HERE / 'src/VideoSpine.tsx').read_text()
bw = re.search(r'BW_GAG: \[number, number\] = \[(\d+), (\d+)\]', spine)
words = json.loads((HERE / 'src/data/words.json').read_text())['words']
wf = lambda i: int(np.floor(words[i]['start'] * FPS + 1e-6))
check('B/N del gag = «y con la sudadera» → «Vengo»', bw and int(bw.group(1)) == wf(89) and int(bw.group(2)) == wf(96), bw.groups() if bw else None)

# 4 · máster
master = HERE / 'Andromeda-C02-00-38s-PREVIEW.mp4'
if master.exists():
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=codec_type,codec_name,width,height,r_frame_rate,nb_read_frames,sample_rate,channels', '-of', 'json', str(master)]))
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    check('máster 1080×1920 24 fps 920 f H.264', v['codec_name'] == 'h264' and v['width'] == 1080 and v['height'] == 1920 and v['r_frame_rate'] == '24/1' and int(v['nb_read_frames']) == 920, v)
    check('audio AAC 48 kHz', a['codec_name'] == 'aac' and a['sample_rate'] == '48000', a)
    # Mezcla de referencia desde los stems con sus ganancias
    ref = np.zeros((round(920 * SR / FPS), 2), np.float32)
    for t in audio['tracks']:
        if not t.get('src') or t.get('enabled') is False:
            continue
        x = decode(PUB / t['src']) * t['gain']
        a0 = round(t['from'] * SR / FPS)
        b0 = min(len(ref), a0 + len(x))
        ref[a0:b0] += x[: b0 - a0]
    out = decode(master)
    lags = []
    for start in [1.0, 6.5, 15.0, 22.0, 27.0, 33.0]:
        a0 = int(start * SR)
        seg_r = ref[a0: a0 + SR, 0]
        seg_o = out[a0 - 2400: a0 + SR + 2400, 0]
        c = np.correlate(seg_o, seg_r, mode='valid')
        lags.append(int(np.argmax(c)) - 2400)
    check('desfase audio máster vs stems = 0 muestras', all(abs(l) <= 1 for l in lags), lags)

(HERE / 'QA.json').write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str))
print('TOTAL', 'OK' if report['ok'] else 'FALLOS')

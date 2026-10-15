"""Comprobaciones ejecutables de C06 (montaje, audio y rótulos de C05 + cámara y efectos). No certifican gusto, lipsync perceptivo ni escucha.

1. Montaje: 17 unidades contiguas y 2050 f; fuente, IN/OUT, estado y offsets idénticos al
   MASTER_COMPLETO_24FPS.json y .csv de la entrega (02: IN 12 f; 15: IN 18 f, 59 f) y clip con
   fotogramas suficientes. Composiciones AndromedaC06, -144, -60, -audit (rótulos sobre negro,
   solo para la auditoría de márgenes), C06Block (estudio A/B del bloque) y HookStudy.
2. Audio: narrador = NARRADOR_COMPLETO_ORIGINAL desde 0, entero (85,39425 s), muestra a muestra;
   hook = audio nativo del clip 00 en sus mismas muestras (sin stem externo del azul ni cama del 04);
   ambiente nativo de las 17 unidades en su IN exacto y en su posición del máster; ganancias de
   00–05 las de C03; música = banda sonora conformada (../music) con ducking, en su propia pista.
3. Cobertura: toda palabra 0–118 del narrador (hasta «dará») tiene rótulo, salvo el gag de la
   sudadera (89–95), suprimido por instrucción de Ale; el blanco y negro cubre ese intervalo.
   Los rótulos de 07–15 (palabras 119+) están pendientes y no se comprueban.
4. Másteres (los que existan): 1080×1920, 24 / 60 / 144 fps con 2050 / 5125 / 12300 f, AAC 48 kHz,
   desfase 0 y ganancia ≈ 1 frente a la mezcla de referencia reconstruida desde los stems, en
   ventanas repartidas por los 85 s.

Uso: python3 ecommerce-andromeda-claude/c06/verify.py
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
# Ganancias de C03 que C04 conserva (pista → ganancia).
C03_GAINS = {'hook-nativo': 0.8, 'nativo-01': 0.65, 'nativo-02': 0.65, 'nativo-03': 0.75, 'nativo-03b': 0.75, 'nativo-04': 0.75, 'nativo-05': 0.6}
report = {'checks': [], 'ok': True}


def check(name, ok, detail=None):
    report['checks'].append({'name': name, 'ok': bool(ok), 'detail': detail})
    report['ok'] &= bool(ok)
    print(('OK  ' if ok else 'FAIL'), name, '' if detail is None else detail)


def decode(path, channels=2, ss=None, t=None):
    cmd = ['ffmpeg', '-v', 'error'] + (['-ss', str(ss)] if ss is not None else []) + (['-t', str(t)] if t is not None else []) + ['-i', str(path), '-f', 'f32le', '-ar', str(SR), '-ac', str(channels), '-']
    return np.frombuffer(subprocess.check_output(cmd), np.float32).reshape(-1, channels)


def video_frames(path):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=nb_frames', '-of', 'csv=p=0', str(path)], text=True).strip()
    return int(out)


# 1 · montaje frente al máster del director (JSON y CSV)
tl = json.loads((HERE / 'src/data/timeline.json').read_text())
master = json.loads((HERE / 'source-notes/MASTER_COMPLETO_24FPS.json').read_text())
rows = list(csv.DictReader(open(HERE / 'source-notes/MASTER_COMPLETO_24FPS.csv', encoding='utf-8-sig')))
N = tl['renderedFrames']
check('17 unidades (timeline = máster JSON = CSV)', len(tl['scenes']) == len(master['scenes']) == len(rows) == 17)
check('sin lista «pending» obsoleta', 'pending' not in tl)
pos = 0
for s, m, r in zip(tl['scenes'], master['scenes'], rows):
    rin, rout = m['record_in_frame'], m['record_out_frame']
    sin = round(m['source_in'] * FPS)
    name = Path(m['source']).name
    same_csv = (r['id'], int(r['record_in_frame']), int(r['record_out_frame']), round(float(r['source_in']) * FPS), Path(r['source']).name, r['status']) == (m['id'], rin, rout, sin, name, m['status'])
    same_json = s['from'] == rin == pos and s['from'] + s['dur'] == rout and s['srcIn'] == sin and s['asset'] == f'assets/clips/{name}' and s['status'] == m['status'] and s['masterId'] == m['id']
    avail = video_frames(PUB / s['asset'])
    check(f"corte {s['id']}", same_json and same_csv and s['srcIn'] + s['dur'] <= avail,
          {'from': s['from'], 'dur': s['dur'], 'srcIn': s['srcIn'], 'master': [rin, rout, sin], 'fotogramasFuente': avail, 'asset': name})
    pos = rout
check(f'{N} fotogramas contiguos', pos == N == master['planned_picture_frames'] == 2050)
index = (HERE / 'src/index.tsx').read_text()
comps = re.findall(r'<Composition id="([^"]+)"', index)
check('composiciones AndromedaC06 (24), -144, -60, -audit (QA de márgenes), C06Block (estudio A/B) y HookStudy', comps == ['AndromedaC06', 'AndromedaC06-144', 'AndromedaC06-60', 'AndromedaC06-audit', 'C06Block', 'HookStudy'] and all(re.fullmatch(r'[A-Za-z0-9-]+', c) for c in comps), comps)

# 2 · audio
audio = json.loads((HERE / 'src/data/audio.json').read_text())
ids = {t['id']: t for t in audio['tracks']}
check('sin stem externo del azul', not any('AZUL' in (t.get('src') or '') for t in audio['tracks']))
import wave as _wave
_mus = HERE.parent / 'music' / 'final_soundtrack_85_4s.wav'
with _wave.open(str(_mus)) as _w:
    _mus_n = _w.getnframes()
_duck = decode(PUB / 'assets/audio/stems/musica.wav')
check('música: banda sonora de 85,400 s en su pista, desde 0 y con ducking (stem de toda la timeline)',
      ids['musica'].get('enabled') is not False and ids['musica']['src'] == 'assets/audio/stems/musica.wav' and ids['musica']['from'] == 0
      and _mus_n == 4_099_200 and len(_duck) == round(N * SR / FPS),
      {'master_samples': _mus_n, 'stem_samples': len(_duck), 'gain': ids['musica']['gain']})
narr_stem = decode(PUB / 'assets/audio/stems/narrador.wav')
narr_src = decode(PUB / 'assets/audio/NARRADOR_COMPLETO_ORIGINAL.mp3')
err = float(np.abs(narr_stem - narr_src).max()) if narr_stem.shape == narr_src.shape else None
check('narrador desde 0, entero y sin retiming (muestra a muestra)', err == 0.0 and ids['narrador']['from'] == 0 and ids['narrador']['gain'] == 1.0,
      {'maxAbsError': err, 'muestras': len(narr_stem), 'segundos': len(narr_stem) / SR})
check('narrador cubre sus 85,39425 s dentro de la imagen', len(narr_stem) / SR >= master['narration_duration'] and len(narr_stem) / SR <= N / FPS,
      {'narrador': len(narr_stem) / SR, 'imagen': N / FPS})
by_scene = {}
for t in audio['tracks']:
    if t['id'] == 'hook-nativo':
        by_scene['00'] = t
    elif t['id'].startswith('nativo-'):
        by_scene[t['id'][len('nativo-'):]] = t
for s in tl['scenes']:
    key = s['id'].split('_')[0]
    t = by_scene.get(key)
    stem = decode(PUB / f"assets/audio/stems/native-{s['id']}.wav")
    src = decode(PUB / s['asset'])
    a = round(s['srcIn'] * SR / FPS)
    ref = src[a: a + len(stem)]
    real = len(ref)  # muestras de audio real que trae la fuente en este tramo
    pad = len(stem) - real
    ref = np.vstack([ref, np.zeros((pad, 2), np.float32)]) if pad else ref
    inner = slice(int(0.01 * SR), real - int(0.01 * SR))
    e = float(np.abs(stem[inner] - ref[inner]).max())
    tail_silent = bool(pad == 0 or np.abs(stem[real:]).max() == 0)
    in_place = t is not None and t['src'] == f"assets/audio/stems/native-{s['id']}.wav" and t['from'] == s['from'] and t['gain'] > 0 and t.get('enabled') is not False
    check(f"audio nativo {s['id']} en su IN y su posición", e < 1e-4 and len(stem) == round(s['dur'] * SR / FPS) and tail_silent and in_place,
          {'maxErr': e, 'samples': len(stem), 'silencioFinal': pad, 'gain': t and t['gain']})
check('ganancias de 00–05 = las de C03', all(ids[k]['gain'] == v for k, v in C03_GAINS.items()), {k: ids[k]['gain'] for k in C03_GAINS})
check('hook con audio nativo', ids['hook-nativo']['src'].endswith('native-00_hook.wav') and ids['hook-nativo']['from'] == 0)

# 3 · cobertura de palabras en los rótulos (las 274 de la locución, salvo el gag en B/N)
src_text = '\n'.join(p.read_text() for p in (HERE / 'src/captions').glob('*.tsx') if 'Descartado' not in p.name)
film = (HERE / 'src/Film.tsx').read_text()
hook = 'HookA' if '<HookA />' in film else None
used = set(int(m) for m in re.findall(r'wf\((\d+)\)', src_text))
# El aparte vertical del gag existe como estudio descartado: no cuenta como cobertura.
aside = re.search(r'export const AsideDescartado[\s\S]*?\n};', src_text)
if aside:
    used -= set(int(m) for m in re.findall(r'wf\((\d+)\)', aside.group(0))) - set(int(m) for m in re.findall(r'wf\((\d+)\)', src_text.replace(aside.group(0), '')))
gag = set(range(89, 96))
missing = [i for i in range(0, len(json.loads((HERE / 'src/data/words.json').read_text())['words'])) if i not in used and i not in gag]
check('hook = variante A aprobada', hook == 'HookA')
check('cobertura de las 274 palabras salvo el gag', not missing, {'faltan': missing})
spine = (HERE / 'src/VideoSpine.tsx').read_text()
bw = re.search(r'BW_GAG: \[number, number\] = \[(\d+), (\d+)\]', spine)
words = json.loads((HERE / 'src/data/words.json').read_text())['words']
wf = lambda i: int(np.floor(words[i]['start'] * FPS + 1e-6))
check('B/N del gag = «y con la sudadera» → «Vengo»', bw and int(bw.group(1)) == wf(89) and int(bw.group(2)) == wf(96), bw.groups() if bw else None)

# 4 · másteres (24 fps de referencia, 60 y 144 fps pedidos por Ale)
WINDOWS = [1.0, 6.5, 15.0, 22.0, 27.0, 33.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 84.0]
_ref = None


def reference_mix():
    """Mezcla reconstruida desde los stems de audio.json (con su ganancia y su posición)."""
    global _ref
    if _ref is None:
        _ref = np.zeros((round(N * SR / FPS), 2), np.float32)
        for t in audio['tracks']:
            if not t.get('src') or t.get('enabled') is False:
                continue
            x = decode(PUB / t['src']) * t['gain']
            a0 = round(t['from'] * SR / FPS)
            b0 = min(len(_ref), a0 + len(x))
            _ref[a0:b0] += x[: b0 - a0]
    return _ref


def check_master(name, fps, frames):
    master_file = HERE / name
    if not master_file.exists():
        print('--  (sin máster)', name)
        return
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=codec_type,codec_name,width,height,r_frame_rate,nb_read_frames,sample_rate,channels', '-of', 'json', str(master_file)]))
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    a = next(s for s in info['streams'] if s['codec_type'] == 'audio')
    check(f'{name}: 1080×1920 {fps} fps {frames} f H.264', v['codec_name'] == 'h264' and v['width'] == 1080 and v['height'] == 1920 and v['r_frame_rate'] == f'{fps}/1' and int(v['nb_read_frames']) == frames, v)
    check(f'{name}: audio AAC 48 kHz', a['codec_name'] == 'aac' and a['sample_rate'] == '48000', a)
    ref = reference_mix()
    out = decode(master_file)
    lags, scales, used_windows = [], [], []
    for start in WINDOWS:
        a0 = int(start * SR)
        seg_r = ref[a0: a0 + SR, 0]
        if len(seg_r) < SR or float(np.sqrt((seg_r ** 2).mean())) < 3e-3:
            continue  # ventana sin señal suficiente para correlar (silencio del narrador)
        seg_o = out[a0 - 2400: a0 + SR + 2400, 0]
        c = np.correlate(seg_o, seg_r, mode='valid')
        lag = int(np.argmax(c)) - 2400
        aligned = out[a0 + lag: a0 + lag + SR, 0]
        lags.append(lag)
        scales.append(round(float(np.dot(aligned, seg_r) / np.dot(seg_r, seg_r)), 3))
        used_windows.append(start)
    check(f'{name}: desfase audio vs stems = 0 muestras', len(lags) >= 12 and all(abs(l) <= 1 for l in lags), {'ventanas_s': used_windows, 'lags': lags})
    check(f'{name}: ganancia de la mezcla ≈ 1 frente a los stems', all(0.9 < s < 1.1 for s in scales), scales)


check_master('Andromeda-C06-00-85s-24fps-1080.mp4', 24, N)
check_master('Andromeda-C06-00-85s-144fps-1080.mp4', 144, N * 6)
check_master('Andromeda-C06-00-85s-60fps-1080.mp4', 60, round(N * 2.5))

(HERE / 'QA.json').write_text(json.dumps(report, indent=1, ensure_ascii=False, default=str))
print('TOTAL', 'OK' if report['ok'] else 'FALLOS')

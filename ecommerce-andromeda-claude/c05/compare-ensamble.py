"""Compara un render de C04 con el ENSAMBLE_COMPLETO_85s_PREVIEW del director (solo lectura).

Imagen  Fotograma a fotograma en gris 270×480 (escalado por área). Para cada inicio de unidad S y para S−1:
        MAD y PSNR frente al fotograma del director y desfase óptimo (−2…+2). En el render hay rótulos hasta el
        f919 y el ensamble no los lleva: ahí cuenta el desfase óptimo, no el PSNR absoluto. También el desfase
        óptimo de los 2050 fotogramas.
Audio   Correlación cruzada (FFT) por ventanas de 2 s del audio del render con (a) el audio del ensamble,
        (b) el STEM_NARRADOR_COMPLETO (mono, sin ganancia) y (c) por unidad, el stem nativo de C04 con el
        STEM_AMBIENTE_COMPLETO del director (0,65 de ganancia). Lag esperado: 0 muestras.

Uso: python3 ecommerce-andromeda-claude/c04/compare-ensamble.py [render.mp4]
Sale: study/comparacion-ensamble.json y study/qa-cortes-S-render-vs-director.jpg
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DIRECTOR = Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-10-14-ecommerce-andromeda/ENTREGA_EDITOR/04_MONTAJES')
ENSAMBLE = DIRECTOR / 'ENSAMBLE_COMPLETO_85s_PREVIEW_CON_OBSERVACIONES.mp4'
OURS = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'Andromeda-C04-00-85s-24fps-PREVIEW-sin-musica.mp4'
SR = 48000
W, H = 270, 480
TL = json.loads((HERE / 'src/data/timeline.json').read_text())
STARTS = [s['from'] for s in TL['scenes']]
WINDOWS = [1, 6, 15, 25, 33, 40, 45, 50, 55, 60, 65, 70, 75, 80]
MAXLAG = 4800


def run(cmd, tries=3):
    for i in range(tries):
        try:
            return subprocess.check_output(cmd)
        except subprocess.CalledProcessError:
            if i == tries - 1:
                raise
            time.sleep(5)  # la carpeta del director está en iCloud: una lectura puede agotar el tiempo


def gray_frames(path: Path, select=None) -> np.ndarray:
    vf = (f"select='{select}'," if select else '') + f'scale={W}:{H}:flags=area,format=gray'
    raw = run(['ffmpeg', '-v', 'error', '-i', str(path), '-vf', vf, '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'])
    n = len(raw) // (W * H)
    return np.frombuffer(raw, np.uint8)[: n * W * H].reshape(n, H, W)


def decode(path: Path, channels=2) -> np.ndarray:
    raw = run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ar', str(SR), '-ac', str(channels), '-'])
    return np.frombuffer(raw, np.float32).reshape(-1, channels)


def mad(a, b):
    return float(np.abs(a.astype(np.int16) - b.astype(np.int16)).mean())


def psnr(a, b):
    m = float(((a.astype(np.float64) - b) ** 2).mean())
    return 99.0 if m == 0 else float(10 * np.log10(255 ** 2 / m))


def xcorr_lag(ref, x, maxlag):
    """Lag (muestras) tal que x[n+lag] ≈ ref[n]; x tiene len(ref)+2·maxlag muestras. Devuelve entero, fraccionario y correlación."""
    n = len(ref)
    size = 1 << int(np.ceil(np.log2(len(x) + n)))
    c = np.fft.irfft(np.fft.rfft(x, size) * np.conj(np.fft.rfft(ref, size)), size)[: 2 * maxlag + 1]
    k = int(np.argmax(c))
    frac = 0.0
    if 0 < k < len(c) - 1:
        den = c[k - 1] - 2 * c[k] + c[k + 1]
        frac = 0.5 * (c[k - 1] - c[k + 1]) / den if den != 0 else 0.0
    corr = float(c[k] / np.sqrt((ref ** 2).sum() * (x[k: k + n] ** 2).sum() + 1e-12))
    return k - maxlag, round(float(k - maxlag + frac), 3), round(corr, 4)


def picture(report):
    a, d = gray_frames(OURS), gray_frames(ENSAMBLE)
    n = min(len(a), len(d))
    print('fotogramas: render', len(a), '· ensamble', len(d))
    units = []
    for s in TL['scenes']:
        S = s['from']
        row = {'id': s['id'], 'from': S}
        cand = {o: mad(a[S], d[S + o]) for o in range(-2, 3) if 0 <= S + o < n}
        row.update(madStart=round(cand[0], 2), psnrStart=round(psnr(a[S], d[S]), 1), bestOffsetStart=min(cand, key=cand.get), madCross=None)
        ok = row['bestOffsetStart'] == 0
        if S > 0:
            cp = {o: mad(a[S - 1], d[S - 1 + o]) for o in range(-2, 3) if 0 <= S - 1 + o < n}
            row.update(madPrev=round(cp[0], 2), psnrPrev=round(psnr(a[S - 1], d[S - 1]), 1), bestOffsetPrev=min(cp, key=cp.get), madCross=round(mad(a[S], d[S - 1]), 1))
            ok &= row['bestOffsetPrev'] == 0
        row['ok'] = bool(ok)
        units.append(row)
        print(f"  {s['id']:16s} S={S:5d} MAD {row['madStart']:5.2f} PSNR {row['psnrStart']:5.1f} offset {row['bestOffsetStart']:+d} | S−1: " +
              (f"MAD {row['madPrev']:5.2f} PSNR {row['psnrPrev']:5.1f} offset {row['bestOffsetPrev']:+d} | cruce {row['madCross']:5.1f}" if S else '—') + ('  OK' if ok else '  REVISAR'))
    report['unidades'] = units
    report['unidadesDudosas'] = [u['id'] for u in units if not u['ok']]
    best = np.zeros(n, int)
    for i in range(n):
        v = np.array([mad(a[i], d[i + o]) if 0 <= i + o < n else 1e9 for o in range(-2, 3)])
        best[i] = int(v.argmin()) - 2
    nonzero = [int(i) for i in np.where(best != 0)[0]]
    report['todosLosFotogramas'] = {'total': n, 'desfaseOptimo0': int((best == 0).sum()), 'desfaseOptimoDistinto0': nonzero}
    print(f"  desfase óptimo 0 en {int((best == 0).sum())} de {n} fotogramas; distintos de 0 (ruido en planos casi estáticos): {nonzero}")
    # hoja de contacto: fila superior render, fila inferior ensamble, en los 17 inicios de unidad
    sel = '+'.join(f'eq(n\\,{f})' for f in STARTS)
    cw, ch = 180, 320

    def tiles(path):
        raw = run(['ffmpeg', '-v', 'error', '-i', str(path), '-vf', f"select='{sel}',scale={cw}:{ch}:flags=area", '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
        return np.frombuffer(raw, np.uint8).reshape(-1, ch, cw, 3)

    ta, td = tiles(OURS), tiles(ENSAMBLE)
    cols = 6
    rows = -(-len(STARTS) // cols)
    sheet = np.full((rows * 2 * ch, cols * cw, 3), 16, np.uint8)
    for i in range(len(STARTS)):
        r, c = divmod(i, cols)
        sheet[2 * r * ch:(2 * r + 1) * ch, c * cw:(c + 1) * cw] = ta[i]
        sheet[(2 * r + 1) * ch:(2 * r + 2) * ch, c * cw:(c + 1) * cw] = td[i]
    out = HERE / 'study/qa-cortes-S-render-vs-director.jpg'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{cols * cw}x{rows * 2 * ch}', '-i', '-', '-frames:v', '1', '-q:v', '3', str(out)], input=sheet.tobytes(), check=True)


def audio(report):
    ours = decode(OURS)
    ens = decode(ENSAMBLE)
    narr = decode(DIRECTOR / 'STEM_NARRADOR_COMPLETO.wav', 1)
    print(f'muestras: render {len(ours)} · ensamble {len(ens)} · narrador del director {len(narr)}')

    def windows(ref):
        res = []
        for t in WINDOWS:
            a0 = int(t * SR)
            r = ref[a0: a0 + 2 * SR, 0]
            if len(r) < 2 * SR or np.sqrt((r ** 2).mean()) < 2e-3:
                continue
            lag, frac, corr = xcorr_lag(r, ours[a0 - MAXLAG: a0 + 2 * SR + MAXLAG, 0], MAXLAG)
            al = ours[a0 + lag: a0 + lag + 2 * SR, 0]
            res.append({'t': t, 'lag': lag, 'fracLag': frac, 'corr': corr, 'gain': round(float(np.dot(al, r) / np.dot(r, r)), 3)})
        return res

    report['audioVsEnsamble'] = windows(ens)
    report['audioVsNarradorDirector'] = windows(narr)
    for key, label in (('audioVsEnsamble', 'audio del ensamble'), ('audioVsNarradorDirector', 'stem mono del narrador')):
        print(f'  render vs {label}: lags', [w['lag'] for w in report[key]], '· ganancia', [w['gain'] for w in report[key]])
    amb = decode(DIRECTOR / 'STEM_AMBIENTE_COMPLETO.wav')
    per_unit = []
    for s in TL['scenes']:
        if s['id'] == '00_hook':
            continue  # el ensamble del director usa una cama del 04 en el hook
        mine = decode(HERE / f"public/assets/audio/stems/native-{s['id']}.wav")
        a0, n = s['from'] * 2000, s['dur'] * 2000
        m0 = int(0.06 * SR)  # fuera de los fundidos de 25/30 ms del director
        ref = mine[m0: n - m0, 0]
        if np.sqrt((ref ** 2).mean()) < 1e-4:
            continue
        lag, frac, corr = xcorr_lag(ref, amb[a0 + m0 - 2400: a0 + n - m0 + 2400, 0], 2400)
        dref = amb[a0 + m0: a0 + n - m0, 0]
        g = float(np.dot(dref, ref) / np.dot(ref, ref))
        per_unit.append({'id': s['id'], 'lag': lag, 'fracLag': frac, 'corr': corr, 'gain': round(g, 4), 'residuoRelativo': round(float(np.sqrt(((dref - g * ref) ** 2).sum() / (dref ** 2).sum())), 4)})
    report['ambientePorUnidad'] = per_unit
    print('  ambiente nativo por unidad: lags', [u['lag'] for u in per_unit], '· ganancia', sorted({u['gain'] for u in per_unit}))


def main():
    report = {'render': OURS.name}
    picture(report)
    audio(report)
    ok = (not report['unidadesDudosas'] and all(w['lag'] == 0 for w in report['audioVsEnsamble'] + report['audioVsNarradorDirector'])
          and all(u['lag'] == 0 for u in report['ambientePorUnidad']))
    report['ok'] = bool(ok)
    (HERE / 'study/comparacion-ensamble.json').write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print('TOTAL', 'OK' if ok else 'REVISAR')


if __name__ == '__main__':
    main()

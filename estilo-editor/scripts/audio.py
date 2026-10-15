#!/usr/bin/env python3
"""Análisis de audio: sonoridad, golpes (onsets), tempo, ducking y espectrogramas anotados.

  audio.py <slug> [...]

Escribe datos/<slug>/audio.json y analysis/spectro/<slug>/s_<t0>-<t1>.png
(un espectrograma por cada 8 s con cortes, palabras de la locución y golpes marcados).
"""
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from common import ANALYSIS, DATOS, probe, src  # noqa: E402

SR = 44100
N = 2048
HOP = 441          # 10 ms


def load(slug):
    p = ANALYSIS / "audio" / f"{slug}.wav"
    with wave.open(str(p)) as w:
        ch, n = w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768.0
    x = x.reshape(-1, ch)
    return x


def stft(mono):
    win = np.hanning(N).astype(np.float32)
    pad = np.concatenate([np.zeros(N // 2, np.float32), mono, np.zeros(N, np.float32)])
    nfr = 1 + (len(mono)) // HOP
    idx = np.arange(N)[None, :] + HOP * np.arange(nfr)[:, None]
    return np.abs(np.fft.rfft(pad[idx] * win, axis=1)).astype(np.float32)


def ebur128(slug):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src(slug)), "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = r[r.rfind("Summary:"):]
    g = lambda pat: (lambda m: float(m.group(1)) if m else None)(re.search(pat, tail))  # noqa: E731
    st = [float(m) for m in re.findall(r"S:\s*(-?\d+\.\d+)", r)]
    return {"integrated_lufs": g(r"I:\s*(-?\d+\.\d+) LUFS"), "lra": g(r"LRA:\s*(-?\d+\.\d+) LU"),
            "true_peak_dbfs": g(r"Peak:\s*(-?\d+\.\d+) dBFS"), "short_term": st}


def band(freqs, lo, hi):
    return (freqs >= lo) & (freqs < hi)


def run(slug):
    info = probe(slug)
    x = load(slug)
    mono = x.mean(axis=1)
    dur = len(mono) / SR
    S = stft(mono)
    freqs = np.fft.rfftfreq(N, 1 / SR)
    T = S.shape[0]
    times = np.arange(T) * HOP / SR
    L = np.log1p(200 * S)

    flux_bins = np.maximum(0, np.diff(L, axis=0, prepend=L[:1]))
    bands = {"sub": (20, 90), "bass": (90, 250), "mid": (250, 2000), "pres": (2000, 6000), "air": (6000, 20000)}
    flux_b = {k: flux_bins[:, band(freqs, *v)].sum(axis=1) for k, v in bands.items()}
    flux = sum(flux_b.values())
    pow_b = {k: 10 * np.log10((S[:, band(freqs, *v)] ** 2).sum(axis=1) + 1e-9) for k, v in bands.items()}
    rms_db = 10 * np.log10((S ** 2).sum(axis=1) + 1e-9)
    rms_db -= rms_db.max()

    # --- golpes: picos del flujo espectral frente a su entorno
    onsets = []
    half = 50
    for i in range(2, T - 2):
        lo, hi = max(0, i - half), min(T, i + half)
        med = np.median(flux[lo:hi])
        mad = np.median(np.abs(flux[lo:hi] - med)) + 1e-6
        z = (flux[i] - med) / (1.4826 * mad)
        if z >= 4.5 and flux[i] == flux[max(0, i - 5):i + 6].max():
            tot = sum(flux_b[k][i] for k in bands) + 1e-9
            prof = {k: round(float(flux_b[k][i] / tot), 2) for k in bands}
            # ¿golpe seco o subida gradual? energía 150 ms antes frente al pico
            pre = float(rms_db[max(0, i - 15)])
            onsets.append({"t": round(float(times[i]), 3), "z": round(float(z), 1), "rise_db": round(float(rms_db[i] - pre), 1),
                           "level_db": round(float(rms_db[i]), 1), "low": round(prof["sub"] + prof["bass"], 2),
                           "mid": prof["mid"], "high": round(prof["pres"] + prof["air"], 2)})

    # --- tempo: autocorrelación del flujo en graves y total
    def tempo(env):
        e = env - env.mean()
        ac = np.correlate(e, e, "full")[len(e) - 1:]
        ac /= ac[0] + 1e-9
        out = []
        for bpm in np.arange(70, 181, 0.5):
            lag = 60 / bpm * SR / HOP
            lo = int(np.floor(lag))
            v = ac[lo] * (1 - (lag - lo)) + ac[lo + 1] * (lag - lo)
            out.append((float(v), float(bpm)))
        out.sort(reverse=True)
        picks = []
        for v, b in out:
            if all(abs(b - q[1]) > 4 for q in picks):
                picks.append((round(v, 3), b))
            if len(picks) == 3:
                break
        return picks

    t_low = tempo(flux_b["sub"] + flux_b["bass"])
    t_all = tempo(flux)
    bpm = t_low[0][1]
    period = 60 / bpm * SR / HOP
    env = flux_b["sub"] + flux_b["bass"]
    best_phase, best = 0.0, -1
    for ph in np.arange(0, period, 0.5):
        idx = np.arange(ph, T - 1, period).astype(int)
        s = env[idx].sum()
        if s > best:
            best, best_phase = s, ph
    beats = [round(float(i * HOP / SR), 3) for i in np.arange(best_phase, T - 1, period)]

    # --- ducking: nivel de subgraves (música) con voz y sin voz
    wj = DATOS / slug / "words.json"
    duck = None
    if wj.exists():
        words = json.loads(wj.read_text())["words"]
        speech = np.zeros(T, bool)
        for w in words:
            speech[int(w["t0"] * SR / HOP):int(w["t1"] * SR / HOP) + 1] = True
        sub = pow_b["sub"]
        if speech.any() and (~speech).any():
            first, last = int(words[0]["t0"] * SR / HOP), int(words[-1]["t1"] * SR / HOP)
            inner = np.zeros(T, bool)
            inner[first:last] = True
            duck = {
                "sub_db_con_voz": round(float(np.median(sub[speech])), 1),
                "sub_db_pausas_internas": round(float(np.median(sub[~speech & inner])), 1) if (~speech & inner).any() else None,
                "sub_db_sin_voz_extremos": round(float(np.median(sub[~speech & ~inner])), 1) if (~speech & ~inner).any() else None,
                "total_db_con_voz": round(float(np.median(rms_db[speech])), 1),
                "total_db_sin_voz": round(float(np.median(rms_db[~speech])), 1),
            }

    # --- estéreo
    stereo = None
    if x.shape[1] == 2:
        l, r = x[:, 0], x[:, 1]
        mid, side = (l + r) / 2, (l - r) / 2
        stereo = {"lr_corr": round(float(np.corrcoef(l, r)[0, 1]), 3),
                  "side_to_mid_db": round(float(10 * np.log10((side ** 2).mean() / ((mid ** 2).mean() + 1e-12) + 1e-12)), 1)}

    thr = -50
    active = np.nonzero(rms_db > thr)[0]
    loud = ebur128(slug)
    out = DATOS / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "audio.json").write_text(json.dumps({
        "slug": slug, "duration": round(dur, 3), "sample_rate": info["audio_rate"],
        "loudness": {k: v for k, v in loud.items() if k != "short_term"},
        "short_term_lufs_every_100ms": loud["short_term"],
        "first_sound_t": round(float(times[active[0]]), 3) if len(active) else None,
        "last_sound_t": round(float(times[active[-1]]), 3) if len(active) else None,
        "tempo_bpm_graves": t_low, "tempo_bpm_total": t_all, "beat_grid_s": beats,
        "ducking": duck, "stereo": stereo,
        "onsets": onsets,
        "rms_db_10ms": [round(float(v), 1) for v in rms_db],
        "sub_db_10ms": [round(float(v), 1) for v in pow_b["sub"]],
    }))

    # --- espectrogramas anotados ------------------------------------------------
    cuts = json.loads((out / "cuts.json").read_text()) if (out / "cuts.json").exists() else []
    words = json.loads(wj.read_text())["words"] if wj.exists() else []
    sp = ANALYSIS / "spectro" / slug
    sp.mkdir(parents=True, exist_ok=True)
    for old in sp.glob("s_*.png"):
        old.unlink()
    PXS, HH, TOP = 190, 360, 74                 # px por segundo, alto del espectro, franja de anotación
    fmin, fmax = 40.0, 16000.0
    rows = np.geomspace(fmin, fmax, HH)
    bin_of = np.clip(np.searchsorted(freqs, rows), 1, len(freqs) - 1)
    db = 20 * np.log10(S + 1e-6)
    db = np.clip((db - db.max() + 85) / 85, 0, 1)
    ttf = "/System/Library/Fonts/Supplemental/Arial.ttf"
    font = ImageFont.truetype(ttf, 12)
    small = ImageFont.truetype(ttf, 10)
    SEG = 8.0
    k = 0
    while k * SEG < dur:
        t0, t1 = k * SEG, min(dur, (k + 1) * SEG)
        wpx = int((t1 - t0) * PXS)
        cols = np.clip(((np.arange(wpx) / PXS + t0) * SR / HOP).astype(int), 0, T - 1)
        img = db[cols][:, bin_of].T[::-1]
        # mapa de color sencillo: negro -> morado -> naranja -> blanco
        r = np.clip(img * 3 - 0.6, 0, 1)
        g = np.clip(img * 3 - 1.6, 0, 1)
        b = np.clip(np.where(img < 0.5, img * 1.6, 1.3 - img), 0, 1)
        rgb = (np.dstack([r, g, b]) * 255).astype(np.uint8)
        canvas = Image.new("RGB", (wpx, TOP + HH + 16), (16, 16, 16))
        canvas.paste(Image.fromarray(rgb), (0, TOP))
        d = ImageDraw.Draw(canvas)
        for s in range(int(np.ceil(t0)), int(t1) + 1):
            xx = int((s - t0) * PXS)
            d.line([xx, TOP + HH, xx, TOP + HH + 5], fill=(200, 200, 200))
            d.text((xx + 2, TOP + HH + 3), f"{s}s", fill=(200, 200, 200), font=small)
        for fq in (100, 1000, 5000):
            yy = TOP + HH - int(np.searchsorted(rows, fq))
            d.line([0, yy, 6, yy], fill=(255, 255, 255))
            d.text((8, yy - 6), f"{fq}Hz", fill=(255, 255, 255), font=small)
        for c in cuts:
            if t0 <= c["t"] < t1:
                xx = int((c["t"] - t0) * PXS)
                col = (255, 60, 60) if c["conf"] == "alta" else (255, 160, 40)
                d.line([xx, 30, xx, TOP + HH], fill=col)
                d.text((xx + 2, 30), f"f{c['f']}", fill=col, font=small)
        row = 0
        for w in words:
            if t0 <= w["t0"] < t1:
                xx = int((w["t0"] - t0) * PXS)
                d.line([xx, 46 + 13 * (row % 2), xx, TOP], fill=(120, 220, 255))
                d.text((xx + 2, 44 + 13 * (row % 2)), w["w"], fill=(120, 220, 255), font=font)
                row += 1
        for o in onsets:
            if t0 <= o["t"] < t1:
                xx = int((o["t"] - t0) * PXS)
                d.polygon([(xx - 4, 2), (xx + 4, 2), (xx, 12)], fill=(255, 255, 80))
                d.text((xx + 5, 0), f"{o['z']:.0f}", fill=(255, 255, 80), font=small)
        d.text((2, 16), f"{slug}  {t0:.0f}-{t1:.0f}s   amarillo = golpe de audio (z) · rojo = corte · azul = palabra de la locución", fill=(230, 230, 230), font=small)
        canvas.save(sp / f"s_{int(t0):03d}-{int(np.ceil(t1)):03d}.png")
        k += 1

    print(f"{slug:15s} {loud['integrated_lufs']} LUFS  LRA {loud['lra']}  pico {loud['true_peak_dbfs']} dBTP  "
          f"tempo graves {t_low[0][1]} BPM ({t_low[0][0]})  golpes {len(onsets)}  ducking {duck and duck['sub_db_con_voz']} / "
          f"{duck and duck['sub_db_sin_voz_extremos']}")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)

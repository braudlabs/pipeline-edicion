#!/usr/bin/env python3
"""Espectrograma ampliado con marcas de fotograma (solo numpy + PIL).

  spec.py <t0> <t1> <salida.png> [--n 1024] [--marks "f102:corte,f137:corte"]
Eje de frecuencia logarítmico 30 Hz–16 kHz. Marcas verticales cada fotograma (24 fps), rótulo cada 4.
Debajo: envolvente RMS total (blanco), <120 Hz (naranja) y >4 kHz (cian), en dB.
"""
import argparse
import json
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
SLUG = "lafabrica-v1"
FPS = 24.0


def load():
    with wave.open(str(ROOT / "analysis" / "audio" / f"{SLUG}.wav")) as w:
        ch, n, sr = w.getnchannels(), w.getnframes(), w.getframerate()
        x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768.0
    return x.reshape(-1, ch), sr


def font(sz):
    for p in ["/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("t0", type=float)
    ap.add_argument("t1", type=float)
    ap.add_argument("out")
    ap.add_argument("--n", type=int, default=1024)
    ap.add_argument("--w", type=int, default=1560)
    ap.add_argument("--marks", default="")
    ap.add_argument("--side", action="store_true")
    ap.add_argument("--lo", type=float, default=-85.0)
    ap.add_argument("--hi", type=float, default=-15.0)
    a = ap.parse_args()
    x, sr = load()
    mono = x.mean(axis=1) if not a.side else (x[:, 0] - x[:, 1]) / 2
    N = a.n
    Wpx = a.w
    Hs = 520
    left = 46
    plotw = Wpx - left
    t = np.linspace(a.t0, a.t1, plotw, endpoint=False)
    win = np.hanning(N).astype(np.float32)
    pad = np.concatenate([np.zeros(N, np.float32), mono, np.zeros(N, np.float32)])
    cols = []
    for tt in t:
        c = int(tt * sr) + N - N // 2
        seg = pad[c:c + N] * win
        cols.append(np.abs(np.fft.rfft(seg)))
    S = np.array(cols).T                      # freq x time
    freqs = np.fft.rfftfreq(N, 1 / sr)
    fy = np.geomspace(30, 16000, Hs)[::-1]
    idx = np.clip(np.searchsorted(freqs, fy), 1, len(freqs) - 1)
    # para bins bajos, interpola
    Sl = np.empty((Hs, plotw), np.float32)
    for i, f in enumerate(fy):
        j = idx[i]
        f0, f1 = freqs[j - 1], freqs[j]
        w1 = (f - f0) / (f1 - f0)
        Sl[i] = S[j - 1] * (1 - w1) + S[j] * w1
    db = 20 * np.log10(Sl / (N / 4) + 1e-7)
    lo, hi = a.lo, a.hi
    v = np.clip((db - lo) / (hi - lo), 0, 1)
    # paleta tipo magma sencilla
    stops = np.array([[0, 0, 4], [40, 11, 84], [101, 21, 110], [159, 42, 99], [212, 72, 66], [245, 125, 21], [250, 193, 39], [252, 255, 164]], np.float32)
    pos = v * (len(stops) - 1)
    i0 = np.clip(pos.astype(int), 0, len(stops) - 2)
    fr = (pos - i0)[..., None]
    rgb = (stops[i0] * (1 - fr) + stops[i0 + 1] * fr).astype(np.uint8)
    He = 150
    top = 54
    img = Image.new("RGB", (Wpx, top + Hs + He + 22), (18, 18, 18))
    img.paste(Image.fromarray(rgb), (left, top))
    d = ImageDraw.Draw(img)
    f10, f12 = font(11), font(13)
    for hz in [50, 100, 200, 500, 1000, 2000, 5000, 10000]:
        y = top + int(np.argmin(np.abs(fy - hz)))
        d.line([(left - 4, y), (left, y)], fill=(200, 200, 200))
        d.text((2, y - 6), f"{hz if hz < 1000 else str(hz // 1000) + 'k'}", fill=(200, 200, 200), font=f10)
    X = lambda tt: left + (tt - a.t0) / (a.t1 - a.t0) * plotw  # noqa: E731
    f_a, f_b = int(np.ceil(a.t0 * FPS)), int(np.floor(a.t1 * FPS))
    for f in range(f_a, f_b + 1):
        xx = X(f / FPS)
        major = f % 4 == 0
        d.line([(xx, top - (10 if major else 4)), (xx, top)], fill=(255, 220, 90))
        if major:
            d.text((xx + 2, top - 24), f"f{f}", fill=(255, 220, 90), font=f10)
            for yy in range(top, top + Hs, 6):
                d.point((xx, yy), fill=(255, 255, 255))
    # palabras
    words = json.loads((ROOT / "datos" / SLUG / "words.json").read_text())
    wl = words["words"] if isinstance(words, dict) else words
    for w in wl:
        s, e = w.get("start", w.get("t0")), w.get("end", w.get("t1"))
        if s is None or e < a.t0 or s > a.t1:
            continue
        d.line([(X(s), 26), (X(s), 40)], fill=(110, 200, 255))
        d.text((X(s) + 2, 26), str(w.get("word", w.get("w", ""))).strip(), fill=(110, 200, 255), font=f12)
    for m in [m for m in a.marks.split(",") if m]:
        ff, lab = m.split(":")
        fnum = float(ff.lstrip("f"))
        xx = X(fnum / FPS)
        d.line([(xx, top), (xx, top + Hs + He)], fill=(255, 60, 60))
        d.text((xx + 2, 4), f"{ff} {lab}", fill=(255, 90, 90), font=f12)
    # envolventes
    hop = 64
    def env(sig):
        n = len(sig) // hop
        r = np.sqrt((sig[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
        k = 6
        r = np.convolve(r, np.ones(k) / k, mode="same")
        return 20 * np.log10(r + 1e-9)
    spec_full = np.fft.rfft(mono)
    fq = np.fft.rfftfreq(len(mono), 1 / sr)
    def bandsig(lo_, hi_):
        m = (fq >= lo_) & (fq < hi_)
        return np.fft.irfft(spec_full * m, len(mono)).astype(np.float32)
    y0 = top + Hs + 4
    for sig, col in [(mono, (235, 235, 235)), (bandsig(20, 120), (255, 150, 40)), (bandsig(4000, 20000), (80, 220, 255)), (bandsig(1000, 4000), (160, 255, 120))]:
        e = env(sig)
        te = np.arange(len(e)) * hop / sr
        m = (te >= a.t0) & (te < a.t1)
        xs = left + (te[m] - a.t0) / (a.t1 - a.t0) * plotw
        ys = y0 + (1 - np.clip((e[m] + 70) / 70, 0, 1)) * (He - 6)
        d.line(list(zip(xs.tolist(), ys.tolist())), fill=col)
    for dbv in [-60, -40, -20, 0]:
        yy = y0 + (1 - (dbv + 70) / 70) * (He - 6)
        d.text((2, yy - 6), f"{dbv}dB", fill=(160, 160, 160), font=f10)
        d.line([(left, yy), (Wpx, yy)], fill=(50, 50, 50))
    d.text((left, top + Hs + He + 4), f"{SLUG}  {a.t0:.2f}-{a.t1:.2f} s   N={N}   blanco=total  naranja=<120Hz  verde=1-4kHz  cian=>4kHz", fill=(180, 180, 180), font=f10)
    img.save(a.out)
    print(a.out, img.size)


if __name__ == "__main__":
    main()

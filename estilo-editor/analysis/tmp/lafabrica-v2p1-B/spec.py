#!/usr/bin/env python3
"""Espectrograma ampliado (canal medio y canal lateral L-R) con rejilla de fotogramas y palabras.
  spec.py t0 t1 -o out.png [--pxs 400] [--n 1024] [--marks 661,676]"""
import argparse, json, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import fr
ap = argparse.ArgumentParser()
ap.add_argument("t0", type=float); ap.add_argument("t1", type=float)
ap.add_argument("-o", required=True)
ap.add_argument("--pxs", type=float, default=380)
ap.add_argument("--n", type=int, default=1024)
ap.add_argument("--marks", default="")
ap.add_argument("--hh", type=int, default=300)
a = ap.parse_args()
SR = 44100
p = fr.ROOT / "analysis" / "audio" / f"{fr.SLUG}.wav"
with wave.open(str(p)) as w:
    ch, n = w.getnchannels(), w.getnframes()
    x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768.0
x = x.reshape(-1, ch)
mid = x.mean(1); side = (x[:, 0] - x[:, 1]) / 2 if ch == 2 else np.zeros_like(mid)
N = a.n; HOP = max(1, int(SR / a.pxs))
def stft(sig, t0, t1):
    i0 = int(t0 * SR); i1 = int(t1 * SR)
    pad = np.concatenate([np.zeros(N, np.float32), sig, np.zeros(N, np.float32)])
    starts = np.arange(i0, i1, HOP) + N - N // 2
    idx = starts[:, None] + np.arange(N)[None, :]
    return np.abs(np.fft.rfft(pad[idx] * np.hanning(N).astype(np.float32), axis=1))
freqs = np.fft.rfftfreq(N, 1 / SR)
rows = np.geomspace(40.0, 18000.0, a.hh)
bin_of = np.clip(np.searchsorted(freqs, rows), 1, len(freqs) - 1)
def render(sig, ref_db):
    S = stft(sig, a.t0, a.t1)
    db = 20 * np.log10(S + 1e-7)
    img = np.clip((db - ref_db + 80) / 80, 0, 1)[:, bin_of].T[::-1]
    r = np.clip(img * 3 - 0.6, 0, 1); g = np.clip(img * 3 - 1.6, 0, 1); b = np.clip(np.where(img < 0.5, img * 1.6, 1.3 - img), 0, 1)
    return (np.dstack([r, g, b]) * 255).astype(np.uint8), db.max()
Sm = stft(mid, a.t0, a.t1); refm = 20 * np.log10(Sm.max() + 1e-7)
im_m, _ = render(mid, refm)
Ss = stft(side, a.t0, a.t1); refs = 20 * np.log10(Ss.max() + 1e-7)
im_s, _ = render(side, refs)
W = im_m.shape[1]; TOP = 46; GAP = 22
H = TOP + a.hh + GAP + a.hh + 16
can = Image.new("RGB", (W + 50, H), (16, 16, 16))
can.paste(Image.fromarray(im_m), (50, TOP)); can.paste(Image.fromarray(im_s), (50, TOP + a.hh + GAP))
d = ImageDraw.Draw(can)
font = ImageFont.load_default(size=11)
def X(t): return 50 + (t - a.t0) * SR / HOP
d.text((2, TOP + 2), "MEDIO", fill=(255, 255, 255), font=font)
d.text((2, TOP + a.hh + GAP + 2), f"LATERAL", fill=(255, 255, 255), font=font)
d.text((2, TOP + a.hh + GAP + 14), f"{refs-refm:+.0f}dB", fill=(200, 200, 200), font=font)
for hz in (100, 300, 1000, 3000, 10000):
    yy = a.hh - 1 - np.searchsorted(rows, hz)
    for base in (TOP, TOP + a.hh + GAP):
        d.text((22, base + yy - 5), f"{hz if hz<1000 else str(hz//1000)+'k'}", fill=(160, 160, 160), font=font)
        d.line([(46, base + yy), (50, base + yy)], fill=(160, 160, 160))
f0 = int(np.ceil(a.t0 * 24)); f1 = int(np.floor(a.t1 * 24))
marks = {int(v) for v in a.marks.split(",") if v}
for f in range(f0, f1 + 1):
    x_ = X(f / 24)
    big = (f % 4 == 0)
    col = (255, 60, 60) if f in marks else ((120, 220, 255) if big else (70, 110, 130))
    for base in (TOP, TOP + a.hh + GAP):
        d.line([(x_, base - (8 if big or f in marks else 4)), (x_, base + (a.hh if f in marks else 0))], fill=col, width=1)
    if big or f in marks:
        d.text((x_ + 2, TOP - 20 if f not in marks else TOP - 32), f"f{f}", fill=col, font=font)
words = json.loads((fr.ROOT / "datos" / fr.SLUG / "words.json").read_text())["words"]
for w in words:
    if w["t1"] < a.t0 or w["t0"] > a.t1: continue
    xa, xb = X(w["t0"]), X(w["t1"])
    d.line([(xa, 2), (xa, 14)], fill=(120, 170, 255)); d.line([(xa, 14), (xb - 1, 14)], fill=(120, 170, 255))
    d.text((xa + 2, 1), w.get("w", w.get("word", "?")), fill=(160, 200, 255), font=font)
d.text((50, H - 14), f"{a.t0:.2f}s .. {a.t1:.2f}s   hop {HOP/SR*1000:.1f} ms  N={N}", fill=(200, 200, 200), font=font)
can.save(a.o)
print(a.o, can.size)

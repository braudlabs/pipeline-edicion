"""Espectrogramas ampliados (mid y side) con rejilla de fotogramas.
uso: spec.py t0 t1 salida.png [side|mid|both]"""
import sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[3]
WAV = ROOT / "analysis" / "audio" / "v2-churros.wav"
FPS = 24.0

def load():
    w = wave.open(str(WAV)); sr = w.getframerate(); ch = w.getnchannels(); n = w.getnframes()
    x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768
    x = x.reshape(-1, ch)
    return sr, x

def stft(x, sr, t0, t1, nfft=2048, hop=None, width=1500):
    i0, i1 = int(t0 * sr), int(t1 * sr)
    hop = hop or max(1, (i1 - i0) // width)
    win = np.hanning(nfft).astype(np.float32)
    pad = np.concatenate([np.zeros(nfft // 2, np.float32), x, np.zeros(nfft, np.float32)])
    cols = []
    for c in range(i0, i1, hop):
        seg = pad[c:c + nfft] * win
        cols.append(np.abs(np.fft.rfft(seg)))
    S = np.stack(cols, 1)
    return 20 * np.log10(S / (nfft / 4) + 1e-9), hop

def render(db, sr, t0, t1, title, h=420, fmin=40, fmax=15000, lo=-95, hi=-15):
    nb = db.shape[0]; freqs = np.linspace(0, sr / 2, nb)
    ys = np.exp(np.linspace(np.log(fmax), np.log(fmin), h))
    idx = np.clip(np.searchsorted(freqs, ys), 0, nb - 1)
    img = db[idx]
    v = np.clip((img - lo) / (hi - lo), 0, 1)
    # paleta sencilla tipo magma
    r = np.clip(v * 2.2, 0, 1); g = np.clip(v * 2.2 - 0.9, 0, 1); b = np.clip(np.where(v < 0.5, v * 1.6, 1.6 - v * 1.6) + np.clip(v * 3 - 2.3, 0, 1), 0, 1)
    rgb = (np.stack([r, g, b], 2) * 255).astype(np.uint8)
    im = Image.fromarray(rgb)
    W = im.width
    out = Image.new("RGB", (W + 60, h + 46), (16, 16, 16))
    out.paste(im, (60, 26))
    d = ImageDraw.Draw(out)
    try: font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except Exception: font = ImageFont.load_default()
    d.text((4, 4), title, fill=(255, 255, 255), font=font)
    for f in (50, 100, 200, 500, 1000, 2000, 5000, 10000):
        y = 26 + int(np.interp(np.log(f), np.log(ys[::-1]), np.arange(h)[::-1]))
        d.line([(54, y), (60, y)], fill=(200, 200, 200)); d.text((2, y - 6), f"{f}", fill=(200, 200, 200), font=font)
    f0 = int(np.ceil(t0 * FPS)); f1 = int(np.floor(t1 * FPS))
    for f in range(f0, f1 + 1):
        x = 60 + int((f / FPS - t0) / (t1 - t0) * W)
        big = f % 6 == 0
        d.line([(x, 26 + h), (x, 26 + h + (8 if big else 3))], fill=(255, 220, 90))
        if big:
            d.line([(x, 26), (x, 26 + h)], fill=(70, 70, 40))
            d.text((x + 2, 26 + h + 6), f"f{f}", fill=(255, 220, 90), font=font)
    return out

if __name__ == "__main__":
    t0, t1 = float(sys.argv[1]), float(sys.argv[2]); outp = sys.argv[3]; mode = sys.argv[4] if len(sys.argv) > 4 else "both"
    sr, x = load()
    mid = x.mean(axis=1); side = (x[:, 0] - x[:, 1]) / 2 if x.shape[1] > 1 else np.zeros(len(x), np.float32)
    ims = []
    if mode in ("mid", "both"):
        db, hop = stft(mid, sr, t0, t1); ims.append(render(db, sr, t0, t1, f"MID (L+R)  {t0:.2f}-{t1:.2f} s  · rejilla = fotogramas (línea cada 6)"))
    if mode in ("side", "both"):
        db, hop = stft(side, sr, t0, t1); ims.append(render(db, sr, t0, t1, f"SIDE (L-R: sin la voz centrada)  {t0:.2f}-{t1:.2f} s", lo=-115, hi=-40))
    Wd = max(i.width for i in ims); Ht = sum(i.height for i in ims)
    out = Image.new("RGB", (Wd, Ht), (16, 16, 16)); y = 0
    for i in ims: out.paste(i, (0, y)); y += i.height
    out.save(outp); print(outp, out.size)

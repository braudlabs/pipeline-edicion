"""Diseño sonoro del demo (copia de trabajo fuera de iCloud). Igual que tools/sound.py del proyecto.
Efectos sintetizados → remotion/public/audio/sfx-*.wav; música montada → music-stem.wav."""
import json, subprocess, wave
from pathlib import Path
import numpy as np
root = Path(__file__).resolve().parent.parent
out = root / 'remotion/public/audio'
SR = 48000
rng = np.random.default_rng(7)
def save(name, x):
    x = np.clip(np.asarray(x, dtype=np.float64), -1, 1)
    st = np.stack([x, x], 1) if x.ndim == 1 else x
    with wave.open(str(out / f'{name}.wav'), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
def t_(d): return np.arange(int(d * SR)) / SR
def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * np.asarray(fc) / SR) * np.ones_like(x)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc; y[i] = acc
    return y
def bandsweep(d, f0, f1, q=3.0):
    n = rng.standard_normal(int(d * SR)); fc = np.geomspace(f0, f1, len(n))
    return onepole_lp(n, fc * (1 + 1 / q)) - onepole_lp(n, fc / (1 + 1 / q))
def env_ar(n, a, r, curve=2.0):
    t = np.linspace(0, 1, n); k = a / (a + r)
    return np.where(t < k, (t / k) ** curve, ((1 - t) / (1 - k)) ** curve)
def norm(x, peak=0.9): return x / (np.max(np.abs(x)) + 1e-9) * peak
def whoosh(d, f0, f1, peak): return norm(bandsweep(d, f0, f1) * env_ar(int(d * SR), 0.55, 0.45, 1.6), peak)
def impact(d=1.4):
    t = t_(d)
    sub = np.sin(2 * np.pi * np.cumsum(np.geomspace(90, 34, len(t))) / SR) * np.exp(-t * 3.2)
    click = rng.standard_normal(len(t)) * np.exp(-t * 90) * 0.6
    tail = onepole_lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 2.2) * 2.5
    return norm(sub * 0.9 + click + tail * 0.35, 0.95)
def tick(d=0.05, f=2400):
    t = t_(d); return norm(np.sin(2 * np.pi * f * t) * np.exp(-t * 160) + rng.standard_normal(len(t)) * np.exp(-t * 400) * 0.3, 0.7)
def pop(d=0.12):
    t = t_(d); f = np.geomspace(900, 320, len(t)); return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 38), 0.8)
def shimmer(d=1.1):
    t = t_(d); x = sum(np.sin(2 * np.pi * f * t + p) for f, p in [(1760, 0), (2637, 1), (3520, 2), (4699, .5)])
    return norm(x * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)) * np.exp(-t * 3.5) * np.minimum(1, t / 0.02), 0.45)
def riser(d=2.8):
    t = t_(d); k = t / d
    noise = bandsweep(d, 300, 9000, 2.0) * k ** 2.2
    tone = np.sin(2 * np.pi * np.cumsum(np.geomspace(110, 880, len(t))) / SR) * k ** 3 * 0.35
    return norm((noise + tone) * np.minimum(1, (d - t) / 0.03), 0.85)
def thump(d=0.5):
    t = t_(d); return norm(np.sin(2 * np.pi * np.cumsum(np.geomspace(140, 45, len(t))) / SR) * np.exp(-t * 9), 0.9)
def clock(d=0.09):
    t = t_(d); return norm((np.sin(2 * np.pi * 1300 * t) + 0.5 * np.sin(2 * np.pi * 3100 * t)) * np.exp(-t * 70), 0.55)
def data_blips(d=0.6, n=7):
    x = np.zeros(int(d * SR))
    for i in range(n):
        s = int(i * d / n * SR); b = tick(0.04, 1800 + 300 * (i % 3)) * (0.6 + 0.4 * rng.random()); x[s:s + len(b)] += b[:len(x) - s]
    return norm(x, 0.6)
effects = {'sfx-whoosh-fast': whoosh(0.42, 400, 7000, 0.8), 'sfx-whoosh-long': whoosh(0.95, 250, 5500, 0.85),
    'sfx-whoosh-down': whoosh(0.6, 6000, 300, 0.75), 'sfx-impact': impact(), 'sfx-tick': tick(), 'sfx-pop': pop(),
    'sfx-shimmer': shimmer(), 'sfx-riser': riser(2.8), 'sfx-thump': thump(), 'sfx-clock': clock(), 'sfx-blips': data_blips()}
for k, v in effects.items(): save(k, v)
def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).astype(np.float64)
music = load(out / 'music-tech-house-vibes.mp3')
DUR, OFF, STOP0, STOP1, BACK = 125.0, 7.05, 4.00, 4.45, 6.20
N = int(DUR * SR); stem = np.zeros((N, 2))
def seg(v0, v1, s0):
    a, b = int(v0 * SR), int(v1 * SR); s = int(s0 * SR); chunk = music[s:s + (b - a)]; stem[a:a + len(chunk)] += chunk
# V03 («la música está muy fuerte»): sin frenazo de cinta. La pista sigue sin cortes y en «ritmo de mes»
# solo se filtra (lejana) con fundidos de 0,25 s; vuelve abierta con «Y los anuncios…».
seg(0, DUR, OFF)
a, b = int(STOP0 * SR), int(BACK * SR)
far = np.stack([onepole_lp(stem[a:b, 0], 420), onepole_lp(stem[a:b, 1], 420)], 1) * 0.6
fade = np.ones(b - a); fl = int(0.25 * SR); fade[:fl] = np.linspace(0, 1, fl); fade[-fl:] = np.linspace(1, 0, fl)
stem[a:b] = stem[a:b] * (1 - fade)[:, None] + far * fade[:, None]
envj = json.loads((root / 'remotion/src/data/voice-env.json').read_text())
env = np.interp(np.arange(N) / SR * 60, np.arange(len(envj)), envj)
stem *= (1 - 0.55 * onepole_lp(np.clip(env * 1.6, 0, 1), 3.0))[:, None] * 0.24  # ~7 dB menos que V02 y más ducking
save('music-stem', stem)
print('sfx', len(effects), '· música', round(N / SR, 1), 's')

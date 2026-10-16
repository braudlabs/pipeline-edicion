#!/usr/bin/env python3
"""aud2.py t0 t1 ventana_s: energía media por bandas (dB) en ventanas consecutivas (promedio de espectros)."""
import sys
import numpy as np
sr = 22050
x = np.frombuffer(open("a_mono.raw", "rb").read(), np.int16).astype(np.float32) / 32768
t0, t1, win = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
N = 2048
bands = [(20, 60), (60, 120), (120, 250), (250, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 11000)]
fq = np.fft.rfftfreq(N, 1 / sr)
print("t0\tf0\t" + "\t".join(f"{a}-{b}" for a, b in bands))
t = t0
while t < t1:
    a, b = int(t * sr), int((t + win) * sr)
    acc = np.zeros(N // 2 + 1); n = 0
    for i in range(a, b - N, N // 2):
        acc += np.abs(np.fft.rfft(x[i:i + N] * np.hanning(N))) ** 2; n += 1
    acc /= max(1, n)
    print(f"{t:.2f}\t{t*24:.0f}\t" + "\t".join(f"{10*np.log10(acc[(fq>=lo)&(fq<hi)].sum()+1e-9):.0f}" for lo, hi in bands))
    t += win

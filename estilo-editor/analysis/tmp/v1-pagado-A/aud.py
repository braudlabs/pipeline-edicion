#!/usr/bin/env python3
"""aud.py t0 t1 [paso_ms]: energía por bandas (dB) cada paso, para leer música/efectos/voz."""
import sys
import numpy as np
sr = 22050
x = np.frombuffer(open("a_mono.raw", "rb").read(), np.int16).astype(np.float32) / 32768
t0, t1 = float(sys.argv[1]), float(sys.argv[2]); step = float(sys.argv[3]) / 1000 if len(sys.argv) > 3 else 1 / 24
N = 1024
bands = [(20, 60), (60, 120), (120, 250), (250, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 11000)]
fq = np.fft.rfftfreq(N, 1 / sr)
print("t\tf\t" + "\t".join(f"{a}-{b}" for a, b in bands) + "\ttotal")
t = t0
while t < t1:
    i = int(t * sr)
    seg = x[max(0, i - N // 2): i + N // 2]
    if len(seg) < N: seg = np.pad(seg, (0, N - len(seg)))
    S = np.abs(np.fft.rfft(seg * np.hanning(N))) ** 2
    out = []
    for a, b in bands:
        e = S[(fq >= a) & (fq < b)].sum()
        out.append(f"{10*np.log10(e+1e-9):.0f}")
    print(f"{t:.3f}\t{t*24:.1f}\t" + "\t".join(out) + f"\t{10*np.log10(S.sum()+1e-9):.0f}")
    t += step

#!/usr/bin/env python3
"""side.py t0 t1: por fotograma (1/24 s), RMS dB de medio (L+R) y lateral (L-R) y bandas del lateral."""
import sys
import numpy as np
sr = 22050
s = np.frombuffer(open("a_st.raw", "rb").read(), np.int16).astype(np.float32).reshape(-1, 2) / 32768
mid = (s[:, 0] + s[:, 1]) / 2; sd = (s[:, 0] - s[:, 1]) / 2
t0, t1 = float(sys.argv[1]), float(sys.argv[2])
N = 1024; fq = np.fft.rfftfreq(N, 1 / sr)
def db(v): return 10 * np.log10(np.mean(v ** 2) + 1e-12)
f = int(round(t0 * 24))
print("f\tt\tmid\tside\tS<200\tS200-2k\tS2k-11k")
while f / 24 < t1:
    i = int(f / 24 * sr); seg_m = mid[i:i + sr // 24]; seg_s = sd[max(0, i - 50):max(0, i - 50) + N]
    if len(seg_s) < N: break
    S = np.abs(np.fft.rfft(seg_s * np.hanning(N))) ** 2
    b = lambda lo, hi: 10 * np.log10(S[(fq >= lo) & (fq < hi)].sum() + 1e-9)
    print(f"{f}\t{f/24:.3f}\t{db(seg_m):.0f}\t{db(sd[i:i + sr // 24]):.0f}\t{b(20,200):.0f}\t{b(200,2000):.0f}\t{b(2000,11000):.0f}")
    f += 1

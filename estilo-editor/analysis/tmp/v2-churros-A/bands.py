"""Energía por bandas y por fotograma (mid y side). uso: bands.py f0 f1"""
import sys, wave
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from spec import load
FPS = 24.0
sr, x = load()
mid = x.mean(axis=1); side = (x[:, 0] - x[:, 1]) / 2

def band_rms(sig, f, lo, hi, nfft=2048):
    c = int((f + 0.5) / FPS * sr)
    seg = sig[max(0, c - nfft // 2): c + nfft // 2]
    if len(seg) < nfft: seg = np.pad(seg, (0, nfft - len(seg)))
    S = np.abs(np.fft.rfft(seg * np.hanning(nfft))) / (nfft / 4)
    fr = np.fft.rfftfreq(nfft, 1 / sr)
    sel = (fr >= lo) & (fr < hi)
    return 10 * np.log10((S[sel] ** 2).sum() + 1e-12)

def rms(sig, f):
    a = int(f / FPS * sr); b = int((f + 1) / FPS * sr)
    return 10 * np.log10((sig[a:b] ** 2).mean() + 1e-12)

if __name__ == "__main__":
    f0, f1 = int(sys.argv[1]), int(sys.argv[2])
    print("f\tt\tmid\tside\tm<120\tm120-500\tm>6k\ts<150\ts150-2k\ts2k-6k\ts>6k")
    for f in range(f0, f1 + 1):
        print(f"{f}\t{f/FPS:.3f}\t{rms(mid,f):.1f}\t{rms(side,f):.1f}\t{band_rms(mid,f,20,120):.1f}\t{band_rms(mid,f,120,500):.1f}\t{band_rms(mid,f,6000,16000):.1f}\t"
              f"{band_rms(side,f,20,150):.1f}\t{band_rms(side,f,150,2000):.1f}\t{band_rms(side,f,2000,6000):.1f}\t{band_rms(side,f,6000,16000):.1f}")

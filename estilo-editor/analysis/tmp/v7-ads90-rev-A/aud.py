import wave, numpy as np
def load(s):
    w = wave.open(f'analysis/audio/{s}.wav')
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).astype(np.float32) / 32768
    return x, w.getframerate()
a7, sr = load('v7-ads90-rev')
a6, _ = load('v6-ads90-rev')
m7, m6 = a7.mean(1), a6.mean(1)

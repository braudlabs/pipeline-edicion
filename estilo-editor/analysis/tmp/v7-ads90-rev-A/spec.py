"""Espectrograma propio, eje log de frecuencia, rejilla en fotogramas. uso: spec.py slug t0 t1 out.png [marcas f:etiqueta,...]"""
import sys, wave
import numpy as np
from PIL import Image, ImageDraw
slug, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
marks = [] if len(sys.argv) < 6 else [(float(p.split(':')[0]), p.split(':')[1]) for p in sys.argv[5].split(',')]
w = wave.open(f'analysis/audio/{slug}.wav'); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, w.getnchannels()).astype(np.float32).mean(1) / 32768
N = 2048; hop = 147  # 3.33 ms -> 5 columnas por fotograma
i0 = int(t0*sr); i1 = int(t1*sr)
cols = []
win = np.hanning(N)
for i in range(i0, i1, hop):
    a = i - N//2
    seg = x[max(a,0):a+N]
    if a < 0: seg = np.concatenate([np.zeros(-a, np.float32), seg])
    if len(seg) < N: seg = np.concatenate([seg, np.zeros(N-len(seg), np.float32)])
    cols.append(np.abs(np.fft.rfft(seg*win)))
S = np.array(cols).T  # freq x time
f = np.fft.rfftfreq(N, 1/sr)
H = 420
fl = np.geomspace(30, 16000, H)
idx = np.searchsorted(f, fl).clip(1, len(f)-1)
# promedio por banda log
edges = np.concatenate([[fl[0]*0.97], np.sqrt(fl[1:]*fl[:-1]), [fl[-1]*1.03]])
M = np.zeros((H, S.shape[1]), np.float32)
for k in range(H):
    a = np.searchsorted(f, edges[k]); b = max(a+1, np.searchsorted(f, edges[k+1]))
    M[k] = S[a:b].max(0)
D = 20*np.log10(M+1e-6)
D = (D - (D.max()-80)) / 80
D = D.clip(0, 1)[::-1]
# paleta
def pal(v):
    r = np.clip(1.5*v, 0, 1); g = np.clip(2.2*v-0.9, 0, 1); b = np.clip(np.where(v < 0.45, 2.0*v, 1.7-2.6*v), 0, 1) + np.clip(3*v-2.3, 0, 1)
    return (np.stack([r, g, np.clip(b,0,1)], 2)*255).astype(np.uint8)
img = Image.fromarray(pal(D))
scale = max(1, int(round(1500 / img.width)))
img = img.resize((img.width*scale, H), Image.NEAREST)
canvas = Image.new('RGB', (img.width+50, H+60), (16,16,16)); canvas.paste(img, (50, 30))
d = ImageDraw.Draw(canvas)
for hz in (50, 100, 200, 500, 1000, 2000, 5000, 10000):
    y = 30 + H - 1 - int(np.searchsorted(fl, hz)); d.line([(46, y), (50, y)], fill=(200,200,200)); d.text((2, y-6), f'{hz}', fill=(200,200,200))
pxf = (sr/60)/hop*scale
fa = int(np.ceil(t0*60)); fb = int(t1*60)
for fr in range(fa, fb+1):
    xx = 50 + (fr/60 - t0)*sr/hop*scale
    if fr % 10 == 0:
        d.line([(xx, 30+H), (xx, 30+H+8)], fill=(255,220,90)); d.text((xx-8, 30+H+10), f'f{fr}', fill=(255,220,90))
    elif fr % 2 == 0:
        d.line([(xx, 30+H), (xx, 30+H+3)], fill=(120,120,120))
for fr, lab in marks:
    xx = 50 + (fr/60 - t0)*sr/hop*scale
    d.line([(xx, 14), (xx, 30+H)], fill=(90,220,255)); d.text((xx+2, 2), lab, fill=(90,220,255))
d.text((60, 30+H+26), f'{slug}  {t0:.2f}-{t1:.2f} s   (eje x en fotogramas a 60 fps; eje y Hz log)', fill=(180,180,180))
canvas.save(out); print(out, canvas.size, 'px/fotograma', round(pxf,2))

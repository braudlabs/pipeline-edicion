"""Montaje base: 4 clips en orden narrativo, alineado a fotograma de origen (24 fps)."""
import subprocess, json
from pathlib import Path

SRC_FPS, OUT_FPS = 24, 48
# (archivo, fotogramas de origen a conservar, rol)
CORTES = [
    ('assets/src-04.mp4', 166, 'problema'),   # A los 50 el maquillaje ya no tapaba...
    ('assets/src-02.mp4', 121, 'giro'),       # Dejé de gastar dinero en correctores...
    ('assets/src-03.mp4', 166, 'solución'),   # Ahora uso este serum con color...
    ('assets/src-01.mp4', 121, 'cta'),        # Te dejo el enlace aquí abajo...
]
Path('analysis/seg').mkdir(parents=True, exist_ok=True)
plan, t = [], 0
for i,(p,nsrc,rol) in enumerate(CORTES):
    dur = nsrc / SRC_FPS
    seg = f'analysis/seg/s{i}.mov'
    subprocess.run(['ffmpeg','-v','error','-y','-i',p,'-t',f'{dur:.6f}',
        '-c:v','prores_ks','-profile:v','3','-pix_fmt','yuv422p10le',
        '-r',str(SRC_FPS),'-an',seg],check=True)
    aud = f'analysis/seg/s{i}.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',p,'-t',f'{dur:.6f}',
        '-vn','-ac','2','-ar','48000','-c:a','pcm_s16le',aud],check=True)
    plan.append({'i':i,'src':p,'rol':rol,'frames_src':nsrc,'dur':dur,
                 'inicio':round(t,6),'fin':round(t+dur,6),
                 'f48_inicio':round(t*OUT_FPS), 'f48_fin':round((t+dur)*OUT_FPS)})
    t += dur

with open('analysis/seg/lista.txt','w') as f:
    for i in range(len(CORTES)): f.write(f"file 's{i}.mov'\n")
with open('analysis/seg/lista-a.txt','w') as f:
    for i in range(len(CORTES)): f.write(f"file 's{i}.wav'\n")

subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','analysis/seg/lista.txt',
    '-c','copy','assets/Montaje.mov'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','analysis/seg/lista-a.txt',
    '-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','48000','-c:a','pcm_s16le','assets/Voz.wav'],check=True)

json.dump({'fps_salida':OUT_FPS,'fps_origen':SRC_FPS,'total_s':round(t,6),
           'total_f48':round(t*OUT_FPS),'cortes':plan}, open('src/corte.json','w'),
          ensure_ascii=False, indent=1)
print(f"montaje {t:.4f}s · {round(t*OUT_FPS)} fotogramas a 48")
for c in plan: print(f"  {c['rol']:<9} {c['inicio']:6.3f}→{c['fin']:6.3f}s  f48 {c['f48_inicio']:>5}-{c['f48_fin']:<5}")

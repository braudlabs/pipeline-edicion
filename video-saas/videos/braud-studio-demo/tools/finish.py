"""Acabado de un render: audio a −15 LUFS / −1,5 dBTP (dos pasadas), medición, detección de negros
y hoja de fotogramas. Uso: python3 -I tools/finish.py out/Avance02.mp4 BRAUD-Studio-Demo-Avance02 [t1,t2,…]
"""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

src, name = Path(sys.argv[1]), sys.argv[2]
times = [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else None
out = src.with_name(name + '.mp4')
run = lambda *a: subprocess.run(a, capture_output=True, text=True)

m = run('ffmpeg', '-hide_banner', '-i', str(src), '-af', 'loudnorm=I=-15:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-')
j = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', m.stderr).group(0))
ln = (f"loudnorm=I=-15:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=48000")
run('ffmpeg', '-v', 'error', '-y', '-i', str(src), '-c:v', 'copy', '-af', ln, '-c:a', 'aac', '-b:a', '256k', str(out))
e = run('ffmpeg', '-hide_banner', '-i', str(out), '-af', 'ebur128=peak=true', '-f', 'null', '-').stderr
I = re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]; P = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)[-1]
dur = float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(out)).stdout)
blk = run('ffmpeg', '-hide_banner', '-i', str(out), '-vf', 'blackdetect=d=0.15:pix_th=0.06', '-an', '-f', 'null', '-').stderr
blacks = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', blk)
times = times or [round(dur * k / 15, 2) for k in range(1, 15)]
thumbs = []
for t in times:
    p = out.with_name(f'.f-{t}.jpg')
    run('ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(out), '-frames:v', '1', '-vf', 'scale=480:-1', str(p))
    im = Image.open(p).convert('RGB'); d = ImageDraw.Draw(im); d.rectangle((0, 0, 58, 20), fill=(255, 60, 60)); d.text((5, 4), f'{t:.2f}', fill=(255, 255, 255))
    thumbs.append(im); p.unlink()
cols = 5; rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new('RGB', (480 * cols, 270 * rows))
for i, im in enumerate(thumbs): sheet.paste(im, ((i % cols) * 480, (i // cols) * 270))
sheet_path = out.with_name(name + '-contacto.jpg'); sheet.save(sheet_path, quality=85)
print(json.dumps({'file': str(out), 'duration': round(dur, 3), 'lufs': float(I), 'peak_dbfs': float(P), 'black': blacks, 'contact': str(sheet_path)}, ensure_ascii=False))

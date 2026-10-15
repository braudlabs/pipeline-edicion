import json,subprocess
from pathlib import Path
p=Path(__file__).resolve().parent;c=json.loads((p/'audio.json').read_text());tracks=[t for t in c['tracks'] if t.get('src') and t.get('enabled',True)];args=['ffmpeg','-v','error','-y'];filters=[]
for i,t in enumerate(tracks):
 args+=['-i',str(p/'public'/t['src'])];filters.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={t["gain"]}[a{i}]')
filters.append(''.join(f'[a{i}]' for i in range(len(tracks)))+f'amix=inputs={len(tracks)}:normalize=0,alimiter=limit={c["master"]["limiterPeak"]}:level=false:latency=true,atrim=duration={c["master"]["duration"]}[mix]')
subprocess.run(args+['-filter_complex',';'.join(filters),'-map','[mix]','-c:a','pcm_s24le',str(p/'public/assets/mix-preview.wav')],check=True)

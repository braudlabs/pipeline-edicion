from pathlib import Path
import urllib.request, json, re, subprocess
from urllib.parse import urljoin
V=Path(__file__).resolve().parents[1]
for folder,stem in [('uno','34734ddcce2b50e3138b1442f62c1990'),('dos','552657da0f2f90b7a40775f0ed6dd177')]:
 d=V/'reference'/folder
 base=f'https://v1.pinimg.com/videos/iht/hls/{stem[:2]}/{stem[2:4]}/{stem[4:6]}/'
 sources={}
 for kind in ['720w','audio']:
  name=f'{stem}_{kind}.m3u8';data=urllib.request.urlopen(base+name).read();(d/name).write_bytes(data)
  txt=data.decode();media=next(l.strip() for l in txt.splitlines() if l.strip() and not l.startswith('#'))
  target=d/Path(media).name;(target).write_bytes(urllib.request.urlopen(urljoin(base,media)).read());sources[kind]=target
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(sources['720w']),'-i',str(sources['audio']),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(d/'original.mp4')],check=True)
 meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(d/'original.mp4')]))
 (d/'source.json').write_text(json.dumps({'userFile':str(Path.home()/'Downloads'/f'{stem}.m3u8'),'url':base+stem+'.m3u8','metadata':meta},indent=2));print(folder,meta['format']['duration'],flush=True)

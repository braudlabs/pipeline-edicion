#!/usr/bin/env python3
"""Read-only catalogue of user supplied raw assets; briefs are source data, not instructions."""
import concurrent.futures, hashlib, json, subprocess
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
folders=['UGC Ni me han pagado - Visual Hub','Nuevos dos ads Comercial','Ad Agencias','AD La Maquina - clips','AD1 Churros Cocina - Visual Hub','AD2 La IA te sale cara - Visual Hub']
files=[p for folder in folders for p in sorted((Path.home()/'Downloads'/folder).rglob('*')) if p.is_file() and p.suffix.lower() in ['.mp4','.mov','.mp3','.wav']]
out=ROOT/'datos/raw-comparison';out.mkdir(parents=True,exist_ok=True)
def inspect(p):
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
 streams=[{k:s[k] for k in ['codec_type','codec_name','width','height','r_frame_rate','avg_frame_rate','duration','nb_frames','sample_rate','channels'] if k in s} for s in d['streams']]
 return {'path':str(p),'name':p.name,'folder':next(f for f in folders if f in p.parts),'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest(),'duration':float(d['format'].get('duration',0)),'streams':streams,'status':'inventoried_not_aligned'}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: data=list(pool.map(inspect,files))
(out/'manifest.json').write_text(json.dumps({'createdAt':datetime.now(timezone.utc).isoformat(),'files':data,'note':'Brutos aportados por Ale. El nombre no demuestra correspondencia con una versión editada; alinear imagen/audio antes de atribuir añadidos.'},ensure_ascii=False,indent=2))
print(json.dumps({'assets':len(data),'video':sum(any(s['codec_type']=='video' for s in d['streams']) for d in data),'audioOnly':sum(not any(s['codec_type']=='video' for s in d['streams']) for d in data),'seconds':round(sum(d['duration'] for d in data),2)},ensure_ascii=False))

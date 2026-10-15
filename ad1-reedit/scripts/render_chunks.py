from pathlib import Path
import subprocess,json,time
from datetime import datetime
R=Path(__file__).resolve().parents[1]
CACHE=Path('/Users/alejandrorubiocamarero/Library/Caches/Adobe/After Effects/26.5')
CUT=datetime(2026,9,16,12,0).timestamp()
OUT=R/'analysis/native-chunks';OUT.mkdir(exist_ok=True)
cleanup=[];renders=[]
def clean_current_cache():
 count=0;size=0
 for p in CACHE.rglob('*.aecache'):
  try:
   st=p.stat()
   if st.st_mtime<CUT:continue
   p.unlink();count+=1;size+=st.st_size
  except FileNotFoundError:pass
 cleanup.append({'files':count,'bytes':size})
 (R/'analysis/cache-cleanup.json').write_text(json.dumps(cleanup,indent=2))
 print('Temporary cache released:',round(size/2**30,2),'GiB',flush=True)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
bad=R/'output/Cocina-Master.mov'
if bad.exists():
 (R/'analysis/interrupted-master-probe.json').write_text(json.dumps(probe(bad),indent=2));bad.unlink()
for i in range(8):
 clean_current_cache();a=i*425;b=a+424;p=OUT/f'part-{i:02d}.mov';start=time.monotonic()
 cmd=['/Applications/Adobe After Effects 2026/aerender','-project',str(R/'ae/Cocina-Reedicion.aep'),'-rqindex','1','-s',str(a),'-e',str(b),'-output',str(p),'-mem_usage','15','35','-v','ERRORS_AND_PROGRESS']
 with open(OUT/f'part-{i:02d}.log','w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
 meta=probe(p);v=next(s for s in meta['streams'] if s['codec_type']=='video')
 assert int(v['nb_frames'])==425,(i,v)
 renders.append({'part':i,'firstFrame':a,'lastFrame':b,'frames':425,'seconds':time.monotonic()-start,'size':p.stat().st_size})
 (R/'analysis/native-render-report.json').write_text(json.dumps(renders,indent=2))
 print('Native section',i+1,'/8 verified:',a,'to',b,flush=True)
clean_current_cache()
lst=OUT/'concat.txt';lst.write_text(''.join("file '"+str(OUT/f'part-{i:02d}.mov')+"'\n" for i in range(8)))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(lst),'-i',str(R/'assets/Mezcla-Final.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-video_track_timescale','48000','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(R/'output/AD1-Cocina-REEDICION.mp4')],check=True)
print('Full 3400-frame MP4 encoded.',flush=True)

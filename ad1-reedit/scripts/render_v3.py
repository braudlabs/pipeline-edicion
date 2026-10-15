from pathlib import Path
import subprocess,json,time
R=Path(__file__).resolve().parents[1];OUT=R/'analysis/v3'
CACHE=Path('/Users/alejandrorubiocamarero/Library/Caches/Adobe/After Effects/26.5')
cut=(R/'ae/v3-backup.json').stat().st_mtime
def clean():
 n=b=0
 for p in CACHE.rglob('*.aecache'):
  try:
   s=p.stat()
   if s.st_mtime>=cut:p.unlink();n+=1;b+=s.st_size
  except FileNotFoundError:pass
 print('Temporary V3 cache released:',round(b/2**30,2),'GiB',flush=True)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))
clean()
p=OUT/'part-02.mov';cmd=['/Applications/Adobe After Effects 2026/aerender','-project',str(R/'ae/Cocina-Reedicion-V3.aep'),'-rqindex','1','-s','850','-e','1274','-output',str(p),'-mem_usage','15','35','-v','ERRORS_AND_PROGRESS']
with open(OUT/'native-render.log','w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
v=next(s for s in probe(p)['streams'] if s['codec_type']=='video');assert (int(v['nb_frames']),v['width'],v['height'],v['r_frame_rate'])==(425,1080,1920,'48/1'),v
clean();print('Native V3 credits rendered and verified.',flush=True)
parts=[]
for i in range(8):
 if i==2:q=p
 elif i in [3,4,5,6]:q=R/'analysis/v2/native'/f'part-{i:02d}.mov'
 else:q=R/'analysis/native-chunks'/f'part-{i:02d}.mov'
 assert q.is_file(),q
 parts.append(q)
lst=OUT/'concat.txt';lst.write_text(''.join("file '"+str(q)+"'\n" for q in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(lst),'-i',str(R/'assets/Mezcla-Final.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-video_track_timescale','48000','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(R/'output/AD1-Cocina-V3.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-ss',str(1012/48),'-i',str(R/'output/AD1-Cocina-V3.mp4'),'-t',str(196/48),'-c:v','libx264','-crf','17','-preset','fast','-c:a','aac','-b:a','256k','-movflags','+faststart',str(R/'output/Creditos-V3.mp4')],check=True)
print('V3 full film and focused credits preview finished.',flush=True)

from pathlib import Path
import subprocess,json,time
R=Path(__file__).resolve().parents[1]
OUT=R/'analysis/v2/native';OUT.mkdir(exist_ok=True)
CACHE=Path('/Users/alejandrorubiocamarero/Library/Caches/Adobe/After Effects/26.5')
cut=(R/'ae/v2-backup.json').stat().st_mtime;report=[];cleanups=[]
def clean():
 size=count=0
 for p in CACHE.rglob('*.aecache'):
  try:
   st=p.stat()
   if st.st_mtime>=cut:p.unlink();count+=1;size+=st.st_size
  except FileNotFoundError:pass
 cleanups.append({'files':count,'bytes':size})
 (OUT/'cache-cleanup.json').write_text(json.dumps(cleanups,indent=2))
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
clean()
parts=[]
for i in range(8):
 a=i*425;b=a+424
 if i in [0,1,7]:p=R/'analysis/native-chunks'/f'part-{i:02d}.mov';reused=True
 else:
  p=OUT/f'part-{i:02d}.mov';reused=False;started=time.monotonic()
  cmd=['/Applications/Adobe After Effects 2026/aerender','-project',str(R/'ae/Cocina-Reedicion-V2.aep'),'-rqindex','1','-s',str(a),'-e',str(b),'-output',str(p),'-mem_usage','15','35','-v','ERRORS_AND_PROGRESS']
  with open(OUT/f'part-{i:02d}.log','w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
  clean()
  print('Native V2 section',i,'rendered in',round(time.monotonic()-started,1),'s',flush=True)
 meta=probe(p);v=next(x for x in meta['streams'] if x['codec_type']=='video')
 assert (int(v['nb_frames']),v['width'],v['height'],v['r_frame_rate'])==(425,1080,1920,'48/1'),v
 parts.append(p);report.append({'section':i,'firstFrame':a,'lastFrame':b,'frames':425,'reusedUnchangedNativeSection':reused,'path':str(p)})
 (OUT/'report.json').write_text(json.dumps(report,indent=2))
lst=OUT/'concat.txt';lst.write_text(''.join("file '"+str(p)+"'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(lst),'-i',str(R/'assets/Mezcla-Final.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-video_track_timescale','48000','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(R/'output/AD1-Cocina-V2.mp4')],check=True)
print('V2 full 3400-frame MP4 finished.',flush=True)

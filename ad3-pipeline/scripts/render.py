from pathlib import Path
import subprocess,json,time,sys
R=Path(__file__).resolve().parents[1];OUT=R/'analysis/native';CACHE=Path.home()/'Library/Caches/Adobe/After Effects/26.5';cut=(R/'ae/new.json').stat().st_mtime
reports=[]
def clean():
 b=0
 for p in CACHE.rglob('*.aecache'):
  try:
   st=p.stat()
   if st.st_mtime>=cut:p.unlink();b+=st.st_size
  except FileNotFoundError:pass
 print('Released current render cache',round(b/2**30,2),'GiB',flush=True)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
parts=[int(x) for x in sys.argv[1:]] if len(sys.argv)>1 else [0,1,2,3,4]
for i in parts:
 clean();a=i*450;b=a+449;p=OUT/f'part-{i:02d}.mov';start=time.monotonic()
 cmd=['/Applications/Adobe After Effects 2026/aerender','-project',str(R/'ae/AD3-Pipeline-V1.aep'),'-rqindex','1','-s',str(a),'-e',str(b),'-output',str(p),'-mem_usage','15','35','-v','ERRORS_AND_PROGRESS']
 with open(OUT/f'part-{i:02d}.log','w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
 meta=probe(p);v=next(x for x in meta['streams'] if x['codec_type']=='video');assert (int(v['nb_frames']),v['width'],v['height'],v['r_frame_rate'])==(450,1080,1920,'48/1'),v
 reports.append({'part':i,'firstFrame':a,'lastFrame':b,'frames':450,'seconds':time.monotonic()-start,'bytes':p.stat().st_size});(OUT/f'report-{i}.json').write_text(json.dumps(reports[-1],indent=2));print('Native section',i,'verified.',flush=True)
clean()
if len(list(OUT.glob('part-*.mov')))==5:
 lst=OUT/'concat.txt';lst.write_text(''.join("file '"+str(OUT/f'part-{i:02d}.mov')+"'\n" for i in range(5)))
 subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(lst),'-i',str(R/'assets/Mezcla-Final.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-video_track_timescale','48000','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(R/'output/AD3-Pipeline-V1.mp4')],check=True)
 print('Full film encoded.',flush=True)

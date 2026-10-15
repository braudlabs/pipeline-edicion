from pathlib import Path
import subprocess,json,time,shutil,sys
V=Path(__file__).resolve().parents[1];OUT=V/'analysis/native';cut=(V/'ae/init-assets.json').stat().st_mtime;cache=Path.home()/'Library/Caches/Adobe/After Effects/26.5'
def clean():
 b=0
 for p in cache.rglob('*.aecache'):
  try:
   st=p.stat()
   if st.st_mtime>=cut:p.unlink();b+=st.st_size
  except FileNotFoundError:pass
 print('Temporary V2 cache released',round(b/2**30,2),'GiB',flush=True)
for i in ([int(v) for v in sys.argv[1:]] or list(range(5))):
 clean();a=i*450;b=a+449;p=OUT/f'part-{i:02d}.mov';start=time.monotonic()
 cmd=['/Applications/Adobe After Effects 2026/aerender','-project',str(V/'ae/AD3-Pipeline-V2.aep'),'-rqindex','1','-s',str(a),'-e',str(b),'-output',str(p),'-mem_usage','15','35','-v','ERRORS_AND_PROGRESS']
 with open(OUT/f'part-{i:02d}.log','w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
 m=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]));v=next(x for x in m['streams'] if x['codec_type']=='video');assert (int(v['nb_frames']),v['width'],v['height'],v['r_frame_rate'])==(450,1080,1920,'48/1'),v
 (OUT/f'report-{i}.json').write_text(json.dumps({'frames':[a,b],'elapsed':time.monotonic()-start,'bytes':p.stat().st_size}));print('Verified native part',i,flush=True)
clean();lst=OUT/'concat.txt';lst.write_text(''.join("file '"+str(OUT/f'part-{i:02d}.mov')+"'\n" for i in range(5)))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(lst),'-i',str(V.parent/'output/AD3-Pipeline-V1.mp4'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-video_track_timescale','48000','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(V/'output/AD3-Pipeline-V2.mp4')],check=True)
print('V2 encoded; original V1 audio stream preserved.',flush=True)

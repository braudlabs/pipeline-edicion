from pathlib import Path
import subprocess,json,time,sys
R=Path(__file__).resolve().parents[1];A=R/'analysis';CACHE=Path.home()/'Library/Caches/Adobe/After Effects/26.5';cut=(R/'ae/init.json').stat().st_mtime
P=A/'parts';P.mkdir(exist_ok=True);N=2162;STEP=144
def clean():
 total=0;names=[]
 for p in CACHE.rglob('*.aecache'):
  try:
   st=p.stat()
   if st.st_mtime>=cut:total+=st.st_size;names.append(str(p));p.unlink()
  except FileNotFoundError:pass
 with open(A/'cache-release.jsonl','a') as f:f.write(json.dumps({'bytes':total,'files':names})+'\n')
 print('V4 render cache released:',round(total/2**20),'MiB',flush=True)
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
indices=[int(s) for s in sys.argv[1:]] if len(sys.argv)>1 else list(range((N+STEP-1)//STEP))
for i in indices:
 a=i*STEP;b=min(N,a+STEP)-1;out=P/f'{i:02d}.mp4'
 if out.exists() and (P/f'{i:02d}.json').exists():continue
 clean();raw=P/f'{i:02d}.mov';beg=time.time()
 cmd=['/Applications/Adobe After Effects 2026/aerender','-project',str(R/'ae/AD3-Pipeline-V4.aep'),'-rqindex','1','-s',str(a),'-e',str(b),'-output',str(raw),'-mem_usage','15','25','-v','ERRORS_AND_PROGRESS']
 with open(P/f'{i:02d}.log','w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
 v=next(x for x in probe(raw)['streams'] if x['codec_type']=='video');assert int(v['nb_frames'])==b-a+1,(i,v)
 clean()
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-video_track_timescale','48000','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(out)],check=True)
 raw.unlink();(P/f'{i:02d}.json').write_text(json.dumps({'from':a,'toInclusive':b,'frames':b-a+1,'renderSeconds':time.time()-beg,'nativeCodec':v['codec_name']}))
 print('Verified native part',i,'frames',a,b,flush=True)
clean()
if all((P/f'{i:02d}.json').exists() for i in range((N+STEP-1)//STEP)):
 manifest=P/'concat.txt';manifest.write_text(''.join("file '"+str(P/f'{i:02d}.mp4')+"'\n" for i in range((N+STEP-1)//STEP)))
 subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-i',str(R/'assets/Mezcla-Final.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart','-video_track_timescale','48000',str(R/'output/AD3-Pipeline-V4.mp4')],check=True)
 meta=probe(R/'output/AD3-Pipeline-V4.mp4');(A/'final-probe.json').write_text(json.dumps(meta,indent=2));v=next(x for x in meta['streams'] if x['codec_type']=='video');assert int(v['nb_frames'])==N
 print('COMPLETE:',N,'frames',flush=True)

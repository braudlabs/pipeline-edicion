from pathlib import Path
import subprocess,json,time,sys
V=Path(__file__).resolve().parents[1];OUT=V/'analysis/native';OUT.mkdir(exist_ok=True)
for i in ([int(v) for v in sys.argv[1:]] or list(range(5))):
 a=i*450;b=a+449;p=OUT/f'part-{i:02d}.mov';start=time.monotonic()
 cmd=['/Applications/Adobe After Effects 2026/aerender','-project',str(V/'ae/AD3-Pipeline-V3.aep'),'-rqindex','1','-s',str(a),'-e',str(b),'-output',str(p),'-mem_usage','15','35','-v','ERRORS_AND_PROGRESS']
 with open(OUT/f'part-{i:02d}.log','w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
 m=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]));v=next(x for x in m['streams'] if x['codec_type']=='video');assert (int(v['nb_frames']),v['width'],v['height'],v['r_frame_rate'])==(450,1080,1920,'48/1'),v
 print('Verified native part',i,'seconds',round(time.monotonic()-start,1),flush=True)
ls=OUT/'concat.txt';ls.write_text(''.join("file '"+str(OUT/f'part-{i:02d}.mov')+"'\n" for i in range(5)))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(ls),'-i',str(V.parent/'output/AD3-Pipeline-V1.mp4'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-video_track_timescale','48000','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(V/'output/AD3-Pipeline-V3.mp4')],check=True)
print('V3 encoded. Original audio retained bit-for-bit.',flush=True)

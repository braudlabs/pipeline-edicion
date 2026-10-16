import pathlib,subprocess,json,numpy as np
from PIL import Image,ImageDraw
R=pathlib.Path('.');v=R/'output/AD2-La-IA-te-sale-cara-V4.mp4';D=R/'analysis/v4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(v)]));(D/'final-probe.json').write_text(json.dumps(probe,indent=2))
video=next(s for s in probe['streams'] if s['codec_type']=='video');sound=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert video['r_frame_rate']=='48/1' and int(video['nb_frames'])==3160
assert abs(float(video['duration'])-65.8333333)<1e-5
assert video['duration']==sound['duration']
def audio(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','8000','-ac','1','-f','f32le','-']),np.float32)
a=audio(v);b=audio(R/'public/assets/v3/audio-mix-master.wav');sync=[]
for t in [1,18,39,61]:
 start=t*8000;n=8000;pad=800;x=a[start-pad:start+n+pad];y=b[start:start+n];lag=int(np.argmax(np.correlate(x,y,mode='valid')))-pad;corr=float(np.corrcoef(a[start+lag:start+lag+n],y)[0,1]);sync.append({'time':t,'lag_ms':lag/8,'correlation':corr});assert lag==0 and corr>.999
(D/'sync-check.json').write_text(json.dumps(sync,indent=2))
def frame(t,w=270,h=480):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(v),'-frames:v','1','-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-']);return Image.frombytes('RGB',(w,h),raw)
times=[.4,2.35,4.8,6.6,8.6,10.2,13.4,16.2,20.2,23.5,25.6,26.9,28.4,30.5,32.1,33.2,34.5,37,38.3,39.3,39.55,40.3,41.45,42.3,43.45,44.3,48.3,50,52,54,55.8,58,59.8,62.9,64.7,65.6]
sheet=Image.new('RGB',(6*270,6*504),'#20251b');draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):x=i%6*270;y=i//6*504;sheet.paste(frame(t),(x,y));draw.text((x+8,y+484),f'{t:.2f} s',fill='white')
sheet.save(R/'output/hoja-de-revision-V4.jpg',quality=94)
# Full-size glyph crops retain the actual encoded pixels.
g=Image.new('RGB',(1080,4*210),'#20251b');dr=ImageDraw.Draw(g)
for i,t in enumerate([6.6,23.5,26.9,55.8]):
 im=frame(t,1080,1920).crop((0,230,1080,420));g.paste(im,(0,i*210));dr.text((12,i*210+194),f'{t:.2f} s · encoded glyphs, full resolution',fill='white')
g.save(D/'descenders.jpg',quality=97)
# Two rendered frames for every original frame: confirm intermediate graphic motion.
raw=subprocess.check_output(['ffmpeg','-v','error','-ss','39.2','-i',str(v),'-frames:v','20','-vf','scale=270:480','-f','rawvideo','-pix_fmt','rgb24','-']);frames=np.frombuffer(raw,np.uint8).reshape(-1,480,270,3).astype(float);diff=np.abs(np.diff(frames,axis=0)).mean(axis=(1,2,3));assert np.all(diff>.15)
(D/'qc-summary.json').write_text(json.dumps({'fps':48,'frames':3160,'duration':float(video['duration']),'sync':sync,'successive_motion_frame_mean_abs_difference':diff.tolist(),'subtitle_words':206,'face_samples':len(json.load(open(D/'faces.json'))),'preview_times':times},indent=2))
print('Passed: 3160 frames at 48 fps, exact A/V duration, zero sampled audio lag, distinct intermediate motion frames.')

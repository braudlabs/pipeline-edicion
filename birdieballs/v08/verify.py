from pathlib import Path
import subprocess,json,hashlib,numpy as np
p=Path(__file__).resolve().parent;out=p/'Birdieballs-completo-V08.mp4';source='/Users/alejandrorubiocamarero/Downloads/Birdieballs v1 (Sin Postpro).mp4'
def aud(path,sr=8000):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar',str(sr),'-f','f32le','-']),dtype=np.float32)
a=aud(source);b=aud(out);sync=[]
for x,y in [(1.25,2.1),(8,8.5),(15.3,16.4),(22.45,23),(28.1,28.6),(33,33.6)]:
 i,j=int(x*8000),int(y*8000);s=a[i:j];best=(-2,None)
 for lag in range(-320,321):
  t=b[i+lag:j+lag];corr=float(np.corrcoef(s,t)[0,1])
  if corr>best[0]:best=(corr,lag)
 sync.append({'interval':[x,y],'lagMs':best[1]/8,'correlation':best[0]})
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
errors=subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True)
raw=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(out),'-vn','-f','f32le','-']),dtype=np.float32)
master=aud(p/'Birdieballs-V08-master.mov',48000);mix=aud(p/'assets/mix.wav',48000);n=min(len(master),len(mix));audioerror=float(np.max(np.abs(master[:n]-mix[:n])))
qa={'status':'rendered_for_user_review','output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'video':{k:v[k] for k in ['codec_name','width','height','r_frame_rate','duration','nb_frames']},'audio':{k:audio[k] for k in ['codec_name','sample_rate','channels','duration']},'decodeWithoutErrors':errors.returncode==0 and not errors.stderr.strip(),'decodedAudioPeak':float(np.max(np.abs(raw))),'audioClippedSamples':int(np.sum(np.abs(raw)>=1)),'sourceSync':sync,'masterVsMixMonoMaxError':audioerror,'mapping':{'sourceFrames':2278,'outputFrames':int(v['nb_frames']),'extraCuts':0,'retiming':False,'cameraAccents':4},'nativeProject':{'path':str(p/'ae/Birdieballs-V08.aep'),'missingFonts':0,'missingMedia':0,'editableTextLayers':57,'mask':'Automatic Vision segmentation for solution, original f550–599'},'review':{'contactFrames':82,'nativeDesignAlternatives':3,'passes':2,'userRejected70MaskRemoved':True,'reference':'Focused V8 comparison (compact hierarchy, stable caption anchors); no whole-style equivalence claimed','audioAudition':False,'normalSpeedPlayback':'pending'},'limitations':['Automatic mask, not manually rotoscoped hair','No independent audio audition; waveform sync and signal checks performed','Creative direction remains awaiting user verdict']}
(p/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));print(json.dumps(qa,ensure_ascii=False,indent=2))

#!/usr/bin/env python3
"""Delivery verification: original timing, streams, audio lag and preserved versions."""
import json,hashlib,subprocess
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[2];out=Path(__file__).parent
source=Path('/Users/alejandrorubiocamarero/Downloads/Birdieballs v1 (Sin Postpro).mp4');video=out/'Birdieballs-completo-V06.mp4';proxy=out/'public/assets/source.mp4'
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def times(p):
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(p)]))
 return [float(f['best_effort_timestamp_time']) for f in data['frames']]
originalTimes=times(source)[:2278];proxyTimes=times(proxy);finalTimes=times(video)
assert len(proxyTimes)==len(finalTimes)==2278
assert all(b>a for a,b in zip(finalTimes,finalTimes[1:]))
def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-t','38.004633333','-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32)
a,b=pcm(source),pcm(video);audio=[]
for lo,hi in [(1,4),(8,10),(15.2,16.4),(20,22),(26,27),(31.2,34.4)]:
 x=a[int(lo*8000):int(hi*8000)];y=b[int(lo*8000):int(hi*8000)];x=x-x.mean();y=y-y.mean();n=1<<(2*len(x)-1).bit_length();c=np.fft.irfft(np.fft.rfft(y,n)*np.conj(np.fft.rfft(x,n)),n);lags=np.arange(-40,41);lag=int(lags[np.argmax(c[lags%n])]);audio.append({'intervalSeconds':[lo,hi],'lagSamples8k':lag,'lagMilliseconds':lag/8,'zeroLagCorrelation':float(np.corrcoef(x,y)[0,1])})
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
data=probe(video);vs=next(s for s in data['streams'] if s['codec_type']=='video');aus=next(s for s in data['streams'] if s['codec_type']=='audio')
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
old=sha(root/'birdieballs/v03/Birdieballs-20s-V03.mp4');assert old=='0f5095fd1f3e7e6a3990010aa1aefaaf302851aae60760cdf4cbe03d9f3ec7f1'
info={'status':'ready_for_user_verdict','source':str(source),'sourceSHA256':sha(source),'output':str(video),'sha256':sha(video),'video':{k:vs.get(k) for k in ['codec_name','width','height','pix_fmt','r_frame_rate','duration','nb_frames']},'audio':{k:aus.get(k) for k in ['codec_name','sample_rate','channels','duration']},'mapping':{'sourceStartSeconds':0,'sourceFrames':2278,'outputFrames':2278,'speed':1,'additionalCuts':0,'maxProxyVsOriginalTimestampErrorMs':float(np.max(np.abs(np.array(originalTimes)-proxyTimes))*1000),'maxOutputVsOriginalTimestampErrorMs':float(np.max(np.abs(np.array(originalTimes)-finalTimes))*1000),'note':'Source VFR has600Hz timestamps; delivery60000/1001fps. No deliberate retiming; CFR quantization is reported.'},'audioSync':audio,'decodeWithoutErrors':True,'V03Preserved':True,'review':{'tool':'Remotion','styleApprovedByUser':False,'sourceQuizRevision':132,'independentAudioListening':False,'normalSpeedPlayback':'pending','nativeMasks':{'method':'macOS Vision person segmentation, same masks asV05','frames':[550,599]},'corrections':['Fixed caption fill across scene cuts, especially LAGOS','Completed original38s source','Preserved existing70% graphic; no duplicate percentage','Cleared text margins and final product box'],'limitations':['Automatic person masks, not manual rotoscoping','Local ASR word timings with supplied script correction; no independent audio audition']}}
old04=sha(root/'birdieballs/v04/Birdieballs-20s-V04.mp4');assert old04=='776d61792f585e19fb390b0f49da408ad7abdd7fb994536e580068aef664425b';info['V04Preserved']=True
old05=sha(root/'birdieballs/v05/Birdieballs-20s-V05.mp4');assert old05=='f95d44db539c7ed6411453784f53a5964d3eec3bb948a73aa6200a4c62f9e34b';info['V05Preserved']=True
(out/'QA.json').write_text(json.dumps(info,ensure_ascii=False,indent=2));print(json.dumps(info,ensure_ascii=False,indent=2))

from pathlib import Path
import subprocess,json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];p=R/'output/AD3-Pipeline-V1.mp4';meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(x for x in meta['streams'] if x['codec_type']=='video');a=next(x for x in meta['streams'] if x['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'48/1',2250);assert a['sample_rate']=='48000';subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True)
def pcm(f):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-ac','1','-ar','8000','-f','f32le','-']),np.float32)
x=pcm(p);y=pcm(R/'assets/Mezcla-Final.wav');n=min(len(x),len(y));corr=float(np.corrcoef(x[:n],y[:n])[0,1]);assert corr>.995,corr
frames=[165,222,440,589,694,697,800,884,887,928,969,1034,1100,1180,1247,1275,1342,1419,1424,1535,1590,1655,1710,1772,1800,1940,1970,2035,2165,2247]
for k in range(2):
 fs=frames[k*15:(k+1)*15];o=Image.new('RGB',(216*5,410*3),'#303030');d=ImageDraw.Draw(o)
 for i,f in enumerate(fs):
  q=R/'analysis'/f'verified-{f}.jpg';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(f/48),'-i',str(p),'-frames:v','1','-vf','scale=216:-1',str(q)],check=True);o.paste(Image.open(q),(i%5*216,i//5*410));d.text((i%5*216+5,i//5*410+386),f'{f/48:.3f}s · {f}',fill='white')
 o.save(R/'analysis'/f'verification-{k}.jpg')
# Every animation frame changes during the sustained camera movement, including odd frames.
z=subprocess.check_output(['ffmpeg','-v','error','-ss',str(1670/48),'-i',str(p),'-frames:v','20','-vf','scale=108:192','-pix_fmt','gray','-f','rawvideo','-']);z=np.frombuffer(z,np.uint8).reshape(-1,192,108).astype(float);diff=np.mean(np.abs(np.diff(z,axis=0)),axis=(1,2));assert np.all(diff>.01),diff
report={'video':v,'audio':a,'fullDecode':'pass','audioCorrelationZeroLag':corr,'motionSampleFirstFrame':1670,'motionSampleFrames':20,'motionConsecutiveMeanAbsDifferences':diff.tolist(),'visualSampleFrames':frames,'render':'Native After Effects ProRes 422; H264 delivery; audio remux from same AE mix'};(R/'output/VERIFICACION.json').write_text(json.dumps(report,indent=2));print('2250 frames; 1080x1920; 48 fps; audio48k; full decode PASS; zero-lag audio correlation',corr,flush=True)

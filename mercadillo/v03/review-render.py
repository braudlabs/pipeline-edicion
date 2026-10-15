from pathlib import Path
import json,subprocess,numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;out=R/'stills'/'render';out.mkdir(exist_ok=True)
groups={'first-join':list(range(144,163)),'pelillos':list(range(304,313))+list(range(345,358)),'grandma-in':list(range(1126,1141)),'grandma-ya':list(range(1200,1224,2)),'evidentemente':list(range(1285,1302))}
frames=sorted(set(sum(groups.values(),[])));sel='+'.join(f'eq(n,{f})' for f in frames)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/'Mercadillo-V03-master.mov'),'-vf',f"select='{sel}',scale=216:384",'-fps_mode','vfr',str(out/'%04d.jpg')],check=True)
refs={f:out/f'{i+1:04d}.jpg' for i,f in enumerate(frames)}
for name,fs in groups.items():
 for k in range(0,len(fs),12):
  xs=fs[k:k+12];img=Image.new('RGB',(1296,814),'#161616');d=ImageDraw.Draw(img)
  for i,f in enumerate(xs):
   x=i%6*216;y=i//6*407;img.paste(Image.open(refs[f]),(x,y));d.text((x+3,y+387),f'{f} / {f/24:.3f}s',fill='white')
  img.save(out/f'{name}-{k//12+1}.jpg')
def pcm(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','48000','-ac','2','-f','s16le','-'])
a=pcm(R/'assets/mix.wav');b=pcm(R/'Mercadillo-V03-master.mov');z=np.frombuffer(b,np.int16).astype(np.float32)
qa={'audioMatchesMixByteForByte':a==b,'audioFrames':len(z)//2,'peak':float(abs(z).max()/32768),'clippedSamples':int((abs(z)>=32767).sum()),'reviewFrameGroups':groups,'actualVideoProbe':json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,nb_frames,avg_frame_rate,width,height,duration','-of','json',str(R/'Mercadillo-V03-master.mov')]))}
(R/'QA-render.json').write_text(json.dumps(qa,indent=2));print({k:v for k,v in qa.items() if k not in ['actualVideoProbe','reviewFrameGroups']});assert a==b

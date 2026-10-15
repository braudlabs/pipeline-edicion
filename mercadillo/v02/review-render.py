from pathlib import Path
import json, subprocess, numpy as np
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parent
out=R/'stills'/'motion-final';out.mkdir(exist_ok=True)
groups={'hook':list(range(0,38,2)),'grandma':list(range(1162,1261,3)),'criterion':list(range(1352,1418,3))}
frames=sorted(set(sum(groups.values(),[])))
select='+'.join(f'eq(n,{f})' for f in frames)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/'Mercadillo-V02-master.mov'),'-vf',f"select='{select}',scale=270:480",'-fps_mode','vfr',str(out/'%04d.jpg')],check=True)
byframe={f:out/f'{i+1:04d}.jpg' for i,f in enumerate(frames)}
for name,fs in groups.items():
 for k in range(0,len(fs),12):
  chunk=fs[k:k+12];img=Image.new('RGB',(1620,1010),'#181818');d=ImageDraw.Draw(img)
  for i,f in enumerate(chunk):
   x=i%6*270;y=i//6*505;img.paste(Image.open(byframe[f]),(x,y));d.text((x+4,y+482),f'f{f}  {f/24:.3f}s',fill='white')
  img.save(out/f'{name}-{k//12+1}.jpg')
def pcm(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','48000','-ac','2','-f','s16le','-'])
a=pcm(R/'mix.wav');b=pcm(R/'Mercadillo-V02-master.mov');av=np.frombuffer(a,np.int16).astype(np.float32);bv=np.frombuffer(b,np.int16).astype(np.float32)
report={'masterAudioByteIdenticalToMixSpec':a==b,'audioFrames':len(bv)//2,'peak':float(np.max(np.abs(bv)))/32768,'clippedSamples':int(np.sum(np.abs(bv)>=32767)),'audioDifferenceMaxLSB':float(np.max(np.abs(av-bv))) if len(av)==len(bv) else None,'reviewSheets':groups}
(R/'QA-render.json').write_text(json.dumps(report,indent=2));print(report)

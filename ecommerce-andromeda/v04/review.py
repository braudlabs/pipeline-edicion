from pathlib import Path
import json,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent
E=json.loads((p/'choreography.json').read_text());prev=json.loads((p.parent/'v03/choreography.json').read_text())
assert [(w['text'],w['frame']) for e in E for w in e['sourceWords']]==[(w['text'],w['frame']) for e in prev if e['cue']!='c31' for w in e['sourceWords']]
assert not any(e['start']<741 and e['end']>692 for e in E)
assert {e['cue'] for e in E if e['motion']=='occlusion'}=={'c05','c09','c33'}
assert (p/'public/assets/mix-preview.wav').read_bytes()==(p.parent/'v03/public/assets/mix-preview.wav').read_bytes()
f=p/'Andromeda-00-38s-V04-PREVIEW.mp4';probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_frames','-show_entries','format=duration','-of','json',str(f)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');assert (v['width'],v['height'],v['nb_frames'],v['r_frame_rate'])==(1080,1920,'1840','48/1')
frames=[184,461,1277,1383,1384,1430,1481,1482,1534]
expr='+'.join('eq(n\\,%d)'%n for n in frames)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf',f'select={expr},scale=540:960','-fps_mode','passthrough',str(p/'stills/check-%02d.png')],check=True)
r=[];b=Image.new('RGB',(1620,1920),'#172028');draw=ImageDraw.Draw(b)
for i,n in enumerate(frames):
 im=Image.open(p/f'stills/check-{i+1:02}.png').convert('RGB');a=np.asarray(im,dtype=np.float32);spread=float(np.mean(a.max(axis=2)-a.min(axis=2)))
 if 1384<=n<1482:assert spread<3,spread # <1.2% full scale: allows RGB/YUV quantization on neutral gray
 else:assert spread>8,spread
 r.append({'frame':n,'meanChannelSpread':spread,'monochromeExpected':1384<=n<1482})
 im.thumbnail((405,720));x=(i%4)*405;y=(i//4)*640;im=im.resize((340,604));b.paste(im,(x,y+25));draw.text((x+6,y+6),f'{n/48:.3f}s / f{n}',fill='white')
b=b.crop((0,0,1620,1920));b.save(p/'study/review-board.jpg')
def pcm(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ar','48000','-ac','1','-f','f32le','-']),np.float32)
a=pcm(f);b=pcm(p/'public/assets/mix-preview.wav');ac=[]
for t in [2,29]:
 x=a[t*48000:(t+1)*48000].astype(float);y=b[t*48000:(t+1)*48000].astype(float);cc=np.fft.irfft(np.fft.rfft(x,131072)*np.conj(np.fft.rfft(y,131072)));lag=max(range(-96,97),key=lambda k:cc[k%131072]);cor=float(np.corrcoef(x,y)[0,1]);assert lag==0 and cor>.98;ac.append({'seconds':t,'lagSamples':lag,'correlation':cor})
q={'render':probe,'retainedContourMoments':3,'subtitleWords':112,'intentionalOmissionWords':7,'gagCaptionOverlap':False,'monochromePixelChecks':r,'audioMixIdenticalToV03':True,'encodedAudioChecks':ac,'visualReview':'selected frames and both boundaries; not full playback or listening','userApproved':False};(p/'QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2));print(json.dumps(q,indent=2))

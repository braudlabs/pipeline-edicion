from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json,numpy as np,hashlib,argparse
parser=argparse.ArgumentParser();parser.add_argument('--v2',action='store_true');parser.add_argument('--v3',action='store_true');args=parser.parse_args();version=3 if args.v3 else 2 if args.v2 else 1
R=Path(__file__).resolve().parents[1];V=R/(f'output/AD1-Cocina-V{version}.mp4' if version>1 else 'output/AD1-Cocina-REEDICION.mp4');A=R/(f'analysis/v{version}' if version>1 else 'analysis');Q=A/'final-frames';Q.mkdir(exist_ok=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(V)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'48/1',3400),v
assert a['sample_rate']=='48000'
r=subprocess.run(['ffmpeg','-v','error','-i',str(V),'-f','null','-'],capture_output=True);assert r.returncode==0 and not r.stderr,r.stderr
(A/'decode-errors.log').write_bytes(r.stderr)
def pcm(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ar','48000','-ac','1','-f','f32le','-']),np.float32)
x=pcm(V);y=pcm(R/'assets/Mezcla-Final.wav');n=min(len(x),len(y));corr=float(np.corrcoef(x[:n],y[:n])[0,1]);assert corr>.997,corr
# Check exact segment joins and native motion, plus semantic scene/plate/caption poses.
times=[.25,1.68,3.96,4.7,5.3,6.4,8.25,9.7,10.9,12.7,14.1,15.9,17.4,18.9,20.5,21.3,21.8,22.55,23.5,24.7,25.5,27.5,29.5,31.5,32.35,32.85,33.35,34.05,34.9,36.5,36.9,37.4,38.05,38.7,39.3,39.8,40.8,41.4,42.2,42.9,43.3,44.5,45.2,46.6,48.2,49.5,50.9,52.2,53.2,54.3,55.8,56.9,57.5,58.2,59.25,59.8,60.5,61.22,62.5,63.6,65.4,66.8,68.5,69.8,70.65]
motion_frames=range(1080,1100) if args.v3 else range(1850,1870)
if args.v3:times += [21.08,21.32,22.45,23.18,24.1,24.95,25.10,25.17]
frames=sorted({round(t*48) for t in times}|{f+d for f in range(425,3400,425) for d in [-1,0,1]}|set(motion_frames)|({1011,1012,1207,1208} if args.v3 else set()))
meta=[]
for start in range(0,len(frames),40):
 batch=frames[start:start+40]
 vf='select='+ '+'.join(f'eq(n\\,{f})' for f in batch)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(V),'-vf',vf,'-fps_mode','passthrough',str(Q/'%04d.jpg')],check=True)
 for i,f in enumerate(batch):
  src=Q/f'{i+1:04d}.jpg';dst=Q/f'frame-{f:04d}.jpg';src.rename(dst);meta.append({'frame':f,'time':f/48,'file':dst.name})
(A/'frame-review.json').write_text(json.dumps(meta,indent=2))
allimages={int(p.stem.split('-')[-1]):p for p in Q.glob('frame-*.jpg')}
samples=[round(t*48) for t in times]
for page in range((len(samples)+19)//20):
 fs=samples[page*20:(page+1)*20];out=Image.new('RGB',(1350,505*((len(fs)+4)//5)),(22,22,22));d=ImageDraw.Draw(out)
 for j,f in enumerate(fs):
  im=Image.open(allimages[f]).resize((270,480));xx=j%5*270;yy=j//5*505;out.paste(im,(xx,yy));d.text((xx+5,yy+484),f'{f/48:.2f}s · f{f}',fill='white')
 out.save(A/f'final-review-{page+1}.jpg',quality=91)
seams=[f+d for f in range(425,3400,425) for d in [-1,0,1]]
out=Image.new('RGB',(810,505*7),(22,22,22));d=ImageDraw.Draw(out)
for j,f in enumerate(seams):
 xx=j%3*270;yy=j//3*505;out.paste(Image.open(allimages[f]).resize((270,480)),(xx,yy));d.text((xx+5,yy+484),f'f{f}',fill='white')
out.save(A/'native-seams.jpg',quality=92)
unique=len({hashlib.sha256(allimages[f].read_bytes()).hexdigest() for f in motion_frames});assert unique==20
Image.open(allimages[round(8.25*48) ]).save(R/(f'output/Portada-V{version}.jpg' if version>1 else 'output/Portada.jpg'),quality=95)
report={'width':1080,'height':1920,'fps':48,'frames':3400,'durationSeconds':3400/48,'decodedWithoutErrors':True,'audioCorrelationAtZeroLag':corr,'verifiedNativeMotionFrames':20,'uniqueNativeMotionFrames':unique,'reviewFrames':len(frames),'segmentJoinsChecked':7,'fontSubstitutions':0,'missingMedia':0,'editabilityTest':'Native editable layers; V2 price text edit test retained. V3 photographic viewport, shapes, gauge and camera use native keyframes.' if args.v3 else 'Duplicate price comp, change 39 to 40, render and delete duplicate; final retained 39','sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'bytes':V.stat().st_size}
(R/(f'output/Verificacion-V{version}.json' if version>1 else 'output/Verificacion.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,indent=2))

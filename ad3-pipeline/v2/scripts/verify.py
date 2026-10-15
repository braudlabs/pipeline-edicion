from pathlib import Path
import subprocess, json, hashlib, re
from PIL import Image, ImageDraw

V=Path(__file__).resolve().parents[1]
F=V/'output/AD3-Pipeline-V2.mp4'
F1=V.parent/'output/AD3-Pipeline-V1.mp4'
Q=V/'analysis/final';Q.mkdir(exist_ok=True)
def run(cmd):return subprocess.check_output(cmd,stderr=subprocess.STDOUT)
def sha(p):return hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()
m=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(F)]))
s=next(s for s in m['streams'] if s['codec_type']=='video')
assert (s['width'],s['height'],s['r_frame_rate'],int(s['nb_frames']))==(1080,1920,'48/1',2250),s
assert abs(float(m['format']['duration'])-46.875)<0.1,m['format']
decode=run(['ffmpeg','-v','error','-i',str(F),'-f','null','-'])
assert not decode,decode
def audio_hash(p):return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(p),'-vn','-c:a','copy','-f','adts','-'])).hexdigest()
audio=[audio_hash(p) for p in [F1,F]]
assert audio[0]==audio[1],audio
assert sha(F1)=='41ff0592942f76537456db5a497b0f127d5a7e09e7c6f43d93eca1cdcc37d50b'
times=[15.4,16.4,17.7,18.42,19.99,20.98,21.7,26.2,27.1,28.1,29.55,34.3,35.5,36.8,40.8,41.8,43.8]
sheet=Image.new('RGB',(5*216,4*409),(15,24,27));draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 p=Q/f'{t:.2f}.png';run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(F),'-frames:v','1','-update','1',str(p)])
 im=Image.open(p).convert('RGB');im.thumbnail((216,384));x=(i%5)*216;y=(i//5)*409;sheet.paste(im,(x,y));draw.text((x+8,y+389),f'{t:.2f} s',fill='white')
sheet.save(Q/'contacto.jpg',quality=94)
seq=run(['ffmpeg','-v','error','-ss',str(1660/48),'-i',str(F),'-frames:v','24','-an','-f','framemd5','-']).decode()
hashes=[l.rsplit(',',1)[-1].strip() for l in seq.splitlines() if not l.startswith('#') and l.strip()]
assert len(set(hashes))==24,hashes
comparisons={}
for t in [3,10,23.5,31,44]:
 result=run(['ffmpeg','-hide_banner','-ss',str(t),'-i',str(F1),'-ss',str(t),'-i',str(F),'-filter_complex','[0:v][1:v]ssim','-frames:v','1','-an','-f','null','-']).decode()
 match=re.search(r'All:([\d.]+)',result);comparisons[str(t)]=float(match.group(1)) if match else result[-300:]
report={'format':{'width':1080,'height':1920,'fps':48,'frames':2250,'duration':float(m['format']['duration'])},'decodeErrors':0,'videoSha256':sha(F),'V1Unchanged':True,'audioBitstreamIdentical':True,'audioSha256':audio[1],'motionSampleUniqueFrames':len(set(hashes)),'unchangedSectionsSSIM':comparisons,'visualInspection':'Native frames and frame sequences inspected; final MP4 contact sheet and browser spot playback. Not a full audio listening pass.'}
(Q/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,indent=2))

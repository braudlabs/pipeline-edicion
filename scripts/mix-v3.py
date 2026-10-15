"""Rebuild the mix on the tightened V3 timeline, preserving original voice pitch."""
import subprocess,json,pathlib,numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];A=ROOT/'public/assets';V=A/'v3';S=A/'v2';SR=48000
T=json.load(open(ROOT/'src/timing-v3.json'));EDL=json.load(open(ROOT/'src/edl-v3.json'));N=T['duration']*2000
def decode(p,af=None,start=None):
 c=['ffmpeg','-v','error']
 if start is not None:c+=['-ss',str(start)]
 c+=['-i',str(p)]
 if af:c+=['-af',af]
 c+=['-ar',str(SR),'-ac','2','-f','f32le','-']
 return np.frombuffer(subprocess.check_output(c),np.float32).reshape(-1,2).copy()
def write(name,x):subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-c:a','pcm_s24le',str(V/name)],input=x.astype(np.float32).tobytes(),check=True)
voice=decode(V/'voice.wav');music=decode(S/'music-tech-house-vibes.mp3','highpass=f=70,lowpass=f=9500,equalizer=f=2400:t=q:w=0.8:g=-4',8)[:N]
rms=np.sqrt(np.mean(np.pad(voice,((0,(-N)%480),(0,0))).reshape(-1,480,2)**2,axis=(1,2)));duck=[];g=1
for r in rms:
 target=.5 if r>.012 else 1;g+=(.4 if target<g else .03)*(target-g);duck.append(g)
t=np.arange(N)/SR;env=np.interp(np.arange(N),np.arange(len(duck))*480,duck);fade=np.clip(t/.12,0,1)*np.clip((N/SR-t)/.65,0,1)
bed=music*(.23*env*fade)[:,None];sfx=np.zeros_like(voice)
E=T['events'];events=[('whoosh-short',E['hand']['from']/24-.06,.10),('glitch-3',E['label']['from']/24,.06),('click-soft',E['generation']['from']/24,.10),('whoosh-short',E['cost']['from']/24+.45,.09),('click-soft',E['process']['from']/24+.4,.10),('whoosh-short',E['accounts']['from']/24-.05,.09),('whoosh-short',(E['accounts']['from']+36)/24,.12),('click-soft',(E['accounts']['from']+60)/24,.10),('whoosh-short',(E['accounts']['from']+84)/24,.11),('whoosh-short',(E['accounts']['from']+131)/24,.12),('click-soft',(E['accounts']['from']+154)/24,.10),('impact-bass-1',E['brand']['from']/24,.11),('pop',E['price']['from']/24,.08)]
for name,start,gain in events:
 x=decode(S/f'{name}.mp3')[:int((.3 if name=='glitch-3' else 1.8)*SR)];x[-600:]*=np.linspace(1,0,600)[:,None];a=round(start*SR);b=min(N,a+len(x));sfx[a:b]+=gain*x[:b-a]
write('music-bed.wav',bed);write('sound-design.wav',sfx);write('audio-mix-premaster.wav',voice+bed+sfx)
cmd=['ffmpeg','-hide_banner','-i',str(V/'audio-mix-premaster.wav'),'-af','loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json','-f','null','-'];r=subprocess.run(cmd,capture_output=True,text=True);text=r.stderr;stats=json.loads(text[text.rfind('{'):text.rfind('}')+1]);(ROOT/'analysis/v3/loudnorm.json').write_text(json.dumps(stats,indent=2))
af=f"loudnorm=I=-14:TP=-1.5:LRA=9:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:linear=true,aresample=48000,apad,atrim=end_sample={N}"
subprocess.run(['ffmpeg','-v','error','-y','-i',str(V/'audio-mix-premaster.wav'),'-af',af,'-ar','48000','-c:a','pcm_s24le',str(V/'audio-mix-master.wav')],check=True)
print('Mix mastered:',N,'samples; music ducked; 13 motion accents.')

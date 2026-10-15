from pathlib import Path
import numpy as np,subprocess,wave,json
R=Path(__file__).resolve().parents[2];D=json.loads((R/'src/v3/edit-map.json').read_text())['duration'];sr=48000;N=round(D*sr)
def read(p,filter=None):
 cmd=['ffmpeg','-v','error','-i',str(p)]
 if filter:cmd+=['-af',filter]
 return np.frombuffer(subprocess.check_output(cmd+['-f','f32le','-ac','2','-ar',str(sr),'-']),np.float32).reshape(-1,2).copy()
def save(p,a):
 with wave.open(str(p),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
v=read(R/'assets/v3/Voice.wav')[:N];v=np.pad(v,((0,max(0,N-len(v))),(0,0)))
m=read(R/'assets/music-tech-house-vibes.mp3','atrim=start=8,asetpts=PTS-STARTPTS,highpass=f=75,equalizer=f=1800:t=q:w=0.8:g=-5')[:N]
m=m/max(.01,np.sqrt(np.mean(m*m)))*.04
# Voice-led ducking, with a smooth control envelope.
block=480;env=np.array([np.sqrt(np.mean(v[i:i+block]**2)) for i in range(0,N,block)]);env=np.convolve(env,np.ones(25)/25,'same');gain=np.interp(np.arange(N),np.arange(len(env))*block,np.where(env>.025,.68,1.0));m*=gain[:,None]
m[:12000]*=np.linspace(0,1,12000)[:,None];k=round(1.3*sr);m[-k:]*=(.5+.5*np.cos(np.linspace(0,np.pi,k)))[:,None]
fx=np.zeros((N,2),np.float32);cues=[]
def add(name,t,peak,dur=None):
 a=read(R/'assets'/(name+'.mp3'))
 if dur:a=a[:round(sr*dur)]
 a=a/max(.001,np.max(np.abs(a)))*peak;j=round(t*sr);cnt=min(len(a),N-j)
 if cnt>0:fx[j:j+cnt]+=a[:cnt]
 cues.append([name,t,peak])
for t in [0,2.65,4.18,5.18,6.3,9.35,11.05,15.1,16.45,19,20.56,22.55,24.58,27.98,29.9,31.1,32.68,35.95,36.73,39.9,40.6,41.32,42.48,43.52,44.96]:add('whoosh-short',max(0,t-.09),.10,.4)
for t in [9.16,14.16,26.60,28.88,31.15,35.96]:add('click-soft',t,.18,.18)
for t in [7.70,7.89,8.08,8.27,8.46,8.65,8.84,9.03]:add('key-press',t,.035,.11)
for t in [15.4,15.47,15.54,15.61,15.68,17.10,17.68,25.9,31.32,31.38,31.44]:add('click-soft',t,.055,.09)
add('ping',28.9,.13,.65);add('chime',44.96,.10,1.2)
save(R/'assets/v3/Music.wav',m);save(R/'assets/v3/SFX.wav',fx);save(R/'assets/v3/Premaster.wav',v+m+fx)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(R/'assets/v3/Premaster.wav'),'-af','loudnorm=I=-15:TP=-1.5:LRA=8','-ar','48000',str(R/'assets/v3/Mix.wav')],check=True)
(R/'src/v3/sound-cues.json').write_text(json.dumps(cues,indent=2))
print('V3 mix',D)

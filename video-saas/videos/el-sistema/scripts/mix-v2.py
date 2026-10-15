from pathlib import Path
import wave,numpy as np,subprocess,json
from retime import T,D
R=Path(__file__).resolve().parents[1];sr=48000;N=round(D*sr)
def read(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ac','2','-ar',str(sr),'-']),np.float32).reshape(-1,2).copy()
def save(p,a):
 with wave.open(str(p),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
voice=read(R/'assets/Voz-V2.wav');music=read(R/'assets/Musica.wav')[:N]*1.15;fx=np.zeros((N,2),np.float32)
fade=round(2*sr);music[-fade:]*=(.5+.5*np.cos(np.linspace(0,np.pi,fade)))[:,None]
cues=json.loads((R/'src/sound-cues.json').read_text())
for q in cues:
 q[1]={14.03:13.65,14.11:13.91,18.35:19.02}.get(q[1],q[1])
for s,t,g in cues:
 a=read(R/'assets'/(s+'.mp3'))*g;j=round(T(t)*sr);count=min(N-j,len(a));fx[j:j+count]+=a[:count]
fade=round(.4*sr);fx[-fade:]*=np.linspace(1,0,fade)[:,None]
save(R/'assets/Efectos-V2.wav',fx);save(R/'assets/Musica-V2.wav',music);save(R/'assets/Premaster-V2.wav',voice[:N]+music+fx)
(R/'src/sound-cues-v2.json').write_text(json.dumps([(s,T(t),g) for s,t,g in cues],indent=2))
subprocess.run(['ffmpeg','-y','-v','error','-i',str(R/'assets/Premaster-V2.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000',str(R/'assets/Mezcla-V2-final.wav')],check=True)
print('Final mix with tail fade ready')

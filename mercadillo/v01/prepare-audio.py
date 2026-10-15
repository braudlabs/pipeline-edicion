"""Build source dialogue/foley stem; Remotion places music and graphics separately."""
from pathlib import Path
import numpy as np
import json, subprocess, wave
p=Path(__file__).parent
assets=p/'public/assets'
inputs=json.loads((p/'inputs.json').read_text())
rate=48000
def decode(path):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ar',str(rate),'-ac','2','-f','f32le','-'])
    return np.frombuffer(raw,dtype=np.float32).reshape(-1,2).copy()
def write(path,data):
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate)
        w.writeframes((np.clip(data,-1,1)*32767).astype('<i2').tobytes())
stems=[]
gains=[]
for c in inputs['clips']:
    n=c['numero'];length=c['duracion_frames']*2000
    raw=decode(assets/Path(c['archivo']).name)
    raw=np.pad(raw,((0,max(0,length-len(raw))),(0,0)))[:length]
    db=0 if n in [1,2,3,11,12] else -3 if n==4 else -6
    raw*=10**(db/20)
    # A short edge taper on distinct shots; Extend seams retain continuity.
    if n not in [1,2,3,10,11]:
        edge=240;raw[:edge]*=np.linspace(0,1,edge)[:,None];raw[-edge:]*=np.linspace(1,0,edge)[:,None]
    stems.append(raw);gains.append({'clip':n,'gainDb':db,'samples':length})
native=np.concatenate(stems)
vo=decode(assets/'narrator.wav');assert len(vo)==len(native)==2121*2000
base=native+vo
peak=float(abs(base).max());gain=min(1,.79/peak);base*=gain
write(assets/'dialogue-foley.wav',base)
# Gentle voice-band carve applied to the chosen instrumental, without changing tempo.
subprocess.run(['ffmpeg','-v','error','-i',str(assets/'funky-martian.mp3'),'-af','highpass=f=45,equalizer=f=2300:t=q:w=0.9:g=-3,lowpass=f=13000','-ar',str(rate),'-c:a','pcm_s16le','-y',str(assets/'music.wav')],check=True)
# Original short air/low percussion cues: no extracted audio from references.
rng=np.random.default_rng(21)
for name,duration,kind in [('air',.24,'air'),('tap',.13,'tap'),('resolve',.32,'resolve')]:
    t=np.arange(round(duration*rate))/rate
    if kind=='air':
        noise=rng.normal(0,1,len(t));smooth=np.convolve(noise,np.ones(9)/9,'same');envelope=np.sin(np.pi*t/duration)**2
        a=(noise-smooth)*envelope*.07
    else:
        f=105 if kind=='tap' else 78
        phase=2*np.pi*(f*t+30*(1-np.exp(-t*25))/25)
        a=.2*np.sin(phase)*np.exp(-t*(40 if kind=='tap' else 18))
        a+=rng.normal(0,1,len(t))*.023*np.exp(-t*70)
        a*=np.minimum(t/.002,1)
    write(assets/(name+'.wav'),np.stack([a,a],axis=1))
(p/'study/audio-preparation.json').write_text(json.dumps({'nativeGains':gains,'baseGain':gain,'basePeakBeforeGain':peak,'samples':len(base),'duration':len(base)/rate,'music':'Funky Martian — Michael Ramir C., Mixkit 1029','musicProcessing':'45Hz HP, 2.3kHz -3dB carve, 13kHz LP; no speed change','sfx':'Three original procedural air/percussion transients; source foley retained','independentListening':False},indent=2))
print('Dialogue/foley, instrumental and original transients prepared')

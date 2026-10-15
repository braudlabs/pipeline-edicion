"""Render the music automation and selected transition accents to frozen stems.
The voice has no time change. All arrays share exactly 3,530,000 samples.
"""
import subprocess,json,pathlib,numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
A=ROOT/'public/assets'; V=A/'v2'; SR=48000; N=3530000
def decode(path,filters=None,start=None):
    cmd=['ffmpeg','-v','error']
    if start is not None:cmd+=['-ss',str(start)]
    cmd+=['-i',str(path)]
    if filters:cmd+=['-af',filters]
    cmd+=['-ar',str(SR),'-ac','2','-f','f32le','-']
    return np.frombuffer(subprocess.check_output(cmd),np.float32).reshape(-1,2).copy()
def length(x):return np.pad(x[:N],((0,max(0,N-len(x))),(0,0)))
def write(path,x):
    p=subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-c:a','pcm_s24le',str(path)],input=x.astype(np.float32).tobytes(),check=True)
voice=length(decode(A/'narration-master.wav'))
music=length(decode(V/'music-tech-house-vibes.mp3','highpass=f=70,lowpass=f=9500,equalizer=f=2400:t=q:w=0.8:g=-4',start=8))
# An envelope-driven duck with a fast attack and 300 ms release keeps consonants clear.
hop=480
pad=np.pad(voice,((0,(-N)%hop),(0,0)))
rms=np.sqrt(np.mean(pad.reshape(-1,hop,2)**2,axis=(1,2)))
duck=[];g=1.0
for r in rms:
    target=.50 if r>.012 else 1.0
    k=.40 if target<g else .030
    g+=k*(target-g);duck.append(g)
t=np.arange(N)/SR
envelope=np.interp(np.arange(N),np.arange(len(duck))*hop,duck)
automation=np.ones(N)
for a,b,gain in [(13.4,17.12,1.12),(20.19,22.12,1.14),(44.33,50.375,1.18),(52.73,54.417,1.14),(71.79,73.54,1.08)]:
    ramp=np.minimum(np.clip((t-a)/.20,0,1),np.clip((b-t)/.25,0,1));automation*=1+(gain-1)*ramp
fade=np.clip(t/.22,0,1)*np.clip((N/SR-t)/.8,0,1)
bed=music*(.23*envelope*automation*fade)[:,None]
sfx=np.zeros_like(voice)
events=[('whoosh-short',2.30,.12),('click-soft',11.10,.16),('click-soft',12.72,.15),('glitch-3',13.39,.075),('click-soft',14.70,.10),('whoosh-short',15.39,.12),('whoosh-short',20.07,.12),('whoosh-short',20.64,.11),('click-soft',38.30,.12),('whoosh-short',44.18,.14),('whoosh-short',45.15,.10),('whoosh-short',47.70,.12),('impact-bass-1',52.73,.12),('whoosh-short',71.67,.14),('pop',71.80,.075)]
for name,start,gain in events:
    x=decode(V/f'{name}.mp3');x=x[:int((.36 if name=='glitch-3' else 2.2)*SR)]
    if len(x)>600:x[-600:]*=np.linspace(1,0,600)[:,None]
    begin=round(start*SR);end=min(N,begin+len(x));sfx[begin:end]+=gain*x[:end-begin]
write(V/'music-bed.wav',bed)
write(V/'sound-design.wav',sfx)
write(V/'audio-mix-premaster.wav',voice+bed+sfx)
(ROOT/'analysis/audio-v2-events.json').write_text(json.dumps({'sampleRate':SR,'samples':N,'music':'Tech House vibes — Alejandro Magaña (A. M.), Mixkit #130','musicSourceStart':8,'duckRange':[.5,1],'events':events},indent=2))
print('Voice, music and 15 restrained SFX mixed at exact source timing.')

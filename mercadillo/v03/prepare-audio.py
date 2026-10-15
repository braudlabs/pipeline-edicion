from pathlib import Path
import json,subprocess,wave,numpy as np,ast,re,shutil
R=Path(__file__).resolve().parent;old=R.parent/'v01';rate=48000;N=2121*2000
plan=json.loads((R/'timeline.json').read_text());segs=plan['segments'];M=plan['frames']*2000
inputs=json.loads((old/'inputs.json').read_text());prev=json.loads((R.parent/'v02/audio.json').read_text())
def read(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar',str(rate),'-ac','2','-f','f32le','-']),np.float32).reshape(-1,2).copy()
def write(p,a):
 with wave.open(str(p),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes((np.clip(a,-1,1)*32767).astype('<i2').tobytes())
def stretch(a,n):
 if len(a)==n:return a
 b=subprocess.check_output(['ffmpeg','-v','error','-f','f32le','-ar',str(rate),'-ac','2','-i','pipe:0','-af',f'atempo={len(a)/n:.10f}','-f','f32le','pipe:1'],input=a.astype('<f4').tobytes())
 z=np.frombuffer(b,np.float32).reshape(-1,2).copy();return np.pad(z,((0,max(0,n-len(z))),(0,0)))[:n]
def map_t(t):
 f=t*24
 for s in segs:
  if s['sourceIn']<=f<s['sourceOut']:return (s['targetIn']+(f-s['sourceIn'])/s['speed'])/24
 if f>=2121:return M/rate
 return min((s['targetIn']/24 for s in segs if s['sourceIn']>f),default=M/rate)
def map_audio(a):
 return np.concatenate([stretch(a[s['sourceIn']*2000:s['sourceOut']*2000],(s['targetOut']-s['targetIn'])*2000) for s in segs])
vo=read(old/'public/assets/narrator.wav');source=read(Path(inputs['root'])/'02_VOZ/01_NARRADOR_Guillermo_ORIGINAL.mp3')
# The old splice divided /evi/: remove its premature attack, then restore the WHOLE word.
vo[round(47.65*rate):round(56.375*rate)]=0
start,end=56.375,56.965;replacement=source[round(47.9*rate):round(48.635*rate)]
# Match the exact original narrator stem level.
reference=read(old/'public/assets/narrator.wav')[round(56.5*rate):round(56.85*rate)]
rawref=source[round((56.5-8.333333333)*rate):round((56.85-8.333333333)*rate)]
gain=float(np.sqrt(np.mean(reference**2))/np.sqrt(np.mean(rawref**2)));replacement=stretch(replacement,round((end-start)*rate))*gain
edge=144;replacement[:edge]*=np.linspace(0,1,edge)[:,None];replacement[-edge:]*=np.linspace(1,0,edge)[:,None]
vo[round(start*rate):round(end*rate)]=replacement
# Rebuild source sound independently so the comic pause can truly leave only the narrator.
native=[]
for c in inputs['clips']:
 n=c['numero'];length=c['duracion_frames']*2000;a=read(old/'public/assets'/Path(c['archivo']).name);a=np.pad(a,((0,max(0,length-len(a))),(0,0)))[:length]
 a*=10**((0 if n in [1,2,3,11,12] else -3 if n==4 else -6)/20)
 if n not in [1,2,3,10,11]:a[:240]*=np.linspace(0,1,240)[:,None];a[-240:]*=np.linspace(1,0,240)[:,None]
 native.append(a)
native=np.concatenate(native);silent=(13.125,14.875);native[round(silent[0]*rate):round(silent[1]*rate)]=0
# Microfades at the repaired opening join prevent sample steps; no voice crossfade.
for x,fadein in [(149*2000,False),(157*2000,True)]:
 if fadein:native[x:x+144]*=np.linspace(0,1,144)[:,None]
 else:native[x-144:x]*=np.linspace(1,0,144)[:,None]
basegain=json.loads((old/'study/audio-preparation.json').read_text())['baseGain']
voice=map_audio(vo)*basegain;foley=map_audio(native)*basegain;dialogue=voice+foley
write(R/'assets/voice.wav',voice);write(R/'assets/foley.wav',foley);write(R/'assets/dialogue.wav',dialogue)
# Continuous instrumental, with a genuine hard dropout under the aside.
music=read(old/'public/assets/music.wav')[2*rate:2*rate+M];tt=np.arange(M)/rate
pts=sorted([(map_t(a),b) for a,b in prev['musicPoints']]);env=np.interp(tt,[a for a,b in pts],[b for a,b in pts]);a,b=[map_t(t) for t in silent]
env[(tt>=a)&(tt<b)]=0
idx=(tt>=a-.015)&(tt<a);env[idx]*=(a-tt[idx])/.015
idx=(tt>=b)&(tt<b+.075);env[idx]*=(tt[idx]-b)/.075
# Brief space before the grandmother's emphatic YA, while keeping her voice present.
ya=map_t(52.0);idx=(tt>=ya-.10)&(tt<ya);env[idx]*=.18
music*=env[:,None]
sfx=np.zeros_like(dialogue);events=[]
# Existing project library, each sound from the user's workspace; no reference-video audio.
for n in ['whoosh-short','click-soft','impact-bass-1','pop']:
 p=Path('ad3-pipeline/assets')/(n+'.mp3');shutil.copyfile(p,R/'assets'/(n+'.mp3'))
def hit(t,name,volume,why):
 a=read(R/'assets'/(name+'.mp3'));a=a[:round(min(len(a)/rate,.55 if name=='whoosh-short' else .75)*rate)]
 peak=float(abs(a).max());a*=volume/max(peak,.001)
 if len(a)>480:a[-480:]*=np.linspace(1,0,480)[:,None]
 tm=map_t(t);i=round(tm*rate);z=min(len(a),M-i);sfx[i:i+z]+=a[:z];events.append(dict(sourceTime=t,time=tm,sound=name,peak=volume,reason=why))
for args in [(0.7,'whoosh-short',.07,'agencia'),(8.21,'click-soft',.09,'precio'),(9.29,'whoosh-short',.075,'rapidez'),(12.1,'pop',.075,'solución'),(14.96,'impact-bass-1',.12,'vuelve música / Vamos'),(16.70,'click-soft',.11,'destello rodaje'),(19.25,'whoosh-short',.07,'premium'),(21.17,'pop',.11,'percebe'),(24.45,'click-soft',.09,'genera'),(24.79,'pop',.075,'creativos'),(29.4,'whoosh-short',.065,'formación'),(39.75,'impact-bass-1',.16,'BOOM'),(46.77,'click-soft',.07,'ChatGPT'),(49.25,'pop',.08,'hiperrealista'),(50.42,'click-soft',.08,'UGC'),(51.08,'pop',.055,'bla 1'),(51.25,'pop',.065,'bla 2'),(51.42,'pop',.075,'bla 3'),(52.08,'impact-bass-1',.14,'YA'),(58.50,'whoosh-short',.065,'criterio visual'),(68.9,'whoosh-short',.07,'traductor'),(70.3,'impact-bass-1',.10,'malas ideas'),(74.55,'whoosh-short',.08,'arte'),(81.75,'click-soft',.07,'llamada')]:hit(*args)
# A short original dual-tone telephone ring on the physical phone action, behind narration.
t=np.arange(round(.24*rate))/rate;tone=(np.sin(2*np.pi*440*t)+np.sin(2*np.pi*480*t))*.012*np.sin(np.pi*t/.24)**.8
for oldt in [80.75,81.02]:
 i=round(map_t(oldt)*rate);sfx[i:i+len(tone)]+=tone[:,None]
# Silence is an exact contract on all non-voice stems.
sfx[round(a*rate):round(b*rate)]=0
mix=dialogue+music+sfx;peak=float(abs(mix).max());mastergain=min(1,.9/peak)
for name,data in [('music',music),('sfx',sfx),('mix',mix*mastergain)]:write(R/'assets'/f'{name}.wav',data)
report=dict(frames=plan['frames'],duration=M/rate,sourceWord=[47.9,48.635],restoredWordOldTimeline=[start,end],restoredWordFinal=[map_t(start),map_t(end)],prematureNarratorRemoved=[47.65,56.375],silence=[a,b],musicMaxDuringSilence=float(abs(music[round(a*rate):round(b*rate)]).max()),sfxMaxDuringSilence=float(abs(sfx[round(a*rate):round(b*rate)]).max()),foleyMaxDuringSilence=float(abs(foley[round(a*rate):round(b*rate)]).max()),originalNarratorGain=gain,peakBeforeGain=peak,masterGain=mastergain,events=events,independentListening=False)
(R/'audio.json').write_text(json.dumps(report,indent=2));print(report)

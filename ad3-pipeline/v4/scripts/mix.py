from pathlib import Path
import numpy as np,subprocess,json,shutil
R=Path(__file__).resolve().parents[1];A=R/'assets';old=R.parents[1]/'ad1-reedit/assets';sr=48000;T=json.load(open(R/'remotion/src/timeline.json'));N=T['duration']*1000
for n in ['music-tech-house-vibes.mp3','whoosh-short.mp3','click-soft.mp3','pop.mp3','impact-bass-1.mp3']:shutil.copy2(old/n,A/n)
def decode(p,af=None,ss=None):
 args=['ffmpeg','-v','error']
 if ss:args+=['-ss',str(ss)]
 args+=['-i',str(p)]
 if af:args+=['-af',af]
 return np.frombuffer(subprocess.check_output(args+['-ar','48000','-ac','2','-f','f32le','-']),np.float32).reshape(-1,2).copy()
def write(name,a):subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','2','-i','-','-c:a','pcm_s24le',str(A/name)],input=a.astype(np.float32).tobytes(),check=True)
voice=decode(A/'Voz-Montada.wav')[:N];voice=np.pad(voice,((0,max(0,N-len(voice))),(0,0)))
# Gentle per-clip gain correction preserves the whispered hook's internal contrast.
gains=[1.0,.98,.98,.76,.80,1.0,.96,.98,.92,.97]
for c,g in zip(T['clips'],gains):voice[c['from']*1000:c['to']*1000]*=g
music=decode(A/'music-tech-house-vibes.mp3','highpass=f=70,lowpass=f=9000,equalizer=f=2300:t=q:w=0.8:g=-5',19)[:N]
rms=np.sqrt((voice[:N//480*480].reshape(-1,480,2)**2).mean(axis=(1,2)));g=.45;du=[]
for r in rms:
 target=.43 if r>.02 else .85;g+=(.35 if target<g else .035)*(target-g);du.append(g)
env=np.interp(np.arange(N),np.arange(len(du))*480,du);t=np.arange(N)/sr
# Near-silent bed under the intimate reveal; build after the camera moves back.
intro=np.interp(t,[0,1.8,2.6,3.3],[.035,.035,.08,.17]);fade=np.minimum(1,np.maximum(0,(N/sr-t)/.65));bed=music*(env*intro*fade)[:,None]
sfx=np.zeros_like(voice);events=[('whoosh-short',642/48,.10),('click-soft',680/48,.15),('click-soft',705/48,.15),('whoosh-short',810/48,.1),('impact-bass-1',1000/48,.08),('whoosh-short',1186/48,.08),('click-soft',1220/48,.1),('whoosh-short',1510/48,.09),('whoosh-short',1594/48,.07),('whoosh-short',1640/48,.07),('click-soft',1690/48,.1),('whoosh-short',1949/48,.08),('impact-bass-1',2012/48,.1)]
for name,start,gain in events:
 x=decode(A/(name+'.mp3'))[:round(sr*.65)];f=min(len(x),480);x[-f:]*=np.linspace(1,0,f)[:,None];aa=round(start*sr);bb=min(N,aa+len(x));sfx[aa:bb]+=x[:bb-aa]*gain
write('Musica.wav',bed);write('Efectos.wav',sfx);write('Premaster.wav',voice+bed+sfx)
r=subprocess.run(['ffmpeg','-hide_banner','-i',str(A/'Premaster.wav'),'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True);s=r.stderr;stats=json.loads(s[s.rfind('{'):s.rfind('}')+1]);(R/'analysis/loudnorm.json').write_text(json.dumps(stats,indent=2))
af=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:linear=true,aresample=48000,apad,atrim=end_sample={N}"
subprocess.run(['ffmpeg','-v','error','-y','-i',str(A/'Premaster.wav'),'-af',af,'-ar','48000','-c:a','pcm_s24le',str(A/'Mezcla-Final.wav')],check=True)
print('Mixed',N/sr,'seconds; original voice only, whisper dynamics retained.')

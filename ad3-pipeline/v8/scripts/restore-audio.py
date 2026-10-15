from pathlib import Path
import json, subprocess, numpy as np, os

R=Path(__file__).resolve().parents[1]; old=R.parent/'v7'; A=R/'assets'; sr=48000
N=2180000
def decode(p):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar','48000','-ac','2','-f','f32le','-']),np.float32).reshape(-1,2).copy()
def write(p,x):
    subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','2','-i','-','-c:a','pcm_s24le',str(p)],input=x.astype(np.float32).tobytes(),check=True)
alignment=json.loads((R/'analysis/alignment.json').read_text())
start=alignment['clip09StartSample']
original=decode(old/'output/Proyecto/Remotion/public/09-linea-produccion.mp4')
voice=decode(old/'assets/Voz-Montada.wav')[:N]
newvoice=voice.copy()
source_in=round(4.70*sr)
patch_in=start+source_in; end=start+len(original)
# Retain the original waveform through the whole nasal ending. Only the final,
# already quiet 3 ms fade down to the short pause before the existing CTA.
tail=original[source_in:].copy()
tail[-144:]*=np.linspace(1,0,144)[:,None]
newvoice[patch_in:end]=tail
write(A/'Voz-Montada.wav',newvoice)
premaster=decode(old/'assets/Premaster.wav')[:N]
premaster+=(newvoice-voice)*.92
write(A/'Premaster.wav',premaster)
# Reuse V7's level calibration. Preserve its final PCM outside this local repair.
stats=json.loads((old/'analysis/loudnorm.json').read_text())
af=f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}:linear=true,aresample=48000,apad,atrim=end_sample={N}"
subprocess.run(['ffmpeg','-v','error','-y','-i',str(A/'Premaster.wav'),'-af',af,'-ar','48000','-c:a','pcm_s24le',str(A/'Mezcla-Candidata.wav')],check=True)
candidate=decode(A/'Mezcla-Candidata.wav')[:N]
mix=decode(old/'assets/Mezcla-Final.wav')[:N]
p=round(40.25*sr); q=1958000; fade=480
weight=np.ones(q-p,np.float32)
weight[:fade]=np.linspace(0,1,fade);weight[-fade:]=np.linspace(1,0,fade)
mix[p:q]=mix[p:q]*(1-weight[:,None])+candidate[p:q]*weight[:,None]
write(A/'Mezcla-Final.wav',mix)
for n in ['Montaje-AD3.mp4','Musica.wav','Efectos.wav']:
    os.link(old/'assets'/n,A/n)
assert np.max(abs(newvoice[:patch_in]-voice[:patch_in]))==0
assert np.max(abs(newvoice[end:]-voice[end:]))==0
assert np.max(abs(newvoice[patch_in:end-144]-original[source_in:-144]))==0
assert end<1958000
qa={'originalClip09StartSample':start,'sourceAudioSamples':len(original),
    'restoredSourceIntervalSeconds':[4.70,len(original)/sr],
    'previousSourceCutSeconds':4.75,'restoredMissingSeconds':len(original)/sr-4.75,
    'fullOriginalEndInMasterSeconds':end/sr,'ctaStartSeconds':1958000/sr,
    'remainingPauseSeconds':(1958000-end)/sr,'originalTailMaximumDifferenceBeforeFinal3msFade':0,
    'finalMixChangedOnlyInSeconds':[p/sr,q/sr],
    'picture':'V7 video stream reused without re-encoding',
    'verification':'Local source sample alignment and waveform; no external audio upload or claimed full subjective audition.'}
(R/'analysis/audio-repair.json').write_text(json.dumps(qa,indent=2))
print(json.dumps(qa,indent=2))

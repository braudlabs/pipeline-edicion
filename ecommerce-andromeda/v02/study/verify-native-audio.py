from pathlib import Path
import json,subprocess
import numpy as np
p=Path(__file__).resolve().parent.parent
A=json.loads((p/'audio.json').read_text());T=json.loads((p/'timeline.json').read_text());cut=round(T['scenes'][0]['duration_frames']/T['fps']*48000)
def pcm(f):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-ar','48000','-ac','2','-f','f32le','-']),np.float32).reshape(-1,2)
native=pcm(p/'public'/T['scenes'][0]['asset']);stem=pcm(p/'public/assets/hook-native.wav');amb=pcm(p/'public/assets/ambient-after-hook.wav');originalAmb=pcm(p/'public/assets/STEM_AMBIENTE_00-38s.wav')
err=float(np.max(np.abs(native[:cut]-stem[:cut])));assert err<2e-6,err
assert np.max(np.abs(stem[cut:]))==0
assert np.max(np.abs(amb[:cut]))==0
assert np.max(np.abs(amb[cut:len(originalAmb)]-originalAmb[cut:len(amb)]))<2e-6
assert 'AZUL' not in json.dumps([t.get('src','') for t in A['tracks']])
assert A['tracks'][1]['sourceStartSeconds']==A['tracks'][1]['startSeconds']==0
r={'nativeSource':T['scenes'][0]['asset'],'sourceInFrame':0,'outputInFrame':0,'samplesPreserved':cut,'maxPCMError':err,'nativeAfterCutIsSilent':True,'provisionalAmbienceBeforeCutIsSilent':True,'externalVoiceInMix':False,'speed':1,'scope':'Waveform and clock preservation; not independent perceptual lip-sync review'}
(p/'study/native-audio-QA.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

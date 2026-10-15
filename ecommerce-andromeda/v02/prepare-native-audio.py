"""Lock native audio to source video clock; mute by sample index, never shift the remainder."""
from pathlib import Path
import subprocess,json,numpy as np
p=Path(__file__).resolve().parent
t=json.loads((p/'timeline.json').read_text());hook=t['scenes'][0]
assert hook['record_in_frame']==hook['source_in_frame']==0
cut=round(hook['record_out_frame']/t['fps']*48000);length=round(t['assembled_frames']/t['fps']*48000)
def decode(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ar','48000','-ac','2','-f','f32le','-']),np.float32).reshape(-1,2).copy()
def write(path,a):subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','2','-i','-','-c:a','pcm_s24le',str(path)],input=a.astype('<f4').tobytes(),check=True)
native=decode(p/'public'/hook['asset']);out=np.zeros((length,2),np.float32);out[:cut]=native[:cut]
write(p/'public/assets/hook-native.wav',out)
amb=decode(p/'public/assets/STEM_AMBIENTE_00-38s.wav');out[:]=0;out[cut:min(length,len(amb))]=amb[cut:min(length,len(amb))]
write(p/'public/assets/ambient-after-hook.wav',out)

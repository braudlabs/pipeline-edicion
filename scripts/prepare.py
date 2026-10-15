import json, pathlib, subprocess, wave

ROOT = pathlib.Path(__file__).resolve().parents[1]
probes = json.loads((ROOT/'analysis/probes.json').read_text())[:14]
clips=[]
cursor=0
audio=bytearray()
for i,p in enumerate(probes):
    frames=int(p['probe']['streams'][0]['nb_frames'])
    samples=round((cursor+frames)*32000/24)-round(cursor*32000/24)
    pcm=subprocess.check_output(['ffmpeg','-v','error','-i',p['path'],'-vn','-ar','32000','-ac','2','-f','s16le','-'])
    audio.extend(pcm[:samples*4].ljust(samples*4,b'\0'))
    clips.append({'id':i+1,'from':cursor,'duration':frames,'src':f'assets/{i+1:02d}.mp4'})
    cursor+=frames
with wave.open(str(ROOT/'public/assets/narration.wav'),'wb') as w:
    w.setparams((2,2,32000,0,'NONE','not compressed'));w.writeframes(audio)
(ROOT/'src/clips.json').write_text(json.dumps(clips,indent=2))
print(f'{cursor} frames, {cursor/24:.6f}s; original speech assembled at 32000 Hz stereo')

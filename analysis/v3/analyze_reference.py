from PIL import Image,ImageDraw
import subprocess,numpy as np,json,pathlib
P=pathlib.Path('analysis/v3');ref='/Users/alejandrorubiocamarero/Downloads/BRAUDLABS - V1 -  NI ME HAN PAGADO.mp4'
# Successive frames, 24 fps; crop concentrates on the actual subtitle movement.
for name,start,n,step,box in [('caption-a',4.2,40,1,(0,850,1080,1510)),('caption-b',10.5,40,1,(0,820,1080,1480)),('caption-c',36.3,40,1,(0,850,1080,1510)),('camera',14.5,40,3,(0,200,1080,1700))]:
 w,h=324,198 if name!='camera' else 450
 sh=Image.new('RGB',(w*8,(h+24)*5),'#222');d=ImageDraw.Draw(sh)
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(start),'-i',ref,'-frames:v',str(n*step),'-f','rawvideo','-pix_fmt','rgb24','-'])
 frames=np.frombuffer(raw,np.uint8).reshape(-1,1920,1080,3)
 for j in range(n):
  im=Image.fromarray(frames[j*step]).crop(box).resize((w,h));x=j%8*w;y=j//8*(h+24);sh.paste(im,(x,y));d.text((x+5,y+h+4),f'{start+j*step/24:.3f}s  f{round(start*24)+j*step}',fill='white')
 sh.save(P/f'reference-{name}.jpg',quality=92)
# Per-frame waveform and speech ranges from already frozen originals.
clips=json.load(open('src/clips.json'));waves=Image.new('RGB',(1400,14*130),'#131919');dw=ImageDraw.Draw(waves)
audit=[]
for c in clips:
 i=c['id'];a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',f'public/assets/{i:02}.mp4','-ar','48000','-ac','1','-f','f32le','-']),np.float32)
 env=np.sqrt(np.mean(a[:len(a)//480*480].reshape(-1,480)**2,axis=1));mask=env>.007
 # stable voice onset / offset (ignore isolated noise)
 active=[j for j in range(len(mask)-4) if mask[j:j+5].sum()>=4]
 start=active[0]/100 if active else 0;end=(active[-1]+5)/100 if active else len(a)/48000
 words=[w for s in json.load(open(f'analysis/whisper-python/{i:02}.json'))['segments'] for w in s['words']]
 audit.append(dict(id=i,duration=c['duration']/24,onset=start,offset=end,words=words))
 y=(i-1)*130;dw.text((10,y+8),f'{i:02} onset {start:.2f} end {end:.2f} duration {c["duration"]/24:.3f}',fill='white')
 for j,e in enumerate(env):
  x=100+j*1250/len(env);ht=min(70,float(e)*250);dw.line((x,y+112-ht,x,y+112),fill='#96f667')
 for w in words:dw.line((100+w['start']/(c['duration']/24)*1250,y+35,100+w['start']/(c['duration']/24)*1250,y+115),fill='#556677')
json.dump(audit,open(P/'speech-audit.json','w'),indent=2);waves.save(P/'speech-waveforms.jpg')
print('\n'.join(f"{a['id']:02} onset={a['onset']:.2f} end={a['offset']:.2f} full={a['duration']:.2f} :: "+' '.join(w['word'] for w in a['words']) for a in audit))

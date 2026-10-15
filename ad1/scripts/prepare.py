from pathlib import Path
import json,subprocess,math,shutil
import numpy as np
from PIL import Image,ImageFont
R=Path(__file__).resolve().parents[1];A=R/'public/assets';F=48
def words(n):return [w.copy() for s in json.load(open(R/f'analysis/words/{n}.json'))['segments'] for w in s['words']]
voices={n:words(n) for n in ['narrador','plastica','cierre']}
# ASR attaches preceding pauses to these short words; acoustic onsets were checked.
voices['plastica'][0]['start']=.18
voices['plastica'][15]['start']=6.37
voices['cierre'][0]['start']=.60
voices['cierre'][8]['start']=3.43
for w in voices['narrador']:
 if w['word'].strip()=='una' and abs(w['start']-4.74)<.01:w['word']=' un'
cw=voices['cierre'];i=next(i for i,w in enumerate(cw) if 'aprueba' in w['word']);w=cw.pop(i);cw[i:i]=[dict(w,word=' a',end=1.78),dict(w,word=' prueba',start=1.78)]
segments=[];allwords=[];cursor=0
def add(id,voice,a,b):
 global cursor
 a=round(a*F)/F;b=round(b*F)/F;dur=round((b-a)*F);s={'id':id,'voice':voice,'sourceFrom':a,'sourceTo':b,'from':cursor,'duration':dur}
 segments.append(s)
 for w in voices[voice]:
  if a <= (w['start']+w['end'])/2 < b:
   # A cut never retains a partial spoken word; approximate ASR boundaries can straddle silence.
   text=w['word'].strip().strip('.,;:!?¿¡')
   allwords.append({'text':text,'from':cursor+round(max(0,w['start']-a)*F),'to':cursor+round(min(b-a,w['end']-a)*F),'clip':id,'punct':w['word'].strip().endswith(('.',',',';'))})
 cursor+=dur
for id,a,b in [(1,0,4.28),(2,4.34,5.72),(3,5.76,8.65),(4,8.68,12.00)]:add(id,'narrador',a,b)
for a,b in [(.125,2.792),(3.417,5.875),(6.333,7.833)]:add(5,'plastica',a,b)
for id,a,b in [(6,18.82,25.48),(7,25.48,32.40),(8,32.44,34.78),(9,34.98,44.16),(10,44.26,46.30),(11,46.34,52.41),(12,52.41,62.10),(13,62.14,66.40)]:add(id,'narrador',a,b)
for a,b in [(.542,2.583),(3.333,6.125)]:add(14,'cierre',a,b)
cursor+=16 # 1/3 second end hold with music resolution.
byid={i:[s for s in segments if s['id']==i] for i in range(1,15)}
def span(i):ss=byid[i];return ss[0]['from'],ss[-1]['from']+ss[-1]['duration']
def ev(i,offset,endoffset=0):a,b=span(i);return {'from':a+round(offset*F),'to':b+round(endoffset*F)}
events={'credits':ev(6,2.65),'time':ev(8,.75),'accounts':ev(9,2.55),'brand':ev(10,.82),'community':ev(11,4.10),'system':ev(12,2.00,-1.05),'live':ev(13,.20)}
price_word=next(w for w in allwords if w['clip']==14 and w['text']=='Visual');events['price']={'from':price_word['from'],'to':cursor}
events['live']['to']=events['live']['from']+round(1.1*F)
filenames={1:'01-hook.mp4',2:'02-avatar-bueno.mp4',3:'03-avatar-cambiado.mp4',5:'05-plastica-artificial-HABLA-ELLA.mp4',6:'06-creditos-quemados.mp4',7:'07-hora-punta.mp4',8:'08-tiempo-y-dinero.mp4',9:'09-nosotros-procesos-SIN-AUDIO.mp4',10:'10-comanda.mp4',11:'11-brigada.mp4',12:'12-platos-iguales.mp4',13:'13-en-directo-SIN-VOZ-recomendado.mp4',14:'14-cierre-HABLA-ELLA.mp4'}
video=[]
def shot(id,src,from_,duration,source=0,scale=1):video.append({'id':id,'src':src,'from':from_,'duration':duration,'sourceFrame':round(source*F),'scale':scale})
for s in segments:
 i=s['id'];a=s['from'];d=s['duration']
 if i==4:
  cuts=[0,64,114,d]
  for k,src in enumerate(['04a-otra-cocinera.mp4','04b-otra-cocinera.mp4','04c-otra-cocinera.mp4']):shot(i,src,a+cuts[k],cuts[k+1]-cuts[k],source=[1.7,.8,.9][k])
 elif i==7:
  first=round(4.95*F);shot(i,filenames[i],a,first,0);shot(i,filenames[6],a+first,d-first,1.4,1.15)
 elif i==12:
  first=round(3.1*F);shot(i,filenames[i],a,first,.3)
  # Entire middle is covered by the native systems graphic. End on an actual moving plate.
  mid=d-first-round(1.15*F);shot(i,filenames[i],a+first,mid,0)
  shot(i,filenames[i],a+first+mid,d-first-mid,3.6)
 else:
  source=s['sourceFrom'] if i in [5,14] else {1:.625,2:2.1,3:.55,6:0,8:.4,9:0,10:.6,11:0,13:.2}.get(i,0)
  shot(i,filenames[i],a,d,source,1.025 if i==5 and s!=byid[5][0] else 1)
video[-1]['duration']+=16
# Compact spoken groups preserve all words and use one baseline below the face.
caps=[];buf=[]
def finish():
 global buf
 if not buf:return
 text=' '.join(w['text'] for w in buf);size=68
 font=ImageFont.truetype(str(A/'Display-Bold.otf'),size)
 width=font.getlength(text)-max(0,len(text)-1)*size*.025
 if width>880:size=math.floor(size*880/width)
 caps.append({'from':buf[0]['from'],'to':buf[-1]['to']+3,'words':buf,'fontSize':size,'clip':buf[0]['clip']});buf=[]
for w in allwords:
 if buf and (w['clip']!=buf[0]['clip'] or len(buf)>=3 or len(' '.join(x['text'] for x in buf+[w]))>28):finish()
 buf.append(w)
 if w['punct']:finish()
finish()
for a,b in zip(caps,caps[1:]):a['to']=min(max(a['to'],b['from']-1),b['from'])
for name,data in [('timeline',{'fps':F,'duration':cursor,'audio':segments,'video':video,'events':events}),('captions',caps),('words',allwords)]:
 (R/f'src/{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
# Exact PCM editorial mix: no voice stretching or replacement.
audio={}
for n in voices:
 file={'narrador':'voz-narrador-CORTADA.mp3','plastica':filenames[5],'cierre':filenames[14]}[n]
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(A/file),'-vn','-ac','1','-ar','48000','-f','f32le','-']);audio[n]=np.frombuffer(raw,np.float32)
voice=np.zeros(cursor*1000,np.float32)
for s in segments:
 a=round(s['sourceFrom']*48000);n=s['duration']*1000;clip=audio[s['voice']][a:a+n].copy();m=min(len(clip),240);clip[:m]*=np.linspace(0,1,m);clip[-m:]*=np.linspace(1,0,m)
 # Model recording is softer than the narrator; gain only, no time changes.
 gain=1 if s['voice']=='narrador' else 1.32
 voice[s['from']*1000:s['from']*1000+len(clip)]=clip*gain
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','1','-i','-','-c:a','pcm_s24le',str(A/'voice-edit.wav')],input=voice.tobytes(),check=True)
# Freeze frames are only used underneath full-screen graphics or the short closing hold.
for src in {s['src'] for s in video}:
 dst=A/(Path(src).stem+'-last.jpg')
 subprocess.run(['ffmpeg','-v','error','-y','-sseof','-0.1','-i',str(A/src),'-frames:v','1',str(dst)],check=True)
im=Image.open(A/'skool-cursos.png')
for name,box in [('curso-maestria.png',(779,141,1130,399)),('curso-escala.png',(414,529,763,797)),('curso-masterclasses.png',(780,529,1130,797))]:im.crop(box).save(A/name)
Image.open(A/'skool-comunidad.png').crop((411,603,1183,817)).save(A/'comunidad-post.png')
print('Duration',cursor/F,'frames',cursor,'words',len(allwords),'captions',len(caps));print(json.dumps(events,indent=2))

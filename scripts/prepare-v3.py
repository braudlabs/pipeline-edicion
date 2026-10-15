import json,pathlib,subprocess,numpy as np
from PIL import Image,ImageFont
R=pathlib.Path(__file__).resolve().parents[1];S=R/'src';A=R/'public/assets';V=A/'v3'
old=json.load(open(R/'versions/v2/clips.json'))
# Frame-accurate trims verified against words and source waveforms. Continuous pairs retain the shared boundary.
ranges={1:[[8,72],[84,163]],2:[[13,88]],3:[[9,145]],4:[[9,115]],5:[[13,94]],6:[[5,165]],7:[[10,97]],8:[[0,112]],9:[[1,187]],10:[[37,84]],11:[[0,97]],12:[[0,141]],13:[[1,121]],14:[[8,97]]}
edl=[];f=0
for c in old:
 for j,(a,b) in enumerate(ranges[c['id']]):
  edl.append(dict(id=c['id'],part=j,src=c['src'],fromFrame=f,sourceFrom=a,sourceTo=b,oldFrom=c['from']+a,oldTo=c['from']+b,duration=b-a));f+=b-a
json.dump(edl,open(S/'edl-v3.json','w'),indent=2)
def retime(x):
 for e in edl:
  if x<e['oldFrom']:return e['fromFrame']
  if x<e['oldTo']:return e['fromFrame']+x-e['oldFrom']
 return f
caps=json.load(open(R/'versions/v2/captions.json'))
# Correct initial ASR words which included pre-roll; these starts match waveform onsets.
onsets={1:11,2:15,3:11,4:11,5:15,6:7,7:12,8:9,9:2,10:39,11:2,12:6,13:3,14:11}
for c in caps:
 if c is next(x for x in caps if x['clip']==c['clip']):
  c['words'][0]['from']=old[c['clip']-1]['from']+onsets[c['clip']];c['from']=c['words'][0]['from']
 for k in ['from','to']:c[k]=retime(c[k])
 for w in c['words']:
  for k in ['from','to']:w[k]=retime(w[k])
  w['to']=max(w['from']+1,w['to'])
 c['to']=max(c['from']+1,c['to'])
# Subtitle groups each fit inside 880 px, including the largest keyword.
for c in caps:
 for w in c['words']:
  if w['text']=='fallida':w['text']='fallada'
 font=ImageFont.truetype(str(A/'Display-Bold.otf'),80)
 prefix=c['words'][:-1] if c['emphasis'] else c['words']
 t=' '.join(w['text'] for w in prefix)
 c['fontSize']=min(62 if c['emphasis'] else 78,int(860*80/max(1,font.getlength(t))))
 c['keywordSize']=min(148,int(865*80/max(1,font.getlength(c['words'][-1]['text']))))
json.dump(caps,open(S/'captions-v3.json','w'),ensure_ascii=False,indent=2)
events={k:{'from':retime(a),'to':retime(b)} for k,a,b in [('face',133,163),('hand',322,340),('label',353,368),('generation',370,411),('cost',485,532),('process',913,1007),('accounts',1020,1209),('brand',1266,1306),('price',1723,1765)]}
# Give the final CTA 1.75 s to read without extending the original end hold.
events['price']['from']=f-43
json.dump({'duration':f,'fps':24,'events':events},open(S/'timing-v3.json','w'),indent=2)
# Voice and picture use exactly the same edit decisions, at integer frames.
raw=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(A/'narration-master.wav'),'-ar','48000','-ac','2','-f','f32le','-']),np.float32).reshape(-1,2)
parts=[]
for e in edl:
 part=raw[e['oldFrom']*2000:e['oldTo']*2000].copy()
 # 3 ms ramp avoids audio discontinuities; continuous pairs stay untouched.
 if not(e['id'] in [8,12] and e['sourceFrom']==0):part[:144]*=np.linspace(0,1,144)[:,None]
 if not(e['id'] in [7,11] and e['sourceTo']==97):part[-144:]*=np.linspace(1,0,144)[:,None]
 parts.append(part)
voice=np.concatenate(parts)
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','2','-i','-','-c:a','pcm_s24le',str(V/'voice.wav')],input=voice.astype(np.float32).tobytes(),check=True)
# The screenshots remain literal, including the public view counter.
for person,boxes in {'kurt':[(874,735,1108,1098),(642,735,875,1098)],'elliot':[(641,545,875,909),(407,545,641,909)]}.items():
 im=Image.open(V/f'{person}-reels-full.png')
 for j,box in enumerate(boxes):im.crop(box).save(V/f'{person}-proof-{j}.png')
 im.crop((225,92,905,274)).save(V/f'{person}-profile-proof.png')
 im.crop((239,111,389,260)).save(V/f'{person}-avatar.png')
# Mapping frozen for audit and future source edits.
json.dump({'originalFrames':1765,'finalFrames':f,'removedFrames':1765-f,'secondsRemoved':(1765-f)/24,'ranges':ranges},open(R/'analysis/v3/edit-audit.json','w'),indent=2)
print('Final',f,'frames',f/24,'s; removed',(1765-f)/24,'s');print(json.dumps(events,indent=2))

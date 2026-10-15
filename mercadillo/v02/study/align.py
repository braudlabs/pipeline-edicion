from pathlib import Path
import os,json,re,unicodedata,subprocess
os.environ['TORCH_HOME']='/private/tmp/mercadillo-torch-cache'
import torch,numpy as np
from torchaudio.pipelines import MMS_FA as bundle
p=Path(__file__).resolve().parent
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p.parents[1]/'v01/public/assets/dialogue-foley.wav'),'-f','f32le','-ar','16000','-ac','1','-'])
a=np.frombuffer(raw,np.float32).copy()
original=json.load(open(p.parents[1]/'v01/study/words.json'))['transcription']
words=[{'text':w['text'].strip(),'oldStart':w['offsets']['from']/1000,'oldEnd':w['offsets']['to']/1000} for w in original if w['text'].strip()]
bounds=[(0,13.125),(13.125,22.083333),(22.083333,32.58),(32.58,43.333333),(43.333333,47.875),(47.875,52.5),(56.375,61.6),(61.6,67.75),(67.75,71.81),(71.81,77.61),(77.61,80.48),(80.48,88.375)]
print('Loading model',flush=True);model=bundle.get_model().to('mps');tokenizer=bundle.get_tokenizer();aligner=bundle.get_aligner();out=[]
def normalize(s):
 s=''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c))
 s=re.sub('[^a-z0-9 ]','',s)
 return {'10':'diez','ugc':'u ge ce','chatgpt':'chat ge pe te','ia':'i a'}.get(s,s)
for begin,end in bounds:
 ww=[w for w in words if begin<=w['oldStart']<end]
 tokens=[];mapping=[]
 for i,w in enumerate(ww):
  for token in normalize(w['text']).split():tokens.append(token);mapping.append(i)
 data=torch.from_numpy(a[round(begin*16000):round(end*16000)]).unsqueeze(0).to('mps')
 with torch.inference_mode():emission,_=model(data)
 spans=aligner(emission[0].cpu(),tokenizer(tokens));ratio=data.shape[-1]/emission.shape[1]/16000
 agg={}
 for i,ss in zip(mapping,spans):
  agg.setdefault(i,[]).extend(ss)
 for i,ss in agg.items():
  w=dict(ww[i]);w.update(start=round(begin+min(s.start for s in ss)*ratio,4),end=round(begin+max(s.end for s in ss)*ratio,4),score=round(sum(s.score for s in ss)/len(ss),4));out.append(w)
 print(begin,end,[(w['text'],w['start'],w['end']) for w in out[-len(ww):]],flush=True)
(p/'aligned-words.json').write_text(json.dumps({'method':'TorchAudio 2.8 MMS_FA multilingual CTC, local MPS; normalized Spanish transcript','words':out},ensure_ascii=False,indent=2))

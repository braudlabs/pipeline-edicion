from pathlib import Path
import os,json,subprocess,numpy as np
os.environ['TORCH_HOME']='/private/tmp/mercadillo-torch-cache'
import torch
from torchaudio.pipelines import MMS_FA as bundle
R=Path(__file__).resolve().parent
model=bundle.get_model().to('mps');tokenizer=bundle.get_tokenizer();aligner=bundle.get_aligner()
cases=[('evidentemente',R/'narrator-original-16k.wav',44.8,50.3,'le activas el micro y que le diga a chat ge pe te evidentemente lo que prevalece es el'),('first-seam',R.parents[1]/'v01/public/assets/dialogue-foley.wav',5.3,7.7,'el de alla lo unico que te diferencia')]
out={}
for name,path,a,b,words in cases:
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ss',str(a),'-t',str(b-a),'-ar','16000','-ac','1','-f','f32le','-']);data=torch.from_numpy(np.frombuffer(raw,np.float32).copy()).unsqueeze(0).to('mps')
 with torch.inference_mode():emission,_=model(data)
 tt=words.split();spans=aligner(emission[0].cpu(),tokenizer(tt));ratio=data.shape[-1]/emission.shape[1]/16000;rows=[]
 for word,ss in zip(tt,spans):
  rows.append(dict(word=word,start=a+min(s.start for s in ss)*ratio,end=a+max(s.end for s in ss)*ratio,score=sum(s.score for s in ss)/len(ss),letters=[dict(letter=char,start=a+s.start*ratio,end=a+s.end*ratio,score=s.score) for char,s in zip(word,ss)]))
 out[name]=rows;print(name,rows,flush=True)
(R/'aligned-repairs.json').write_text(json.dumps(out,indent=2))

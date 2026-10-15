from pathlib import Path
import os,subprocess,json,numpy as np
os.environ['TORCH_HOME']='/private/tmp/mercadillo-torch-cache'
import torch
from torchaudio.pipelines import MMS_FA as bundle
R=Path(__file__).resolve().parent;model=bundle.get_model().to('mps');tok=bundle.get_tokenizer();aligner=bundle.get_aligner();path=R.parent/'assets/mix.wav';out={}
for name,a,b,phrase in [('grandma',47.125,50.7916667,'hazme un anuncio hiperrealista u ge ce bla bla bla pero ya'),('return',53.7916667,54.8,'evidentemente lo que')]:
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-ss',str(a),'-t',str(b-a),'-ar','16000','-ac','1','-f','f32le','-']);x=torch.from_numpy(np.frombuffer(raw,np.float32).copy()).unsqueeze(0).to('mps')
 with torch.inference_mode():y,_=model(x)
 ws=phrase.split();ss=aligner(y[0].cpu(),tok(ws));ratio=x.shape[-1]/y.shape[1]/16000
 out[name]=[dict(word=w,start=a+min(s.start for s in sps)*ratio,end=a+max(s.end for s in sps)*ratio,score=sum(s.score for s in sps)/len(sps)) for w,sps in zip(ws,ss)]
(R/'final-word-check.json').write_text(json.dumps(out,indent=2));print(out)

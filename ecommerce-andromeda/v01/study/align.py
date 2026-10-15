from pathlib import Path
import os,json,re,unicodedata,subprocess
os.environ['TORCH_HOME']='/private/tmp/mercadillo-torch-cache'
import torch,numpy as np
from torchaudio.pipelines import MMS_FA as bundle
p=Path(__file__).resolve().parent
torch.set_num_threads(4)
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p.parent/'public/assets/STEM_NARRADOR_00-38s.wav'),'-f','f32le','-ar','16000','-ac','1','-']),np.float32).copy()
segments=[
(0,5.72,'Si eres dueño de un ecommerce ya sabes que con Andrómeda necesitas anuncios nuevos cada semana'),
(5.72,10.05,'Y sabes que de la forma tradicional es la misma mierda de siempre'),
(10.05,14.58,'días y días para que el editor o una agencia te entregue las piezas'),
(14.58,18.75,'Quieres testear un nuevo ángulo y necesitas semanas para ver el fruto de eso'),
(18.75,23.09,'Y durante todo ese proceso ya se te han caído los ads antiguos'),
(23.09,25.42,'y venga a repetir otra puta vez'),
(25.42,32.78,'No vengo a hablarte de tu problema ya tienes suficiente con eso y con la sudadera de este tío Vengo a hablarte de la solución'),
(32.78,35.09,'Instalaremos en tu tienda esta maquinita'),
(35.09,38.333333,'Le pedirás cinco ads para un concepto nuevo te los dará')]
print('Load local model',flush=True);device='mps' if torch.backends.mps.is_available() else 'cpu';print(device,flush=True)
model=bundle.get_model().to(device);tokenizer=bundle.get_tokenizer();aligner=bundle.get_aligner();out=[]
for begin,end,text in segments:
 words=text.split(); tokens=[''.join(c for c in unicodedata.normalize('NFKD',w.lower()) if not unicodedata.combining(c)) for w in words]
 tokens=[re.sub('[^a-z]','',w) for w in tokens]
 data=torch.from_numpy(a[round(begin*16000):round(end*16000)]).unsqueeze(0).to(device)
 with torch.inference_mode(): emission,_=model(data)
 spans=aligner(emission[0].cpu(),tokenizer(tokens));ratio=data.shape[-1]/emission.shape[1]/16000
 for word,ss in zip(words,spans):out.append({'text':word,'start':round(begin+min(s.start for s in ss)*ratio,4),'end':round(begin+max(s.end for s in ss)*ratio,4),'score':round(sum(s.score for s in ss)/len(ss),4)})
 print(begin,end,flush=True)
(p/'aligned-words.json').write_text(json.dumps({'method':'local MMS_FA forced alignment of supplied corrected script; not independent transcription/listening','device':device,'words':out},ensure_ascii=False,indent=2))

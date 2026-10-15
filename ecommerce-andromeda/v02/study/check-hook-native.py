import os,json,subprocess
from pathlib import Path
os.environ['TORCH_HOME']='/private/tmp/mercadillo-torch-cache'
import torch,numpy as np
from torchaudio.pipelines import MMS_FA as bundle
p=Path(__file__).resolve().parent.parent
torch.set_num_threads(4)
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p/'public/assets/00_HOOK_visual_aprobado_audio_nativo_no_final.mp4'),'-f','f32le','-ar','16000','-ac','1','-']),np.float32).copy()
model=bundle.get_model(); tokens=['mas','anuncios','mas']
with torch.inference_mode():emission,_=model(torch.from_numpy(a).unsqueeze(0))
spans=bundle.get_aligner()(emission[0],bundle.get_tokenizer()(tokens));ratio=len(a)/emission.shape[1]/16000
out=[{'word':w,'start':min(s.start for s in ss)*ratio,'end':max(s.end for s in ss)*ratio,'score':sum(s.score for s in ss)/len(ss)} for w,ss in zip(tokens,spans)]
r={'method':'Forced alignment of supplied phrase to native source; not independent transcription or perceptual lip-sync review','words':out,'fitsHookCut':max(w['end'] for w in out)<130/24}
(p/'study/native-hook-alignment.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

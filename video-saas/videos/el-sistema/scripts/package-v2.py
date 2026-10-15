from pathlib import Path
import json,shutil
from ae import AE
R=Path(__file__).resolve().parents[1];DEST=Path('/Users/alejandrorubiocamarero/Desktop/El director/video-saas/videos/el-sistema')
S=json.loads((R/'src/design-v2.json').read_text());assets=sorted(set(n['asset'] for c in S['comps'].values() for n in c['layers'] if n['type'] in ['media','audio']))
for d in ['assets','ae','src','scripts','analysis','output']:(DEST/d).mkdir(parents=True,exist_ok=True)
extra=['Voz-V2.wav','Musica-V2.wav','Efectos-V2.wav','locucion.mp3','Musica.wav','music-tech-house-vibes.mp3','click-soft.mp3','whoosh-short.mp3','typing.mp3','key-press.mp3','ping.mp3','whoosh-cinematic.mp3','chime.mp3']
for f in set(assets+extra):
 src=R/'assets'/('Mezcla-V2-final.wav' if f=='Mezcla-V2.wav' else f);shutil.copy2(src,DEST/'assets'/f)
for folder,names in {'src':['design-v2.json','retime.json','sound-cues.json','sound-cues-v2.json'],'scripts':['ae.py','build-ae.py','design-v2.py','finish-v2.py','retime.py','mix-v2.py'],'analysis':['voice-silence.log','maquina-source.json','REFERENCIAS-V2.md','timing-audit-result.json','BRIEF-MAQUINA.txt']}.items():
 for f in names:shutil.copy2(R/folder/f,DEST/folder/f)
for f in ['ENTREGA.md','Revisar-V2.html','CURRENT-VERSION.json']:shutil.copy2(R/f,DEST/f)
for f in ['El-Sistema-V2.srt','El-Sistema-V2.vtt','Avance-02-Maquina.mp4']:shutil.copy2(R/'output'/f,DEST/'output'/f)
with AE(log=R/'analysis/package-ae.jsonl') as a:
 info=a.call('ae_project_info')['result'];ops=[]
 for item in info['items']:
  if item['name'] in assets:ops.append({'operation':'footage.replace','args':{'item':item['id'],'path':str(DEST/'assets'/item['name'])}})
 q=a.call('ae_do',operation='batch.run',args={'ops':ops,'stopOnError':True})
 if q.get('result',{}).get('failed'):raise RuntimeError(q)
 a.call('ae_do',operation='render.set_output',args={'queueIndex':1,'outputPath':str(DEST/'output/El-Sistema-V2-ProRes.mov')})
 a.call('ae_save_project',path=str(DEST/'ae/El-Sistema-V2.aep'))
 missing=a.call('ae_do',operation='footage.list_missing',args={});(DEST/'analysis/media-link-check.json').write_text(json.dumps(missing,indent=2));print(missing)
 print('PACKAGED',DEST,flush=True)

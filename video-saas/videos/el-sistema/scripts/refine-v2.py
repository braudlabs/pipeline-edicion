# Focused patch, sourced from the regenerated full design; the compiler produces the same result.
from pathlib import Path
import json
from ae import AE
R=Path(__file__).resolve().parents[1];S=json.loads((R/'src/design-v2.json').read_text());ops=[]
with AE(log=R/'analysis/refine-v2.jsonl') as a:
 for cn in S['comps']:
  if cn in ['V2 · Cámara superficie','V2 · Apertura','V2 · Inmersión','V2 · Resultado y montaje','V2 · Versiones','V2 · Cierre',S['master']]:
   ops.append({'operation':'layer.delete','args':{'comp':cn,'layer':'Luz superior'}})
 for n in S['comps']['V2 · Moodboard']['layers']:
  if n['name'] in ['Aprobar','Aprobar y animar','Animando','En movimiento']:
   ops.append({'operation':'transform.set','args':{'comp':'V2 · Moodboard','layer':n['name'],'position':n['pos']}})
 n=next(n for n in S['comps']['V2 · Inmersión']['layers'] if n['name']=='Cursor de aprobación')
 ops.append({'operation':'keyframe.set_batch','args':{'comp':'V2 · Inmersión','layer':n['name'],'property':['ADBE Transform Group','ADBE Position'],'times':n['anim']['pos']['times'],'values':n['anim']['pos']['values']}})
 print(a.call('ae_do',operation='batch.run',args={'ops':ops,'stopOnError':True}))
 a.call('ae_save_project',path=str(R/'ae/El-Sistema-V2.aep'))

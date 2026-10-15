from pathlib import Path
import json,copy,subprocess
R=Path(__file__).resolve().parents[1];p=R/'ae/design.json';s=json.loads(p.read_text());req=[];ops=[]
def op(n,**a):ops.append({'operation':n,'args':a})
c='AD3 - FINAL';ink=[32/255,33/255,31/255];cream=[244/255,241/255,234/255]
for n in list(s['comps'][c]['layers']):
 if n['name'].startswith('SUB 21.'):
  name=n['name']+' papel';d=copy.deepcopy(n);d['name']=name;d['from']=1248;d['color']='#20211f';d.pop('textStroke',None);d.pop('shadow',None);n['to']=1248;s['comps'][c]['layers'].append(d)
  op('layer.duplicate',comp=c,layer=n['name'],newName=name);op('layer.set_props',comp=c,layer=n['name'],props={'outPoint':26});op('layer.set_props',comp=c,layer=name,props={'inPoint':26});op('text.set_style',comp=c,layer=name,fillColor=ink,applyStroke=False);op('effect.set_property',comp=c,layer=name,effectIndex=2,property=['ADBE Drop Shadow-0002'],value=0)
 if n['name'].startswith(('SUB 27.','SUB 28.','SUB 29.')):
  n['color']='#f4f1ea';n['textStroke']=['#302a26',1.2];n['shadow']=[0,2,3,'#191915',.65]
  op('text.set_style',comp=c,layer=n['name'],fillColor=cream,strokeColor=[48/255,42/255,38/255],strokeWidth=1.2)
  op('effect.set_property',comp=c,layer=n['name'],effectIndex=2,property=['ADBE Drop Shadow-0001'],value=[25/255,25/255,21/255,1]);op('effect.set_property',comp=c,layer=n['name'],effectIndex=2,property=['ADBE Drop Shadow-0002'],value=255*.65)
cam=s['comps']['MG - Sistemas']['camera'];cam['values'][-1][2]=-3950;cam['values'][-2][2]=-3950
op('keyframe.set_batch',comp='MG - Sistemas',layer='CAMARA - Recorrido',property=['ADBE Transform Group','ADBE Position'],times=[f/48 for f in cam['frames']],values=cam['values'])
for n in s['comps']['MG - Encaje y consistencia']['layers']:
 if n['name']=='Misma persona en 7':
  n['anim']['pos']['values'][-1]=[540,960,0];a=n['anim']['pos'];op('keyframe.set_batch',comp='MG - Encaje y consistencia',layer=n['name'],property=['ADBE Transform Group','ADBE Position'],times=[f/48 for f in a['frames']],values=a['values'])
t=json.load(open(R/'remotion/src/timeline.json'));seg=next(x for x in t['video'] if x['from']<=1424<x['from']+x['duration']);sourceframe=seg['sourceFrame']+(1424-seg['from']);src=Path((R/'source-path.txt').read_text().strip())/'entrega'/seg['src'];subprocess.run(['ffmpeg','-v','error','-y','-ss',str(sourceframe/48),'-i',str(src),'-frames:v','1','-q:v','2',str(R/'assets/07-consistencia.jpg')],check=True);op('footage.reload',item='07-consistencia.jpg')
p.write_text(json.dumps(s,ensure_ascii=False,indent=2));req.append({'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops,'stopOnError':True}}})
req+=json.loads((R/'ae/validate-render.json').read_text())
for t in [26.4,32.5,36.8,29.63,29.68]:req.append({'name':'ae_render_frame','arguments':{'compNameOrId':'AD3 - FINAL','time':t,'outPath':str(R/'analysis'/f'fixed-{t:.2f}.png')}})
(R/'ae/patch-review.json').write_text(json.dumps(req));print('poster07',sourceframe/48,'operations',len(ops))

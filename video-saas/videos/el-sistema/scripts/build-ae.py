from pathlib import Path
import json,sys,math
from ae import AE
R=Path(__file__).resolve().parents[1];V='V2' if '--v2' in sys.argv else 'V1';S=json.loads((R/('src/design-v2.json' if V=='V2' else 'src/design.json')).read_text());AEP=R/('ae/El-Sistema-'+V+'.aep');F=S['fps']
ops=[]
def op(operation,**args):ops.append({'operation':operation,'args':args})
def rgb(h):return [int(h[i:i+2],16)/255 for i in (1,3,5)]
PP={k:['ADBE Transform Group',v] for k,v in {'pos':'ADBE Position','scale':'ADBE Scale','opacity':'ADBE Opacity','rot':'ADBE Rotate Z','rx':'ADBE Rotate X','ry':'ADBE Rotate Y'}.items()}
def keys(c,n,p,k,three=False):
 vals=k['values']
 if p=='scale':vals=[[100*x for x in v]+([100] if three and len(v)==2 else []) for v in vals]
 if p=='opacity':vals=[100*x for x in vals]
 if p=='pos' and three:vals=[v+([0] if len(v)==2 else []) for v in vals]
 op('keyframe.set_batch',comp=c,layer=n,property=PP[p],times=k['times'],values=vals)
 for i in range(len(vals)):
  if k['ease']=='linear':op('keyframe.set_interpolation',comp=c,layer=n,property=PP[p],keyIndex=i+1,inType='linear',outType='linear')
  else:op('keyframe.set_easing',comp=c,layer=n,property=PP[p],keyIndex=i+1,inSpeed=0,outSpeed=0,inInfluence=72 if k['ease']=='out' else 58,outInfluence=18 if k['ease']=='out' else 42)
  if p=='pos':op('keyframe.set_spatial',comp=c,layer=n,property=PP[p],keyIndex=i+1,continuous=False,autoBezier=False)
def layer(c,n,ids):
 name=n['name'];t=n['type'];anchor=n.get('anchor',[0,0]);three=n.get('threeD',False)
 if t=='text':
  op('layer.create_text',comp=c,name=name,text=n['text']);op('text.reset_style',comp=c,layer=name,scope='both')
  op('text.set_style',comp=c,layer=name,font=n['font'],fontSize=n['size'],fillColor=rgb(n['color']),applyFill=True,applyStroke=False,justification=n['align'],tracking=n['track'],allCaps=False,fauxBold=False,fauxItalic=False)
 elif t in ['media','comp','audio']:
  op('layer.create_footage',comp=c,name=name,sourceItemId=ids[n['asset']])
 elif t=='null':op('layer.create_null',comp=c,name=name)
 elif t in ['path','rect','ellipse']:
  op('layer.create_shape',comp=c,name=name);op('shape.add_group',comp=c,layer=name,name='Geometría nativa')
  if t=='path':op('shape.add_path',comp=c,layer=name,groupIndex=1,vertices=n['points'],closed=n.get('closed',False))
  elif t=='rect':
   op('shape.add_rect',comp=c,layer=name,groupIndex=1,size=[n['w'],n['h']],roundness=n.get('round',0));anchor=[-n['w']/2,-n['h']/2]
  else:op('shape.add_ellipse',comp=c,layer=name,groupIndex=1,size=[n['w'],n['h']])
  if n.get('color'):op('shape.add_fill',comp=c,layer=name,groupIndex=1,color=rgb(n['color'])+[1])
  if n.get('stroke'):op('shape.add_stroke',comp=c,layer=name,groupIndex=1,color=rgb(n['stroke'])+[1],width=n.get('strokeWidth',1))
 else:raise ValueError(t)
 props={'motionBlur':True,'threeDLayer':three,'inPoint':n['from'],'outPoint':n['to'],'label':9 if t=='text' else 13}
 if t=='media' and n['asset'].endswith('.mp4'):
  props['audioEnabled']=False
  op('layer.set_props',comp=c,layer=name,props={'startTime':n['from']-n.get('sourceOffset',0)})
 op('layer.set_props',comp=c,layer=name,props=props)
 pos=n['pos'];sc=[v*100 for v in n.get('scale',[1,1])]
 if three:pos=pos+([0] if len(pos)==2 else []);anchor=anchor+([0] if len(anchor)==2 else []);sc=sc+([100] if len(sc)==2 else [])
 op('transform.set',comp=c,layer=name,position=pos,anchorPoint=anchor,scale=sc,opacity=n.get('opacity',1)*100,rotation=n.get('rot',0))
 if n.get('freezeTail'):
  op('layer.set_props',comp=c,layer=name,props={'timeRemapEnabled':True,'inPoint':n['from'],'outPoint':n['to']})
  op('expression.set',comp=c,layer=name,property=['ADBE Time Remapping'],expression='Math.min(source.duration-1/30,Math.max(0,time-startTime));')
 for p,k in n.get('anim',{}).items():keys(c,name,p,k,three)
 for eff in n.get('effects',[]):
  op('effect.add',comp=c,layer=name,matchName=eff['match'],name=eff.get('name',eff['match']))
  for prop,value in eff.get('props',[]):op('effect.set_property',comp=c,layer=name,effectIndex=n['effects'].index(eff)+1,property=prop,value=value)
 if n.get('parent'):op('layer.set_parent',comp=c,layer=name,parentLayer=n['parent'],jump=True)

def checked(a,ls,label):
 for i in range(0,len(ls),100):
  chunk=ls[i:i+100];d=a.call('ae_do',operation='batch.run',args={'ops':chunk,'stopOnError':True})
  if not d.get('ok') or d.get('result',{}).get('failed'):raise RuntimeError(json.dumps(d)[-5000:])
  print(label,i+len(chunk),'/',len(ls),flush=True)
with AE(log=R/'analysis/ae-build.jsonl') as a:
 info=a.call('ae_project_info')['result']
 if info['numItems'] and (not info.get('file') or Path(info['file']).parent != AEP.parent) and not (info.get('file') is None and any(x['name']==S['master'] for x in info.get('items',[]))):raise RuntimeError('Another project is open; preserve it before proceeding: '+str(info['file']))
 a.call('ae_do',operation='project.new',args={})
 cs=[{'operation':'comp.create','args':{'name':n,'width':c['width'],'height':c['height'],'fps':F,'duration':S['duration'],'bgColor':rgb('#0A0A0B')}} for n,c in S['comps'].items()]
 checked(a,cs,'comps');info=a.call('ae_project_info')['result'];ids={x['name']:x['id'] for x in info['items']}
 assets=set(n['asset'] for c in S['comps'].values() for n in c['layers'] if n['type'] in ['media','audio'])
 for file in sorted(assets):
  d=a.call('ae_do',operation='project.import_file',args={'path':str(R/'assets'/file),'name':file})['result'];ids[file]=d.get('id') or d.get('itemId') or d['item']['id']
 allops=[]
 for name,c in S['comps'].items():
  ops=[];op('comp.set_props',comp=name,props={'motionBlur':True,'shutterAngle':200,'shutterPhase':-100,'motionBlurSamplesPerFrame':12,'motionBlurAdaptiveSampleLimit':32})
  for n in c['layers']:layer(name,n,ids)
  allops.extend(ops);checked(a,ops,name)
  a.call('ae_save_project',path=str(AEP))
 (R/'ae/operations.json').write_text(json.dumps(allops,indent=2))
 checked(a,[{'operation':'render.add_to_queue','args':{'comp':S['master'],'outputPath':str(R/'output'/('native-'+V+'.mov'))}},{'operation':'render.set_output','args':{'queueIndex':1,'renderTemplate':'Configuración óptima','outputTemplate':'Calidad alta'}}],'queue')
 templates=a.call('ae_do',operation='render.list_templates',args={});(R/'analysis/render-templates.json').write_text(json.dumps(templates,indent=2))
 a.call('ae_save_project',path=str(AEP));info=a.call('ae_project_info');(R/'analysis/native-project.json').write_text(json.dumps(info,indent=2))
 print('SAVED',AEP,flush=True)

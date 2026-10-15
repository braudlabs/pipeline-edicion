from pathlib import Path
import json,sys,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ae import AE
R=Path(__file__).resolve().parents[2];V='V3';S=json.loads((R/'src/v3/design.json').read_text());AEP=R/'ae/v3/El-Sistema-V3.aep';F=S['fps']
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
  else:op('keyframe.set_easing',comp=c,layer=n,property=PP[p],keyIndex=i+1,inSpeed=0,outSpeed=0,inInfluence=86 if k['ease']=='out' else 76,outInfluence=12 if k['ease']=='out' else 36)
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
 extra(c,n)
 if n.get('parent'):op('layer.set_parent',comp=c,layer=name,parentLayer=n['parent'],jump=True)

def rounded(w,h,r,cx=None,cy=None):
 x=(w/2 if cx is None else cx)-w/2;y=(h/2 if cy is None else cy)-h/2;q=.55228475*r
 v=[[x+r,y],[x+w-r,y],[x+w,y+r],[x+w,y+h-r],[x+w-r,y+h],[x+r,y+h],[x,y+h-r],[x,y+r]]
 it=[[-q,0],[0,0],[0,-q],[0,0],[q,0],[0,0],[0,q],[0,0]];ot=[[0,0],[q,0],[0,0],[0,q],[0,0],[-q,0],[0,0],[0,-q]]
 return v,it,ot
def customkeys(c,name,prop,k):
 op('keyframe.set_batch',comp=c,layer=name,property=prop,times=k['times'],values=k['values'])
 for i in range(len(k['times'])):op('keyframe.set_easing',comp=c,layer=name,property=prop,keyIndex=i+1,inSpeed=0,outSpeed=0,inInfluence=78,outInfluence=22)
def extra(c,n):
 name=n['name']
 if n.get('roundedMask'):
  v,it,ot=rounded(*n['roundedMask']);op('mask.add',comp=c,layer=name,name='Esquinas');op('mask.set_path',comp=c,layer=name,maskIndex=1,vertices=v,inTangents=it,outTangents=ot,closed=True)
 if n.get('trim'):
  op('shape.add_trim_paths',comp=c,layer=name,groupIndex=1,start=0,end=0)
  customkeys(c,name,['ADBE Root Vectors Group',1,'ADBE Vectors Group','ADBE Vector Filter - Trim','ADBE Vector Trim End'],n['trim'])
 if n.get('typeOn'):
  op('text.add_animator',comp=c,layer=name,name='Escritura',properties={'ADBE Text Opacity':0},selector='range',rangeStart=0,rangeEnd=100)
  prop=['ADBE Text Properties','ADBE Text Animators',1,'ADBE Text Selectors',1,'ADBE Text Percent Start']
  op('keyframe.set_batch',comp=c,layer=name,property=prop,times=n['typeOn'],values=[0,100])
  for i in [1,2]:op('keyframe.set_interpolation',comp=c,layer=name,property=prop,keyIndex=i,inType='linear',outType='linear')
 if n.get('morphMask'):
  q=n['morphMask'];op('mask.add',comp=c,layer=name,name='Formato adaptable')
  v,it,ot=rounded(*q['sizes'][0],q['round'],*q['center']);op('mask.set_path',comp=c,layer=name,maskIndex=1,vertices=v,inTangents=it,outTangents=ot,closed=True)
  for j,s in enumerate(['Ancho','Alto']):
   op('effect.add',comp=c,layer=name,matchName='ADBE Slider Control',name=s)
   customkeys(c,name,['ADBE Effect Parade',j+1,1],{'times':q['times'],'values':[z[j] for z in q['sizes']]})
  cx,cy=q['center'];rr=q['round']
  expr='var w=effect("Ancho")(1),h=effect("Alto")(1),r='+str(rr)+',q=r*.55228475,x='+str(cx)+'-w/2,y='+str(cy)+'-h/2;createPath([[x+r,y],[x+w-r,y],[x+w,y+r],[x+w,y+h-r],[x+w-r,y+h],[x+r,y+h],[x,y+h-r],[x,y+r]],[[-q,0],[0,0],[0,-q],[0,0],[q,0],[0,0],[0,q],[0,0]],[[0,0],[q,0],[0,0],[0,q],[0,0],[-q,0],[0,0],[0,-q]],true);'
  op('expression.set',comp=c,layer=name,property=['ADBE Mask Parade',1,'ADBE Mask Shape'],expression=expr)

def checked(a,ls,label):
 for i in range(0,len(ls),100):
  chunk=ls[i:i+100];d=a.call('ae_do',operation='batch.run',args={'ops':chunk,'stopOnError':True})
  if not d.get('ok') or d.get('result',{}).get('failed'):raise RuntimeError(json.dumps(d)[-5000:])
  print(label,i+len(chunk),'/',len(ls),flush=True)
with AE(log=R/'analysis/v3/ae-build.jsonl') as a:
 info=a.call('ae_project_info')['result']
 if info['numItems']:
  if not info.get('file') or 'El-Sistema-' not in str(info.get('file')):raise RuntimeError('Unrelated project open; preserve before build')
  a.call('ae_save_project',path=str(R/'ae/v3/Antes-de-V3.aep'))
 a.call('ae_do',operation='project.new',args={})
 cs=[{'operation':'comp.create','args':{'name':n,'width':c['width'],'height':c['height'],'fps':F,'duration':S['duration'],'bgColor':rgb('#09090B')}} for n,c in S['comps'].items()]
 checked(a,cs,'comps');info=a.call('ae_project_info')['result'];ids={x['name']:x['id'] for x in info['items']}
 assets=set(n['asset'] for c in S['comps'].values() for n in c['layers'] if n['type'] in ['media','audio'])
 for file in sorted(assets):
  d=a.call('ae_do',operation='project.import_file',args={'path':str(R/'assets'/file),'name':file})['result'];ids[file]=d.get('id') or d.get('itemId') or d['item']['id']
 allops=[]
 for name,c in S['comps'].items():
  ops=[];op('comp.set_props',comp=name,props={'motionBlur':True,'shutterAngle':180,'shutterPhase':-90,'motionBlurSamplesPerFrame':16,'motionBlurAdaptiveSampleLimit':64})
  for n in c['layers']:layer(name,n,ids)
  allops.extend(ops);checked(a,ops,name)
  a.call('ae_save_project',path=str(AEP))
 (R/'ae/v3/operations.json').write_text(json.dumps(allops,indent=2))
 checked(a,[{'operation':'render.add_to_queue','args':{'comp':S['master'],'outputPath':str(R/'output/v3/Native-V3.mov')}},{'operation':'render.set_output','args':{'queueIndex':1,'renderTemplate':'Configuración óptima','outputTemplate':'Calidad alta'}}],'queue')
 templates=a.call('ae_do',operation='render.list_templates',args={});(R/'analysis/v3/render-templates.json').write_text(json.dumps(templates,indent=2))
 a.call('ae_save_project',path=str(AEP));info=a.call('ae_project_info');(R/'analysis/v3/native-project.json').write_text(json.dumps(info,indent=2))
 print('SAVED',AEP,flush=True)

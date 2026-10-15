"""Restore the exact V01 composition requested by Ale, keeping CTC timing."""
from native import *
C='V02 MASTER'
rows=[json.loads(s) for s in (R/'matte-import-results.jsonl').read_text().splitlines()]
result=rows[-1]['result']['structuredContent'];assert result['ok'],result
mid=result['result']['id']
spec=json.loads((R.parent/'spec.json').read_text())
matte='CRITERIO — matte sujeto';footage(C,matte,mid,58,59,58);xf(C,matte,scale=[200,200]);props(C,matte,enabled=False,motionBlur=False)
for c in spec['cues']:
 if c['group']!='criterion':continue
 y,size=(655,211) if c['text']=='criterio' else (925,287)
 c.update(y=y,size=size,color='white',motion='rise',baselineAnchor=True,tracking=-55,masked=True,outlineWidth=1.65,outlineOpacity=90)
 n=c['id']+' — '+c['text'];outline=n+' — contorno'
 op('text.set_style',comp=C,layer=n,fontSize=size,fillColor=[1,253/255,243/255],tracking=-55)
 xf(C,n,anchorPoint=[0,0]);enter(C,n,c['start'],540,y,'rise')
 op('layer.duplicate',comp=C,layer=n,newName=outline)
 op('text.set_style',comp=C,layer=outline,applyFill=False,applyStroke=True,strokeWidth=1.65,strokeColor=[1,253/255,243/255])
 op('effect.remove',comp=C,layer=outline,effectIndex=1)
 key(C,outline,O,[c['start'],c['start']+2/24],[0,90],0)
 op('layer.set_track_matte',comp=C,layer=n,matteLayer=matte,matteType='lumaInverted')
 op('layer.move',comp=C,layer=outline,toIndex=1)
# setTrackMatte may enable the matte; keep its own pixels out of the composite.
props(C,matte,enabled=False)
(R.parent/'spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2))
f=R.parent/'make-spec.py';s=f.read_text();needle="(R/'spec.json').write_text";i=s.index(needle)
s=s[:i]+"\n# Ale prefers V01's criterion composition; apply only to this block.\nfor c in cues:\n if c['group']=='criterion':\n  y,size=(655,211) if c['text']=='criterio' else (925,287)\n  c.update(y=y,size=size,color='white',motion='rise',baselineAnchor=True,tracking=-55,masked=True,outlineWidth=1.65,outlineOpacity=90)\n"+s[i:];f.write_text(s)
op('timeline.set_time',comp=C,time=1412/24)
extra=[{'name':'ae_save_project','arguments':{'path':str(R/'Mercadillo-V02.aep')}}]
for fr in [1393,1396,1404,1407,1412,1415,1416]:extra.append({'name':'ae_render_frame','arguments':{'compNameOrId':C,'time':fr/24,'outPath':str(R.parent/'stills'/f'criterion-{fr}.png')}})
extra.append({'name':'ae_comp_info','arguments':{'nameOrId':C}})
save('criterion.json',extra)

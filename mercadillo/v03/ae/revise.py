from native import *
C='V03 CONTENIDO';M='V03 MASTER';plan=json.loads((R.parent/'timeline.json').read_text());spec=json.loads((R.parents[1]/'v02/spec.json').read_text())
rows=[json.loads(s) for s in (R/'import-mix-results.jsonl').read_text().splitlines()];mid=rows[-1]['result']['structuredContent']['result']['id']
op('comp.set_props',comp='V02 MASTER',props={'name':C})
props(C,'MIX — voz foley musica FX',enabled=False,audioEnabled=False)
# Silence shot: same footage, monochrome, exactly the aside's interval.
no='PELILLOS — pausa monocroma';op('layer.duplicate',comp=C,layer='CLIP 04 — Rodaje premium',newName=no);timing(C,no,13.125,14.875,13.125);op('effect.add',comp=C,layer=no,matchName='ADBE Tint',name='Pausa en blanco y negro')
# Purposeful optical accents on the image, keeping captions anchored.
def camera(n,points,anchor=None):
 if anchor:xf(C,n,anchorPoint=anchor,position=anchor)
 key(C,n,S,[t for t,s in points],[[s,s] for t,s in points],75)
camera('CLIP 02 — Precio y velocidad',[(6.20833,103),(6.70,100),(8.125,100),(8.29,105),(8.66,102),(9.2083,102),(9.375,107),(9.83,104),(10.92,104)])
camera('CLIP 05 — Premium, no percebes',[(18.625,100),(21.0833,100),(21.2083,105),(21.50,102),(22.0833,102)])
camera('CLIP 06 — El puesto de creativos',[(22.0833,100),(24.375,100),(24.58,105),(25.05,103),(26.8333,103)])
camera('CLIP 09 — Creativos como churros',[(35.7083,100),(39.6667,100),(39.7917,106),(40.0417,101.5),(43.3333,101.5)])
# Replace the previous YA-only keys: graded escalation throughout the grandmother's request.
n='CLIP 11 — La abuela pide el anuncio'
for i in [3,2,1]:op('keyframe.remove',comp=C,layer=n,property=S,keyIndex=i)
camera(n,[(47.875,100),(48.375,100),(48.58,104),(49.21,104),(49.375,108),(50.375,108),(50.54,111),(51.03,111),(51.15,112),(51.22,112),(51.34,113),(51.39,113),(51.51,114),(52.0,114),(52.17,119),(52.375,117),(52.5,117)],anchor=[660,1000])
# Photographic accent on the word 'literalmente': brief exposure, not a transition over the cut.
rect(C,'RODAJE — destello obturador',540,960,1080,1920,[1,1,1],0,16.6666667,16.875)
key(C,'RODAJE — destello obturador',O,[16.6666667,16.7083333,16.7916667,16.875],[0,19,5,0],0)
# Native glints on relevant words; no glowing box or extra copy.
for n,t,size in [('T026 — premium',19.25,172),('T032 — creativos',24.7916667,174)]:
 op('effect.add',comp=C,layer=n,matchName='CC Light Sweep',name='Acento de revelado');p=['ADBE Effect Parade','Acento de revelado'];key(C,n,p+['CC Light Sweep-0001'],[t,t+.375],[[-430,-size*.34],[430,-size*.34]],65)
 for k,v in [('CC Light Sweep-0004',65),('CC Light Sweep-0005',26),('CC Light Sweep-0006',16),('CC Light Sweep-0007',1.2)]:op('property.set',comp=C,layer=n,property=p+[k],value=v)
# Master pacing: one transform shared by footage, captions, masks and FX.
op('comp.create',name=M,width=1080,height=1920,fps=24,duration=plan['frames']/24)
op('comp.set_props',comp=M,props={'motionBlur':True,'shutterAngle':160,'shutterPhase':-80,'workAreaStart':0,'workAreaDuration':plan['frames']/24})
for i,s in enumerate(plan['segments']):
 n=f"MONTAJE {i+1} — origen {s['sourceIn']} a {s['sourceOut']}";a=s['targetIn']/24;b=s['targetOut']/24;scale=1/s['speed']
 op('layer.create_footage',comp=M,name=n,sourceItemId=34)
 props(M,n,stretch=100*scale)
 timing(M,n,a,b,a-s['sourceIn']/24*scale);props(M,n,audioEnabled=False,frameBlendingType='off',motionBlur=False)
op('layer.create_footage',comp=M,name='V03 — VOZ MUSICA Y EFECTOS',sourceItemId=mid);props(M,'V03 — VOZ MUSICA Y EFECTOS',audioEnabled=True);timing(M,'V03 — VOZ MUSICA Y EFECTOS',0,plan['frames']/24)
op('render.add_to_queue',comp=M,outputPath=str(R.parent/'Mercadillo-V03-master.mov'))
op('render.set_output',queueIndex=2,renderTemplate='Configuración óptima',outputTemplate='Calidad alta',outputPath=str(R.parent/'Mercadillo-V03-master.mov'),timeSpanStart=0,timeSpanDuration=plan['frames']/24)
op('timeline.set_active_comp',comp=M);op('timeline.set_time',comp=M,time=13.4)
def mt(t):
 for s in plan['segments']:
  if s['sourceIn']<=t*24<s['sourceOut']:return (s['targetIn']+(t*24-s['sourceIn'])/s['speed'])/24
 return None
# Store final cue timing and the native content specification together.
final=[]
for c in spec['cues']:
 for s in plan['segments']:
  lo=max(c['start'],s['sourceIn']/24);hi=min(c['end'],s['sourceOut']/24)
  if hi<=lo:continue
  final.append(dict(c,sourceStart=c['start'],sourceEnd=c['end'],start=(s['targetIn']/24+(lo-s['sourceIn']/24)/s['speed']),end=(s['targetIn']/24+(hi-s['sourceIn']/24)/s['speed'])))
(R.parent/'spec.json').write_text(json.dumps({'fps':24,'frames':plan['frames'],'cues':final,'timeline':'timeline.json','sourceContent':'V03 CONTENIDO','preservedCriterionComposition':True},ensure_ascii=False,indent=2))
extra=[{'name':'ae_save_project','arguments':{'path':str(R/'Mercadillo-V03.aep')}}]
for oldt in [6.9,8.4,13.3,14.3,14.8,15.1,16.75,19.5,21.25,24.9,39.8,48.65,49.8,50.65,51.48,52.25,54.2,56.5,58.83,81.9]:
 t=round(mt(oldt)*24)/24;extra.append({'name':'ae_render_frame','arguments':{'compNameOrId':M,'time':t,'outPath':str(R.parent/'stills'/f'f{round(t*24):04d}.png')}})
extra.append({'name':'ae_comp_info','arguments':{'nameOrId':M}})
save('revise.json',extra)

from native import *
C='V02 MASTER';spec=json.load(open(R.parent/'spec.json'))['cues'];mix=json.loads((R/'mix-import-results.jsonl').read_text().splitlines()[1])['result']['structuredContent']['result']['id']
op('layer.create_footage',comp=C,name='MIX — voz foley musica FX',sourceItemId=mix);props(C,'MIX — voz foley musica FX',audioEnabled=True)
nope=next(c for c in spec if c['group']=='nope');n='CLIP 09 — Creativos como churros'
op('layer.duplicate',comp=C,layer=n,newName='REMATE — monocromo')
timing(C,'REMATE — monocromo',nope['start'],43.333333333333,35.708333333333)
op('effect.add',comp=C,layer='REMATE — monocromo',matchName='ADBE Tint',name='Blanco y negro')
a=next(c for c in spec if c['text']=='arte.');n=a['id']+' — '+a['text'];p=['ADBE Effect Parade','Revelado de arte'];key(C,n,p+['CC Light Sweep-0001'],[a['start'],a['start']+.5],[[-420,-80],[420,-80]],68)
for k,v in [('CC Light Sweep-0004',80),('CC Light Sweep-0005',18),('CC Light Sweep-0006',12),('CC Light Sweep-0007',1.3)]:op('property.set',comp=C,layer=n,property=p+[k],value=v)
op('render.set_output',queueIndex=1,renderTemplate='Configuración óptima',outputTemplate='Calidad alta',outputPath=str(R.parent/'Mercadillo-V02-master.mov'),timeSpanStart=0,timeSpanDuration=88.375)
op('timeline.set_active_comp',comp=C);op('timeline.set_time',comp=C,time=49.8)
extra=[{'name':'ae_save_project','arguments':{'path':str(R/'Mercadillo-V02.aep')}}]
for t in [1.45,3.4,8.5,9.7,10.6,12.8,16.9,20.2,23.6,25.9,30.7,38.9,39.8,42.8,46.8,48.6,49.8,50.6,51.48,52.25,56.5,58.8,68.9,71.3,74.8,78.8,81.9,87.9]:
 extra.append({'name':'ae_render_frame','arguments':{'compNameOrId':C,'time':round(t*24)/24,'outPath':str(R.parent/'stills'/f'f{round(t*24):04d}.png')}})
extra.append({'name':'ae_comp_info','arguments':{'nameOrId':C}})
save('finish-build.json',extra)

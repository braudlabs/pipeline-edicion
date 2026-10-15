from native import *
C='V02 MASTER';p=R.parent/'spec.json';spec=json.loads(p.read_text());fix={'T009':('lo único que\nte diferencia',100,1140),'T022':('tus creativos se vean',98,1330),'T024':('como el que\nestás viendo',100,1280),'T029':('Instalaremos una\nmaquinita',100,1295),'T036':('con un buen\noperador detrás',103,1300),'T041':('para que sepa\nutilizarlo',100,1300)}
for c in spec['cues']:
 if c['id'] not in fix:continue
 old=c['text'];s,size,y=fix[c['id']];n=c['id']+' — '+old;c.update(text=s,size=size,y=y);c['aeLayerName']=n
 op('text.set_content',comp=C,layer=n,text=s);op('text.set_style',comp=C,layer=n,fontSize=size,leading=size*.94,autoLeading=False)
 xf(C,n,anchorPoint=[0,-size*.34])
 if c['motion']=='cut':xf(C,n,position=[c['x'],y])
 else:enter(C,n,c['start'],c['x'],y,c['motion'])
p.write_text(json.dumps(spec,ensure_ascii=False,indent=2))
# Keep the six layout corrections in the authoritative generator too.
f=R.parent/'make-spec.py';s=f.read_text();needle="(R/'spec.json').write_text";i=s.index(needle);s=s[:i]+"\n# Optical layout corrections verified in native AE.\nfix="+repr(fix)+"\nfor c in cues:\n if c['id'] in fix:\n  s,size,y=fix[c['id']];c['aeLayerName']=c['id']+' — '+c['text'];c.update(text=s,size=size,y=y)\n"+s[i:];f.write_text(s)
extra=[{'name':'ae_save_project','arguments':{'path':str(R/'Mercadillo-V02.aep')}}]
for t in [7.2,16,18,23.5,28.3,31.8]:extra.append({'name':'ae_render_frame','arguments':{'compNameOrId':C,'time':round(t*24)/24,'outPath':str(R.parent/'stills'/f'refine-{t}.png')}})
save('refine.json',extra)

from pathlib import Path
import json,copy
R=Path(__file__).resolve().parent
s=json.load(open(R/'design.json'));c=s['comps']['MG V2 - Ensamblado'];old=next(n for n in c['layers'] if n['name']=='Resolucion a la toma');n=copy.deepcopy(old);n.update(name='Resultado continuo',pos=[540,820],scale=[.38,.38],**{'from':142,'to':190});n['shadow']=[0,15,20,'#000000',.4];n['anim']={'pos':{'frames':[142,161,189],'values':[[540,820],[540,820],[540,960]],'ease':'out'},'scale':{'frames':[142,161,189],'values':[[.08,.08],[.38,.38],[1,1]],'ease':'out'},'opacity':{'frames':[142,152],'values':[0,1],'ease':'out'}}
c['layers']=[x for x in c['layers'] if x['name'] not in ['Creatividad ensamblada','Resolucion a la toma']]+[n]
changed=[('MG V2 - Ensamblado',['Creatividad ensamblada','Resolucion a la toma'],n)]
for cname,lname,aa,bb in [('MG V2 - Creatividad','Resultado en movimiento',98,110),('MG V2 - Consistencia','Volver a la toma viva',147,161)]:
 n=next(x for x in s['comps'][cname]['layers'] if x['name']==lname);n['anim'].pop('opacity',None);n['opacity']=1;n['anim']['wipe']={'frames':[aa,bb],'values':[100,0],'ease':'out'};changed.append((cname,[lname],n))
(R/'design.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
base=(R/'compile.py').read_text().split('import sys\nnames=')[0];exec(compile(base,str(R/'compile.py'),'exec'))
for c,names,n in changed:
 for name in names:op('layer.delete',comp=c,layer=name)
 compile_layer(c,n)
flush();req.append({'name':'ae_save_project','arguments':{'path':str(R/'AD3-Pipeline-V2.aep')}})
for t in [16.4,18.12,20.8,21.7,26.2,28.1,29.5,34.3,35.5,36.6,40.8]:req.append({'name':'ae_render_frame','arguments':{'compNameOrId':'AD3 - FINAL V2','time':t,'outPath':str(R.parent/'analysis'/f'revision-{t:.2f}.png')}})
(R/'transition-fix.json').write_text(json.dumps(req));print('patch ops',len(req))

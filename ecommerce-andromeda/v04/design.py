from pathlib import Path
import json
p=Path(__file__).parent
cues=json.loads((p.parent/'v01/cues.json').read_text());E=[]
def el(text,start,end,x,y,size=110,weight=700,motion='rise',**kw):
 E.append(dict(id=f'e{len(E):03}',text=text,start=start,end=end,x=x,y=y,size=size,weight=weight,motion=motion,**kw))
def rail(c,size=110,y=None,motion='rise',x=None,width=860):
 el(c['text'],c['start'],c['end'],x or c['x'],y or c['y'],size,700,motion,width=width,sourceWords=c['words'],cue=c['id'])
def stack(c,split,size=190,y=None):
 w=c['words'];y=y or c['y']
 el(' '.join(v['text'] for v in w[:split]),c['start'],c['end'],c['x'],y-86,78,400,'rise',sourceWords=w[:split],cue=c['id'])
 el(' '.join(v['text'] for v in w[split:]),w[split]['frame'],c['end'],c['x'],y+19,size,700,'occlusion',width=920,sourceWords=w[split:],cue=c['id'])
for c in cues:
 id=c['id']
 if id=='c00':rail(c,116)
 elif id=='c01':stack(c,2,185)
 elif id=='c02':rail(c,112,motion='slide')
 elif id=='c03':stack(c,1,185)
 elif id=='c04':rail(c,112)
 elif id=='c05':
  # Same visual hierarchy on both lines, like criterio / visual; no identical small-context pattern.
  for i,w in enumerate(c['words']):el(w['text'],w['frame'],c['end'],540,1034+i*143,190,700,'occlusion',width=900,sourceWords=[w],cue=id)
 elif id=='c06':stack(c,1,208)
 elif id=='c07':rail(c,112)
 elif id=='c08':stack(c,3,182,y=1120)
 elif id=='c09':
  w=c['words'];el('es la misma',191,210,540,1140,112,700,'slide',sourceWords=w[:3],cue=id)
  el('mierda',210,239,540,1105,230,700,'occlusion',width=910,sourceWords=w[3:],cue=id)
 elif id=='c10':rail(c,80,y=1205)
 elif id=='c11':
  el('días',246,263,540,1135,224,700,'occlusion',sourceWords=c['words'][:1],cue=id)
  el('y días',261,275,540,1135,224,700,'occlusion',sourceWords=c['words'][1:],cue=id)
  E[-2]['end']=261
 elif id=='c12':stack(c,3,198,y=1110)
 elif id=='c13':rail(c,114,y=1040,motion='slide')
 elif id=='c14':
  w=c['words'];el('te entregue',318,331,540,1040,114,700,'rise',sourceWords=w[:2],cue=id)
  el('las piezas',331,350,540,1040,124,700,'occlusion',sourceWords=w[2:],cue=id)
 elif id in ['c15','c16','c17']:rail(c,112,y=1190,x=540,motion='slide')
 elif id in ['c18','c19','c20']:
  # The blank fascia above the moving paper is a consistent reading area.
  # Split long phrases into short, full groups instead of hiding the sentence.
  specs={'c15':[('Quieres',0,1),('testear',1,2)],'c16':[('un nuevo',0,2),('ángulo',2,3)],'c17':[(c['text'],0,2)],'c18':[(c['text'],0,1)],'c19':[('para ver',0,2),('el fruto',2,4)],'c20':[(c['text'],0,2)]}
  for text,a,b in specs[id]:
   w=c['words'];end=w[b]['frame'] if b<len(w) else c['end'];el(text,w[a]['frame'],end,775,665,96,700,'slide',width=450,sourceWords=w[a:b],cue=id)
 elif id in ['c21','c22','c23','c24']:rail(c,99,y=775,motion='slide')
 elif id=='c25':rail(c,112,y=1020)
 elif id=='c26':rail(c,152,y=1020,motion='occlusion',width=925)
 elif id=='c27':rail(c,112)
 elif id=='c28':stack(c,2,204,y=1100)
 elif id=='c29':rail(c,112,motion='slide')
 elif id=='c30':rail(c,112)
 elif id=='c31':
  # Fixed caption line above the printed face during the native zoom, not on its eyes/mouth.
  w=c['words'];el('y con la sudadera',692,716,540,740,105,700,'slide',sourceWords=w[:4],cue=id)
  el('de este tío',716,733,540,740,113,700,'rise',sourceWords=w[4:],cue=id)
 elif id=='c32':rail(c,112)
 elif id=='c33':stack(c,2,218,y=1100)
 elif id in ['c34','c35']:rail(c,105,y=780)
 elif id=='c36':rail(c,136,y=780,motion='occlusion',width=920)
 elif id=='c37':rail(c,104,y=430)
 elif id=='c38':rail(c,157,y=430,motion='occlusion',width=900)
 elif id=='c39':
  w=c['words'];el('para un concepto',872,890,540,430,103,700,'rise',sourceWords=w[:3],cue=id)
  el('nuevo',890,900,540,430,144,700,'slide',sourceWords=w[3:],cue=id)
 elif id=='c40':rail(c,116,y=430)
# Ale V04: use the contour/fill resource sparingly, and let the sweatshirt gag play clean.
E=[e for e in E if e['cue']!='c31']
for e in E:
 if e['motion']=='occlusion' and e['cue'] not in ['c05','c09','c33']:
  e['motion']='rise'
# Contour too thin to carry a whole word alone is not acceptable. Final rendering is inspected.
for e in E:
 if e['motion']=='occlusion':
  e['resolveFill']=e['cue'] in ['c01','c03','c05','c06','c11','c12','c14','c28','c33','c36','c38']
(p/'choreography.json').write_text(json.dumps(E,ensure_ascii=False,indent=2))
for c in cues:
 c['kind']='drop' if c['id']=='c31' else 'caption'
 c['reason']='Ale V04: sweatshirt gag without captions, monochrome' if c['id']=='c31' else 'Narration retained'
(p/'cues.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
maskFrames=sorted({f for e in E if e['motion']=='occlusion' for f in range(e['start'],e['end'])})
(p/'study/mask-frames.json').write_text(json.dumps(maskFrames))
print(len(E),'elements;',len(maskFrames),'mask frames; covered words',sum(len(e['sourceWords']) for e in E))

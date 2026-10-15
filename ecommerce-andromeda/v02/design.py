from pathlib import Path
import json
p=Path(__file__).parent
old=json.loads((p.parent/'v01/cues.json').read_text())
E=[]
def el(text,start,end,x,y,size=108,weight=700,motion='rise',**kw):
 E.append(dict(id=f'e{len(E):03}',text=text,start=start,end=end,x=x,y=y,size=size,weight=weight,motion=motion,**kw))
def rail(c,size=None,y=None,motion='rise',width=860):
 # Complete phrase has one anchor. Words enter into reserved positions; existing words never jump.
 el(c['text'],c['start'],c['end'],c['x'],y or c['y'],size or c['size'],700,motion,words=c['words'],width=width)
def stack(c,split,size=170,motion='mask',y=None,weight=400):
 ws=c['words']; y=y or c['y'];first=ws[:split];main=ws[split:]
 el(' '.join(w['text'] for w in first),c['start'],c['end'],c['x'],y-87,76,400,'rise',words=first,width=850)
 el(' '.join(w['text'] for w in main),main[0]['frame'],c['end'],c['x'],y+19,size,weight,motion,words=main,width=850)
for c in old:
 id=c['id']
 if id=='c00':rail(c,112,motion='rise')
 elif id=='c01':stack(c,2,174)
 elif id=='c02':rail(c,112,motion='slide')
 elif id=='c03':rail(c,140,motion='wipe')
 elif id=='c04':rail(c,110,motion='rise')
 elif id=='c05':
  # Two equal-sized words accumulated into a compact line, shared anchor with surrounding captions.
  rail(c,128,motion='slide')
 elif id=='c06':stack(c,1,190,motion='mask')
 elif id=='c07':rail(c,110,motion='rise')
 elif id=='c08':stack(c,3,176,motion='wipe',y=1130)
 elif id=='c09':
  short={**c,'text':'es la misma','end':210,'words':c['words'][:3]};rail(short,112)
  el('mierda',210,239,540,1105,204,700,'impact',duration=5)
 elif id=='c10':rail(c,78,y=1201,motion='slide')
 elif id=='c11':el('días',246,275,540,1135,198,400,'roll',change=263,join=261)
 elif id=='c12':rail(c,108,motion='rise')
 elif id in ['c13','c14']:
  # Native hand/object reaches centre; preserve original omission, full narrator remains.
  continue
 elif id in ['c15','c16','c17','c19','c20']:continue
 elif id=='c18':el('semanas',401,416,775,665,98,700,'wipe',width=450)
 elif id in ['c21','c22']:rail(c,96,motion='slide')
 elif id=='c23':rail(c,96,motion='fall')
 elif id=='c24':rail(c,103,motion='rise')
 elif id=='c25':rail(c,112,motion='rise')
 elif id=='c26':rail(c,150,motion='impact')
 elif id=='c27':rail(c,108,motion='slide')
 elif id=='c28':stack(c,2,176,motion='mask',y=1100)
 elif id=='c29':rail(c,108,motion='rise')
 elif id=='c30':rail(c,112,motion='slide')
 elif id=='c31':continue
 elif id=='c32':rail(c,110,motion='rise')
 elif id=='c33':stack(c,2,194,motion='mask',y=1100,weight=700)
 elif id in ['c34','c35']:rail(c,102,motion='slide')
 elif id=='c36':rail(c,123,motion='wipe')
 elif id=='c37':rail(c,102,motion='rise')
 elif id=='c38':rail(c,147,motion='impact')
 elif id=='c39':
  a={**c,'text':'para un concepto','end':890,'words':c['words'][:3]};rail(a,100,motion='rise')
  el('nuevo',890,900,540,430,140,400,'wipe')
 elif id=='c40':rail(c,112,motion='slide')
(p/'cues.json').write_text(json.dumps(old,ensure_ascii=False,indent=2))
(p/'choreography.json').write_text(json.dumps(E,ensure_ascii=False,indent=2))
print(len(E),'authored elements')

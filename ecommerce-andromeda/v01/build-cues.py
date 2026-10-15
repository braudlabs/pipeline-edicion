import json,math
from pathlib import Path
p=Path(__file__).resolve().parent
words=json.loads((p/'study/aligned-words.json').read_text())['words']
phrases=[
('Si eres dueño','rail'),('de un ecommerce','rail'),('ya sabes que','rail'),('con Andrómeda','rail'),('necesitas','rail'),('anuncios nuevos','rail'),('cada semana','punch'),
('Y sabes que','rail'),('de la forma tradicional','rail'),('es la misma mierda','rail'),('de siempre','rail'),('días y días','days'),('para que el editor','rail'),('o una agencia','drop'),('te entregue las piezas','drop'),
('Quieres testear','rail'),('un nuevo ángulo','rail'),('y necesitas','rail'),('semanas','rail'),('para ver el fruto','rail'),('de eso','rail'),
('Y durante','rail'),('todo ese proceso','rail'),('ya se te han caído','rail'),('los ads antiguos','rail'),('y venga a repetir','rail'),('otra puta vez','punch'),
('No vengo a hablarte','rail'),('de tu problema','rail'),('ya tienes suficiente','rail'),('con eso','rail'),('y con la sudadera de este tío','drop'),('Vengo a hablarte','rail'),('de la solución','rail'),
('Instalaremos','rail'),('en tu tienda','rail'),('esta maquinita','rail'),('Le pedirás','rail'),('cinco ads','rail'),('para un concepto nuevo','rail'),('te los dará','rail')]
cues=[];idx=0
for i,(text,kind) in enumerate(phrases):
 ws=words[idx:idx+len(text.split())];assert ' '.join(w['text'] for w in ws)==text,(i,ws,text);idx+=len(ws)
 t=ws[0]['start']; y=1120; x=540; size=108 if kind=='rail' else 140
 if 5.416<=t<14.584:y=1140
 if 14.584<=t<18.75:
  # Only the time cost reads on the unoccupied machine panel; the paper action stays clear.
  if text=='semanas':x=850;y=1190;size=72
  else:kind='drop'
 if 18.75<=t<23:y=775;size=90
 if 23<=t<25.417:y=1040;size=126
 if 25.417<=t<32.583:y=1100
 if t>=32.583:y=780;size=94
 if t>=35:y=430;size=94
 # No extra full-screen title; complete physical gags keep their image and sound.
 cues.append({'id':f'c{i:02d}','text':text,'kind':kind,'start':math.ceil(t*24),'end':0,'x':x,'y':y,'size':size,'words':[dict(w,frame=math.ceil(w['start']*24)) for w in ws],'reason':'Visual action priority: hook reaction/shirt, small delivered object or sweatshirt gag; full voice and sidecar transcript preserved.' if kind=='drop' else 'Persistent phrase anchor; retain native action.'})
assert idx==len(words)
for i,c in enumerate(cues):
 following=cues[i+1]['start'] if i+1<len(cues) else 920
 c['end']=min(following,math.ceil((c['words'][-1]['end']+.16)*24),920)
 if c['text']=='cada semana':c['end']=min(c['end'],130)
 if c['kind']=='days':c['end']=cues[i+1]['start']
(p/'cues.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
def tc(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
(p/'narrador-completo-del-tramo.srt').write_text('\n'.join(f'{i+1}\n{tc(c["start"]/24)} --> {tc(c["end"]/24)}\n{c["text"]}\n' for i,c in enumerate(cues)))
print(len(cues),'cues',len(words),'aligned words')

from pathlib import Path
import json, re
p=Path(__file__).parent
cream='#fffdf3';lime='#d7f58c'
cues=[]
def cue(text,start,end,x=540,y=1200,size=110,**kw):
    cues.append(dict(id=f'c{len(cues):03d}',text=text,start=start,end=end,x=x,y=y,size=size,color=cream,weight=700,motion='direct',**kw))
def custom(text,start,end,x=540,y=1200,size=110,**kw):
    item=dict(id=f'c{len(cues):03d}',text=text,start=start,end=end,x=x,y=y,size=size,color=cream,weight=700,motion='settle',role='emphasis')
    item.update(kw);cues.append(item)

# Semantic groups keep a common lifetime and coordinated exit.
custom('Si eres',.05,.36,y=990,size=105,color=lime,group='hook',out='fade')
custom('Si eres una',.36,1.72,y=990,size=105,color=lime,motion='direct',group='hook',out='fade')
custom('agencia',.54,1.72,y=1225,size=242,color=lime,group='hook',out='fade')
custom('de contenido',.96,1.72,y=1380,size=116,color=lime,motion='sweep',group='hook',out='fade')
custom('precio',7.79,10.82,y=955,size=248,color=lime,group='tradeoff')
custom('y qué tan',8.18,8.65,y=1160,size=96,color=lime,motion='direct',group='tradeoff')
custom('rápido',8.65,10.82,y=1350,size=244,color=lime,motion='sweep',group='tradeoff')
for text,start,end in [('puedes',9.05,9.45),('sacar',9.45,9.78),('los creativos.',9.78,10.82)]:
    custom(text,start,end,y=1140,size=106,motion='direct',group='tradeoff')
custom('tenemos tu',11.77,13.04,y=1080,size=100,color=lime,motion='soft',group='solution')
custom('solución.',12.31,13.04,y=1300,size=232,color=lime,group='solution')
custom('premium',18.86,20.84,y=1200,size=219,group='premium')
for text,start,end in [('calidad',18.74,19.30),('que trae',19.30,19.74),('clientes',19.74,20.84)]:
    custom(text,start,end,y=980,size=103,motion='direct',group='premium')
custom('no',20.84,21.8,x=216,y=1420,size=96,motion='direct',group='percebe')
custom('percebes.',21.03,21.8,x=638,y=1420,size=159,motion='snap',group='percebe')
custom('genera',23.82,26.70,y=405,size=187,group='produce')
custom('creativos',24.25,26.70,y=1505,size=210,group='produce')
for text,start,end in [('casi listos',24.88,25.58),('para publicar.',25.58,26.70)]:
    custom(text,start,end,y=1290,size=104,motion='direct',group='produce')
custom('formaremos',29.11,30.95,y=1305,size=145,motion='sweep',group='team')
custom('personalmente',29.71,30.44,y=1450,size=112,motion='direct',group='team')
custom('a tu equipo.',30.44,30.95,y=1480,size=159,group='team')
# The extreme close-up fills the frame with a face. Let the delivery and musical
# drop carry this beat rather than putting type over the mouth.
custom('10',38.42,39.31,x=674,y=980,size=345,motion='drop',group='minutes')
custom('minutos',38.85,39.31,x=674,y=1115,size=123,motion='direct',group='minutes')
custom('¡BOOM!',39.31,40.04,y=1235,size=227,motion='punch',group='boom')
custom('creativos',40.30,41.20,y=1305,size=147,motion='soft',group='churros')
custom('como churros.',40.52,41.20,y=1480,size=147,motion='sweep',group='churros')
custom('Ni de coña.',42.16,43.14,y=1430,size=171,motion='snap',group='nope')
custom('Hazme un anuncio',47.94,48.53,y=1270,size=106,color=lime,motion='soft',group='grandma')
custom('hiperrealista',48.53,49.80,y=1430,size=158,color=lime,motion='sweep',group='grandma')
custom('UGC,',49.80,50.21,y=1430,size=165,color=lime,motion='direct',group='grandma')
for x,start,end in [(285,50.21,51.16),(540,50.47,51.16),(795,50.73,51.16)]:
    custom('bla,',start,end,x=x,y=1430,size=143,color=lime,motion='snap',group='blah')
custom('¡pero',51.16,52.22,x=306,y=1290,size=117,color=lime,motion='direct',group='now')
custom('YA!',51.61,52.22,x=620,y=1485,size=329,color=lime,motion='punch',group='now')
custom('criterio',58.18,59.12,y=655,size=211,masked=True,group='criterion')
custom('visual.',58.64,59.12,y=925,size=287,masked=True,group='criterion')
custom('La IA es un',67.84,69.28,y=1380,size=103,motion='direct',group='translator')
custom('traductor.',68.13,69.28,y=1580,size=182,motion='sweep',group='translator')
custom('ideas de',69.72,70.64,y=1380,size=107,motion='direct',group='bad')
custom('mierda.',70.15,71.60,y=1580,size=222,motion='punch',group='bad')
custom('sacas',70.64,71.60,y=1380,size=107,motion='direct',group='bad')
custom('conceptos',72.03,73.41,y=1320,size=105,motion='soft',group='good')
custom('con criterio.',72.59,73.41,y=1520,size=168,motion='sweep',group='good')
custom('obras de',73.78,74.80,x=329,y=1070,size=103,motion='soft',group='art')
custom('arte.',74.16,74.80,y=1390,size=336,color=lime,masked=True,motion='settle',group='art')
custom('agenda ya una',80.62,81.74,y=555,size=87,motion='soft',group='call')
custom('llamada.',81.28,81.74,y=770,size=206,motion='settle',group='call')
custom('Y si no,',86.83,87.21,y=1060,size=114,motion='direct',group='end')
custom('también.',87.21,88.22,y=1060,size=172,motion='settle',group='end')

exclude=[(0,1.72),(7.79,10.83),(11.77,13.05),(18.74,21.82),(23.82,26.71),(29.11,30.96),(33.70,35.31),(38.42,40.04),(40.30,41.21),(42.16,43.15),(47.88,56.46),(58.18,59.13),(61.60,65.53),(67.84,69.29),(69.72,71.61),(72.03,73.42),(73.78,74.80),(80.62,81.75),(86.83,88.38)]
def excluded(t):return any(a<=t<b for a,b in exclude)
def baseline(t):
    for end,y in [(13.125,1150),(18.625,1400),(22.084,1420),(26.834,1330),(32.584,1410),(35.709,1480),(43.334,1410),(52.5,1430),(61.334,1480),(67.751,1340),(71.917,1580),(77.75,1510),(80.542,1460),(89,1060)]:
        if t<end:return y
data=json.loads((p/'study/words.json').read_text())['transcription']
words=[{'text':s['text'].strip(),'start':s['offsets']['from']/1000,'end':s['offsets']['to']/1000} for s in data if s['text'].strip()]
# Repair a few zero-duration ASR words against local phrase boundaries; marked as editorial alignment.
repairs={('Vamos',14.92):(14.66,14.92),('Instalaremos',22.98):(22.16,22.70),('una',22.98):(22.70,22.98),('No',35.82):(35.72,35.77),('te',35.82):(35.77,35.82),('La',67.84):(67.78,67.84),('Si',71.90):(71.82,71.90),('Y',74.98):(74.85,74.98),('Ese',77.72):(77.61,77.72)}
for w in words:
    if (w['text'],w['start']) in repairs:w['start'],w['end']=repairs[(w['text'],w['start'])]
    w['text']=w['text'].replace('Encaje','encaje').replace('Premium','premium').replace('Pelillos','pelillos')
words=[w for w in words if not excluded(w['start']) and w['end']>w['start']]
i=0
while i<len(words):
    w=words[i];text=w['text'];start=w['start'];end=w['end'];i+=1
    # Connect articles/prepositions and short phonetic fragments to a readable unit.
    while i<len(words) and (len(text)<6 or end-start<.17) and words[i]['start']-end<.08 and not excluded((end+words[i]['start'])/2) and len(text+' '+words[i]['text'])<=23 and baseline(start)==baseline(words[i]['start']):
        text+=' '+words[i]['text'];end=words[i]['end'];i+=1
    first=not cues or start<.1
    for a,b in exclude:
        if start<a<end:end=a
    size=106 if len(text)<18 else 96
    color=lime if start<13.125 else cream
    cues.append(dict(id=f'c{len(cues):03d}',text=text,start=start,end=end+.025,x=540,y=baseline(start),size=size,color=color,weight=700,motion='direct',role='rail'))
cues.sort(key=lambda c:(c['start'],c['id']))
(p/'cues.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
(p/'study/alignment-repairs.json').write_text(json.dumps([{'word':key[0],'ASRStart':key[1],'editorialRange':value} for key,value in repairs.items()],ensure_ascii=False,indent=2))
print(len(cues),'caption elements')

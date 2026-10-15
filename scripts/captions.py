import json,pathlib,re,wave,numpy as np
root=pathlib.Path(__file__).resolve().parents[1]
clips=json.loads((root/'src/clips.json').read_text())
phrases=[
'La IA creativa|debería hacerte|producir más rápido|y te lo|digo yo|que literalmente|soy la prueba|de ello',
'Pero a mucha|gente le está|pasando exactamente|lo contrario',
'Abres una app|generas|no sale bien|vuelves a generar|cambias el prompt|pruebas otra app',
'Y cuando|por fin tienes|algo que puedes|utilizar|has gastado horas|y un montón|de créditos',
'Eso puede|dar igual|si estás jugando|con IA|por curiosidad',
'Pero si tienes|una agencia|una marca|o produces contenido|para clientes|cada generación fallida|es dinero|y tiempo|que estás tirando',
'El problema|no es simplemente|qué herramienta utilizas',
'Es saber|qué proceso seguir|para llegar|al resultado|que buscas|con muchas menos|iteraciones',
'Nosotros llevamos meses|trabajando de esta forma|y hemos utilizado|estos sistemas|para crear y escalar|dos cuentas completas|basadas en avatares|generados con IA',
'Por eso creamos|Visual Hub',
'Dentro encontrarás|plantillas y sistemas|listos para utilizar|y enseñamos cómo|trabajamos realmente',
'Cómo planteamos|las generaciones|cómo conseguimos|consistencia|cómo evitamos|resultados artificiales|y cómo reducimos|todo ese|prueba y error',
'Está pensado especialmente|para personas|que quieren utilizar|IA creativa|dentro de un negocio|o con clientes',
'Puedes entrar|a Visual Hub|por 39 dólares'
]
emphasis={'rápido','prueba','contrario','generas','bien','generar','prompt','horas','créditos','curiosidad','agencia','marca','clientes','fallida','dinero','tiempo','problema','proceso','resultado','iteraciones','sistemas','consistencia','artificiales','error','negocio'}
captions=[];allwords=[]
for clip,line in zip(clips,phrases):
    n=clip['id'];p=root/f'analysis/whisper-python/{n:02d}.json'
    raw=[w for s in json.loads(p.read_text())['segments'] for w in s['words']]
    expected=line.replace('|',' ').split()
    if len(raw)!=len(expected):
        print('MISMATCH',n,len(raw),len(expected),[w['word'] for w in raw]);continue
    # Fix known recognition spellings against the full large-v3 transcript/brief.
    for w,text in zip(raw,expected):w['word']=text
    # Whisper's initial word may include pre-speech room tone. These onsets
    # were checked on the source waveform, in the uncompressed time base.
    if n==1:raw[0]['start']=0.44
    if n==10:raw[0]['start']=1.64
    if n==14:raw[0]['start']=0.44
    if n==1:raw[8]['start']=3.57
    cursor=0
    for phrase in line.split('|'):
        count=len(phrase.split());group=raw[cursor:cursor+count];cursor+=count
        start=clip['from']+round(group[0]['start']*24)
        end=min(clip['from']+clip['duration'],clip['from']+round(group[-1]['end']*24)+3)
        worddata=[{'text':w['word'],'from':clip['from']+round(w['start']*24),'to':clip['from']+max(round(w['start']*24)+1,round(w['end']*24))} for w in group]
        allwords.extend(worddata)
        clean=phrase.split()[-1].lower()
        captions.append({'from':start,'to':max(start+1,end),'words':worddata,'emphasis':clean in emphasis,'clip':n})
for i,c in enumerate(captions[:-1]):c['to']=min(c['to'],captions[i+1]['from'])
# Keep the last cost keyword visible until the next source shot.
[c for c in captions if c['clip']==4][-1]['to']=532
(root/'src/captions.json').write_text(json.dumps(captions,ensure_ascii=False,indent=2))
(root/'analysis/words-final.json').write_text(json.dumps(allwords,ensure_ascii=False,indent=2))
print(len(captions),'caption groups;',len(allwords),'words; last',allwords[-1])

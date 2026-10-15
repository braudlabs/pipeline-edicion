exec(compile(open(__file__.replace('captions.py','helpers.py')).read(),__file__,'exec'))
S=json.load(open(R/'ae/design.json'));T=json.load(open(R/'remotion/src/timeline.json'));c=S['comps'][S['master']]
# Phrase boundaries checked against source word timings; orthography corrected against the supplied script.
chunks={
1:[(.08,1.48,'Tengo que revelarte algo'),(2.40,2.70,'No'),(3.24,3.92,'Este anuncio'),(3.92,4.50,'no solo'),(4.50,5.22,'se ha hecho con IA'),(5.90,6.54,'sino que además'),(6.54,7.65,'se ha montado solo')],
2:[(.10,1.22,'Esta persona'),(1.22,1.91,'no es real'),(2.54,3.60,'Este escenario tampoco')],
3:[(.1,1.08,'Estos planos'),(1.08,1.84,'no se han grabado'),(2.78,3.65,'Y esta voz tampoco')],
4:[(.1,1.08,'Hasta los cortes'),(1.08,2.02,'y los subtítulos'),(2.02,2.84,'se ensamblan'),(2.84,3.92,'automáticamente')],
5:[(.27,1.25,'No son clips sueltos'),(1.34,1.86,'personaje'),(2.08,2.44,'escenas'),(2.58,2.75,'voz'),(2.75,3.42,'y montaje'),(3.60,4.68,'Una creatividad completa')],
6:[(.1,1.30,'Generar con IA'),(1.30,2.18,'es fácil'),(2.78,3.80,'Lo difícil es'),(3.80,4.72,'que todo encaje')],
7:[(.1,.99,'Misma persona'),(1.20,1.77,'mismo look'),(2.18,3.08,'Sin volver a empezar'),(3.08,3.81,'con cada plano')],
8:[(.05,.98,'En Visual Hub'),(.98,2.09,'compartimos los sistemas'),(2.09,2.91,'para producir'),(2.91,3.47,'imágenes'),(3.66,4.00,'vídeos'),(4.20,4.67,'avatares'),(4.67,5.32,'y anuncios'),(5.32,5.84,'con IA')],
9:[(.1,1.27,'Si tienes una agencia'),(1.46,1.89,'una marca'),(1.89,3.24,'o produces para clientes'),(3.30,3.94,'necesitas una'),(3.94,4.73,'línea de producción')],
10:[(0,1.10,'Entra en Visual Hub'),(1.60,2.96,'39 dólares al mes'),(3.00,4.90,'Puedes cancelar cuando quieras')]
}
def mapped(clip,a,b):
 out=[]
 for s in T['video']:
  if s['clip']!=clip:continue
  aa=max(a*48,s['sourceFrame']);bb=min(b*48,s['sourceEnd'])
  if bb>aa:out.append((round(s['from']+aa-s['sourceFrame']),round(s['from']+bb-s['sourceFrame'])))
 return out
records=[];num=0
for clip,groups in chunks.items():
 for a,b,text in groups:
  for fr,to in mapped(clip,a,b):
   if to<=fr:continue
   rec={'clip':clip,'from':fr,'to':to,'text':text,'burned':True};records.append(rec)
   # Close whispered opening fills the frame with the face. Keep this beat clean; full SRT carries its words.
   if (clip==1 and a<2) or clip==10:rec['burned']=False;rec['reason']='Face-filled whisper' if clip==1 else 'Native offer typography';continue
   segments=[(fr,to)]
   for e in S['events'].values():
    if e.get('dropCaptions'):
     new=[]
     for aa,bb in segments:
      if bb<=e['from'] or aa>=e['to']:new.append((aa,bb))
      else:
       if aa<e['from']:new.append((aa,e['from']))
       if bb>e['to']:new.append((e['to'],bb))
     segments=new
   if not segments:rec['burned']=False;rec['reason']='Phrase represented by motion';continue
   for aa,bb in segments:
    num+=1;graphic=next((e for e in S['events'].values() if e['from']<=aa<e['to']),None)
    y=graphic.get('captionY',1390) if graphic else {1:1425,2:1415,3:1400,4:1415,5:1360,6:1365,7:1390,8:1340,9:1400}.get(clip,1380)
    color=INK if graphic or clip in [5,8] else CREAM
    size=68 if text in ['no es real','es fácil','automáticamente','mismo look','que todo encaje'] else 61
    while word_width(text,size)>860:size-=1
    words=text.split();gap=word_width(' ',size);total=sum(word_width(w,size) for w in words)+gap*(len(words)-1);xx=540-total/2
    axis='y' if num%3==0 else 'x';delta=48 if axis=='y' else (-52 if num%3==1 else 52)
    for j,w in enumerate(words):
     width=word_width(w,size);start=min(bb-2,aa+j*2);end=min(bb-1,start+10)
     n=txt(c,f'SUB {num:02d}.{j+1} {w}',w,xx+width/2,y,size,color,start,bb,shadow=[0,2,3,CREAM if color==INK else '#191915',.4 if color==INK else .65],textStroke=[CREAM if color==INK else '#302a26',.6 if color==INK else 1.2])
     if end>start:enter(n,start,end-start,axis,delta,2.5)
     xx+=width+gap
(R/'analysis/captions.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));(R/'ae/design.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
def ts(f):
 ms=round(f/48*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
(R/'output/AD3-Pipeline.srt').write_text('\n\n'.join(f"{i+1}\n{ts(x['from'])} --> {ts(x['to'])}\n{x['text']}" for i,x in enumerate(records))+'\n')
print('Caption phrases',len(records),'native groups',num)

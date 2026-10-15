from native import *
init=json.loads((R/'init-results.jsonl').read_text().splitlines()[1])['result']['structuredContent']['result']['results'];ids={r['name']:r['id'] for r in init if 'id'in r}
for c in ['DESIGN A — VOICE','DESIGN B — QUOTE','DESIGN C — DIALOGUE']:footage(c,'ABUELA',ids['SOURCE 11'],47.875,52.5,47.875)
c='DESIGN A — VOICE'
text(c,'Pedido','un anuncio',540,1150,102)
text(c,'Cualidad','hiperrealista',540,1280,134,LIME)
rect(c,'Capsula voz',540,1450,350,94,INK,47)
ellipse(c,'Micro',418,1450,62,62,LIME)
rect(c,'Capsula micro',418,1445,12,27,INK,6)
path(c,'Arco micro',[[405,1443],[405,1460],[418,1465],[431,1460],[431,1443]],3,INK)
path(c,'Base micro',[[418,1465],[418,1473],[410,1473],[426,1473]],3,INK)
for i,h in enumerate([18,36,50,28,62,42,22]):rect(c,'Onda '+str(i),480+i*24,1450,9,h,LIME,4)
c='DESIGN B — QUOTE'
text(c,'Comillas','“',218,1120,290,LIME)
text(c,'Pedido','Hazme un anuncio',540,1250,99)
text(c,'Cualidad','hiperrealista',540,1364,128)
c='DESIGN C — DIALOGUE'
rect(c,'Prompt',540,1330,880,335,[.92,.94,.89],36)
text(c,'Pedido','Hazme un anuncio',540,1245,79,INK,font='SFProDisplay-Regular')
text(c,'Cualidad','hiperrealista.',540,1380,132,INK)
path(c,'Cursor',[[943,1300],[943,1410]],4,INK)
extra=[{'name':'ae_save_project','arguments':{'path':str(R/'Mercadillo-V02.aep')}}]+[{'name':'ae_render_frame','arguments':{'compNameOrId':c,'time':49.8,'outPath':str(R.parent/'stills'/('design-'+a+'.png'))}} for a,c in zip('ABC',['DESIGN A — VOICE','DESIGN B — QUOTE','DESIGN C — DIALOGUE'])]
save('design.json',extra)

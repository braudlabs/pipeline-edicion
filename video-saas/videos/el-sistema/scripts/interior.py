# Executed inside design.py: a single continuous native composition.
board=comp('02A - Sistema interior',5400,2900);bg(board)
# Routing first, behind every station.
for k,pts in enumerate([[[1490,660],[1810,660]],[[3090,660],[3470,660]],[[4800,650],[5190,650],[5190,1920],[5060,1920]],[[3800,2010],[3380,2010]],[[1590,2010],[1410,2010]],[[750,1470],[750,1120]]]):
 line(board,'Ruta '+str(k),pts,col='#57503A',width=3)
for x in range(150,5350,150):
 for y in range(100,2880,150):
  # Fine drafting grid, sparse enough to stay quiet.
  rect(board,f'Punto {x} {y}',x,y,2,2,'#232427',round=0)
def station(c,idx,x,y,w,h,title):
 rect(c,idx+' panel',x,y,w,h,P,stroke=LINE,round=32)
 tx(c,idx,x+44,y+70,24,col=Y,track=150)
 tx(c,title,x+110,y+77,42,font='HelveticaNeue-Medium')
 line(c,idx+' separador',[[x+42,y+111],[x+w-42,y+111]],col='#343434',width=1)
def tick(c,name,x,y,a,col=GREEN):
 return line(c,name,[[x,y],[x+14,y+14],[x+44,y-22]],a,D,col,5)
# 01: Confirmation is actual dialogue, no fictitious credit price.
station(board,'01',220,200,1320,920,'La idea')
rect(board,'Mensaje usuario',650,360,814,180,'#23211B',round=26)
tx(board,'Un anuncio de esta chaqueta.',690,425,38)
tx(board,'Modelo y detalles del denim.',690,478,38)
tx(board,'EL SISTEMA',285,644,22,col=Y,font='HelveticaNeue-Bold',track=120)
for j,s in enumerate(['Una prenda. Cinco planos.', 'Mismo personaje, mismo producto.']):
 reveal(tx(board,s,285,728+j*60,43,16.30,D,font='HelveticaNeue-Medium'),16.30+j*.12,dy=28)
rect(board,'Presupuesto antes de generar',285,918,740,93,'#1F1E19',18.15,D,stroke='#6C5A26',round=19)
tx(board,'Coste previsto antes de generar',318,976,31,18.15,D,col=Y)
rect(board,'Confirmar propuesta',1100,918,360,93,Y,19.02,D,round=19)
tx(board,'Confirmar',1280,977,32,19.02,D,col='#141200',align='center',font='HelveticaNeue-Bold')
tick(board,'Idea confirmada',1394,850,19.90)
# 02: five real shots from the actual own dossier.
station(board,'02',1810,200,1320,920,'Del guion a cinco escenas')
shots=['La chaqueta en uso','Textura de la sarga','Botón metálico','Etiqueta interior','Costura del puño']
for j,s in enumerate(shots):
 y=355+j*137;t=20.70+j*.14
 rect(board,f'Escena {j+1}',1853,y,1227,114,'#1B1C1D',t,D,stroke='#343535',round=17)
 reveal(tx(board,f'0{j+1}',1890,y+69,30,t,D,col=Y,track=70),t,dx=22,dy=0)
 tx(board,s,2000,y+69,38,t,D)
 tx(board,'7 s' if j==0 else '4 s',3025,y+69,28,t,D,col=SOFT,align='right')
# 03: lock identity with the hero photograph; texture evidence keeps the prenda concrete.
station(board,'03',3470,200,1360,920,'Referencias que se mantienen')
pic(board,'Personaje y prenda anclados','denim-01.jpg',3815,708,320,0,D)
for j,(s,im) in enumerate([('Producto','denim-02.jpg'),('Detalles','denim-03.jpg')]):
 pic(board,s+' fotografía',im,4250+j*330,623,238)
 tx(board,s,4250+j*330,878,30,col=SOFT,align='center')
for j,(s,x) in enumerate([('Personaje',3655),('Producto',4032),('Estética',4409)]):
 t=22.75+j*.54;rect(board,s+' lock',x,975,332,72,'#24251F',t,D,stroke='#555D42',round=15)
 tx(board,s,x+32,1022,26,t,D);tick(board,s+' check',x+256,1010,t+.18)
tx(board,'Una misma prenda, en todos los planos.',4145,1168,33,24.0,D,col=SOFT,align='center')
# 04: actual models used for this piece, prompt content deliberately unrecoverable.
station(board,'04',3800,1500,1360,970,'El modelo adecuado para cada plano')
rect(board,'Modelo imagen',3850,1660,579,178,'#20211F',stroke='#4B5141',round=20)
tx(board,'ANCLA',3882,1707,20,col=SOFT,track=100)
tx(board,'Soul 2.0',3882,1779,51,font='HelveticaNeue-Medium')
rect(board,'Modelo vídeo',4470,1660,637,178,'#242116',stroke='#6F5B1F',round=20)
tx(board,'VÍDEO',4502,1707,20,col=Y,track=100)
tx(board,'Seedance 2.5',4502,1779,48,font='HelveticaNeue-Medium')
line(board,'Modelo hacia instrucciones',[[4456,1852],[4456,1905]],27.3,D,Y,2)
rect(board,'Instrucciones abstractas',3850,1906,1255,483,'#101112',stroke=LINE,round=20)
for j in range(11):
 y=1960+j*34
 tx(board,f'{j+1:02}',3880,y+10,16,col='#716C5C',track=80)
 for k in range(3):
  w=[220,130,265,180,100][(j+k)%5];x=3940+k*341
  n=rect(board,f'Trama de instrucción {j}-{k}',x,y,w,8,'#776839' if (j+k)%4==0 else '#3F4140',27.7+j*.12+k*.06,D,round=3)
  reveal(n,27.7+j*.12+k*.06,dx=18,dy=0,d=.25)
# 05: images become actual footage after approval.
station(board,'05',1570,1440,1850,1160,'El mapa completo')
for j in range(5):
 x=1760+j*327
 tx(board,f'0{j+1}',x-140,1660,24,col=Y,track=130)
 rect(board,f'Marco plano {j}',x-147,1686,294,543,'#222325',stroke='#44433D',round=8)
 pic(board,f'Fotograma plano {j}',f'denim-{j+1:02}.jpg',x,1958,285,0,35.34)
 n=pic(board,f'Plano animado {j}',f'denim-{j+1:02}.mp4',x,1958,285,35.34,D);n['freezeTail']=True
 tx(board,['Try-on','Sarga','Botón','Etiqueta','Puño'][j],x,2281,29,col=SOFT,align='center')
rect(board,'Botón aprobar mapa',2205,2394,610,102,Y,0,35.34,round=23)
tx(board,'Aprobar y animar',2510,2460,38,0,35.34,col='#141200',font='HelveticaNeue-Bold',align='center')
rect(board,'Estado animando',2205,2394,610,102,'#21271E',35.34,D,stroke='#576349',round=23)
tx(board,'Planos en movimiento',2510,2460,34,35.34,D,col=GREEN,align='center')
cursor(board,'Aprobación mapa',[[3200,2530],[2710,2450],[2710,2450],[2920,2720]],[33.4,34.10,34.3,34.95],33.4,35.12)
# 06: distinguish the documented diction rejection from good footage.
station(board,'06',80,1450,1320,1160,'Solo avanza lo que está a la altura')
pic(board,'Toma en revisión','denim-01.jpg',410,1990,345)
rect(board,'Dicción necesita revisión',211,2340,398,86,'#28211B',36.6,D,stroke='#755A38',round=18)
tx(board,'Dicción · revisar',410,2396,29,36.6,D,col='#DAB784',align='center')
line(board,'Selección revisada',[[629,1985],[812,1985]],36.6,D,Y,3)
for j in range(3):
 n=pic(board,f'Tomas aprobadas {j}',f'denim-{j+2:02}.jpg',1050+j*35,1990+j*25,300,37.3+j*.15,D)
 reveal(n,37.3+j*.15,dx=65,dy=0,d=.5)
rect(board,'Aprobado estado',861,2370,400,86,'#20291D',38.45,D,stroke='#465D3A',round=18)
tx(board,'Selección aprobada',1061,2426,29,38.45,D,col=GREEN,align='center')
# Peripheral memory: relevant structure is visible in the wide view.
for j,(t,sub) in enumerate([('Marca','Tono y estilo'),('Dossier','Versiones y archivos'),('Referencias','Personaje · producto'),('Validación','Antes de avanzar')]):
 x=1850+j*790;rect(board,'Memoria '+t,x,1210,700,145,'#0E1010',stroke='#242725',round=19)
 tx(board,t,x+30,1263,28,col=SOFT);tx(board,sub,x+30,1310,25,col='#666A64')
# One camera path across the same plane: wide > detail > move > settle.
inside=comp('02 - Recorrido interior');bg(inside)
n=nested(inside,'Cámara del sistema',board['name'],0,0,14.30,42.08,1,[0,0])
views=[(14.30,2700,1450,.62),(15.10,2700,1450,.33),(15.48,2700,1450,.33),(16.30,880,670,.96),
 (20.43,880,670,.96),(20.93,2460,660,.98),(22.25,2460,660,.98),(22.82,4140,685,.94),
 (26.91,4140,685,.94),(27.52,4480,1985,.98),(31.83,4480,1985,.98),(32.33,2495,2020,.85),
 (36.11,2495,2020,.85),(36.62,750,2020,.89),(40.67,750,2020,.89),(41.62,2700,1450,.32),(42.08,2700,1450,.30)]
anim(n,'scale',[v[0] for v in views],[[v[3],v[3]] for v in views],'flow')
anim(n,'pos',[v[0] for v in views],[[960-v[1]*v[3],540-v[2]*v[3]] for v in views],'flow')
# Amber has meaning: same line carries the idea between stations.
logo(inside,184,91,21,14.65,41.64)
tx(inside,'DENIM TRUCKER',1735,89,20,14.65,41.64,col=SOFT,track=150,align='right')

from native import *
def ambient(c,color=INK,light=[.24,.22,.17]):
 bg(c,color);op('effect.add',comp=c,layer='Fondo',matchName='ADBE Ramp',name='Luz de cocina')
 for p,v in [('ADBE Ramp-0001',[540,680]),('ADBE Ramp-0002',light+[1]),('ADBE Ramp-0003',[1250,1500]),('ADBE Ramp-0004',color+[1]),('ADBE Ramp-0005',2),('ADBE Ramp-0006',24)]:op('effect.set_property',comp=c,layer='Fondo',effectIndex=1,property=[p],value=v)

# A growing kitchen order, made entirely from editable paths and typography.
C='COMANDA - Papel'
shape(C,'Papel troquelado',0,0)
vertices=[[22,15],[738,15],[738,1325]]+[[738-i*24,1343 if i%2 else 1325] for i in range(1,30)]+[[22,1325]]
op('shape.add_path',comp=C,layer='Papel troquelado',groupIndex=1,vertices=vertices,closed=True);fill(C,'Papel troquelado',CREAM)
text(C,'Cabecera','COMANDA / IA',380,151,59,INK,60)
text(C,'Subcabecera','UN INTENTO MÁS.',380,214,30,INK,90)
path(C,'Separador',[[84,264],[676,264]],INK,3)
for i in range(6):
 y=354+i*107;n=f'Intento {i+1:02d}';text(C,n,'OTRA GENERACIÓN',106,y,39,INK,0,'left')
 props(C,n,inPoint=(6+i*15)/48);rise(C,n,106,y,6+i*15,12+i*15,30)
 path(C,f'No válido {i+1}a',[[611,y-29],[641,y+1]],ORANGE,7);trim(C,f'No válido {i+1}a',12+i*15,18+i*15)
 path(C,f'No válido {i+1}b',[[641,y-29],[611,y+1]],ORANGE,7);trim(C,f'No válido {i+1}b',12+i*15,18+i*15)
path(C,'Separador total',[[84,991],[676,991]],INK,3)
text(C,'Total','CRÉDITOS',380,1112,102,INK,-45)
rect(C,'Sello quemados',380,1190,570,100,ORANGE,3)
text(C,'Quemados','QUEMADOS',380,1211,55,CREAM,70)
keys(C,'Sello quemados',SCALE,[114,123,129],[[140,140],[95,95],[100,100]],65)
keys(C,'Sello quemados',OPACITY,[114,119],[0,100]);props(C,'Quemados',inPoint=119/48)
flush()
C='MG - credits';D=duration('credits');ambient(C)
image(C,'Comanda en movimiento','COMANDA - Papel',540,680,66);props(C,'Comanda en movimiento',threeDLayer=True)
keys(C,'Comanda en movimiento',POS,[0,14,95,130,D],[[540,1600,0],[540,680,0],[540,680,0],[540,420,-200],[540,420,-200]],68,True)
keys(C,'Comanda en movimiento',ROT,[0,14,95,130,D],[-8,0,0,0,0],65)
keys(C,'Comanda en movimiento',SCALE,[0,14,95,130,D],[[66,66,66],[66,66,66],[66,66,66],[105,105,105],[105,105,105]],68)
camera(C);flush()

# Plate/clock becomes a coin through a genuine 3D edge-on flip.
C='RELOJ - Disco';circle(C,'Disco',380,380,736,CREAM);circle(C,'Aro',380,380,682,line=ORANGE,width=4)
for i in range(12):
 a=i*math.pi/6;r=293;r2=318
 path(C,f'Marca {i+1:02d}',[[380+math.sin(a)*r,380-math.cos(a)*r],[380+math.sin(a)*r2,380-math.cos(a)*r2]],INK,9)
path(C,'Horas',[[0,0],[0,-166]],INK,24);xf(C,'Horas',position=[380,380]);keys(C,'Horas',ROT,[0,76],[40,130],33)
path(C,'Minutos',[[0,0],[0,-259]],ORANGE,15);xf(C,'Minutos',position=[380,380]);keys(C,'Minutos',ROT,[0,76],[0,580],33)
circle(C,'Eje',380,380,43,INK);flush()
C='MONEDA - Disco';circle(C,'Moneda',380,380,736,ORANGE);circle(C,'Borde',380,380,680,line=CREAM,width=4)
text(C,'Dinero','$',380,534,445,CREAM,-60);flush()
C='MG - time';ambient(C)
image(C,'Tiempo','RELOJ - Disco',540,694);props(C,'Tiempo',threeDLayer=True,outPoint=41/48)
keys(C,'Tiempo',SCALE,[0,12],[[75,75,75],[100,100,100]],72)
keys(C,'Tiempo',RY,[22,41],[0,90],70)
image(C,'Dinero','MONEDA - Disco',540,694);props(C,'Dinero',threeDLayer=True,inPoint=39/48)
keys(C,'Dinero',RY,[39,58],[-90,0],70);camera(C);flush()

# Brief native brand lock-up on the actual order-rail shot.
C='MG - brand';text(C,'Marca','Visual.Hub',540,904,149,WHITE,-55);shadow(C,'Marca',90,5,30);rise(C,'Marca',540,904,0,12,65)
path(C,'Subrayado',[[190,943],[890,943]],ORANGE,9);trim(C,'Subrayado',4,23);flush()

# Real community post and course covers arrive as a physical spread.
C='MG - community';D=duration('community');ambient(C)
text(C,'Brigada','TU BRIGADA CREATIVA.',540,350,55,CREAM,0)
for i,(src,x,y,rot) in enumerate([('curso-maestria.png',338,582,-7),('curso-masterclasses.png',746,633,8)]):
 n=f'Curso real {i+1}';image(C,n,src,x,y,115);props(C,n,threeDLayer=True)
 keys(C,n,POS,[i*4,i*4+18],[[x,1600,180],[x,y,0]],70,True)
 keys(C,n,ROT,[i*4,i*4+18],[rot*3,rot],70)
 keys(C,n,RX,[i*4,i*4+18],[35,0],65)
image(C,'Comunidad real','comunidad-post.jpg',540,982,105);props(C,'Comunidad real',threeDLayer=True)
keys(C,'Comunidad real',POS,[8,27],[[540,1700,150],[540,982,0]],75,True)
camera(C);keys(C,'CAMARA',POS,[0,23,D],[[540,960,-1750],[540,960,-1550],[540,960,-1520]],55,True)
flush()

# A visual recipe: a card fans out into three consistent servings, then repetition is cancelled.
C='MG - system';D=duration('system');ambient(C)
null(C,'MESA DE TRABAJO',[540,660,0])
for i,(x,z,r) in enumerate([(-170,80,-9),(0,0,0),(170,-80,9)]):
 n=f'RECETA {i+1}';rect(C,n,0,0,570,660,CREAM,12);props(C,n,threeDLayer=True);parent(C,n,'MESA DE TRABAJO');xf(C,n,position=[x,0,z])
 keys(C,n,POS,[0,18,78,101],[[x,1150,z],[x,0,z],[x,0,z],[x*2.1,0,z]],70,True)
 keys(C,n,ROT,[0,18,78,101],[r*3,r,r,0],70)
 label=f'Titulo receta {i+1}';text(C,label,['PLANTILLAS','SISTEMAS','RESULTADOS'][i],0,-215,40,INK,20)
 props(C,label,threeDLayer=True);parent(C,label,n);xf(C,label,position=[0,-215,-1])
 # Recipe marks become a familiar plating pattern.
 for k in range(3):
  q=f'Ingrediente {i+1}-{k+1}';path(C,q,[[-180,-115+k*75],[130-k*25,-115+k*75]],ORANGE if k==0 else [.66,.65,.59],12)
  props(C,q,threeDLayer=True);parent(C,q,n);xf(C,q,position=[0,0,-1]);trim(C,q,18+k*7+i*3,30+k*7+i*3)
 foot=f'Pie receta {i+1}';text(C,foot,'LISTO PARA CREAR',0,229,25,INK,75);props(C,foot,threeDLayer=True);parent(C,foot,n);xf(C,foot,position=[0,229,-1])
 # Remove cards together so the next scene inherits their outward motion.
 props(C,n,outPoint=128/48)
 for child in [label,foot]+[f'Ingrediente {i+1}-{k+1}' for k in range(3)]:props(C,child,outPoint=128/48)
camera(C);keys(C,'CAMARA',POS,[0,18,77,105,126,141,D],[[540,960,-1850],[540,960,-1500],[540,960,-1500],[540,960,-2050],[540,960,-2050],[540,960,-1500],[540,960,-1500]],60,True)
text(C,'Receta titular','UNA RECETA. UN SISTEMA.',540,331,48,CREAM,0);props(C,'Receta titular',outPoint=128/48);rise(C,'Receta titular',540,331,0,18,45)
for i,x in enumerate([235,540,845]):
 n=f'Servicio consistente {i+1}';circle(C,n,x,673,268,CREAM);props(C,n,inPoint=128/48,outPoint=233/48)
 keys(C,n,SCALE,[128+i*4,144+i*4],[[20,20],[100,100]],70)
 ring=n+' aro';circle(C,ring,x,673,235,line=ORANGE,width=3);props(C,ring,inPoint=128/48,outPoint=233/48);keys(C,ring,SCALE,[128+i*4,144+i*4],[[20,20],[100,100]],70)
 # The same three-stroke plating mark on every plate makes consistency visible.
 for k in range(3):
  q=f'Emplatado {i+1}-{k+1}';path(C,q,[[x-60,643+k*29],[x+60,643+k*29]],INK,12);props(C,q,inPoint=128/48,outPoint=233/48);trim(C,q,147+i*4+k*3,158+i*4+k*3)
text(C,'Consistencia','CONSISTENTES.',540,944,73,CREAM,-30);props(C,'Consistencia',inPoint=141/48,outPoint=233/48);rise(C,'Consistencia',540,944,141,155,35)
text(C,'Realismo','REALISTAS.',540,1033,73,ORANGE,-30);props(C,'Realismo',inPoint=165/48,outPoint=233/48);rise(C,'Realismo',540,1033,165,179,35)
circle(C,'Disco repeticion',540,675,764,ORANGE);props(C,'Disco repeticion',inPoint=233/48)
keys(C,'Disco repeticion',SCALE,[233,246],[[140,140],[100,100]],75)
text(C,'Repeticiones','50',540,783,333,CREAM,-55);props(C,'Repeticiones',inPoint=233/48);rise(C,'Repeticiones',540,783,233,245,85)
text(C,'Generaciones','GENERACIONES',540,883,52,CREAM,35);props(C,'Generaciones',inPoint=239/48)
path(C,'Cancelar repeticion',[[218,921],[862,455]],INK,17);props(C,'Cancelar repeticion',inPoint=257/48);trim(C,'Cancelar repeticion',257,273)
flush()

C='MG - live';rect(C,'Fondo directo',540,449,366,81,INK,41);circle(C,'Piloto',402,449,19,ORANGE)
text(C,'Directo','EN DIRECTO',570,461,34,CREAM,45)
for n in ['Fondo directo','Piloto','Directo']:keys(C,n,OPACITY,[0,7,43,53],[0,100,100,0])
flush()

# Closing plate is also a native, editable price lock-up.
C='MG - price';D=duration('price');ambient(C)
circle(C,'Plato de cierre',540,701,896,CREAM)
circle(C,'Aro cierre',540,701,843,line=ORANGE,width=5)
for n in ['Plato de cierre','Aro cierre']:keys(C,n,SCALE,[0,16],[[160,160],[100,100]],74)
text(C,'Marca','Visual.Hub',540,523,98,INK,-35);rise(C,'Marca',540,523,4,18,42)
text(C,'Precio','39',477,836,342,INK,-70);rise(C,'Precio',477,836,22,36,80)
text(C,'Moneda','$',736,716,123,ORANGE,-40);rise(C,'Moneda',736,716,26,39,35)
text(C,'Acceso','ENTRA A LA COMUNIDAD',540,955,35,INK,55);rise(C,'Acceso',540,955,37,49,22)
text(C,'Direccion','skool.com/visual',540,1250,43,CREAM,-10);rise(C,'Direccion',540,1250,45,58,22)
save('scenes',extra=[{'name':'ae_save_project','arguments':{}}]+[{'name':'ae_render_frame','arguments':{'compNameOrId':'MG - '+e,'time':t,'outPath':str(R/('scene-'+e+'.png'))}} for e,t in [('credits',3.15),('time',1.3),('community',1.3),('system',3.7),('price',1.7)]])

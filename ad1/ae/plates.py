from native import *
for i,(c,handle,slug,metric,unit) in enumerate([
 ('PLATO - Kurt audiencia','@notkurtgodel','kurt','83,3 mil','seguidores'),
 ('PLATO - Kurt alcance','@notkurtgodel','kurt','7,7 M','visualizaciones'),
 ('PLATO - Elliot audiencia','@notelliotkay','elliot','13,5 mil','seguidores'),
 ('PLATO - Elliot alcance','@notelliotkay','elliot','4,9 M','visualizaciones')]):
 circle(c,'Porcelana',480,500,920,CREAM)
 circle(c,'Borde exterior',480,500,888,line=[.75,.67,.50],width=2)
 circle(c,'Borde interior',480,500,846,line=[.85,.79,.65],width=2)
 circle(c,'Sello de cuenta',480,153,57,ORANGE)
 text(c,'Numero de servicio',str(i+1).zfill(2),480,162,25,CREAM,0)
 if unit=='seguidores':
  image(c,'Avatar real',slug+'-avatar.png',480,245,52)
  op('mask.add',comp=c,layer='Avatar real',name='Recorte circular')
  op('mask.set_path',comp=c,layer='Avatar real',maskIndex=1,vertices=[[75,0],[150,75],[75,149],[0,75]],inTangents=[[-41.42,0],[0,-41.42],[41.42,0],[0,41.42]],outTangents=[[41.42,0],[0,41.42],[-41.42,0],[0,-41.42]],closed=True)
  text(c,'Cuenta',handle,480,338,38,INK)
  text(c,'Cifra editable',metric,480,523,195,INK,-55)
  text(c,'Unidad',unit,480,586,42,INK,-10)
  rect(c,'Soporte de prueba',480,728,756,212,WHITE,10)
  image(c,'Captura original verificable',slug+'-profile-proof.png',480,727,106)
 else:
  text(c,'Cuenta',handle,480,309,38,INK)
  text(c,'Cifra editable',metric,333,504,180,INK,-60)
  text(c,'Unidad',unit,333,564,32,INK,-15)
  text(c,'Contexto de la cifra','en un solo reel',333,612,27,INK,-5)
  rect(c,'Marco del reel',709,545,230,354,WHITE,12)
  image(c,'Captura original verificable',slug+'-proof-0.png',709,545,92)
  path(c,'Linea a la prueba',[[322,649],[322,725],[602,725]],ORANGE,5)
 text(c,'Procedencia','INSTAGRAM · CAPTURA REAL',480,872,22,INK,100)
 flush()

C='MG - accounts';D=duration('accounts')
for p,v in [('ADBE Ramp-0001',[540,650]),('ADBE Ramp-0002',[.22,.27,.23,1]),('ADBE Ramp-0003',[1200,1460]),('ADBE Ramp-0004',INK+[1]),('ADBE Ramp-0005',2),('ADBE Ramp-0006',25)]:op('effect.set_property',comp=C,layer='Fondo',effectIndex=1,property=[p],value=v)
# All four plates inhabit a rotating 3D rig. No flat board or previous pan path.
null(C,'SERVICIO GIRATORIO',[540,680,900])
for i,c in enumerate(['PLATO - Kurt audiencia','PLATO - Kurt alcance','PLATO - Elliot audiencia','PLATO - Elliot alcance']):
 n=f'PLATO {i+1:02d}';image(C,n,c,540,680);props(C,n,threeDLayer=True)
 parent(C,n,'SERVICIO GIRATORIO');angle=i*math.pi/2
 xf(C,n,position=[900*math.sin(angle),0,-900*math.cos(angle)])
 op('property.set',comp=C,layer=n,property=RY,value=-90*i)
 # Gate the rear of the carousel; only a departing and an arriving plate are visible.
 starts=[0,65,145,226];ends=[86,166,247,D]
 props(C,n,inPoint=starts[i]/48,outPoint=ends[i]/48)
 if i:keys(C,n,OPACITY,[starts[i],starts[i]+4],[0,100])
 if i<3:keys(C,n,OPACITY,[ends[i]-4,ends[i]],[100,0])
keys(C,'SERVICIO GIRATORIO',RY,[0,65,86,145,166,226,247,D],[0,0,90,90,180,180,270,270],68)
camera(C)
keys(C,'CAMARA',POS,[0,14,65,75,86,98,145,155,166,178,226,237,247,260,D],[[540,960,-1950],[540,960,-1550],[540,960,-1550],[540,960,-2160],[540,960,-1850],[540,960,-1550],[540,960,-1550],[540,960,-2160],[540,960,-1850],[540,960,-1550],[540,960,-1550],[540,960,-2160],[540,960,-1850],[540,960,-1550],[540,960,-1550]],60,True,speeds=[0,0,0,0,1400,0,0,0,1400,0,0,0,1400,0,0])
text(C,'Encabezado','RESULTADOS SERVIDOS.',540,246,38,CREAM,10)
rise(C,'Encabezado',540,246,0,14,22)
save('plates',extra=[{'name':'ae_save_project','arguments':{}},{'name':'ae_render_frame','arguments':{'compNameOrId':C,'time':.9,'outPath':str(R/'plates-01.png')}},{'name':'ae_render_frame','arguments':{'compNameOrId':C,'time':2.5,'outPath':str(R/'plates-02.png')}}])

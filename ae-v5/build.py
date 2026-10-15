"""Create documented native AE operations; no arbitrary bridge evaluation."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parent
data=json.loads((R/'init-result.jsonl').read_text().splitlines()[0])['result']['structuredContent']['result']['results']
ids={x['name']:x['id'] for x in data if 'id' in x}
cream=[.953,.941,.898]; green=[.208,.333,.149]; ink=[.11,.16,.098]; muted=[.40,.45,.37]
requests=[];ops=[]
def op(n,**a):ops.append({'operation':n,'args':a})
def flush():
 global ops
 if ops:requests.append({'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops,'stopOnError':True}}});ops=[]
def xf(c,n,**a):op('transform.set',comp=c,layer=n,**a)
def props(c,n,**a):op('layer.set_props',comp=c,layer=n,props=a)
def text(c,n,s,x,y,size,color=ink,tracking=-35):
 op('layer.create_text',comp=c,name=n,text=s);op('text.reset_style',comp=c,layer=n)
 op('text.set_style',comp=c,layer=n,font='SFProDisplay-Bold',fontSize=size,fillColor=color,applyFill=True,applyStroke=False,justification='center',tracking=tracking,allCaps=False,fauxBold=False,fauxItalic=False,horizontalScale=1,verticalScale=1)
 xf(c,n,position=[x,y],anchorPoint=[0,0]);props(c,n,motionBlur=True)
def rect(c,n,x,y,w,h,color,roundness=0):
 op('layer.create_shape',comp=c,name=n);op('shape.add_group',comp=c,layer=n,name='Superficie')
 op('shape.add_rect',comp=c,layer=n,groupIndex=1,size=[w,h],roundness=roundness)
 op('shape.add_fill',comp=c,layer=n,groupIndex=1,color=color+[1]);xf(c,n,position=[x,y]);props(c,n,motionBlur=True)
def path(c,n,points,width=3,color=green,alpha=100):
 op('layer.create_shape',comp=c,name=n);op('shape.add_group',comp=c,layer=n,name='Trazo')
 op('shape.add_path',comp=c,layer=n,groupIndex=1,vertices=points,closed=False)
 op('shape.add_stroke',comp=c,layer=n,groupIndex=1,color=color+[1],width=width)
 xf(c,n,position=[0,0],opacity=alpha);props(c,n,motionBlur=True)
def image(c,n,source,x,y,scale=100):
 op('layer.create_footage',comp=c,name=n,sourceItemId=ids[source]);xf(c,n,position=[x,y],scale=[scale,scale]);props(c,n,motionBlur=True)
def keys(c,n,p,frames,values,influence=65,spatial=False):
 op('keyframe.set_batch',comp=c,layer=n,property=p,times=[f/24 for f in frames],values=values)
 for i in range(len(frames)):
  op('keyframe.set_easing',comp=c,layer=n,property=p,keyIndex=i+1,inSpeed=0,outSpeed=0,inInfluence=influence,outInfluence=influence)
  if spatial:op('keyframe.set_spatial',comp=c,layer=n,property=p,keyIndex=i+1,inTangent=[0,0,0],outTangent=[0,0,0],continuous=False,autoBezier=False)
pos=['ADBE Transform Group','ADBE Position'];sca=['ADBE Transform Group','ADBE Scale'];opacity=['ADBE Transform Group','ADBE Opacity']
for c,handle,metric,slug,arrival in [('01 KURT - Seguidores','@notkurtgodel','83,3 mil','kurt',0),('03 ELLIOT - Seguidores','@notelliotkay','13,5 mil','elliot',94)]:
 rect(c,'Sombra de la captura',482,570,782,238,[.84,.85,.79],22)
 rect(c,'Tarjeta de evidencia',480,562,782,238,[1,1,1],22)
 image(c,'Captura original - perfil',slug+'-profile-proof.png',480,562,108)
 image(c,'Avatar original',slug+'-avatar.png',238,95,48)
 text(c,'Cuenta',handle,510,111,39,ink,-18)
 text(c,'Seguidores - editable',metric,480,335,192,green,-50)
 text(c,'Unidad','seguidores',480,397,47,ink,-10)
 # Single-axis rises. Camera owns the shared movement.
 keys(c,'Seguidores - editable',pos,[max(0,arrival),arrival+8],[[480,378],[480,335]],72,True)
 keys(c,'Seguidores - editable',opacity,[max(0,arrival),arrival+4],[0,100])
 flush()
for c,handle,metric,slug,arrival in [('02 KURT - Visualizaciones','@notkurtgodel','7,7 M','kurt',44),('04 ELLIOT - Visualizaciones','@notelliotkay','4,9 M','elliot',141)]:
 rect(c,'Sombra del reel',756,423,260,405,[.82,.84,.77],19)
 rect(c,'Marco de evidencia',750,415,260,405,[1,1,1],19)
 image(c,'Captura original - reel',slug+'-proof-0.png',750,415,103)
 text(c,'Cuenta',handle,480,112,39,ink,-18)
 text(c,'Visualizaciones - editable',metric,315,354,192,green,-45)
 text(c,'Unidad','visualizaciones',315,418,44,ink,-22)
 text(c,'Alcance de la cifra','en un solo reel',315,473,30,muted,-10)
 path(c,'Conexion cifra - evidencia',[[300,516],[300,561],[605,561],[630,535]],3,green,80)
 op('shape.add_trim_paths',comp=c,layer='Conexion cifra - evidencia',groupIndex=1,end=0)
 keys(c,'Conexion cifra - evidencia',['ADBE Root Vectors Group',1,'ADBE Vectors Group','ADBE Vector Filter - Trim','ADBE Vector Trim End'],[arrival,arrival+13],[0,100])
 keys(c,'Visualizaciones - editable',pos,[arrival,arrival+8],[[315,397],[315,354]],72,True)
 keys(c,'Visualizaciones - editable',opacity,[arrival,arrival+4],[0,100])
 flush()
C='WORLD - Camara y conexiones'
# Continuous board: all four evidence nodes remain in one world.
path(C,'Ruta - seguidores a visualizaciones',[[540,930],[540,1900],[1990,1900],[1990,3150]],5,green,25)
props(C,'Ruta - seguidores a visualizaciones',threeDLayer=True)
xf(C,'Ruta - seguidores a visualizaciones',position=[0,0,100])
nodes=[('01 KURT - Seguidores',540,720),('02 KURT - Visualizaciones',540,1970),('03 ELLIOT - Seguidores',1990,1970),('04 ELLIOT - Visualizaciones',1990,3220)]
for name,x,y in nodes:
 image(C,name,name,x,y);props(C,name,threeDLayer=True);xf(C,name,position=[x,y,0])
# A real perspective camera; pull back before each pan, push in on the next proof.
op('layer.create_camera',comp=C,name='CAMARA - zoom y recorrido')
props(C,'CAMARA - zoom y recorrido',autoOrient='off')
op('property.set',comp=C,layer='CAMARA - zoom y recorrido',property=['ADBE Camera Options Group','ADBE Camera Zoom'],value=1500)
frames=[0,10,29,38,44,56,78,87,94,106,125,134,141,153,183]
camera=[[540,960,-1580],[540,960,-1500],[540,960,-1500],[540,960,-2500],[540,2210,-2500],[540,2210,-1500],[540,2210,-1500],[540,2210,-2550],[1990,2210,-2550],[1990,2210,-1500],[1990,2210,-1500],[1990,2210,-2550],[1990,3460,-2550],[1990,3460,-1500],[1990,3460,-1500]]
keys(C,'CAMARA - zoom y recorrido',pos,frames,camera,72,True)
flush()
C='VH - Cuentas - V5'
op('layer.create_solid',comp=C,name='Fondo marfil',color=cream)
image(C,'ESCENARIO - animacion nativa','WORLD - Camara y conexiones',540,960)
# Native mask keeps only the active proof in the legible part of the frame.
op('mask.add',comp=C,layer='ESCENARIO - animacion nativa',name='Ventana del escenario')
op('mask.set_path',comp=C,layer='ESCENARIO - animacion nativa',maskIndex=1,vertices=[[40,380],[1040,380],[1040,1065],[40,1065]],closed=True)
op('mask.set_props',comp=C,layer='ESCENARIO - animacion nativa',maskIndex=1,feather=[30,35])
text(C,'Encabezado','CUENTAS CON IA',540,315,39,ink,110)
text(C,'Subtitulo editorial','Audiencias reales. Resultados visibles.',540,365,25,muted,0)
rect(C,'Linea progreso - fondo',540,1240,700,3,[.82,.84,.76])
rect(C,'Linea progreso - activa',190,1240,700,3,green)
xf(C,'Linea progreso - activa',anchorPoint=[-350,0])
keys(C,'Linea progreso - activa',sca,[0,183],[[0,100],[100,100]],33)
op('timeline.set_active_comp',comp=C);op('timeline.set_time',comp=C,time=1)
flush()
requests.append({'name':'ae_save_project','arguments':{'path':str(R/'Visual-Hub-Cuentas-V5.aep')}})
requests.append({'name':'ae_render_frame','arguments':{'compNameOrId':C,'time':1,'outPath':str(R/'preview-1.png')}})
(R/'build.json').write_text(json.dumps(requests,ensure_ascii=False))
print(len(requests),'verified operation batches generated')

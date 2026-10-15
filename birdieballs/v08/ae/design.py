from native import *
FPS=60000/1001;D=2278/FPS
CREAM=[.988,.984,.941];ACC=[.863,.953,.584]
def title(c,n,s,x,y,size,col=CREAM,bold=False):
 text(c,n,s,x,y,size,col,'SFProDisplay-Bold' if bold else 'SFProDisplay-Regular',-45,0,D);xf(c,n,anchorPoint=[0,0])
for k in ['A','B','C']:
 c='ESTUDIO '+k+' - REVISION';op('comp.create',name=c,width=1080,height=1920,fps=FPS,duration=D);footage(c,'Metraje',1,0,D,0)
 if k=='A':
  title(c,'Una 1','una',322,545,170,ACC);title(c,'Enlace','a',540,545,96);title(c,'Una 2','una.',753,545,170,ACC)
  for i,(x,y,dx,dy) in enumerate([(70,855,1,1),(852,855,-1,1),(70,1520,1,-1),(852,1520,-1,-1)]):path(c,'Esquina '+str(i),[[x,y+dy*72],[x,y],[x+dx*72,y]],4,CREAM,0,D)
  path(c,'Marca de revision',[[865,720],[894,749],[944,684]],9,ACC,0,D)
 elif k=='B':
  title(c,'Nucleo','UNA',540,410,240,ACC,True);title(c,'Apoyo','A UNA.',540,565,164,CREAM,True)
  path(c,'Subrayado',[[275,610],[805,610]],5,ACC,0,D)
 elif k=='C':
  title(c,'Una','una',235,490,188,ACC);title(c,'Enlace','a',540,560,110);title(c,'Otra','una.',819,635,188,ACC)
  path(c,'Trayectoria',[[325,550],[540,640],[735,700]],5,CREAM,0,D)
  op('layer.create_shape',comp=c,name='Halo');op('shape.add_group',comp=c,layer='Halo',name='Contorno');op('shape.add_ellipse',comp=c,layer='Halo',groupIndex=1,size=[800,800]);op('shape.add_stroke',comp=c,layer='Halo',groupIndex=1,color=ACC+[1],width=4);xf(c,'Halo',position=[470,1230])
save('design.json',[{'name':'ae_render_frame','arguments':{'compNameOrId':'ESTUDIO '+k+' - REVISION','time':21.9,'outPath':str(R.parent/'stills'/('design-'+k+'.png'))}} for k in 'ABC'])

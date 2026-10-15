from native import *
# Keep headings clear and make the three recipe names legible throughout the hold.
op('layer.delete',comp='MG - accounts',layer='Encabezado')
C='MG - system';xf(C,'MESA DE TRABAJO',position=[540,720,0],scale=[65,65,65])
for i,(x,z) in enumerate([(-455,0),(0,0),(455,0)]):
 n=f'RECETA {i+1}'
 keys(C,n,POS,[0,18,78,101],[[x,1150,z],[x,0,z],[x,0,z],[x*1.25,0,z]],70,True)
 op('text.set_style',comp=C,layer=f'Titulo receta {i+1}',fontSize=53)
 op('layer.delete',comp=C,layer=f'Pie receta {i+1}')
 for k in range(3):op('layer.delete',comp=C,layer=f'Emplatado {i+1}-{k+1}')
 # Native plated-food motif replaces the abstract bars.
 px=[235,540,845][i]
 for k,(y,col) in enumerate([(694,[.50,.25,.08]),(674,[.70,.38,.11]),(652,[.88,.56,.20])]):
  q=f'Plato {i+1} - bocado {k+1}';shape(C,q,px,y);op('shape.add_ellipse',comp=C,layer=q,groupIndex=1,size=[104,36]);fill(C,q,col);stroke(C,q,[.38,.19,.06],2)
  props(C,q,inPoint=128/48,outPoint=233/48);keys(C,q,SCALE,[144+i*4+k*2,155+i*4+k*2],[[15,15],[100,100]],70)
 q=f'Plato {i+1} - hoja';shape(C,q,px+42,640);op('shape.add_ellipse',comp=C,layer=q,groupIndex=1,size=[43,18]);fill(C,q,[.22,.34,.09]);xf(C,q,rotation=-35);props(C,q,inPoint=160/48,outPoint=233/48)
 keys(C,q,SCALE,[160+i*3,169+i*3],[[0,0],[100,100]],70)
C='MG - price';keys(C,'Direccion',POS,[45,58],[[540,1232],[540,1210]],75,True)
props('AD1 - FINAL','MEZCLA - Voz musica y efectos',label=9)
flush()
op('render.add_to_queue',comp='AD1 - FINAL',outputPath=str(R.parent/'output/AD1-Native-Master.mov'))
save('polish',extra=[{'name':'ae_do','arguments':{'operation':'render.list_templates','args':{}}},{'name':'ae_save_project','arguments':{}},{'name':'ae_render_frame','arguments':{'compNameOrId':'AD1 - FINAL','time':54.8,'outPath':str(R/'polished-system.png')}}])

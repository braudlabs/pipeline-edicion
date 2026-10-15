exec(compile(open(__file__.replace('styleframes.py','helpers.py')).read(),__file__,'exec'))
assets=sorted(p.name for p in A.glob('*.jpg'))
# Shared photographic planes, all source footage from this ad.
for i in [0,1,2,4]:photo_obj('FOTO - '+str(i+1),assets[i],260,370,65)
# A: actual material becomes three aligned editorial tracks.
c=comp('DIRECCION A - Mesa de montaje',144);bg(c)
for i in range(3):
 nested(c,'Plano '+str(i),'FOTO - '+str(i+1),260+i*280,680,1,round=14,shadow=[0,14,22,'#262620',.22])
for j,(lab,y,col) in enumerate([('Clips',990,RED),('Voz',1110,BLUE),('Subtítulos',1230,INK)]):
 txt(c,'Etiqueta '+lab,lab,110,y-24,27,align='left',track=10)
 rect(c,'Rail '+lab,110,y,860,70,'#e1ded5',round=12)
 if j==0:
  for k in range(3):rect(c,'Pieza '+str(k),120+k*282,y+8,267,54,col,round=7)
 elif j==1:
  pts=[[125+k*7,y+35+math.sin(k*1.8)*math.sin(k*.32)*22] for k in range(118)];path(c,'Forma de voz',pts,col,3)
 else:
  for k,(x,w,s) in enumerate([(120,223,'los cortes'),(360,260,'los subtítulos'),(638,320,'se ensamblan')]):
   rect(c,'Bloque texto '+str(k),x,y+8,w,54,col,round=7);txt(c,'Contenido '+str(k),s,x+w/2,y+46,26,CREAM)
path(c,'Cabezal',[[650,960],[650,1325]],RED,4);path(c,'Marca cabezal',[[638,946],[662,946],[650,964]],RED,3,closed=True)
# B: exploded picture, sound and typesetting planes assemble into one master.
c=comp('DIRECCION B - Capas en profundidad',144);bg(c,True);c['camera']=camera([0,143],[[540,960,-2050],[540,960,-2050]])
for i,(x,y,z,col) in enumerate([(700,660,480,BLUE),(580,820,180,'#e4dfd2'),(440,940,-80,CREAM)]):
 n=three(rect(c,'Plano material '+str(i),x-220,y-330,440,660,col,round=14),z);n['ry']=-16;n['rot']=-8
n=three(nested(c,'Imagen protagonista','FOTO - 3',440,795,1.55,round=14),-90);n['ry']=-16;n['rot']=-8
path(c,'Voz',[[170+k*7,1190+math.sin(k*1.6)*math.sin(k*.32)*25] for k in range(107)],BLUE,4)
txt(c,'Contenido','se ensamblan',520,1340,89,CREAM)
# C: a phototypeset strip feeds a graphic cutting register.
c=comp('DIRECCION C - Tira editorial',144);bg(c)
for i in range(3):
 n=nested(c,'Panel fotografico '+str(i),'FOTO - '+str(i+1),230+i*300,770,1.13,round=0);n['rot']=[-7,0,7][i]
path(c,'Regla de corte',[[140,1100],[940,1100]],INK,2)
for i in range(21):path(c,'Registro '+str(i),[[140+i*40,1100],[140+i*40,1112 if i%5 else 1125]],INK,2)
txt(c,'Palabra uno','cortes',295,1280,139,INK);txt(c,'Palabra dos','subtítulos',610,1390,114,RED)
path(c,'Seccion',[[475,1090],[475,1310]],RED,6)
(R/'ae/styleframes.json').write_text(json.dumps(S,ensure_ascii=False,indent=2));print('Style frames native:',len(S['comps']))

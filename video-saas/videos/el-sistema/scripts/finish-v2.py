# The result remains the same object while the editor builds around it.
product=comp('V2 · Anuncio La Máquina',1080,1920)
pic(product,'Ancla de la pieza','denim-01.jpg',540,960,1080)
for j,(a,b) in enumerate([(41.65,44.0),(44.0,46.20),(46.20,48.40),(48.40,50.60),(50.60,53.56)]):
 n=pic(product,'Toma '+str(j+1),f'denim-{j+1:02}.mp4',540,960,1080,a,b);n['sourceOffset']=.30 if j else 1.0
# Demonstration of the four real product subtitle styles, contained in the output.
for a,b,words,sz,col in [(48.85,49.47,'máquina',138,INK),(49.47,50.13,'FABRICA CREATIVOS',92,'#FFD400'),(50.13,50.78,'Tu máquina de creativos',78,INK),(50.78,51.75,'CREATIVOS',152,'#FFE01B')]:
 n=tx(product,words,540,1460,sz,a,b,col=col,font='HelveticaNeue-Bold',align='center',track=-20)
 anim(n,'scale',[a,a+.16],[[.93,.93],[1,1]],'out')
 if a==50.13:
  # Put the clean rail under this text (shape order uses the list position).
  panel=rect(product,'Contraste clean',92,1300,896,199,'#171719',a,b,round=20,opacity=.6)
  product['layers'].remove(panel);product['layers'].insert(product['layers'].index(n),panel)
editor=comp('V2 · Editor',1840,960);glass(editor,'Editor',7,7,1826,946,r=32,fill='#111315')
logo(editor,225,75,24);tx(editor,'La máquina de fabricar creativos',1730,74,25,col=SOFT,align='right')
line(editor,'Cabecera editor',[[10,112],[1830,112]],col='#343631',width=1)
tx(editor,'Montaje',845,198,67,font='HelveticaNeue-Medium')
tx(editor,'Silencios',850,285,36,45.2,48.0,col=SOFT)
tx(editor,'Ritmo',1115,285,36,47.95,49.3,col=Y)
tx(editor,'Subtítulos',1365,285,36,48.85,52.05,col=Y)
# Editing controls are subordinate to the output and active timeline.
for j,s in enumerate(['Pop','Karaoke','Clean','Impact']):
 x=845+j*220;rect(editor,'Estilo '+s,x,368,199,64,'#22251F',48.78,D,stroke='#555945',round=16)
 tx(editor,s,x+99,410,27,48.78,D,col=INK,align='center')
# Filmstrip gaps actually close; related waveforms travel with every clip.
for j in range(5):
 cc=comp('V2 · Clip timeline '+str(j),160,205)
 rect(cc,'Clip',0,0,160,132,'#4B482F',stroke='#A29457',round=10)
 pic(cc,'Fotograma',f'denim-{j+1:02}.jpg',80,63,71)
 tx(cc,f'0{j+1}',12,31,20,col=Y)
 for k in range(25):
  h=8+((k*13+j*7)%27);rect(cc,'Audio '+str(k),k*6.3,166-h/2,3,h,'#857B48',round=1)
 n=nested(editor,'Fragmento '+str(j),cc['name'],845+j*190,535,45.2,53.56)
 anim(n,'pos',[45.2,47.08,47.54,48.3],[[845+j*190,535],[845+j*190,535],[845+j*162,535],[845+j*162,535]],'flow')
line(editor,'Base tiempo',[[845,760],[1790,760]],45.2,D,'#42443E',2)
for j in range(11):
 x=845+j*86;line(editor,'Tick '+str(j),[[x,752],[x,769]],45.2,D,'#727465',1)
 tx(editor,f'{j*2:02}',x,801,19,45.2,D,col=SOFT,align='center')
n=line(editor,'Cabezal',[[845,497],[845,748]],45.2,52.18,Y,3);anim(n,'pos',[45.2,51.8],[[0,0],[820,0]],'linear')
rect(editor,'Estado de entrega',846,836,865,64,'#242D20',52.18,D,stroke='#4B6340',round=16)
tx(editor,'Aprobado · listo para publicar',1278,881,32,52.18,D,col=GREEN,align='center')
# A continuous shot: input resolves to an ad, editor closes around the ad.
result=comp('V2 · Resultado y montaje');background(result)
caption(result,'Una frase.',522,376,110,41.72,45.3)
n=nested(result,'Frase original',prompt['name'],540,553,41.72,45.4,.63,[640,84]);anim(n,'pos',[41.72,42.3,44.93,45.4],[[510,790],[540,553],[540,553],[-850,553]],'flow')
editorN=floating(result,'Editor que se ensambla',editor['name'],[45.05,45.86,51.92,52.54,53.7],[[1470,620,600],[960,540,90],[960,540,90],[960,540,140],[540,560,650]],[.94,.94,.94,.9,.58],[12,2,2,0,8],[-25,-4,-4,0,20],45.05,53.7)
# Same footage layer, same continuous source time, from hero to the editing window.
floating(result,'El anuncio permanece',product['name'],[41.72,42.3,44.93,45.86,51.92,52.54,53.7],[[1510,610,280],[1438,553,-40],[1438,553,-40],[517,554,20],[517,554,20],[523,554,70],[420,566,620]],[.368,.368,.368,.357,.357,.338,.2],[10,2,2,2,2,0,8],[-18,-6,-6,-4,-4,0,20],41.72,53.7)
# Versions: same source footage, then separate hooks, angle and aspect-ratio crops.
variants=comp('V2 · Versiones');background(variants)
caption(variants,'De una pieza,',960,220,84,53.50,58.10)
caption(variants,'nuevas versiones.',960,321,102,54.60,58.10,col=Y)
for j,(title,im) in enumerate([('La sorpresa','denim-03.jpg'),('La máquina','denim-01.jpg'),('El problema','denim-02.jpg')]):
 cc=comp('V2 · Versión '+str(j),460,634);glass(cc,'Versión',6,6,448,622,r=25)
 pic(cc,'Prenda',im,230,278,278);tx(cc,title,230,582,32,align='center',font='HelveticaNeue-Medium')
 x=477+j*483
 floating(variants,'Rama '+str(j),cc['name'],[53.50+j*.12,54.5+j*.12,57.74,58.30],[[420,590,500],[x,695,90+j*40],[x,695,90+j*40],[x-1600,610,700]],[.86,.86,.86,.7],[12,3,3,12],[25,-8+j*8,-8+j*8,35],53.50+j*.12,58.30)
# Three deliberate transformations rather than three unrelated panels.
for j,(a,b,s) in enumerate([(58.25,59.37,'Otro gancho.'),(59.37,60.28,'Otro ángulo.'),(60.28,61.24,'Otro formato.')]):
 caption(variants,s,960,228,100,a,b)
 im=f'denim-{[3,2,1][j]:02}.jpg'
 if j<2:
  n=pic(variants,'Alternativa '+str(j),im,960,672,335,a,b);reveal(n,a,dx=130 if j==0 else -130,dy=0,d=.34)
 else:
  # Native comp crops show formats, using the same product rather than fabricated new footage.
  for k,(w,h,label) in enumerate([(340,340,'1:1'),(265,471,'9:16'),(560,315,'16:9')]):
   cc=comp('V2 · Formato '+label,w,h);pic(cc,'Encuadre',im,w/2,h/2,max(w,h*1080/1920))
   x=[462,918,1477][k];nested(variants,'Salida '+label,cc['name'],x,680,a,b,1,[w/2,h/2]);tx(variants,label,x,972,30,a,b,col=SOFT,align='center')
caption(variants,'El concepto que gana.',960,229,93,61.15,63.28)
# The chosen visual expands into a family; no invented performance claim.
for j in range(9):
 cc=photo_card('V2 · Lote '+str(j),f'denim-{1+j%5:02}.jpg',142,253)
 row=j//5;col=j%5;x=390+col*284+(140 if row else 0);y=530+row*292
 n=nested(variants,'Familia '+str(j),cc['name'],960,650,61.45+j*.07,63.36,.83,[81,136.5]);anim(n,'pos',[61.45+j*.07,62.37+j*.04],[[960,650],[x,y]],'flow');anim(n,'opacity',[61.45+j*.07,61.65+j*.07],[0,1])
# Close on the actual product identity, no fictitious CTA.
closing=comp('V2 · Cierre');background(closing)
caption(closing,'Tú me cuentas la idea.',960,493,91,63.22,64.45)
caption(closing,'Del proceso me encargo yo.',960,572,87,64.36,66.18)
logo(closing,960,580,112,66.26,D)
# Initial and final states breathe briefly, keeping the entire word Sistema.

from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
p=R/'scripts/v3/design.py';s=p.read_text()
s=s.replace("xx=1120+j*245", "xx=1070+j*340")
s=s.replace("cc,xx,700,20.62,23.05,.82", "cc,xx,700,20.62,23.05,.70")
s=s.replace("[1310+(j-1)*190,710,70],[2000+(j-1)*190,700,100]],[.7,.82,.82,.9,.8]", "[1370+(j-1)*385,710,70],[2300+(j-1)*385,700,100]],[.6,.70,.70,.74,.7]")
s=s.replace("shots[4],1350,330,20.57,22.83,.40", "shots[4],1350,330,20.57,22.83,.60")
s=s.replace("comp('V3 | Mapa 16 planos',1900,3420)","comp('V3 | Mapa 16 planos',3820,1740)")
s=s.replace("x=248+(j%4)*466;y=420+(j//4)*820", "x=248+(j%8)*466;y=420+(j//8)*820")
s=s.replace("[[960,1440,50],[960,1420,0],[960,680,0],[960,520,0],[960,520,0],[960,520,-90],[960,1660,-1400]],[.98,.98,.66,.28,.28,.30,.7],[18,2,0,0,0,0,0],[-18,-5,0,0,0,0,0]", "[[1900,980,0],[1880,940,0],[1140,560,0],[960,480,0],[960,480,0],[960,480,0],[3453,1215,0]],[.98,.98,.55,.445,.445,.445,1.5],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]")
s=s.replace("title(mapscene,'El mapa completo.',960,175,88,24.75,26.05)","title(mapscene,'El mapa completo.',960,185,88,24.75,25.20)")
s=s.replace("[[960,550,660],[960,540,0],[960,540,0],[1370,485,100]],[.6,.97,.97,.72]", "[[960,540,0],[960,540,0],[960,540,0],[1370,485,100]],[.97,.97,.97,.72]")
s=s.replace("[1030,150,-390],[1030,150,-390]", "[1030,340,-390],[1030,340,-390]")
s=s.replace("tx(editor,'El ritmo,',130,314,123);tx(editor,'resuelto.',130,454,123,col=ORANGE)", "tx(editor,'El ritmo,',130,314,123,0,31.32);tx(editor,'resuelto.',130,454,123,0,31.32,col=ORANGE)")
s=s.replace("pic(formats,'Imagen común','maquina-01.jpg',700,480,1400)", "pic(formats,'Imagen común','maquina-01.jpg',700,795,1400)")
# Local continuation of the same shot from the grid into the hero.
s=s.replace("# 4 Editor: native timeline", "livehero['layers'][0]['sourceOffset']=2.67\n# 4 Editor: native timeline")
# Staged response rather than an unchanging confirmation panel.
s=s.replace("tile(conf,'Ejemplo '+str(i),shots[i],160+j*235,427,s=.36)", "n=tile(conf,'Ejemplo '+str(i),shots[i],160+j*235,427,s=.36)\n anim(n,'opacity',[10.90,11.55+j*.32,11.80+j*.32],[.22,.22,1]);anim(n,'scale',[11.55+j*.32,11.84+j*.32,12.04+j*.32],[[.36,.36],[.41,.41],[.36,.36]])")
s=s.replace("tx(conf,'Antes de gastar.',73,709,45,col=INK)", "n=tx(conf,'Antes de gastar.',73,709,45,13.3,D,col=INK);enter(n,13.3,dx=-70,dy=0,d=.32)")
s=s.replace("# Publish state uses type", "title(edit,'Sin pausas.',960,270,102,31.34,32.50)\n# Publish state uses type")
p.write_text(s)

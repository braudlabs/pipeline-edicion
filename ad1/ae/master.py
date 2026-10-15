from native import *
from PIL import ImageFont
C='AD1 - FINAL'
op('layer.delete',comp=C,layer='PRUEBA sombra')
image(C,'MONTAJE - Remotion sin graficos','AD1-Base.mp4',540,960)
image(C,'MEZCLA - Voz musica y efectos','audio-mix-master.wav',540,960)
for e,b in T['events'].items():
 n='MOTION - '+e;image(C,n,'MG - '+e,540,960)
 props(C,n,startTime=b['from']/48,inPoint=b['from']/48,outPoint=b['to']/48)
flush()
caps=json.load(open(R.parent/'src/captions.json'));measure=[]
for ci,c in enumerate(caps):
 size=c['fontSize'];font=ImageFont.truetype(str(R.parent/'public/assets/Display-Bold.otf'),size)
 def width(t):return font.getlength(t)-max(0,len(t)-1)*size*.025
 widths=[width(w['text']) for w in c['words']];space=font.getlength(' ')-size*.025
 cursor=(1080-sum(widths)-space*(len(widths)-1))/2
 for wi,(w,ww) in enumerate(zip(c['words'],widths)):
  a=w['from'];b=min(c['to'],T['events']['price']['from'])
  if b<=a:continue
  n=f'SUB {ci+1:02d}.{wi+1} | '+w['text'];x=cursor+ww/2;y=1220
  text(C,n,w['text'],x,y,size,WHITE,-25);shadow(C,n,180,4,14)
  props(C,n,inPoint=a/48,outPoint=b/48)
  keys(C,n,POS,[a,a+6],[[x,y+18],[x,y]],78,True)
  keys(C,n,OPACITY,[a,a+4],[40,100],65)
  measure.append({'layer':n,'from':a,'to':b,'left':cursor,'right':cursor+ww,'baseline':y,'size':size})
  cursor+=ww+space
 if ci%4==3:flush()
(R/'caption-layout.json').write_text(json.dumps(measure,ensure_ascii=False,indent=2))
op('timeline.set_active_comp',comp=C);op('timeline.set_time',comp=C,time=12.6)
save('master',extra=[{'name':'ae_save_project','arguments':{}}]+[{'name':'ae_render_frame','arguments':{'compNameOrId':C,'time':t,'outPath':str(R/f'master-{t}.png')}} for t in [1.3,12.6,17.6,23.8,39.5,54.8,67.8,70.1]])

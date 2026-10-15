from pathlib import Path
from PIL import Image,ImageFont
import json,math,numpy as np
R=Path(__file__).resolve().parents[1];A=R/'assets';F=48
INK='#20211f';CREAM='#f4f1ea';RED='#dd4235';BLUE='#5966d8';MUTED='#898980'
S={'fps':F,'master':'AD3 - FINAL','comps':{},'events':{}}
def comp(name,dur,w=1080,h=1920,camera=None):
 c={'name':name,'width':w,'height':h,'duration':dur,'layers':[]}
 if camera:c['camera']=camera
 S['comps'][name]=c;return c
def node(c,t,name,pos=(0,0),a=0,b=None,**kw):
 n={'type':t,'name':name,'pos':list(pos),'from':a,'to':c['duration'] if b is None else b,**kw};c['layers'].append(n);return n
def anim(n,p,frames,values,ease='out'):
 assert len(frames)==len(values) and all(a<b for a,b in zip(frames,frames[1:])),(n['name'],p,frames)
 n.setdefault('anim',{})[p]={'frames':frames,'values':values,'ease':ease};return n
def txt(c,name,s,x,y,size=70,col=INK,a=0,b=None,align='center',font='bold',**kw):return node(c,'text',name,(x,y),a,b,text=s,size=size,color=col,font=font,track=kw.pop('track',-25),align=align,**kw)
def rect(c,name,x,y,w,h,col=INK,a=0,b=None,**kw):return node(c,'rect',name,(x,y),a,b,w=w,h=h,color=col,**kw)
def ellipse(c,name,x,y,w,h=None,col=None,a=0,b=None,**kw):return node(c,'ellipse',name,(x,y),a,b,w=w,h=h or w,color=col,**kw)
def path(c,name,pts,col=RED,width=3,a=0,b=None,**kw):return node(c,'path',name,a=a,b=b,points=pts,stroke=col,strokeWidth=width,**kw)
def media(c,name,asset,x,y,w,a=0,b=None,**kw):
 iw,ih=Image.open(A/asset).size
 return node(c,'image',name,(x,y),a,b,asset=asset,w=w,h=w*ih/iw,anchor=[iw/2,ih/2],**kw)
def nested(c,name,src,x,y,scale=1,a=0,b=None,**kw):
 cc=S['comps'][src];return node(c,'comp',name,(x,y),a,b,source=src,anchor=[cc['width']/2,cc['height']/2],scale=[scale,scale],**kw)
def enter(n,a=0,d=16,axis='y',delta=80,blur=0):
 p=n['pos'];p0=p.copy();p0[0 if axis=='x' else 1]+=delta
 anim(n,'pos',[a,a+d],[p0,p]);anim(n,'opacity',[a,a+min(d,6)],[0,1])
 if blur:anim(n,'blur',[a,a+d],[blur,0])
 return n
def three(n,z=0):n['threeD']=True;n['pos']+=[z];return n
def bg(c,dark=False):
 col,end=('#272b30','#101316') if dark else ('#fcfaf6','#e6e4dc')
 node(c,'gradient','Campo de luz',(540,960),w=1080,h=1920,anchor=[540,960],color=col,endColor=end,center=[470,710],radius=1500)
def camera(frames,values):return {'frames':frames,'values':values,'zoom':1800}
def word_width(s,size):
 font=ImageFont.truetype('/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/ad1-reedit/assets/Display-Bold.otf',size)
 return font.getlength(s)-max(0,len(s)-1)*size*.025

def photo_obj(name,asset,w,h,offset=0):
 c=comp(name,2600,w,h);rect(c,'Papel',0,0,w,h,CREAM,round=18)
 media(c,'Fotografia sustituible',asset,w/2,h/2+offset,w)
 return c

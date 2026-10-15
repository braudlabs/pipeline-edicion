from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'analysis/v3';A=R/'assets';W=1920;H=1080
BG='#F5F5F7';INK='#19191D';BLUE='#0966FF'
def f(s,b=True):return ImageFont.truetype('/Users/alejandrorubiocamarero/Library/Fonts/SFPRODISPLAY'+('BOLD' if b else 'REGULAR')+'.OTF',s)
def tx(im,txt,x,y,s,c=INK,center=False,b=True):
 d=ImageDraw.Draw(im);font=f(s,b);d.text((x,y),txt,font=font,fill=c,anchor='mm' if center else 'lt',stroke_width=0)
def photo(im,n,x,y,w,h):
 p=Image.open(A/f'maquina-{n:02}.jpg').convert('RGB');scale=max(w/p.width,h/p.height);p=p.resize((round(p.width*scale),round(p.height*scale)));p=p.crop(((p.width-w)//2,(p.height-h)//2,(p.width+w)//2,(p.height+h)//2));mask=Image.new('L',(w,h),0);ImageDraw.Draw(mask).rounded_rectangle((0,0,w,h),28,fill=255)
 shadow=Image.new('RGBA',im.size);ImageDraw.Draw(shadow).rounded_rectangle((x,y+15,x+w,y+h+15),32,fill=(15,20,35,34));shadow=shadow.filter(ImageFilter.GaussianBlur(25));im.alpha_composite(shadow);im.paste(p,(x,y),mask)
def board(name,bg=BG):return Image.new('RGBA',(W,H),bg)
# Distinct visual mechanisms: a sentence unfolded into frames; an aperture; a typographic rail.
im=board('A');tx(im,'Una idea.',960,195,158,center=True);tx(im,'Todas sus posibilidades.',960,350,88,'#85858A',center=True)
for j,i in enumerate([10,4,1,11,12]):
 h=[290,400,490,400,290][j];photo(im,i,135+j*337,720-h//2,302,h)
d=ImageDraw.Draw(im);d.rounded_rectangle((832,953,1088,997),22,fill=BLUE);tx(im,'16 escenas',960,975,25,'white',True)
im.convert('RGB').save(O/'A-origen-a-secuencias.jpg',quality=95)
im=board('B','#0C0C10');d=ImageDraw.Draw(im);d.rounded_rectangle((228,123,1692,957),190,fill='#15161C',outline='#45444D',width=2)
for j in range(7):d.rounded_rectangle((280+j*90,168+j*35,1640-j*90,912-j*35),150-j*12,outline='#262833',width=3)
photo(im,1,784,222,352,636);tx(im,'Dentro de la idea.',960,130,86,'#F5F5F7',True)
im.convert('RGB').save(O/'B-apertura-profunda.jpg',quality=95)
im=board('C');tx(im,'Piensa.',110,195,214);tx(im,'Crea.',110,421,214,BLUE);tx(im,'Publica.',110,647,214)
photo(im,1,1250,110,460,818);d=ImageDraw.Draw(im);d.line((945,225,945,845),fill=BLUE,width=5)
for y in [225,535,845]:d.ellipse((932,y-13,958,y+13),fill=BLUE)
im.convert('RGB').save(O/'C-tipografia-causal.jpg',quality=95)
# Chosen opening and resolution. Source text and film tiles remain identifiable through motion.
im=board('start');tx(im,'Tu idea empieza aquí.',960,290,116,center=True);d=ImageDraw.Draw(im);d.rounded_rectangle((345,448,1575,643),42,fill='white',outline='#DDDDE4',width=2);tx(im,'Una máquina que fabrica creativos',420,515,54,b=False);d.ellipse((1444,495,1536,587),fill=BLUE);tx(im,'↑',1490,541,62,'white',True);im.convert('RGB').save(O/'Elegida-inicio.jpg',quality=95)
im=board('logo');d=ImageDraw.Draw(im);d.rounded_rectangle((438,438,604,604),45,fill=BLUE)
for j in range(3):d.rounded_rectangle((469,474+j*32,557+j*8,490+j*32),8,fill='white')
tx(im,'el sistema',655,523,160,center=False);im.convert('RGB').save(O/'Marca-V3.jpg',quality=95)

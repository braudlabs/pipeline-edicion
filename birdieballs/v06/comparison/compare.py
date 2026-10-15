from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,io
p=Path(__file__).parent;root=p.parents[2]
ref=root/'estilo-editor/analysis/refs/v8.mp4';film=p.parent/'Birdieballs-completo-V06.mp4'
rows=[('V8 · continuidad y jerarquía',ref,[452,463,550,575]),('V06 · cambios de ancla en el producto',film,[736,756,757,794]),('V06 · distribución y saltos laterales',film,[170,930,976,1810])]
o=Image.new('RGB',(1080,1680),'#111b16');d=ImageDraw.Draw(o)
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',20)
for row,(title,source,frames) in enumerate(rows):
 y=row*560;d.text((12,y+8),title,font=font,fill='white')
 for col,f in enumerate(frames):
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-vf',f'select=eq(n\\,{f})','-frames:v','1','-f','image2pipe','-c:v','png','-']);im=Image.open(io.BytesIO(raw)).convert('RGB');im.save(p/f'{row}-{f}.jpg',quality=94);o.paste(im.resize((270,480)),(col*270,y+70));d.text((col*270+10,y+42),f'{f*1001/60000:.3f}s · f{f}',font=font,fill='#d8efa5')
o.save(p/'V06-vs-V8.jpg',quality=94)

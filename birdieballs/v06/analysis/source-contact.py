from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io
p=Path(__file__).parent
frames=[19.9,20.7,21.5,22.4,23.3,24.3,25.3,26.3,27.3,28.3,29.3,30.3,31.3,32.3,33.3,34.3,35.3,36.3,37.4]
w,h=216,384;cols=5;o=Image.new('RGB',(w*cols,((len(frames)+cols-1)//cols)*(h+24)),'#17271e');d=ImageDraw.Draw(o)
for i,t in enumerate(frames):
 data=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i','/Users/alejandrorubiocamarero/Downloads/Birdieballs v1 (Sin Postpro).mp4','-frames:v','1','-f','image2pipe','-c:v','png','-']);im=Image.open(io.BytesIO(data));x=i%cols*w;y=i//cols*(h+24);o.paste(im.resize((w,h)),(x,y+24));d.text((x+5,y+4),str(t),fill='white')
o.save(p/'source-tail.jpg',quality=90)

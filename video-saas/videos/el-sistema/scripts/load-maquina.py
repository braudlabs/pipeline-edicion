from pathlib import Path
import subprocess,json,shutil
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];S=Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-24-la-maquina/AD La Maquina - clips');meta=[]
for i,p in enumerate(sorted(S.glob('*.mp4')),1):
 out=R/'assets'/f'maquina-{i:02}.mp4';shutil.copy2(p,out)
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height,r_frame_rate','-of','json',str(out)]));meta.append({'id':i,'source':str(p),'asset':out.name,**d})
 subprocess.run(['ffmpeg','-y','-v','error','-ss','1.5','-i',str(out),'-frames:v','1','-vf','scale=540:960',str(out.with_suffix('.jpg'))],check=True)
 print(i,p.name,d['format']['duration'],flush=True)
im=Image.new('RGB',(1440,2160),'#121212');draw=ImageDraw.Draw(im);f=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',18)
for j,q in enumerate(meta):
 p=R/'assets'/q['asset'];a=Image.open(p.with_suffix('.jpg')).resize((270,480));im.paste(a,((j%4)*360+45,(j//4)*540));draw.text(((j%4)*360+10,(j//4)*540+488),Path(q['source']).name[:29],font=f,fill='white')
im.save(R/'references/maquina-contact.jpg');(R/'analysis/maquina-source.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False));shutil.copy2(S/'BRIEF-EDITOR.txt',R/'analysis/BRIEF-MAQUINA.txt')

import pathlib,subprocess,json,numpy as np
from PIL import Image,ImageDraw
R=pathlib.Path('.');v=R/'output/AD2-La-IA-te-sale-cara-V3.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(v)]));(R/'analysis/v3/final-probe.json').write_text(json.dumps(probe,indent=2))
def audio(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ar','8000','-ac','1','-f','f32le','-']),np.float32)
a=audio(v);b=audio(R/'public/assets/v3/audio-mix-master.wav');results=[]
for t in [1,18,39,61]:
 start=t*8000;n=8000;pad=800;x=a[start-pad:start+n+pad];y=b[start:start+n];corr=np.correlate(x,y,mode='valid');lag=int(np.argmax(corr))-pad;xx=a[start+lag:start+lag+n];results.append({'time':t,'lag_ms':lag/8,'correlation':float(np.corrcoef(xx,y)[0,1])})
(R/'analysis/v3/sync-check.json').write_text(json.dumps(results,indent=2));print('AV frozen-mix sync',results)
# Review real decoded delivery frames, not just composition previews.
times=[.2,2.2,5.0,8.0,11.4,13.8,17.6,18.7,25.6,34.6,38.3,40.3,42.2,44.6,46.35,54,58.5,65.4]
sheet=Image.new('RGB',(6*270,3*510),'#1a1d17');d=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(v),'-frames:v','1','-vf','scale=270:480','-f','rawvideo','-pix_fmt','rgb24','-']);im=Image.frombytes('RGB',(270,480),raw);x=i%6*270;y=i//6*510;sheet.paste(im,(x,y));d.text((x+9,y+486),f'{t:.2f} s',fill='white')
sheet.save(R/'output/hoja-de-revision-V3.jpg',quality=93)
# Frame sequence across the exact three camera moves, preserving time labels.
for name,times in [('camera',[37.875+j/8 for j in range(60)]),('captions',[1.75+j/24 for j in range(24)])]:
 cols=10 if name=='camera' else 8;rows=(len(times)+cols-1)//cols;w,h=162,288
 out=Image.new('RGB',(cols*w,rows*(h+18)),'#1a1d17');draw=ImageDraw.Draw(out)
 for i,t in enumerate(times):
  raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(v),'-frames:v','1','-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-']);im=Image.frombytes('RGB',(w,h),raw);x=i%cols*w;y=i//cols*(h+18);out.paste(im,(x,y));draw.text((x+5,y+h+2),f'{t:.3f}',fill='white')
 out.save(R/f'analysis/v3/final-{name}.jpg',quality=92)
# Safe-zone guide applied to final decoded frames for practical layout inspection.
guide=Image.new('RGB',(3*360,640),'#101010')
for j,t in enumerate([25.6,40.3,65.4]):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(v),'-frames:v','1','-vf','scale=360:640','-f','rawvideo','-pix_fmt','rgb24','-']);im=Image.frombytes('RGB',(360,640),raw).convert('RGBA');ov=Image.new('RGBA',im.size);dr=ImageDraw.Draw(ov);dr.rectangle((0,0,360,89),fill=(255,40,40,55));dr.rectangle((0,416,360,640),fill=(255,40,40,70));dr.rectangle((0,89,21,416),fill=(255,40,40,55));dr.rectangle((339,89,360,416),fill=(255,40,40,55));dr.rectangle((25,100,326,413),outline=(100,255,100,255),width=2);guide.paste(Image.alpha_composite(im,ov).convert('RGB'),(j*360,0))
guide.save(R/'analysis/v3/safe-zone-review.jpg',quality=94)
print('Delivery review sheets and metadata complete.')

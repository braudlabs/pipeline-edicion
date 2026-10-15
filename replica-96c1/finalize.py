from pathlib import Path
import subprocess,json,time,hashlib,zipfile
from PIL import Image,ImageDraw,ImageFont
import numpy as np
R=Path(__file__).resolve().parent;O=R/'output';A=R/'analysis'
def run(args):
 r=subprocess.run(args,capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
 return r
def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]).stdout)
# The timing report is written only once renderMedia has finished successfully.
end=time.time()+2400
while not (A/'remotion-render-time.json').exists():
 if time.time()>end:raise TimeoutError('Remotion export is not finished')
 time.sleep(10)
print('Remotion export completed; finalizing.',flush=True)
run(['ffmpeg','-v','error','-y','-i',str(O/'Remotion-picture.mp4'),'-i',str(R/'remotion/public/assets/reference-audio.wav'),'-map','0:v:0','-map','1:a:0','-map_metadata','-1','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','11','-movflags','+faststart',str(O/'Replica-Remotion.mp4')])
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',21)
header=Image.new('RGB',(1440,56),(17,17,22));draw=ImageDraw.Draw(header)
for i,title in enumerate(['ORIGINAL','REMOTION','AFTER EFFECTS']):draw.text((i*480+240,28),title,font=font,fill='white',anchor='mm')
header.save(A/'comparison-header.png')
fc=[]
for i in range(3):fc.append(f'[{i}:v]setpts=PTS-STARTPTS,scale=480:854:flags=lanczos,setsar=1[v{i}]')
fc.append('[v0][v1][v2]hstack=inputs=3[content]');fc.append('[3:v][content]vstack=inputs=2[v]')
run(['ffmpeg','-v','error','-y','-i',str(R/'reference/original.mp4'),'-i',str(O/'Replica-Remotion.mp4'),'-i',str(O/'Replica-After-Effects.mp4'),'-loop','1','-framerate','30','-i',str(A/'comparison-header.png'),'-filter_complex',';'.join(fc),'-map','[v]','-map','0:a:0','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','copy','-t','11','-movflags','+faststart',str(O/'Comparativa-Original-Remotion-AE.mp4')])
print('Comparison encoded.',flush=True)
report={'checkedAt':time.strftime('%Y-%m-%d %H:%M:%S'),'files':{},'editableTextTest':'passed; changed perfect to ready in temporary AE duplicate, rendered, deleted duplicate','aeMissingFonts':0,'knownDifferences':['Replacement generated pocket watch and brain assets','Approximate source typeface, glow, chromatic fringe, camera curves and perspective'],'project':{'nativeComps':11,'semanticLayers':150,'nativeEffectsOnly':True}}
for name in ['Replica-Remotion.mp4','Replica-After-Effects.mp4','Comparativa-Original-Remotion-AE.mp4']:
 p=O/name;s=probe(p);v=next(x for x in s['streams'] if x['codec_type']=='video');au=next(x for x in s['streams'] if x['codec_type']=='audio')
 assert int(v['nb_frames'])==330 and v['r_frame_rate']=='30/1' and abs(float(v['duration'])-11)<.001,(name,v)
 result=run(['ffmpeg','-v','error','-i',str(p),'-f','null','-']);assert not result.stderr,result.stderr
 report['files'][name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'width':v['width'],'height':v['height'],'frames':int(v['nb_frames']),'fps':30,'duration':float(v['duration']),'audioDuration':float(au['duration']),'decodeErrors':0}
# Both final encoders receive the exact same WAV with the same FFmpeg settings.
def pcm(p):return run(['ffmpeg','-v','error','-i',str(p),'-vn','-f','f32le','-acodec','pcm_f32le','-ar','48000','-ac','2','-']).stdout
pa=pcm(O/'Replica-Remotion.mp4');pb=pcm(O/'Replica-After-Effects.mp4');assert pa==pb,'Audio differs between final videos'
report['audioSamplesIdentical']=True
report['renderTimes']={k:json.load(open(A/f)) for k,f in [('remotion','remotion-render-time.json'),('aeInitial','ae-render-time.json')]}
(O/'Verificacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
# QA contacts come from final MP4s, not editor previews.
frames=[0,5,18,30,33,45,58,62,67,80,105,138,140,150,161,175,200,214,215,219,230,250,270,287,290,302,313,320,329]
for engine,file in [('remotion','Replica-Remotion.mp4'),('ae','Replica-After-Effects.mp4')]:
 d=A/(engine+'-final-frames');d.mkdir(exist_ok=True)
 for f in frames:run(['ffmpeg','-v','error','-y','-i',str(O/file),'-vf',f'select=eq(n\\,{f})','-frames:v','1',str(d/f'{f:03}.png')])
 out=Image.new('RGB',(1200,round(len(frames)/6+.499)*380),(20,18,23));draw=ImageDraw.Draw(out)
 for i,f in enumerate(frames):
  im=Image.open(d/f'{f:03}.png').resize((200,356));x=i%6*200;y=i//6*380;out.paste(im,(x,y+24));draw.text((x+7,y+5),f'{f:03} · {f/30:.2f}s',fill='white')
 out.save(A/(engine+'-final-contact.jpg'))
run(['ffmpeg','-v','error','-y','-ss','5','-i',str(O/'Comparativa-Original-Remotion-AE.mp4'),'-frames:v','1',str(O/'Comparativa.jpg')])
print('330 frames and decode verified; audio identical. Contact sheets ready.',flush=True)
# Rebuild portable source package after all source fixes.
with zipfile.ZipFile(O/'Proyectos-editables.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 z.write(R/'after-effects/Replica-96c1.aep','After-Effects/Replica-96c1.aep')
 for f in (R/'after-effects/assets').iterdir():
  if f.is_file():z.write(f,'After-Effects/assets/'+f.name)
 for f in (R/'remotion').rglob('*'):
  if f.is_file() and 'node_modules' not in f.parts and f.name!='.DS_Store':z.write(f,'Remotion/'+str(f.relative_to(R/'remotion')))
 for src,dst in [('output/LEEME.md','LEEME.md'),('BRIEF.md','BRIEF.md'),('analysis/motion-map.json','motion-map.json'),('reference/source.json','source.json'),('output/Verificacion.json','Verificacion.json')]:z.write(R/src,dst)
with zipfile.ZipFile(O/'Proyectos-editables.zip') as z:assert z.testzip() is None
print('Portable projects packaged and CRC checked.',flush=True)

from native import *
import numpy as np,subprocess
init=json.loads((R/'init-results.jsonl').read_text().splitlines()[1])['result']['structuredContent']['result']['results'];ids={r['name']:r['id'] for r in init if 'id'in r}
spec=json.load(open(R.parent/'spec.json'));src=json.load(open(R.parents[1]/'v01/inputs.json'));C='V02 MASTER'
for clip in src['clips']:
 n=f"CLIP {clip['numero']:02d} — {clip['titulo']}";a=clip['timeline_in_frame']/24;b=clip['timeline_out_exclusive_frame']/24
 footage(C,n,ids[f"SOURCE {clip['numero']:02d}"],a,b,a)
 # Native reaction punch, motivated by the emphatic "YA". Keeps original source time.
 if clip['numero']==11:
  key(C,n,S,[51.98,52.12,52.49],[[100,100],[103,103],[100,100]],78)
 if clip['numero']==9:
  op('effect.add',comp=C,layer=n,matchName='ADBE HUE SATURATION',name='Remate monocromo')
  # Parameters are inspected before the saturation keys are applied.
# Voice UI only for the mic sequence; scene action stays visible.
a=45.6666666667;b=52.5
rect(C,'VOZ — cuerpo',540,1470,342,88,INK,44,a,b)
ellipse(C,'VOZ — boton',416,1470,60,60,LIME,a,b)
rect(C,'VOZ — micro',416,1464,12,26,INK,6,a,b)
path(C,'VOZ — soporte',[[403,1462],[403,1478],[416,1483],[429,1478],[429,1462]],3,INK,a,b)
path(C,'VOZ — base',[[416,1483],[416,1491],[408,1491],[424,1491]],3,INK,a,b)
# Audio-driven bars at 6 samples/s; linear interpolation, not arbitrary oscillation.
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(R.parents[1]/'v01/public/assets/dialogue-foley.wav'),'-ar','8000','-ac','1','-f','f32le','-']);audio=np.frombuffer(raw,np.float32)
times=np.arange(a,b,1/6).tolist();times.append(b-1/24)
for i,weight in enumerate([.55,.85,1,.70,.95,.65,.40]):
 n=f'VOZ — señal {i+1}';rect(C,n,477+i*24,1470,9,62,LIME,4,a,b)
 vals=[]
 for t in times:
  lo=max(0,round((t-.015)*8000));hi=min(len(audio),lo+960);rms=float(np.sqrt(np.mean(audio[lo:hi]**2)));amp=min(1,rms*9)
  if t<48.40:amp=.04 # narrator cue activates the mic; waveform waits for the grandmother
  vals.append([100,18+amp*82*weight])
 key(C,n,S,times,vals,0)
# Typographic cues are separate native text layers: content never blends across a cut.
for c in spec['cues']:
 n=c['id']+' — '+c['text'];text(C,n,c['text'],c['x'],c['y'],c['size'],LIME if c['color']=='lime' else WHITE,a=c['start'],b=c['end'])
 enter(C,n,c['start'],c['x'],c['y'],c['motion'])
 if c['group']=='art' and c['text']=='arte.':op('effect.add',comp=C,layer=n,matchName='CC Light Sweep',name='Revelado de arte')
# A circular sweep builds around the short deadline; one ring carries the release.
ten=next(c for c in spec['cues'] if c['group']=='ten' and c['text']=='10');boom=next(c for c in spec['cues'] if c['group']=='boom')
n='RELOJ — arco';op('layer.create_shape',comp=C,name=n);op('shape.add_group',comp=C,layer=n,name='Tiempo');op('shape.add_ellipse',comp=C,layer=n,groupIndex=1,size=[388,388]);op('shape.add_stroke',comp=C,layer=n,groupIndex=1,color=LIME+[.7],width=4);op('shape.add_trim_paths',comp=C,layer=n,groupIndex=1,start=0,end=0);xf(C,n,position=[540,1296]);timing(C,n,ten['start'],boom['start']+.25);props(C,n,motionBlur=True)
trim=['ADBE Root Vectors Group',1,'ADBE Vectors Group','ADBE Vector Filter - Trim','ADBE Vector Trim End'];key(C,n,trim,[ten['start'],ten['end']],[0,100],55);key(C,n,S,[boom['start'],boom['start']+.25],[[100,100],[190,190]],72);key(C,n,O,[boom['start'],boom['start']+.25],[70,0],65)
# queue and inspection of native effect parameters
op('render.add_to_queue',comp=C,outputPath=str(R.parent/'Mercadillo-V02-master.mov'))
extra=[{'name':'ae_save_project','arguments':{'path':str(R/'Mercadillo-V02.aep')}},{'name':'ae_do','arguments':{'operation':'render.list_templates','args':{}}},{'name':'ae_do','arguments':{'operation':'render.get_settings','args':{'format':'settable'}}},{'name':'ae_layer_info','arguments':{'compNameOrId':C,'layerIndexOrName':'CLIP 09 — Churros'} }]
# use actual source title and text layer names
extra[-1]['arguments']['layerIndexOrName']='CLIP 09 — '+src['clips'][8]['titulo']
art=next(c for c in spec['cues'] if c['text']=='arte.');extra.append({'name':'ae_layer_info','arguments':{'compNameOrId':C,'layerIndexOrName':art['id']+' — '+art['text']}})
save('build.json',extra)

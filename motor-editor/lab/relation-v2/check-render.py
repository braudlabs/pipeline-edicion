"""Decode output frames and measure blue handle centres, independently of SVG state."""
import json, subprocess, hashlib
from pathlib import Path
from PIL import Image, ImageDraw
p=Path(__file__).resolve().parent
plan=json.loads((p/'plan.json').read_text())
n=plan['graphics'][0]['nodes'][0]; s=n['relation']; fps=60000/1001
frames=[60,70,85,95,105,130]
out=p/'decoded'; out.mkdir(exist_ok=True)
select='+'.join(f'eq(n\\,{f})' for f in frames)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'relation-lab.mp4'),'-vf',f'select={select}','-fps_mode','passthrough',str(out/'%02d.png')],check=True)
curves=json.loads((p.parent.parent.parent/'estilo-editor/datos/revision-v2/v8-selector-curves.json').read_text())['rows']
def nominal_width(t):
    f=230+(t-s['closeStart'])*fps
    if f<=230 or f>=300: return s['width']/2
    lo=int(f); fract=f-lo
    def value(frame):
        r=next(x for x in curves if x['frame']==frame)
        return (r['threshold50']['separationX']+r['threshold70']['separationX'])/2/810
    return (value(lo)*(1-fract)+value(lo+1)*fract)*s['width']/2
r=540*.012; top=n['y']/2-s['height']/4-r; bottom=n['y']/2+s['height']/4+r
measurements=[]
for k,f in enumerate(frames,1):
    im=Image.open(out/f'{k:02}.png').convert('RGB')
    centres=[]
    for cy in [top,bottom]:
        weighted=[]
        for y in range(round(cy-r*.4),round(cy+r*.4)+1):
            for x in range(im.width):
                R,G,B=im.getpixel((x,y))
                if B>150 and B>R*1.6 and B>G*1.25: weighted.append((x,B-R))
        centres.append(sum(x*w for x,w in weighted)/sum(w for _,w in weighted))
    width=centres[1]-centres[0]; expected=nominal_width(f/fps)
    measurements.append({'outputFrame':f,'sourceFrameEquivalent':230+(f/fps-s['closeStart'])*fps,'renderedHandleSeparationPx':width,'nominalInstantaneousPx':expected,'differencePx':width-expected})
board=Image.new('RGB',(6*270,2*480+32),'#20242a'); draw=ImageDraw.Draw(board)
for k,f in enumerate(frames,1):
    ref=Image.open(p/'reference-frames'/f'v8-{k:02}.png').convert('RGB').resize((270,480))
    trial=Image.open(out/f'{k:02}.png').convert('RGB').resize((270,480))
    board.paste(ref,((k-1)*270,32));board.paste(trial,((k-1)*270,512))
    draw.text(((k-1)*270+6,8),f'V8 f{round(measurements[k-1]["sourceFrameEquivalent"])} / lab f{f}',fill='white')
board.save(p/'comparison.jpg',quality=94)
qa={'output':'relation-lab.mp4','sha256':hashlib.sha256((p/'relation-lab.mp4').read_bytes()).hexdigest(),'frames':210,'fps':{'num':60000,'den':1001},'dimensions':[540,960],'audio':False,'technicalTestsPassed':64,'typecheck':'passed','handleMeasurement':{'method':'blue pixel weighted centroid on upper/lower handle rows in decoded H264; compares instantaneous model, not shutter integration','samples':measurements,'maxAbsDifferencePx':max(abs(m['differencePx']) for m in measurements)},'visualReview':{'selectedLabFrames':[59,80,98,130],'sourceSamples':[230,240,255,265,275,300],'scope':'mechanism and typography; not full playback, audio or cross-family fidelity','initialRejected':'Bold term/small context hierarchy; shutter blended discrete context labels at the transition' ,'revision':'Regular terms/larger context; independent clip width, no glyph squash; discrete context frozen to presentation frame across shutter samples','pending':['foreground occlusion','calibrated alpha and vertical translation','initial opening and authored exit','integration over client footage','independent family transfer']},'sourceReferenceSha256':'d1f7217c1fad432e80058e9784388d62acb103d041d258f7fd3cff9103cec85b','userApproved':False}
(p/'QA.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps(qa['handleMeasurement'],indent=2))

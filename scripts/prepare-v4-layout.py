import json,pathlib,math
from PIL import ImageFont
R=pathlib.Path(__file__).resolve().parents[1];caps=json.load(open(R/'src/captions-v3.json'));edl=json.load(open(R/'src/edl-v3.json'));faces=json.load(open(R/'analysis/v4/faces.json'))
above={1,2,4,5,6,7,8,11,12};layout=[]
for idx,c in enumerate(caps):
 i=c['clip'];points=[]
 for e in edl:
  if e['id']!=i:continue
  for ff in faces:
   if not ff['file'].startswith(f'{i:02}-') or not ff['faces']:continue
   sample=int(ff['file'].split('-')[1].split('.')[0]);sf=(sample-.5)*6;f=e['fromFrame']+sf-e['sourceFrom']
   if not(c['from']-6<=f<=c['to']+6):continue
   b=max(ff['faces'],key=lambda z:z['w']*z['h']);y=b['y']-.25*b['h'];bottom=b['y']+b['h']
   if i==6:y*=1.08;bottom*=1.08
   elif i in [1,3,13]:y=768+(y-768)*1.065;bottom=768+(bottom-768)*1.065
   points.append((y,bottom))
 head=min((p[0] for p in points),default=410);bottom=max((p[1] for p in points),default=1000)
 if i in above:
  # The complete line, descenders and padding stay above the expanded face box.
  top=278;size=min(80,math.floor((head-top-15)/1.25))
  size=max(44,size);mode='above';keyword=size
 else:
  top=max(1015,math.ceil(bottom+30));mode='below';size=74;keyword=110
  if top+212>1240:mode='inline';top=min(top,1130);size=74;keyword=size
 text=' '.join(w['text'] for w in c['words']);font=ImageFont.truetype(str(R/'public/assets/Display-Bold.otf'),100)
 if mode!='below':size=min(size,math.floor(866*100/font.getlength(text)))
 layout.append({'caption':idx,'mode':mode,'top':top,'fontSize':size,'keywordSize':keyword,'headTop':round(head),'faceBottom':round(bottom)})
json.dump(layout,open(R/'src/caption-layout-v4.json','w'),indent=2)
print('Layout sizes:',[(i,min(z['fontSize'] for z,c in zip(layout,caps) if c['clip']==i),max(z['fontSize'] for z,c in zip(layout,caps) if c['clip']==i)) for i in range(1,15)])

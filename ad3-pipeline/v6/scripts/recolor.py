from pathlib import Path
import json,os,shutil,math
R=Path(__file__).resolve().parents[1];P=R.parent/'v5';rows=[json.loads(s)['result']['structuredContent']['result'] for s in (R/'ae/inspect-results.jsonl').open()]
def rgb(h):return [int(h[i:i+2],16)/255 for i in (1,3,5)]
mapcolors={(39,62,27):'#71352C',(146,189,101):'#E7957D'}
ops=[];changes=[];intervals=[(642,858),(988,1054),(1186,1262),(1508,1712),(1886,2162)]
for row in rows[3:]:
 for l in row['layers']:
  key=tuple(round(x*255) for x in l.get('fillColor',[]))
  if key in mapcolors:
   ops.append({'operation':'text.set_style','args':{'comp':row['compName'],'layer':l['name'],'fillColor':rgb(mapcolors[key])}})
   changes.append({'comp':row['compName'],'layer':l['name'],'old':key,'new':mapcolors[key]})
   if row['compName']=='AD3 - V5 FINAL' and l['enabled']:intervals.append((round(l['inPoint']*48),round(l['outPoint']*48)))
for prop,h in [('ADBE Ramp-0002','#763C31'),('ADBE Ramp-0004','#42241F')]:
 ops.append({'operation':'property.set','args':{'comp':'00 - Verde BRAUD','layer':'Luz radial','property':['ADBE Effect Parade','ADBE Ramp',prop],'value':rgb(h)+[1]}})
 changes.append({'comp':'00 - Verde BRAUD','layer':'Luz radial','property':prop,'new':h})
ops.append({'operation':'comp.set_props','args':{'comp':'AD3 - V5 FINAL','props':{'name':'AD3 - V6 FINAL'}}})
ops.append({'operation':'render.set_output','args':{'queueIndex':1,'outputTemplate':'Calidad alta','outputPath':str(R/'analysis/native-part.mov'),'timeSpanStart':0,'timeSpanDuration':2162/48,'render':True,'skipFrames':0}})
req=[{'name':'ae_save_project','arguments':{'path':str(R/'ae/AD3-Pipeline-V6.aep')}},{'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops,'stopOnError':True}}},{'name':'ae_save_project','arguments':{'path':str(R/'ae/AD3-Pipeline-V6.aep')}}]
for f in [414,900,1625,2070]:req.append({'name':'ae_render_frame','arguments':{'compNameOrId':'AD3 - V6 FINAL','time':f/48,'outPath':str(R/f'analysis/native-{f}.png')}})
for c in ['00 - Verde BRAUD','AD3 - V6 FINAL','01B - Caja continua']:req.append({'name':'ae_layer_info','arguments':{'compNameOrId':c,'layerIndex':'all','includeProperties':True}})
(R/'ae/recolor.json').write_text(json.dumps(req));(R/'analysis/color-changes.json').write_text(json.dumps(changes,indent=2))
affected=sorted(set(i for a,b in intervals for i in range(a//144,(b-1)//144+1)));(R/'analysis/affected-parts.json').write_text(json.dumps(affected))
for i in range(16):
 if i not in affected:
  for ext in ['mp4','json']:os.link(P/f'analysis/parts/{i:02d}.{ext}',R/f'analysis/parts/{i:02d}.{ext}')
for n in ['Montaje-AD3.mp4','Mezcla-Final.wav']:os.link(P/'assets'/n,R/'assets'/n)
shutil.copy2(P/'output/AD3-Pipeline-V5.srt',R/'output/AD3-Pipeline-V6.srt')
(R/'scripts/render-parts.py').write_text((P/'scripts/render-parts.py').read_text().replace('V5','V6'))
print(len(changes),'color properties, affected chunks',affected)

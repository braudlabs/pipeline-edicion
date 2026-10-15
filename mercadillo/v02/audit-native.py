import json
from pathlib import Path
R=Path(__file__).resolve().parent
rows=[json.loads(s) for s in (R/'ae/criterion-results.jsonl').read_text().splitlines()]
comp=next(r['result']['structuredContent']['result'] for r in rows if r['name']=='ae_comp_info')
(R/'ae/native-comp.json').write_text(json.dumps(comp,ensure_ascii=False,indent=2))
spec=json.loads((R/'spec.json').read_text());src=json.loads((R.parent/'v01/inputs.json').read_text())
layers={l['name']:l for l in comp['layers']};errors=[]
for c in spec['cues']:
 name=c.get('aeLayerName',c['id']+' — '+c['text']);l=layers.get(name)
 if not l:errors.append(['missing caption',name]);continue
 for field,expected in [('inPoint',c['start']),('outPoint',c['end']),('fontSize',c['size'])]:
  if abs(l[field]-expected)>1e-7:errors.append([name,field,l[field],expected])
 if l['font']!='SFProDisplay-Bold':errors.append(['font',name,l['font']])
for s in src['clips']:
 name=f"CLIP {s['numero']:02d} — {s['titulo']}";l=layers[name]
 for field,expected in [('inPoint',s['timeline_in_frame']/24),('outPoint',s['timeline_out_exclusive_frame']/24),('startTime',s['timeline_in_frame']/24)]:
  if abs(l[field]-expected)>1e-7:errors.append([name,field,l[field],expected])
collisions=[]
for i,c in enumerate(spec['cues']):
 for d in spec['cues'][i+1:]:
  if c['x']==d['x'] and c['y']==d['y'] and min(c['end'],d['end'])-max(c['start'],d['start'])>1e-7:collisions.append([c['id'],d['id']])
report={'nativeComp':{k:comp[k] for k in ['name','width','height','frameRate','duration','layerCount','shutterAngle','shutterPhase','motionBlur']},'captionsChecked':len(spec['cues']),'sourceClipsChecked':len(src['clips']),'nativeSpecMismatches':errors,'sameAnchorOverlaps':collisions,'criterion':{'layout':'V01 requested composition','font':'SFProDisplay-Bold','baselines':[655,925],'sizes':[211,287],'tracking':-55,'matte':'assets/criterion-matte-25f.mov','matteNote':'Frame 1392 repeats 1393 during fully transparent text start; subsequent frames use original per-frame person segmentation.','outlinePx':1.65,'outlineOpacity':90},'visualChecks':['28 native representative frames reviewed before refinement','6 long-caption layouts corrected and rechecked','7 frames of criterion entrance / settled / exit reviewed'],'limitations':['No independent auditory listening by the agent','Aesthetic approval remains with Ale']}
(R/'QA-native.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2));assert not errors and not collisions

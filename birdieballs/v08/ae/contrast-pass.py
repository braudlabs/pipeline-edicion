from native import *
C='BIRDIEBALLS V08 - MASTER';fps=60000/1001
cs=json.load(open(R.parent/'study/cues-native.json'))
# Keep one stable reading rail below the ball/mouth during the macro reaction.
patch={}
for c in cs:
 if c['block']=='inspection-dialogue':
  dy=(1490 if c['id']=='no-son' else 1680 if c['id']=='nuevas' else 1640)-c['y'];patch[c['nativeLayer']]=dy;c['y']+=dy
for n,dy in patch.items():
 xf(C,n,anchorPoint=[0,-dy]);op('text.set_style',comp=C,layer=n,strokeWidth=1.6)
 op('property.set',comp=C,layer=n,property=['ADBE Effect Parade','Legibilidad',2],value=70)
 op('property.set',comp=C,layer=n,property=['ADBE Effect Parade','Legibilidad',5],value=12)
# Soft localized contrast behind offer support, without recoloring its text.
rect(C,'OFERTA - contraste suave',540,125,1350,535,[.018,.035,.026],0,27.31,31.0)
op('effect.add',comp=C,layer='OFERTA - contraste suave',matchName='ADBE Gaussian Blur 2',name='Difusion')
op('property.set',comp=C,layer='OFERTA - contraste suave',property=['ADBE Effect Parade','Difusion',1],value=160)
xf(C,'OFERTA - contraste suave',opacity=70)
op('layer.move',comp=C,layer='OFERTA - contraste suave',toIndex=74)
key(C,'OFERTA - contraste suave',O,[27.31,27.40,30.89,31.0],[0,70,70,0],65)
# Avoid saying that the old manifest is final; record the actual native anchor offset.
for c in cs:
 if c['nativeLayer'] in patch:c['nativeAnchorPoint']=[0,-patch[c['nativeLayer']]]
 if c['id']=='por-menos':c['size']=192
(R.parent/'study/cues-native-final.json').write_text(json.dumps(cs,ensure_ascii=False,indent=2))
save('contrast-pass.json',[{'name':'ae_save_project','arguments':{'path':str(R/'Birdieballs-V08.aep')}}]+[{'name':'ae_render_frame','arguments':{'compNameOrId':C,'time':t,'outPath':str(R.parent/'stills'/(n+'.png'))}} for n,t in [('contrast-after',24.35),('offer-after',29.66),('new-after',25.38),('dialogue-after',26.42)]])

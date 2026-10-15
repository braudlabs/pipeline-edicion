# Share validated operations and interpolation helpers without executing the source build.
exec(open('braud-style-lab/scripts/build.py').read().split("C='01 - Treinta variantes'")[0].replace('R=Path(__file__).resolve().parents[1]','R=Path("braud-style-lab").resolve()'))
C='01 - Treinta variantes';T='02 - Costo mínimo';M='BRAUDLABS - Motion aislado';BG='00 - Verde texturizado'
info=json.loads(open(R/'ae/build-sources-results.jsonl').readlines()[-1])['result']['structuredContent']['result'];ids={x['name']:x['id'] for x in info['items']}
for c,l,anchor,pos in [(BG,'Fondo - verde texturizado',[540,960],[540,960]),(C,'Plano de variantes - recorrido 3D',[600,600,0],[565.3,904.14,24.07]),(T,'Costo mínimo - recorrido',[600,600],[546,1007])]:
 op('layer.create_footage',comp=M,sourceItemId=ids[c],name=l);op('layer.set_props',comp=M,layer=l,props={'motionBlur':True,'threeDLayer':c==C,'label':13});op('transform.set',comp=M,layer=l,anchorPoint=anchor,position=pos)
l='Plano de variantes - recorrido 3D';data=json.load(open(R/'analysis/plane-motion.json'));end=json.load(open(R/'analysis/end-pose.json'));fr=[383,405,413,418,423,430,438,444,449];vals=[];angles=[]
for f in fr:
 v=data['405'] if f<405 else (data[str(f)] if f<=438 else end)
 t=v['t'];vals.append([540+t[0],960+t[1],t[2]-718.1063]);angles.append(v['angles'])
keys(M,l,P['pos'],fr,vals,'flow',True)
for ax,i in [('rx',0),('ry',1),('rot',2)]:keys(M,l,P[ax],fr,[a[i] for a in angles],'flow')
# Slight native softness matches the reference's enlarged diagram at the end.
fx(M,l,1,'ADBE Gaussian Blur 2','Foco del plano',{'ADBE Gaussian Blur 2-0001':0.4,'ADBE Gaussian Blur 2-0003':0})
keys(M,l,['ADBE Effect Parade',1,'ADBE Gaussian Blur 2-0001'],[413,420,426,444],[.4,3,2.2,2.2],'flow')
l='Costo mínimo - recorrido';fr=[409,413,418,420,426,432,440,449];pos=[[765,1555],[765,1548],[725,1455],[688,1354],[615,1177],[578.5,1083],[554,1022],[545.5,1002]];sc=[.71,.71,.75,.785,.894,.948,.99,1.004]
keys(M,l,P['pos'],fr,pos,'flow',True);keys(M,l,P['scale'],fr,[[100*s,100*s] for s in sc],'flow');keys(M,l,P['rot'],[409,418,426,440,449],[-7,-4,-.7,0,0],'flow')
fx(M,l,1,'ADBE Gaussian Blur 2','Suavidad óptica',{'ADBE Gaussian Blur 2-0001':.8,'ADBE Gaussian Blur 2-0003':0})
keys(M,l,['ADBE Effect Parade',1,'ADBE Gaussian Blur 2-0001'],[417,419,425,449],[4,3,1.1,.8],'flow')
op('layer.create_camera',comp=M,name='Cámara - perspectiva medida');op('layer.set_props',comp=M,layer='Cámara - perspectiva medida',props={'autoOrient':'off'});op('transform.set',comp=M,layer='Cámara - perspectiva medida',position=[540,960,-718.1063]);op('property.set',comp=M,layer='Cámara - perspectiva medida',property=['ADBE Camera Options Group','ADBE Camera Zoom'],value=718.1063)
flush()
op('project.import_file',path=str(R/'assets/Audio-referencia.wav'),name='Audio de BRAUDLABS - referencia reutilizada');op('font.list_missing');op('footage.list_missing');flush()
req.append({'name':'ae_save_project','arguments':{'path':str(R/'ae/BRAUDLABS-Motion-Piloto.aep')}})
for f in [387,405,420,444]:req.append({'name':'ae_render_frame','arguments':{'compNameOrId':M,'time':(f-383)/24,'outPath':str(R/f'analysis/native-{f}.png')}})
req.append({'name':'ae_project_info','arguments':{}})
(R/'ae/build-master.json').write_text(json.dumps(req));print(len(req),'requests')

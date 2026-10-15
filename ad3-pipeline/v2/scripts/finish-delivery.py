from pathlib import Path
import json, shutil, zipfile, hashlib

V=Path(__file__).resolve().parents[1];P=V/'Entrega';D=Path((V/'destination.txt').read_text())
report=json.loads((V/'analysis/final/verification.json').read_text())
responses=[json.loads(l) for l in (V/'ae/collect-results.jsonl').read_text().splitlines()]
assert len(responses)==len(json.loads((V/'ae/collect.json').read_text()))
for r in responses:
 s=r['result'].get('structuredContent',{})
 assert not r['result'].get('isError') and s.get('ok') is not False,r
font,media=[r['result']['structuredContent']['result'] for r in responses[-3:-1]]
assert font['count']==0 and media['count']==0
proj=responses[-1]['result']['structuredContent']['result']
assert not proj['dirty']
files=[i for i in proj['items'] if i.get('file')]
assert all(Path(i['file']).is_file() and str(D) in i['file'] for i in files)
report['nativeProject']={'missingFonts':0,'missingFootage':0,'compositions':sum(i['type']=='CompItem' for i in proj['items']),'layers':sum(i.get('layerCount',0) for i in proj['items']),'editableTextTest':'CAPA V2 - Texto duplicated; native text changed to PRUEBA and rendered. Test comp excluded from delivery.','sourceMediaCollected':len(files)}
report['visualInspection']='Native frames, consecutive frame sequences and final MP4 contact sheet inspected. Browser playback operation verified; not a full continuous audiovisual review.'
(P/'Verificacion').mkdir(exist_ok=True)
(P/'Verificacion/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
(P/'Verificacion/REVISION.md').write_text('''# Revisión V2

## Correcciones realizadas

- Ensamblado, 15–17 s: los primeros recortes dejaban parte de los rostros fuera. Se ajustó el encuadre de las tres imágenes y se separaron pistas, rótulos y subtítulos. Verificado en fotogramas nativos y secuencia del bloque.
- Resolución del ensamblado, 17,5–18,5 s: un fundido cruzado generaba dos tamaños de la misma persona. Se sustituyó por una sola imagen con crecimiento continuo.
- Creatividad y consistencia, 21,5 s y 29 s: se eliminó la mezcla de retrato estático y toma viva; ahora la toma original aparece mediante una apertura de máscara.
- Creatividad, 20,98 s: se separó el marco de onda y la palabra «voz» desplazando la onda hacia arriba. Comprobado en captura nativa y exportación final.

## Alcance de la comprobación

Se inspeccionaron fotogramas y secuencias de movimiento, y se comprobó el funcionamiento del reproductor. No se hizo una escucha completa nueva: la pista de audio comprimida es idéntica a V1. El MP4 se decodifica entero sin errores. Una muestra de 24 fotogramas consecutivos del nuevo motion contiene 24 imágenes distintas. La aprobación creativa corresponde al usuario.
''',encoding='utf8')
shutil.copy2(V/'analysis/final/contacto.jpg',P/'Verificacion/contacto.jpg')
shutil.copy2(V/'analysis/editabilidad.png',P/'Verificacion/editabilidad.png')
shutil.copy2(V/'ae/design.json',P/'Arte/native-design.json')
shutil.copy2(D/'After-Effects/AD3-Pipeline-V2.aep',P/'After-Effects/AD3-Pipeline-V2.aep')
decision=P/'Arte/Decision.md';decision.write_text(decision.read_text().replace('se construirán en After Effects','se han construido en After Effects'))
z=V/'output/AD3-Pipeline-V2-Editables.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for f in sorted(P.rglob('*')):
  if f.is_file() and f.name!='.DS_Store':out.write(f,'AD3-Pipeline-V2/'+str(f.relative_to(P)))
with zipfile.ZipFile(z) as out:assert out.testzip() is None
shutil.copytree(P,D,dirs_exist_ok=True)
shutil.copy2(V/'output/AD3-Pipeline-V2.mp4',D/'AD3-Pipeline-V2.mp4')
shutil.copy2(z,D/z.name);shutil.copy2(z,V.parent/'output'/z.name)
v1=json.loads((V.parent/'CURRENT-VERSION.json').read_text())
state={'version':2,'status':'rendered-and-inspected','userApproval':False,'duration':46.875,'fps':48,'width':1080,'height':1920,'video':str(D/'AD3-Pipeline-V2.mp4'),'aep':str(D/'After-Effects/AD3-Pipeline-V2.aep'),'editables':str(D/z.name),'review':'http://127.0.0.1:8779/Revisar-V2.html','videoSha256':report['videoSha256'],'previousVersion':v1,'creativeDirection':'Petróleo y coral; generated raster materials with native AE cameras, motion and typography.'}
for p in [V/'CURRENT-VERSION.json',V.parent/'CURRENT-VERSION.json',D/'CURRENT-VERSION.json']:p.write_text(json.dumps(state,ensure_ascii=False,indent=2))
assert hashlib.file_digest(open(D/'AD3-Pipeline-V2.mp4','rb'),'sha256').hexdigest()==report['videoSha256']
print(json.dumps({'destination':str(D),'videoMB':round((D/'AD3-Pipeline-V2.mp4').stat().st_size/1e6,1),'zipMB':round(z.stat().st_size/1e6,1),'verification':report},ensure_ascii=False,indent=2))

from pathlib import Path
import json,shutil,zipfile,hashlib
V=Path(__file__).resolve().parents[1];P=V/'Entrega';D=Path((V/'destination.txt').read_text())
r=[json.loads(x) for x in (V/'ae/collect-results.jsonl').read_text().splitlines()]
assert len(r)==len(json.load(open(V/'ae/collect.json')))
for j in r:
 s=j['result'].get('structuredContent',{});assert not j['result'].get('isError') and s.get('ok') is not False and not s.get('result',{}).get('failed'),j
fonts,media=[x['result']['structuredContent']['result'] for x in r[-3:-1]];assert fonts['count']==media['count']==0
proj=r[-1]['result']['structuredContent']['result'];assert not proj['dirty']
files=[i for i in proj['items'] if i.get('file')];assert all(Path(i['file']).is_file() and str(D) in i['file'] for i in files)
report=json.load(open(V/'analysis/final/verification.json'));old=json.load(open(V.parent/'CURRENT-VERSION.json'));assert old['version']==2
assert hashlib.file_digest(open(old['video'],'rb'),'sha256').hexdigest()==old['videoSha256']
report['V2Unchanged']=True;report['nativeProject']={'missingFonts':0,'missingFootage':0,'compositions':sum(i['type']=='CompItem' for i in proj['items']),'layers':sum(i.get('layerCount',0) for i in proj['items']),'mediaCollected':len(files),'editabilityTest':'Native text Cortes changed to planos in duplicated PLIEGO; rendered and inspected. Test comp removed from delivery.'}
report['nativeRender']='Frames 0–449 reused from unchanged V2 native render; frames 450–2249 rendered natively from V3. Final video re-encoded H.264, original AAC copied.'
Q=P/'Verificacion';Q.mkdir(exist_ok=True)
(Q/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
(Q/'REVISION.md').write_text('''# Revisión V3

- Ensamblado 16,7 s: se separó «se ensamblan» de la cabecera del pliego después de revisar el piloto nativo. Comprobado de nuevo en la exportación.
- Sistemas 34–36,5 s: se ajustó el recorrido para que cada categoría pase por el centro antes del alejamiento que revela el conjunto.
- Los subtítulos que cruzaban el inicio de un motion se recortaron a su límite. «Sin volver a» reaparece al finalizar el bloque de consistencia, conservando la continuidad de la locución.
- Editabilidad: duplicado temporal de PLIEGO y cambio de «cortes» a «planos»; la palabra sigue siendo texto nativo. La prueba se excluyó del proyecto final.

Se inspeccionaron fotogramas nativos, secuencias de fotogramas y una hoja del MP4 final. No se afirma haber observado de forma continua la reproducción completa ni una nueva escucha completa. El audio AAC es idéntico al de V1/V2. El MP4 completo se decodifica sin errores. Las pruebas técnicas no constituyen aprobación creativa del usuario.
''')
for src,dest in [(V/'analysis/final/contacto.jpg',Q/'contacto.jpg'),(V/'analysis/editabilidad.png',Q/'editabilidad.png'),(V/'ae/design.json',P/'Diseno/native-design.json'),(D/'After-Effects/AD3-Pipeline-V3.aep',P/'After-Effects/AD3-Pipeline-V3.aep')]:shutil.copy2(src,dest)
z=V/'output/AD3-Pipeline-V3-Editables.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
 for f in sorted(P.rglob('*')):
  if f.is_file() and f.name!='.DS_Store':out.write(f,'AD3-Pipeline-V3/'+str(f.relative_to(P)))
with zipfile.ZipFile(z) as out:assert out.testzip() is None
shutil.copytree(P,D,dirs_exist_ok=True)
shutil.copy2(V/'output/AD3-Pipeline-V3.mp4',D/'AD3-Pipeline-V3.mp4');shutil.copy2(z,D/z.name);shutil.copy2(z,V.parent/'output'/z.name)
state={'version':3,'status':'rendered-and-inspected','userApproval':False,'duration':46.875,'fps':48,'width':1080,'height':1920,'video':str(D/'AD3-Pipeline-V3.mp4'),'aep':str(D/'After-Effects/AD3-Pipeline-V3.aep'),'editables':str(D/z.name),'review':'http://127.0.0.1:8779/Revisar-V3.html','videoSha256':report['videoSha256'],'previousVersion':old,'creativeDirection':'Editorial, primarily guided by user reference 552657: stone and ink backgrounds, Didot/Helvetica Neue typography, photographic circles, fine animated lines, yellow highlights. Native AE graphics, no decorative generated renders.'}
for p in [V/'CURRENT-VERSION.json',V.parent/'CURRENT-VERSION.json',D/'CURRENT-VERSION.json']:p.write_text(json.dumps(state,ensure_ascii=False,indent=2))
assert hashlib.file_digest(open(D/'AD3-Pipeline-V3.mp4','rb'),'sha256').hexdigest()==report['videoSha256']
print(json.dumps({'destination':str(D),'mp4Bytes':(D/'AD3-Pipeline-V3.mp4').stat().st_size,'zipBytes':z.stat().st_size,'project':report['nativeProject']},ensure_ascii=False,indent=2))

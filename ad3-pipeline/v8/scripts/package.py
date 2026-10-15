from pathlib import Path
import json,os,shutil
R=Path(__file__).resolve().parents[1];old=R.parent/'v7';o=R/'output';pack=o/'Proyecto'
def cp(s,d):
    if Path(s).suffix.lower() in ['.mp4','.wav','.jpg','.png']:os.link(s,d)
    else:shutil.copy2(s,d)
shutil.copytree(old/'output/Proyecto',pack,copy_function=cp)
(pack/'After-Effects/AD3-Pipeline-V7.aep').unlink()
for src,dst in [(R/'assets/Voz-Montada.wav',pack/'Audio/Voz-Montada.wav'),(R/'assets/Mezcla-Final.wav',pack/'After-Effects/Assets/Mezcla-Final.wav')]:
    dst.unlink();os.link(src,dst)
srt=(old/'output/AD3-Pipeline-V7.srt').read_text().replace('00:00:39,604 --> 00:00:40,417','00:00:39,604 --> 00:00:40,717')
(o/'AD3-Pipeline-V8.srt').write_text(srt);(pack/'AD3-Pipeline-V7.srt').unlink();(pack/'AD3-Pipeline-V8.srt').write_text(srt)
p=pack/'Remotion/src/timeline.json';timeline=json.loads(p.read_text())
timeline['audioRepairs']=[{'clip':9,'source':'09-linea-produccion.mp4','sourceEndSeconds':5.05,'masterStartSample48kHz':1712005,'voiceStem':'../../Audio/Voz-Montada.wav','description':'Original final 0.30 seconds restored in voice stem; muted picture hold and CTA timing unchanged.'}]
p.write_text(json.dumps(timeline,indent=2,ensure_ascii=False))
shutil.copy2(R/'analysis/audio-repair.json',pack/'REPARACION-AUDIO.json')
p=pack/'LEEME.md';p.write_text('''# AD3 · V8 · Final de «producción» recuperado

1080 × 1920 · 48 fps · 2180 fotogramas · 45,417 segundos.

Abrir **After-Effects/AD3-Pipeline-V8.aep** en After Effects 2026, composición **AD3 - V8 FINAL**. Conserva la paleta verde, las fotografías Soul Cinematic y todas las animaciones de V7. SF Pro Display Bold, sin plugins externos.

## Corrección V8

La toma 09 duraba 5,05 segundos y se había recortado a 4,75. Se ha recuperado el audio original hasta el final, incluida la terminación de «producción», dentro del espacio previo al CTA. No se ha sintetizado voz. La imagen y la duración total son idénticas a V7.

Audio/Voz-Montada.wav contiene la voz reparada; After-Effects/Assets/Mezcla-Final.wav contiene la mezcla final. Música y efectos se conservan. El cambio en la mezcla PCM queda limitado al intervalo 40,250–40,792 s. El SRT amplía el final de «línea de producción» hasta 40,717 s.

Remotion conserva el montaje visual mudo con los diez originales. Ejecutar `npm ci` y `node render.mjs` dentro de Remotion para reconstruir ese metraje. AE añade la mezcla y todos los gráficos nativos. La voz reparada continúa sobre el último fotograma de la toma 09 bajo la escena gráfica; el CTA mantiene su entrada.

## Recursos y edición

00 contiene el fondo común; 01 y 01B contienen la transición a la caja; 04/04A contienen el sistema y las cuatro fotografías; 05 contiene producción y oferta. Los subtítulos del máster son capas nativas. Las imágenes se generaron con Higgsfield Soul Cinematic y se conservan en Assets/*-soul.png. Prompts exactos en PROMPTS-HIGGSFIELD.json. Son ejemplos visuales ficticios, sin fotogramas de los vídeos de referencia.
''')
(pack/'DIRECCION.md').write_text('V8 es una corrección local de audio sobre V7: recuperar el final original de producción. Conserva íntegra la imagen verde y todos los motions aprobados de V7.\n')
h=(old/'output/Revisar-V7.html').read_text().replace('V7','V8').replace('Verde original · Solapes corregidos · Recursos Soul Cinematic.','Final de «producción» recuperado.').replace('00:39 · Producción y oferta','00:39 · Escuchar la corrección')
(o/'Revisar-V8.html').write_text(h)
os.link(old/'output/poster.jpg',o/'poster.jpg')
(R/'serve-review.py').write_text((old/'serve-review.py').read_text().replace('8784','8785'))
info=json.loads((old/'ae/package-results.jsonl').read_text().splitlines()[-1])['result']['structuredContent']['result']
ops=[{'operation':'comp.set_props','args':{'comp':121,'props':{'name':'AD3 - V8 FINAL'}}}]
for item in info['items']:
    if item['type']!='FootageItem' or not item.get('file'):continue
    target=pack/'After-Effects/Assets'/Path(item['file']).name
    assert target.exists(),target
    ops.append({'operation':'footage.replace','args':{'item':item['id'],'path':str(target)}})
ops += [{'operation':'font.list_missing','args':{}},{'operation':'footage.list_missing','args':{}},{'operation':'render.set_output','args':{'queueIndex':1,'outputPath':str(o/'AD3-Pipeline-V8.mp4')}}]
req=[{'name':'ae_do','arguments':{'operation':'project.open','args':{'path':str(old/'output/Proyecto/After-Effects/AD3-Pipeline-V7.aep')}}},
    {'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops,'stopOnError':True}}},
    {'name':'ae_save_project','arguments':{'path':str(pack/'After-Effects/AD3-Pipeline-V8.aep')}},
    {'name':'ae_project_info','arguments':{}}]
(R/'ae/package.json').write_text(json.dumps(req))
print('V8 package staged')

from pathlib import Path
import json,os,shutil
r=Path(__file__).resolve().parents[1];o=r/'output';old=r.parent/'v6/output';pack=o/'Proyecto'
def cp(s,d):
 if Path(s).suffix.lower() in ['.mp4','.wav','.jpg','.png']:os.link(s,d)
 else:shutil.copy2(s,d)
shutil.copytree(old/'Proyecto',pack,copy_function=cp)
(pack/'After-Effects/AD3-Pipeline-V6.aep').unlink()
(pack/'AD3-Pipeline-V6.srt').unlink();shutil.copy2(o/'AD3-Pipeline-V7.srt',pack/'AD3-Pipeline-V7.srt')
for n in ['Montaje-AD3.mp4','Mezcla-Final.wav']:
 p=pack/'After-Effects/Assets'/n;p.unlink();os.link(r/'assets'/n,p)
for n in ['Voz-Montada.wav','Musica.wav','Efectos.wav']:
 p=pack/'Audio'/n;p.unlink();os.link(r/'assets'/n,p)
for n in ['timeline.json','index.tsx']:shutil.copy2(r/'remotion/src'/n,pack/'Remotion/src'/n)
# Same portable render path as delivered projects.
shutil.copy2(r.parent/'v6/output/Proyecto/Remotion/render.mjs',pack/'Remotion/render.mjs')
for n in ['imagenes','videos','avatares','anuncios']:os.link(r/f'assets/generated/{n}-soul.png',pack/f'After-Effects/Assets/{n}-soul.png')
shutil.copy2(r/'assets/generated/prompts-higgsfield.json',pack/'PROMPTS-HIGGSFIELD.json')
(pack/'LEEME.md').write_text('''# AD3 · V7 · Pipeline autónomo

1080 × 1920 · 48 fps · 2180 fotogramas · 45,417 segundos.

Abrir **After-Effects/AD3-Pipeline-V7.aep** en Adobe After Effects 2026. Composición principal: **AD3 - V7 FINAL**. Fuente: SF Pro Display Bold, no redistribuida. Sin plugins externos.

## Cambios de esta revisión

- Recupera exactamente la paleta verde de V5.
- «solo» termina al entrar «Esta», en el fotograma 340.
- El plano de la caja ocupa un panel amplio durante el descenso; el acercamiento termina antes y continúa con el vídeo y sus subtítulos sincronizados.
- Los cuatro ejemplos de imágenes, vídeos, avatares y anuncios usan recursos nuevos generados con **Higgsfield Soul Cinematic**, en lugar de repetir tomas de la presentadora. Son imágenes estáticas dentro de la escena animada; «vídeos» se representa mediante un fotograma de aspecto cinematográfico.
- El cierre hablado y la oferta se retrasan 18 fotogramas (0,375 s); «Entra en» aparece después de terminar «una línea de producción».

## Edición

00 contiene el fondo compartido. 01 contiene el montaje y los nulos **Camara - descenso** / **Camara - entrada al plano**; **01B - Caja continua** conserva el remapeo temporal del vídeo y sus subtítulos. 04/04A contienen el sistema y las cuatro fotografías. 05 contiene la producción y la oferta; **39** es una capa de texto editable. Las capas SUB del máster son subtítulos nativos.

Remotion conserva los diez originales, la línea de tiempo y una pausa de 18 fotogramas antes del último clip. Ejecutar `npm ci` y `node render.mjs` dentro de Remotion para reconstruir el metraje base. Audio contiene voz, música y efectos separados. AE emplea Mezcla-Final.wav.

Los originales de Soul Cinematic están en After-Effects/Assets/*-soul.png. Los prompts exactos y el modelo están en PROMPTS-HIGGSFIELD.json. Son ejemplos visuales ficticios generados para este anuncio. El resto del metraje pertenece a las fuentes AD3; no se inserta material de BRAUDLABS.
''')
p=pack/'CREDITOS.md';p.write_text(p.read_text()+'\n\n## Recursos V7\nCuatro imágenes originales generadas para el bloque Sistema mediante Higgsfield CLI, modelo soul_cinematic (Soul Cinematic), 16-09-2026, 2048 × 2048 px. Solicitudes y prompts registrados en PROMPTS-HIGGSFIELD.json. Coste estimado por el servicio: 0,12 créditos por recurso, 0,48 total. Las imágenes previas de imagegen se descartaron y no forman parte de esta entrega.\n')
(p:=pack/'DIRECCION.md').write_text('V7 recupera la dirección verde de V5 y corrige los puntos señalados por el usuario en V6. Recursos fotográficos diferenciados de Soul Cinematic, sin rediseñar la familia de motion. Mantiene tipografía, grano, geometría y edición previa, con la entrada de caja revisada y pausa breve antes del CTA.\n')
h=(r.parent/'v5/output/Revisar-V5.html').read_text().replace('V5','V7').replace('2161','2179').replace('45.04','45.42').replace('Transición integrada hacia el plano de la caja.','Verde original · Solapes corregidos · Recursos Soul Cinematic.').replace('00:16 · Nueva transición','00:16 · Entrada de caja').replace('<button data-frame="630">','<button data-frame="330">00:07 · Subtítulos corregidos</button><button data-frame="630">')
(o/'Revisar-V7.html').write_text(h);(r/'serve-review.py').write_text((r.parent/'v6/serve-review.py').read_text().replace('8783','8784'))
info=json.loads((r/'ae/patch-results.jsonl').read_text().splitlines()[-1])['result']['structuredContent']['result']
ops=[]
for item in info['items']:
 if item['type']!='FootageItem' or not item.get('file'):continue
 name=item['name'];target=None
 if name.startswith('Soul - '):target=pack/'After-Effects/Assets'/(name[7:]+'-soul.png')
 elif (pack/'After-Effects/Assets'/name).exists():target=pack/'After-Effects/Assets'/name
 if target:ops.append({'operation':'footage.replace','args':{'item':item['id'],'path':str(target)}})
ops += [{'operation':'font.list_missing','args':{}},{'operation':'footage.list_missing','args':{}},{'operation':'render.set_output','args':{'queueIndex':1,'outputTemplate':'H.264: Ajustes de procesamiento de coincidencia, 40\u00a0Mbps','outputPath':str(o/'AD3-Pipeline-V7.mp4')}}]
req=[{'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops,'stopOnError':True}}},{'name':'ae_save_project','arguments':{'path':str(pack/'After-Effects/AD3-Pipeline-V7.aep')}},{'name':'ae_project_info','arguments':{}}]
(r/'ae/package.json').write_text(json.dumps(req));print('Staged package with',len(ops)-3,'media relinks')

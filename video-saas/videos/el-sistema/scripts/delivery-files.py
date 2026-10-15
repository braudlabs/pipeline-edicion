import re
from pathlib import Path
import json,sys
from retime import T,D
R=Path(__file__).resolve().parents[1]
chapters=[('Inicio',0),('La idea',T(9.36)),('El proceso',T(14.23)),('Montaje',T(45.05)),('Versiones',T(53.5)),('Cierre',T(63.22))]
(R/'output/El-Sistema-V2.vtt').write_text('WEBVTT\n\n'+re.sub(r'(\d{2}:\d{2}:\d{2}),(\d{3})',r'\1.\2',(R/'output/El-Sistema-V2.srt').read_text()))
buttons=''.join(f'<button onclick="document.querySelector(\'video\').currentTime={t:.3f}">{s}</button>' for s,t in chapters)
(R/'Revisar-V2.html').write_text('''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>El Sistema · V2</title><style>body{margin:0;background:#0a0a0b;color:#ededea;font:16px Helvetica,Arial,sans-serif;padding:30px}main{max-width:1200px;margin:auto}h1{font-size:24px;letter-spacing:.1em}h1 span{color:#f2b800}p{color:#aaa69c}video{width:100%;max-height:76vh;display:block;background:#000;border-radius:12px}nav{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}button,a{background:#23231e;color:#ededea;padding:10px 16px;border:1px solid #3b3b32;border-radius:20px;text-decoration:none;cursor:pointer}footer{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}</style><main><h1>EL <span>SISTEMA</span> · V2</h1><p>La máquina de fabricar creativos · 65 segundos · After Effects</p><video controls preload="metadata" playsinline src="output/El-Sistema-V2.mp4"><track kind="subtitles" src="output/El-Sistema-V2.vtt" srclang="es" label="Español (opcional)"></video><nav>'''+buttons+'''</nav><footer><a href="output/El-Sistema-V2.mp4" download>MP4</a><a href="ae/El-Sistema-V2.aep" download>Proyecto After Effects</a><a href="output/El-Sistema-V2.srt" download>Subtítulos SRT</a><a href="output/Contacto-V2.jpg">Fotogramas</a></footer></main></html>''')
(R/'ENTREGA.md').write_text(f'''# El Sistema · V2 · La máquina

Vídeo SaaS de {D:.3f} s, 1920 × 1080, 30 fps. Proyecto y motion graphics nativos de After Effects. Versión para revisión del usuario; no se registra como aprobada.

## Archivos

- `output/El-Sistema-V2.mp4`: H.264, audio AAC estéreo.
- `ae/El-Sistema-V2.aep`: 40 composiciones; texto, formas, claves y planos con perspectiva editables.
- `output/El-Sistema-V2.srt`: subtítulos separados de la película. `El-Sistema-V2.vtt` permite activarlos en la página de revisión.
- `output/Contacto-V2.jpg`: fotogramas numerados y tiempos del resultado.
- `assets/Voz-V2.wav`, `Musica-V2.wav`, `Efectos-V2.wav`: pistas separadas. `Mezcla-V2.wav`: mezcla utilizada.
- `Revisar-V2.html`: reproductor local con capítulos.
- `src/design-v2.json` y `scripts/design-v2.py`: fuente de composición; `scripts/build-ae.py --v2` reconstruye la película en el entorno de trabajo original.

## Decisiones

La última indicación del usuario sustituye Denim Trucker por el anuncio de la maquinita. Se usan los 16 clips aportados de ese anuncio para el mapa y una selección de cinco para el montaje demostrativo. Las voces de esos clips no se mezclan con la locución del SaaS.

La interfaz toma su jerarquía y colores de la plataforma real; se reconstruye y simplifica en capas para la película. Los módulos del interior, revisión, editor y variantes son visualizaciones del funcionamiento. No son una grabación de operaciones ejecutadas en el backend. Los fotogramas del moodboard proceden de los vídeos existentes; no se afirma que fueran sus anclas originales. No se atribuye un modelo generativo concreto a La Máquina ni se inventa un descarte documentado.

Las tres referencias aportadas se estudiaron como dirección visual: aproximación al campo de entrada, montaje de módulos y planos oblicuos. No se han insertado sus fotogramas, logotipos o audio. La geometría utiliza planos 3D de AE y perspectiva; no hay modelos 3D volumétricos de la máquina.

Se han eliminado 3,824536 s del centro de 22 pausas de la locución. Se conservan palabras y velocidad original. El mapa `src/retime.json` gobierna las animaciones y el SRT. Se deja cola tras «El Sistema».

## Sonido

Locución ElevenLabs aportada. Música y efectos de la biblioteca local existente; no se han consumido créditos de generación. Clics, escritura, movimientos y encajes se sitúan en el reloj retimado. Mezcla medida: −16,24 LUFS integrados, pico verdadero −1,50 dBTP y rango de sonoridad 3,8 LU.

## Revisión

Comprobados estados clave de las seis partes, mapas antes/después de animar, clips del editor, márgenes de textos y cierres. Correcciones: orden de entrada de los vídeos, escala de la apertura, margen del botón del mapa y subtítulo Clean. Se comprueban además duración, decodificación, audio y medios enlazados en la entrega. La inspección realizada mediante herramientas se basa en fotogramas y secuencias muestreadas; no se presenta como una aprobación estética ni una escucha humana integral.
''')
print('Delivery documents ready')

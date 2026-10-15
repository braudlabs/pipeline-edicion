# Ecommerce / Andrómeda · V01 de revisión

Prueba independiente sobre los 38,333333s disponibles. 920frames, 1080×1920, 24fps,
H264/AAC. **No anuncio final:** el plano06 (35–38,333s) debe sustituirse; faltan07–15
y la selección musical. No se han generado clips ni cambiado el montaje entregado.

## Proyecto editable

- `index.tsx`: composición Remotion, fuentes, texto y animación. Clips identificados por
  escena, con fuentes separadas y cortes exactos. `AndromedaV01` es la composición principal.
- `timeline.json`: EDL de entrada con hashes, IN/OUT exclusivos y estado de cada escena.
- `cues.json` / `build-cues.py`: 41 frases con palabras temporizadas, modo, ancla y tamaño.
  Se mantiene un ancla durante cada frase. El texto se revela sin recentrar palabras previas.
- `study/aligned-words.json`: alineación forzada local MMS_FA del guion corregido contra la
  voz real. No es transcripción independiente ni certificación fonética. Fuente ASR guardada.
- `audio.json` / `build-audio.py`: narrador, susurro colocado, ambiente/SFX y slot de música
  desactivado. Son pistas independientes y editables. Remotion reproduce su mezcla derivada
  `mix-preview.wav`, nunca voces de los brutos además de los stems.
- `public/assets`: ocho clips y voces/stems originales copiados; no modificación de fuentes.
- `narrador-completo-del-tramo.srt`: también conserva las frases omitidas visualmente.

Desde la raíz del workspace:

```sh
python3 ecommerce-andromeda/v01/build-cues.py
python3 ecommerce-andromeda/v01/build-audio.py
node ecommerce-andromeda/v01/render.mjs --bundle --stills
node ecommerce-andromeda/v01/render.mjs
python3 ecommerce-andromeda/v01/verify.py
```

El render usa Remotion4.0.534 del runtime local ya instalado en
`/private/tmp/birdie-v07-runtime`; se puede cambiar mediante `REMOTION_RUNTIME`.
Chromium está fijado al binario disponible en el workspace. No se instala otro editor.

## Decisiones y corrección solicitada por Ale

La primera propuesta ponía captions a y1470–1740. Ale pidió subirlos para Meta. Queda
reemplazada por anclas entre y775–1190 en los planos de narración. Excepción justificada:
plano06 a y430 para no tapar el reproductor que ocupa casi toda la zona central. Las
anclas son revisadas sobre imagen; no una posición universal del algoritmo.

Hook: rail al pecho, «cada semana» compacto en una línea. Espera: «días y días» construye
una sola línea; se descartaron stack de dos líneas y sustitución aislada. Ticket: solo
«semanas» sobre el panel libre, sin texto sobre el papel ni manos. Entrega de la pieza y
gag de sudadera: voz íntegra, texto omitido deliberadamente. Apagados: texto entre caras
y pantallas. Repetición: «otra puta vez» debajo de las caras y antes de la bobina. No hay
blancos/negros, zooms ni whooshes añadidos que dupliquen el movimiento de la fuente.

El rail normal cambia directamente; los énfasis tienen entrada por un eje de5frames.
Obturador180°/8muestras solo en el texto que se mueve, con selección discreta de palabras
por frame para no mezclar strings. Curvas y tamaños son propuestas para esta pieza, no
keyframes originales recuperados del editor profesional.

La guía de revisión Meta (`stills/review-meta-board.jpg`) es orientativa y no se quema en
el vídeo. El placement real debe comprobarse en Ads Manager. No se reservó banda ni se
movió el metraje para acomodar captions. Las páginas oficiales consultadas redirigieron
a login; no se afirma que esa guía sea una captura actual de la interfaz.

## Qué se ha verificado y qué falta

Hashes8/8, continuidad de920frames, ticket con IN12frames, puente03b de58frames, límites
de texto sin solape de frases y TypeScript. Revisión de23fotogramas, conceptos y guía
central. Audio mezclado desde los mismos tres stems y con limitador0,96/compensación de
latencia; sin retiming ni voces nuevas. Se comprobaron16fotogramas en los inicios/finales de los ocho clips contra sus índices fuente,
y seis ventanas de audio con0ms de desplazamiento frente a la mezcla entregada al render.
Eso comprueba conservación técnica, no escucha ni lipsync. Evidencia en `QA.json`.

La revisión normal de audio y lipsync del hook sigue pendiente. `dapi --help` no respondió;
no se atribuye escucha al alineador ni a una hoja de contacto. Tampoco hay aprobación
artística de Ale. El plano06 sigue mostrando la interfaz antigua y es PROVISIONAL:
esta edición no intenta disimularlo ni darlo por terminado.

Al recibir06 definitivo: sustituir su fuente sin mover las voces y rehacer su layout.
07 debe enlazar con su último frame utilizado, recortando prefijos realmente duplicados.
Conservar el hueco07/08 antes de09; no pegar el gag09 directamente al final actual.

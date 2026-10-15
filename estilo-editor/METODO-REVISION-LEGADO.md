# Revisión forense de un tramo de vídeo — instrucciones

## Para qué sirve tu trabajo

Ale tiene diez vídeos montados por un editor profesional (anuncios verticales de BRAUDLABS y
LaFabrica, y un vídeo horizontal de landing). Quiere reproducir ese estilo de edición con
Remotion (React), sin After Effects. Para eso hay que convertir el estilo en un «algoritmo»:
reglas y parámetros medidos que digan qué hacer en cada momento de un montaje.

Tú revisas **un tramo** de uno de los vídeos y dejas por escrito, con precisión de fotograma,
todo lo que hace el editor en él. Otros agentes revisan los demás tramos. Después se juntan
todas las notas para derivar las reglas. Lo que no anotes se pierde: nadie más va a mirar tus
fotogramas.

El usuario pidió expresamente que el estudio sea **fotograma a fotograma, sin muestrear**,
porque los «mini detalles» (una entrada de 3 fotogramas, un destello de 1, un desenfoque, un
desplazamiento de pocos píxeles) son justo lo que distingue este montaje. Trátalo así.

## Qué tienes

Directorio de trabajo: `/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/estilo-editor`
(ejecuta los comandos desde ahí).

**Hojas densas** — `analysis/dense/<slug>/dNNN_fAAAAA-fBBBBB.jpg`. Contienen TODOS los
fotogramas en orden, cada uno rotulado con número de fotograma y segundo. Solo faltan las
repeticiones exactas del fotograma anterior; el fotograma conservado lleva «+k» (le siguen k
repeticiones idénticas). Barra roja/naranja sobre una miniatura = el detector marcó ahí un
corte (confianza alta/media); es una pista, no un veredicto.

**Datos medidos por código sobre cada fotograma** — `datos/<slug>/`:
- `texts.tsv` / `texts.json`: cada rótulo en pantalla como «pista»: fotograma de entrada y
  salida, centro (% del fotograma), alto y ancho en px, ángulo, y su geometría fotograma a
  fotograma. Lo leyó un OCR: el texto puede tener erratas («nimehan» = «ni me han») y la caja
  baila ±15 px; fíate del tiempo, contrasta la geometría fina con tus ojos o con `inkbox.py`.
- `words.json`: locución transcrita con el inicio y fin de cada palabra (precisión ≈ ±50 ms).
- `cuts.json`, `bursts.json`: cortes candidatos y ráfagas de movimiento fuerte.
- `faces.json`: caja de la cara por fotograma.
- `audio.json`: sonoridad, golpes (onsets) con su perfil, rejilla de tempo estimada.
- `repeats.json`: qué fotogramas son repeticiones exactas y cadencia del metraje.

**Espectrogramas anotados** — `analysis/spectro/<slug>/s_TTT-TTT.png`, uno por cada 8 s, con
cortes (rojo), palabras de la locución (azul) y golpes de audio (amarillo). No puedes oír el
audio; léelo aquí: un barrido de ruido ancho que crece = whoosh/riser; una línea vertical
con cola en graves = golpe/impacto; rayas horizontales estables = música o tono; un hueco =
silencio.

**Herramientas** (todas en `scripts/`):

```bash
# Cronología fusionada: cortes, rótulos, voz, golpes y caras.
python3 scripts/digest.py <slug> <f0> <f1>              # todo tu tramo: es tu mapa
# Con --anim añade la geometría de cada rótulo fotograma a fotograma en su entrada y salida.
# Es muy largo: úsalo sobre subtramos cortos (40-120 fotogramas), no sobre el tramo entero.
python3 scripts/digest.py <slug> <a> <b> --anim

# Fotogramas a resolución NATIVA (para tipografía, bordes, sombras, desenfoques, destellos).
python3 scripts/sheet.py <slug> --range 120:131 --full --w 540 --cols 6 -o analysis/tmp/<tu-id>/x.jpg
python3 scripts/sheet.py <slug> --frames 124,125,126 --full --crop 0.1,0.55,0.8,0.25 --cols 3 -o analysis/tmp/<tu-id>/y.jpg
#   --crop x,y,ancho,alto normalizados 0..1 ; sin --w conserva el tamaño real del recorte
#   sin --full usa los fotogramas a 360 px de ancho (rápido, para repasar movimiento)

# Caja exacta de la tinta de un rótulo, fotograma a fotograma (curvas de entrada/salida al píxel).
python3 scripts/inkbox.py <slug> --range 185:200 --roi 0.05,0.40,0.9,0.22 --mode bg     # fondo plano
python3 scripts/inkbox.py <slug> --range 40:60 --roi 0.2,0.55,0.6,0.1 --mode white      # texto blanco sobre imagen oscura

# Color exacto en puntos de un fotograma (px del original).
python3 scripts/px.py <slug> 190 540,960 100,100
```

Las imágenes se ven con la herramienta Read. Mantén cada hoja que generes por debajo de
~1600 px de ancho para que no se reduzca al verla.

## Procedimiento obligatorio

1. Lee la cronología de tu tramo entero con `digest.py <slug> <f0> <f1>` (sin `--anim`). Es tu mapa.
   Después, hoja a hoja, pide `--anim` del subtramo que estés mirando para tener la geometría de cada rótulo.
2. Mira **todas** las hojas densas de tu tramo, en orden, una a una. No te saltes ninguna
   aunque «parezca lo mismo»: ahí es donde aparecen los detalles. Ve escribiendo las notas en
   tu archivo según avanzas (cada 3–4 hojas), no al final.
3. En cada suceso —corte, transición, entrada o salida de un rótulo, palabra de énfasis,
   escena gráfica, efecto de color, congelado, movimiento de cámara, superposición— saca la
   secuencia a resolución nativa de los fotogramas implicados (y uno o dos antes y después) y
   descríbela fotograma a fotograma. Recorta la zona cuando haga falta ver bordes, sombras,
   contornos o desenfoque.
4. Mide cuando se pueda: duraciones en fotogramas, posiciones y tamaños en px y en % del
   fotograma, colores con `px.py`, curvas con `inkbox.py` o con la geometría de `--anim`.
   Para una entrada, da los valores fotograma a fotograma (p. ej. «alto: f124 0 %, f125 62 %,
   f126 84 %, f127 95 %, f128 100 %»), no solo «entra rápido».
5. Lee los espectrogramas de tu tramo y relaciona cada sonido con lo que pasa en imagen:
   qué suena, cuántos fotogramas antes o después del suceso visual, y sobre qué palabra.
6. Verifica los cortes: confirma o descarta cada candidato del detector y añade los que se
   le escaparon (un salto de encuadre en un busto parlante, un corte dentro de un movimiento).
7. Guarda hasta 8 láminas de evidencia de lo más característico en
   `laminas/<slug>/<tu-id>-NN-descripcion.jpg` (≤1600 px de ancho).

## Qué anotar — plantilla del archivo de notas

Escribe en `analysis/notas/<tu-id>.md`, en español, con estas secciones. Cita siempre
fotogramas («f124–f129») y segundos. Separa lo que **ves o mides** de lo que **interpretas**
(marca la interpretación con «Lectura:»). Si algo no se distingue, dilo; no rellenes.

```
# <slug> · f<inicio>–f<fin> · <tu-id>

## 1. Planos
Tabla: fotogramas, duración (f y s), tipo (busto parlante / recurso / gráfico a pantalla
completa / congelado / logo…), escenario y vestuario, encuadre (tamaño y posición de la
cara según `digest`), movimiento de cámara dentro del plano (estático, cámara en mano,
acercamiento lento… con cuánto cambia la escala o la posición), tratamiento (color, B/N,
tinte, viñeta, grano, nitidez), cadencia (¿el metraje va a menos fps que la línea de tiempo?).

## 2. Cortes y transiciones
Una entrada por cada cambio de plano: fotograma exacto, tipo (corte seco, corte con cambio
de escala, destello, barrido, desenfoque, fundido, deslizamiento…), duración en fotogramas,
descripción fotograma a fotograma, sobre qué palabra o pausa de la voz cae, y qué sonido lo
acompaña. Indica si el corte es a otro escenario, a otra escala del mismo plano o a un
gráfico.

## 3. Subtítulos base
El sistema de subtítulos del tramo: cuántas palabras por unidad, si sustituyen o se
acumulan, posición (centro en %), tamaño (alto en px), caja (mayúsculas/minúsculas),
color, sombra/contorno, interletrado, cómo entra cada palabra (fotograma a fotograma:
opacidad, escala, desplazamiento, desenfoque), cómo sale, cuánto dura en pantalla y su
relación con la voz (¿aparece antes, a la vez o después de la palabra? ¿cuántos fotogramas?).
Anota las excepciones: palabras que no se subtitulan, huecos sin subtítulo, cambios de
posición y por qué (¿evita la cara, un objeto, otro rótulo?).

## 4. Palabras de énfasis y tipografía cinética
Cada palabra o grupo destacado: qué palabra, qué papel tiene en la frase (cifra, verbo,
negación, marca, remate…), tamaño (alto en px y %), posición, color, orden de capas
(¿delante o detrás del sujeto?, ¿contorno por delante?), relación con la línea pequeña
(encima, debajo, sustituye), entrada fotograma a fotograma con valores, tiempo en pantalla,
salida. Cómo se recoloca el conjunto cuando llega una palabra nueva.

## 5. Escenas gráficas (motion graphics)
Para cada una: fondo (color medido, degradado, viñeta, textura, grano), elementos, tipografía,
jerarquía, coreografía completa fotograma a fotograma (qué se mueve, cuándo, cuánto, con qué
forma de curva: arranque brusco y frenada larga, rebote, lineal…), cámara (¿2D?, ¿perspectiva
3D?, ¿recorrido?), desenfoque de movimiento, contadores, líneas y formas, cómo entra y cómo
sale la escena, sincronía con la voz y con el sonido.

## 6. Superposiciones y efectos sobre la imagen
Recuadros, líneas, iconos, emojis, pegatinas, capturas, interfaces, máscaras (texto detrás del
sujeto), cambios de color, viñetas, fugas de luz, temblor, brillo, zoom digital, ralentí o
aceleración, fotogramas congelados. Con fotogramas y medidas.

## 7. Sonido
Lo que se lee en el espectrograma: música (¿hay?, ¿cuándo entra, cambia o se corta?),
efectos (tiempo, tipo probable, suceso visual al que acompañan y desfase en fotogramas),
silencios y pausas de la voz, cambios de nivel.

## 8. Ritmo
Cuántas cosas cambian por segundo; qué cambia con cada frase; el tramo más largo sin ningún
cambio visual (en fotogramas); dónde se acelera y dónde respira.

## 9. Reglas que se deducen de este tramo
Reglas del tipo «cuando pasa X, el editor hace Y», cada una con los fotogramas que la
respaldan. Solo las que este tramo demuestra.

## 10. Dudas y lo que no se pudo verificar

## 11. Láminas guardadas
```

Al final del archivo añade un bloque ```json con la lista de sucesos normalizada, para poder
contarlos entre vídeos:

```json
[{"tipo": "corte|transicion|enfasis|grafico|superposicion|efecto|congelado|camara|sfx|subtitulo_excepcion",
  "f0": 124, "f1": 137, "nombre": "palabra gigante", "texto": "pagado", "detalle": "entra desde abajo 6 f con fundido"}]
```

## Vocabulario de partida

Úsalo cuando encaje y acuña nombres nuevos cuando veas algo distinto:
- **subtítulo palabra a palabra**: una sola palabra en pantalla que sustituye a la anterior.
- **línea acumulativa**: palabras pequeñas que se van sumando en la misma línea («ni» → «ni me» → «ni me han»).
- **palabra gigante**: la palabra clave de la frase a gran tamaño, normalmente bajo la línea pequeña.
- **texto detrás del sujeto**: rótulo grande tapado por la persona, a veces con su contorno fino dibujado por delante.
- **texto en arco**: palabras sobre un trazado curvo.
- **recuadro de cara**: cuadrado fino que sigue a la cara.
- **congelado en B/N**: el plano pasa a blanco y negro y se detiene como una foto.
- **interludio gráfico**: escena de motion graphics a pantalla completa entre planos de persona.
- **contador**: cifra que sube hasta su valor.
- **rótulo de nombre**: nombre y cargo de quien habla.
- **subtítulo de color**: subtítulo en otro color para otro hablante o una exclamación.

## Lo que ya se sabe (no hace falta redescubrirlo, sí confirmarlo o matizarlo)

- Los vídeos son 1080×1920 (la landing 1920×1080). Líneas de tiempo a 24, 29,97 y 60 fps; el
  metraje de persona suele ir a ~24–25 fps repetido dentro de las líneas de 30 y 60, mientras
  los rótulos se animan a la cadencia completa.
- La voz va a ~3 palabras por segundo, casi sin pausas.
- El subtítulo base es de una palabra, blanco, en minúsculas, de palo seco muy apretado,
  centrado hacia el 60 % de la altura; ciertas palabras crecen hasta ocupar el ancho.

## Medido por código sobre todos los vídeos (contrástalo con lo que veas; anota toda excepción)

- **Tipografía**: SF Pro Display Bold con interletrado ≈ −60 milésimas de eme (solape 0,92–0,96 con la
  tinta real en tres muestras). En la landing hay además un peso fino de la misma familia para líneas
  secundarias. El subtítulo base de los verticales de BRAUDLABS mide ≈ 98 px de cuerpo.
- **Subtítulo base**: aparece a su tamaño y posición finales desde el primer fotograma legible y no
  deriva mientras está en pantalla. Falta saber si antes hay 1–2 fotogramas de fundido o desenfoque:
  míralo a resolución nativa en varias palabras.
- **Sincronía**: cada palabra aparece escrita en el fotograma en que empieza a sonar (desfase mediano 0;
  entre −2 y +2 fotogramas a 24 fps, que es el margen de error de la transcripción).
- **Palabra gigante**: ocupa ≈ 70–76 % del ancho del fotograma sea cual sea su longitud (el cuerpo se
  ajusta a la anchura).
- **Cortes**: caen sobre el inicio de una palabra (mediana 0 fotogramas de separación).
- **Gráficos a pantalla completa** (visto en V1): el texto está en un plano con perspectiva (crece hacia
  un lado) y deriva lentamente de escala mientras se lee. Comprueba si pasa en el tuyo y mídelo.

## Reglas de trabajo

- Solo puedes escribir en `analysis/notas/<tu-id>.md`, `analysis/tmp/<tu-id>/` y
  `laminas/<slug>/`. No modifiques ni borres nada más. No uses red.
- No des nada por visto sin mirarlo. Si afirmas un valor, que salga de una medida o de un
  fotograma que hayas abierto.
- Tu mensaje final debe ser breve: ruta del archivo de notas, las 5–8 observaciones más
  importantes, y lo que quedó sin verificar. El detalle va en el archivo.

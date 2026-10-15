# Ecommerce Andrómeda · C04 (Claude) · versión completa 0–85,417 s

C03 (0–38,333 s) se conserva intacta en `../c03/` (y C02/C01 en `../c02/` y `../c01/`). C04 amplía el
montaje a la timeline completa de la entrega del director (`MASTER_COMPLETO_24FPS`: 17 unidades,
2.050 f a 24 fps = 85,416667 s, con la locución original de 85,39425 s entera) y sustituye el 06
provisional por la v5. Lleva **subtítulos en las 17 unidades** (06 rehecho para la v5; 07–15 nuevos) y la
**banda sonora** (toma 2 de ElevenLabs montada a la timeline en `../music/`) en su propia pista, con ducking
bajo el narrador. Sigue siendo un **WIP con las observaciones visuales del director** (UI de 06/07/08,
proyección de 12, anticipación de 09): ver «Pendiente».

## Qué cambia frente a C03

1. **Timeline completa.** `src/data/timeline.json` se genera con `build-timeline.py` desde el JSON del
   máster (ya no hay lista `pending`). El JSON y el brief coinciden en fotogramas, archivo, IN/OUT y estado
   de las 17 unidades (comprobado unidad por unidad, y el CSV también). Los ids de 00–06 son los de C03 (los
   usan los stems); el id exacto del máster queda en `masterId`.

   | id | `from` | `dur` | `srcIn` | clip (`public/assets/clips/`) | estado (máster) | ambiente nativo: ganancia · LUFS |
   |---|---:|---:|---:|---|---|---|
   | 00_hook | 0 | 130 | 0 | `00_HOOK_visual_aprobado_audio_nativo_no_final.mp4` | VISUAL_APROBADO_AUDIO_ORIGINAL_EN_PREVIEW_QC_FINAL_PENDIENTE | 0,8 · -18,9 |
   | 01_ventanilla | 130 | 220 | 0 | `01_ventanilla_espera.mp4` | UTILIZABLE_BASE_DEL_MONTAJE | 0,65 · -20,5 |
   | 02_ticket | 350 | 100 | 12 | `02_ticket_angulo.mp4` | UTILIZABLE_BASE_DEL_MONTAJE | 0,65 · -26,7 |
   | 03_apagados | 450 | 102 | 0 | `03_ads_apagados.mp4` | UTILIZABLE_BASE_DEL_MONTAJE | 0,75 · -30,9 |
   | 03b_repetir | 552 | 58 | 0 | `03b_repetir.mp4` | UTILIZABLE_BASE_DEL_MONTAJE | 0,75 · -26,9 |
   | 04_sudadera | 610 | 172 | 0 | `04_sudadera.mp4` | UTILIZABLE_BASE_DEL_MONTAJE | 0,75 · -30,5 |
   | 05_presentacion | 782 | 58 | 0 | `05_presentacion.mp4` | UTILIZABLE_BASE_DEL_MONTAJE | 0,6 · -17,0 |
   | 06_cinco_ads | 840 | 80 | 0 | `06_V5_CANDIDATO_FILA_DUPLICADA.mp4` | CANDIDATO_UI_FILA_DUPLICADA | 0,75 · -36,1 |
   | 07_gestion | 920 | 102 | 0 | `07_CAMPANAS_V3_REVISADO.mp4` | UTILIZABLE_PREVIEW_CON_LIMITACIONES | 0,75 · -31,6 |
   | 08_optimizacion | 1022 | 215 | 0 | `08_GAG_V3_CANDIDATO_UI_PENDIENTE.mp4` | CANDIDATO_VISUAL_UTILIZABLE_CON_LIMITACIONES | 0,75 · -31,8 |
   | 09_papeles | 1237 | 103 | 0 | `09_PAPELES_V2_GENERADO_AJUSTE_DE_BEAT.mp4` | GENERADO_DISPONIBLE_CON_OBSERVACION_DE_BEAT | 0,65 · -21,7 |
   | 10_fundadores | 1340 | 138 | 0 | `10_FUNDADORES_VISUAL_REVISADO.mp4` | VISUAL_REVISADO_AUDIO_FINAL_PENDIENTE | 0,75 · -33,2 |
   | 11_criterio | 1478 | 107 | 0 | `11_CRITERIO_VISUAL_REVISADO_AUDIO_PENDIENTE.mp4` | VISUAL_REVISADO_AUDIO_FINAL_PENDIENTE | 0,65 · -20,3 |
   | 12_habitacion | 1585 | 96 | 0 | `12_HABITACION_V3_CANDIDATO_PROYECCION.mp4` | CANDIDATO_VISUAL_CON_LIMITACIONES | 0,65 · -20,4 |
   | 13_metagag | 1681 | 105 | 0 | `13_METAGAG_VISUAL_REVISADO.mp4` | VISUAL_REVISADO_AUDIO_FINAL_PENDIENTE | 0,75 · -33,7 |
   | 14_cta | 1786 | 205 | 0 | `14_CTA_HONESTO_VISUAL_REVISADO.mp4` | VISUAL_REVISADO_AUDIO_FINAL_PENDIENTE | 0,65 · -21,4 |
   | 15_salida | 1991 | 59 | 18 | `15_SALIDA_V2_PANTALLA_ENCENDIDA.mp4` | VISUAL_REVISADO_AUDIO_FINAL_PENDIENTE | 0,65 · -26,5 |

   Total 2.050 f contiguos; OUT exclusivo; 02 entra en 0,5 s (12 f) y 15 en 0,75 s (18 f, 59 f). Los clips
   00–05 son byte a byte los de C03 (sha256 de la entrega, `source-notes/sha256.txt`); los de 06–15 son copias
   idénticas de `01_CLIPS`.
2. **06 = v5.** `06_V5_CANDIDATO_FILA_DUPLICADA.mp4` (80 f, IN 0) sustituye al provisional. Su UI trae la fila 5
   duplicada (observación del director, sin corregir). Los rótulos del 06 se rehacen para la v5 (`Scene06.tsx`):
   banda entre las barbillas y el canto de la pantalla, sobre los torsos; la pantalla queda limpia.
3. **Audio nativo de las 17 unidades**, cada una en su IN/OUT exacto y en su posición del máster, con
   microfundidos de 8 ms (`build-audio.py` → `public/assets/audio/stems/native-<id>.wav`, WAV 16 bits, 48 kHz).
   Las ganancias de 00–05 son las de C03 y el hook sigue con su audio nativo (voz generada incluida, por
   instrucción de Ale; no se usa `AZUL_SUSURRO`). Las de 06–15 salen de medir cada stem (EBU R128, tabla
   anterior): 0,65 por defecto y 0,75 —el mismo criterio que C03 aplicó a 03 y 04 (−31 y −30 LUFS)— a los que
   quedan en −30 LUFS o menos: 06 (−36,1), 07, 08, 10 y 13. El 06 ya no necesita el 0,42 del provisional (su
   tono de interfaz a −13,9 LUFS no existe en la v5). Los stems 00–05 y el de SFX se regeneran byte a byte
   iguales a los de C03 (comprobado).
   - Incidencia 12: la fuente trae 32 ms menos de audio que de vídeo (3,968 s frente a 4,000 s); las últimas 1.536
     muestras del stem son silencio y el microfundido de salida se aplica al final del audio real.
4. **Narrador completo e intacto.** `narrador.wav` cubre 0–85,39425 s (4.098.926 muestras) sin retiming, recorte ni
   fundidos; es WAV float32, idéntico muestra a muestra (error máx. 0) a la decodificación del mp3. El mp3 es mono:
   el `-ac 2` de ffmpeg lo reparte con −3 dB por canal, igual que en C03 y en el preview del director (medido:
   0,705 frente a su stem mono), así que el equilibrio con los ambientes de 00–05 es el mismo que en C03.
5. **Composiciones** (`src/index.tsx`): `AndromedaC04` (2.050 f a 24 fps), `AndromedaC04-144` (12.300 f, `TimeScale` 6) y
   `AndromedaC04-60` (5.125 f, `TimeScale` 2,5), más `HookStudy`. La duración sale de `timeline.json`. A 60 fps los
   cortes en fotograma impar (09, 12, 13, 15) caen en medio fotograma y `VideoSpine`/`AudioTracks` los redondean
   (±8,3 ms), sin huecos entre planos.
6. `render.mjs` y `verify.py` parametrizados para C04 (nombres `Andromeda-C04-…`, 2.050 / 5.125 / 12.300 f). `render.mjs` admite
   `--range a-b` para renderizar un tramo suelto a `study/` sin pisar los másteres. `verify.py` añade: contra el JSON
   y el CSV del máster, fotogramas de cada clip, narrador entero, ambientes en su posición y ganancia de mezcla.

7. **Subtítulos 07–15** (`src/captions/Scene07…Scene14.tsx`, `Tag.tsx`). Mismo lenguaje de C02/C03 (frase corta
   en una línea, SF Pro ~800, blanco con acento azul claro, subida con asentamiento, obturador), colocado en la
   zona libre de cada plano medida fotograma a fotograma:
   - **07 y 08** tienen acercamientos y alejamientos a la pantalla: la línea viaja con el canto superior de la
     pantalla (`yKeys`), entre barbillas y pantalla en abierto y sobre los torsos en el acercamiento. En los
     cortes internos (primeros planos del azul y del prota) la línea cambia de zona en el fotograma del corte.
   - **Voz de la máquina** (08, «Hey, … ¿quieres que te empiece a generar más versiones?»): toda en azul claro,
     sin bocadillo ni recuadro. «Sí» grande en el plano abierto (la /s/ empieza en 49,86 s; la alineación lo daba
     3 f tarde y el brief lo situaba en 50,48, que es el arranque de «y escalarás»); «escalarás» crece mientras se dice.
   - **09**: la línea vive en el cesto; «mierda» cae dentro con gravedad, como los papeles, y en «el doble de mierda»
     sale duplicada (eco). Sin golpe sonoro.
   - **10**: tinta marino y acento azul BRAUD sobre la camiseta y la camisa claras. Handles en pastilla pequeña,
     distinta del subtítulo: `@notelliotkay` junto a Elliot en su primer plano, `@notkurtgodel` sobre kiwi en el
     suyo y ambos sobre sus cabezas en el plano de los dos (entrada de 5 f, más de 1 s en pantalla, nunca sobre la cara).
   - **11 · criterio**: frases detrás de las cabezas con contorno fino delante (lenguaje del hook A; segunda y última
     vez). Matte de Vision más clave de color de la piel azul (Vision no recorta la cabeza del azul en este plano):
     `public/assets/mattes/criterio-holdout/`. Nada baja a las manos ni a los papeles.
   - **12**: pared alta, sobre las proyecciones; en «creativos» la pared se llena de copias de la palabra.
   - **13**: sobre la sudadera mientras mira a cámara; al girarse, sube a la franja libre sobre la pantalla. Nada
     encima de la maquinita.
   - **14**: en la capucha, entre la barbilla y el estampado; «pincha abajo» baja desde arriba como el gesto. Desde
     «Veremos» (encaje), tramo sobrio sin acentos. **15**: tinta marino sobre el mostrador, delante de la máquina.
   Cobertura: las 274 palabras salvo el gag en blanco y negro (comprobado en `verify.py`).
8. **Música** (`build-music.py` → `public/assets/audio/stems/musica.wav`, pista `musica`). Banda sonora de
   `../music/final_soundtrack_85_4s.wav` (85,400 s, máster sin tocar) con ducking bajo el narrador original: −12 dB
   con voz, hasta −6 dB en huecos de 150 ms o más, −3 dB extra en el hook para el susurro; ataque de 80 ms con
   60 ms de anticipación y recuperación de 300 ms (`study/music-duck.json`). La música sigue la spec funk de 122 BPM
   que entregó Ale; el brief del director describe otra pieza (118 BPM, pizzicato/fagot/piano).

## Sin cambios

Hook (variante A), cartel de la persiana, «OTRA PUTA VEZ», gag de la sudadera en blanco y negro, rótulos 00–05,
pista de SFX de rótulos (0–38,3 s) y ganancias de 00–05.

## Pendiente (no se ha hecho a propósito)

- **Escucha**: nada de esto está escuchado (ni la música ni la mezcla). Las ganancias de 06–15 son un punto de partida medido; revisar a oído 08 (pico de
  −1,8 dBFS en 46,35 s), 14 (−1,2 dBFS en 78,31 s) y 09 (−1,8 dBFS en 52,86 s) bajo la locución.
- Observaciones del director que siguen abiertas (no son de montaje): UI con fila 5 duplicada y textos ilegibles en 06 y 08;
  título y botón imperfectos en 07 y salto de postura 07→08; en 09 la caída de los papeles (1,125–1,625 s de fuente) llega antes
  de «el doble» (~54,79–55,07 s); en 12 la dirección óptica de las lentes no es coherente. Lipsync final no certificado.

## Discrepancias y avisos

- **Brief frente a JSON**: ninguna en fotogramas, archivos, IN/OUT ni estados (se siguió el JSON). Solo cambian los ids de 01 (`01_ventanilla_espera`),
  02 (`02_ticket_angulo`) y 03 (`03_ads_apagados`) frente a C03, que se conservan (`masterId` guarda el del máster).
- **Hook**: el brief dice susurro original del azul en 1,970 s y NO duplicar la voz generada del clip; C03/C04 mantienen el audio
  nativo del hook (con su voz generada) por instrucción explícita de Ale. Si Ale cambia de idea, basta colocar `AZUL_SUSURRO_ORIGINAL.mp3`
  en 1,970 s y limpiar la voz del clip 00.
- El clip 12 trae menos audio que vídeo (arriba). Los clips de vídeo son HEVC 10 bits a 24 fps; el audio nativo, AAC a 32 kHz.

## Verificación

**C04 con subtítulos y música** — `verify.py` → `QA.json`: TOTAL OK sobre `Andromeda-C04-00-85s-24fps-1080.mp4`
(2.050 f, 1080×1920, H.264 CRF 16 + AAC 48 kHz; 485 s con concurrencia 2 y caché de 768 MB):

- Cobertura de las 274 palabras de la locución salvo el gag en B/N (f691–739); las tres correcciones de tiempo
  («Sí» −3 f, «y escalarás» −2 f, «Así» desde el corte) siguen ligadas a su palabra.
- Música: banda sonora de 85,400 s (4.099.200 muestras) en la pista `musica`, stem con ducking de 2.050 f.
- Audio del máster frente a la mezcla de stems (incluida la música): desfase 0 muestras en 16 ventanas, ganancia 0,97–1,00.
- Sonoridad del máster: −17,6 LUFS integrados, LRA 3,6 LU, pico real −1,5 dBTP (por debajo de −1 dBTP del brief).
- Fotogramas de revisión en el render real: `study/revision-24fps-ajustes.jpg` y hojas por escena en `stills/`.
- Incidencias de render: con el swap del Mac casi lleno (13,3 de 14,3 GB) y el disco al 97 %, macOS mató el
  compositor (SIGKILL) con caché de 3 GB; además, dos procesos de Remotion sobre el mismo `build/` rompieron la
  carga de fuentes. Se resolvió con renders de uno en uno, `--concurrency 2–3` y `--cache-mb 768–1024`.

**Base de montaje (render de las 10:24, sin rótulos de 07–15 ni música)** — comparación con el ensamble del director:

**Alcance.** Las cifras de abajo describen la base de esta versión —montaje de las 17 unidades, 06 v5, audio nativo y
narrador— sobre el preview de 24 fps sin música ni rótulos de 07–15 (`Andromeda-C04-00-85s-24fps-PREVIEW-sin-musica.mp4`,
render de las 10:24 del 15/10, sha256 `0e0970c7…6ee5`). Los rótulos 07–15 y la música (puntos 7 y 8) se añadieron
después: no están cubiertos por estas cifras. `verify.py` y `compare-ensamble.py` sirven para repetirlas sobre el siguiente render.

`verify.py` → `QA.json` (todo OK en ese render) y `compare-ensamble.py` → `study/comparacion-ensamble.json`, contra
`ENSAMBLE_COMPLETO_85s_PREVIEW_CON_OBSERVACIONES.mp4` del director:

- Render 24 fps: 1080×1920, 2.050 f, H.264 (CRF 16) + AAC 48 kHz estéreo, 97,6 MB; 130 s con concurrencia 6.
- Imagen: en los 17 inicios de unidad y en el fotograma anterior, el mejor desfase frente al ensamble del director es 0 (MAD 0,8 sobre 255 en gris
  270×480, PSNR 45–47 dB en el primer fotograma de cada unidad; el cruce S contra S−1 da MAD 33–79). Fotograma a fotograma: desfase óptimo 0 en
  2.041 de 2.050; los 9 restantes (f1, 17, 240, 586, 706, 1509, 1511, 1598, 1682) son planos casi estáticos o duplicados al inicio de un plano
  (diferencia entre candidatos ≤ 0,1 de MAD, es decir, ruido de compresión). En aquel render había rótulos hasta el f919 y el ensamble no los lleva.
  `study/qa-cortes-S-render-vs-director.jpg`: fila superior, nuestro f(S); fila inferior, el del director.
- Audio: desfase 0 muestras (±0,05 fraccionario) frente al audio del ensamble del director en 14 ventanas de 2 s entre 1 y 80 s, y 0 frente a los stems de
  C04 en 16 ventanas (`verify.py`); ganancia de la mezcla 0,97–1,00. Los 16 stems nativos de 01 a 15 coinciden con el `STEM_AMBIENTE_COMPLETO` del
  director (correlación 1,0000, desfase 0, ganancia 0,6500).
- 60 y 144 fps (no se renderizaron enteros): `AndromedaC04-60` (5.125 f) y `AndromedaC04-144` (12.300 f) se comprobaron con fotogramas y un tramo de cada una.
  A 60 fps, f3092/f3093, f3962/f3963 y f4977/f4978 son el último de la unidad anterior y el primero de la siguiente (cortes 09, 12 y 15, en fotograma
  impar, redondeados al fotograma de 60 fps siguiente); a 144 fps, f7421/f7422. Un tramo de 1 s a 60 fps (3070–3130) y otro de 0,7 s a 144 fps (7400–7500) con
  audio en lag 0 frente al máster de 24 fps (`study/tramo-*.mp4`). A 60 fps, tras un corte en fotograma impar, la cadencia 3:2 va ≤ 1 fotograma de 60 fps
  por detrás del reloj ideal (8 de 61 fotogramas del tramo).
- c03 sin cambios: tamaño, mtime, inodo y nº de enlaces idénticos en sus 1.466 archivos (y en `build/`, `build60/`), y sha256 idéntico en los 1.466 antes y después.

# Método de estudio y continuación

## Índices y tiempos

Fotogramas desde cero; rangos de notas con ambos extremos incluidos. Para Remotion,
convertirlos a `[startFrame, endFrameExclusive)` usando `endFrameExclusive = f1 + 1`.
Duración = `(f1-f0+1) * fps_den/fps_num`. Mantener 30000/1001 como racional, no
29,97 redondeado. Un desfase de voz calculado desde Whisper no certifica sincronía
subfotograma: la estimación de voz heredada tiene incertidumbre aproximada de 50 ms.

La extracción nativa usa `select=eq(n,N)` o `select=between(n,A,B)` sobre el índice
decodificado. `sheet.py` fue corregido el 10/10/2026: el seek temporal anterior podía
introducir diferencias de índice. Las medidas nativas antiguas necesitan volver a
comprobarse antes de tratarlas como fronteras exactas.

## Cobertura sin muestreo de segundos

Cada referencia tiene metadatos y series automáticas de todos sus fotogramas.
Eso no equivale a revisión visual. Abrir cada hoja de `analysis/dense/<slug>/` en
orden y registrar los nombres exactos en `sheets_viewed` del JSON de cobertura.

El detector heredado de repetidos compara bloques de JPG reducido con umbral 3/255.
Por tanto, las hojas densas omiten imágenes **similares**, no solo idénticas. El
texto «+k» informa omisiones del detector; no prueba ausencia de animación.

`audit_frames.py` compara el hash del fotograma decodificado a resolución nativa con
el anterior. Registra `datos/<slug>/native-framemd5.txt` y `exact-frames.json`. Genera
hojas en `analysis/supplemental/<slug>/` para todos los fotogramas omitidos que no
resultan idénticos. Abrirlas también y registrar `supplemental_sheets_viewed`. Su
orden de celdas puede ser discontinuo: los índices están escritos en cada celda y
en `index.json`. Solo el hash idéntico autoriza no volver a mirar una repetición.

Un hash distinto no implica un efecto: puede ser ruido del códec. Las miniaturas
reducidas detectan estructura; texto fino, desenfoque, opacidad, máscaras y colores
requieren secuencias nativas. No certificar esos detalles solo con miniaturas.

## Revisión de un tramo

1. Leer el mapa fusionado con `digest.py <slug> <f0> <f1>` y conservarlo en tmp del tramo.
2. Abrir densas y suplementarias. Comprobar las etiquetas de la celda concreta: un
   detalle de la celda siguiente puede parecer del fotograma anterior.
3. Guardar notas cada 3–4 hojas; listar lo visto, lo medido y la interpretación por separado.
4. Extraer a resolución nativa las entradas/salidas, cortes dudosos, insertos de 1 f,
   cambios de escala, máscaras, B/N y gráficos. Incluir fotogramas antes/después.
5. Medir con `inkbox.py`, `px.py`, OCR por fotograma y ajustes tipográficos. Guardar
   tablas/curvas completas, método, ROI y sus límites. «Fuerza» de tinta es contraste,
   no alpha de la capa: no convertirlo en opacidad exacta sin modelo de fondo.
6. Abrir espectrogramas. Anotar onsets como picos del **mix**; sin escucha/separación
   no atribuir un pico a un whoosh, a música o a voz con certeza. Una rejilla de tempo
   estimada no demuestra que los cortes se diseñaran sobre el beat.
7. Confirmar o descartar candidatos de corte, añadir los omitidos. Distinguir corte
   de material, salto de escala, flash, cambio de iluminación y cambio tipográfico.
8. Añadir sucesos normalizados en el bloque JSON final de la nota. Cada afirmación
   importante cita original, rango y lámina/medida cuando exista.

## Registro de confianza

- `automatic_candidate`: OCR/detector; puede fallar o fusionar rótulos.
- `dense_observation`: revisado en secuencia de miniaturas, precisión limitada en detalle fino.
- `native_observation`: visto en secuencia nativa con índices corregidos.
- `measured_native`: valor numérico con ROI/método preservados.
- `design_proposal`: regla operativa propuesta; no se atribuye al editor como intención demostrada.

Los campos `native_ranges` y `spectrograms_viewed` declaran controles hechos, no
certifican automáticamente que todos los eventos del tramo estén resueltos.
`forensic_complete` se reserva al cierre de la revisión de todos los eventos.
La incertidumbre sobre una herramienta o curva original no puede eliminarse mirando
más píxeles: conservar medición aproximada en vez de inventar el proyecto fuente.

## Persistencia

`CURRENT-STUDY.json` + `ESTADO.md` son el punto de entrada actualizado. Las notas
canónicas van en `notas/`; los revisores escriben primero en `analysis/notas/` y
`estado.py` las copia. `consolidate.py` produce fichas y sucesos; no convierte una
nota parcial en ficha validada. `stats.py` produce tablas automáticas: revisar
denominadores, exclusiones y origen de los candidatos antes de derivar reglas.

Las revisiones V6 original, V6 revisión y V7 comparten montaje. Se conservan como
variantes relacionadas, no como tres ejemplos independientes de una regla. La
comparación por similitud no permite suponer que todo el resto de V7 sea idéntico.

El CLI `dapi` está instalado, pero Diffusion Studio no estaba arrancado durante
esta revisión. Se usan ffprobe/ffmpeg y datos locales para la inspección; no se
afirma haber realizado escucha perceptual con dapi ni se consumen créditos.

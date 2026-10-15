# Birdieballs · iteraciones cortas

Ver `CURRENT-VERSION.json` antes de continuar. El encargo actual son los primeros 20 segundos de edición final integrada (V04, 19,603 s hasta «Justo ahí»). El resto del anuncio espera feedback.

- `BRIEF.md`: criterio visual y protocolo de iteración.
- `GUION-RAW.md`: guion original del usuario.
- `analysis/edl.json`: EDL histórico de versiones anteriores; no usar para V04, que conserva la fuente continua desde 0.
- `analysis/intro-sheet.jpg`: contacto visual de los primeros doce segundos.
- `analysis/turbo/intro.json`: transcripción local por palabra. Los tiempos ASR son estimaciones, no alineación fonética certificada.
- `build-plan.mjs`: compila mediante `motor-editor` y aplica overrides editoriales documentados de posición, tamaño y animación por palabra.
- `v01/plan.json`: fuente de verdad que consume la composición Remotion; no hay parámetros ocultos en otro proyecto.
- `render.mjs`: usa el bundle compartido y abre un navegador para fotogramas o vídeo, con cuatro workers.
- `v01/Birdieballs-B01-V01.mp4`: resultado del primer bloque.

## Iteración

1. Leer las notas de la versión correcta en `../motor-editor/review/data/project.json`.
2. Corregir solo el bloque y conservar la versión anterior. Guardar los nuevos planes/renders en una carpeta nueva.
3. Renderizar solo lo afectado. No extender una aprobación parcial al resto del vídeo.
4. Importar el resultado con `node motor-editor/review/import.mjs /ruta/render.mp4 "Birdieballs · B01 · V02"` desde la raíz.
5. Esperar feedback sobre el bloque antes de editar el siguiente.

## Render V04

`node birdieballs/v04/render.mjs --bundle` desde la raíz. Implementación específica en `v04/Film.tsx`, medios congelados y procedencia en `v04/assets/`, controles en `v04/QA.json`. No equivale a haber migrado el planificador legacy a todas las reglas V2. Prueba de reconstrucción contra V8 en `v04/reference-test/`; comparación de brutos en `http://127.0.0.1:4317/raw-study`.

## Render V03

`node birdieballs/v03/build.mjs` y `node birdieballs/v03/render.mjs`. Requiere el bundle actualizado `motor-editor/build-v03`; los originales usan el bundle anterior. Feedback persistido en `estilo-editor/FEEDBACK-ALE.md`; cambios de esta versión en `v03/CAMBIOS.md`.

## Render V02

Desde la raíz: `node birdieballs/v02/build.mjs`, después `node birdieballs/v02/render.mjs --stills` o `node birdieballs/v02/render.mjs`. Diseño, alternativas y revisión en `v02/DIRECCION-Y-QA.md`; validación en `v02/QA.json`. La V02 conserva el montaje, las curvas, los medios y el sonido en un único `v02/plan.json`.

## Render histórico V01

Desde la raíz: `node birdieballs/build-plan.mjs`, después `node birdieballs/render.mjs --stills` o `node birdieballs/render.mjs`.
El empaquetado Remotion 4.0.534 se completó usando Rspack y ejecución local con permiso de procesos. El build se reutiliza para no reconstruirlo en cada iteración. Si cambia el código del adaptador, regenerarlo antes de renderizar; cambios en `plan.json` no requieren empaquetar.

La V01 conserva el audio original y prueba ritmo/rótulos sobre un gag ya filmado. No es una demostración de todas las recetas de motion ni un estilo aprobado. Diffusion Studio no estaba abierto; el análisis usó ffprobe, ffmpeg y Whisper local. No se atribuyen efectos sonoros que no hayan sido identificados.

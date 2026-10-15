# Cuestionario de dirección · Birdieballs

Entrada: http://127.0.0.1:4317/quiz, enlazada desde la cabecera de Cutroom. 69 preguntas, 10 secciones y acceso a las once referencias. El catálogo incluye 84 fragmentos documentados; cada pregunta muestra los pertinentes, y el reproductor permite abrir el vídeo completo. Q01 (conservar montaje) es una restricción ya expresada, no se vuelve a solicitar autorización.

## Fuente de verdad

- `catalog.json`: preguntas, opciones, constraints, referencias por SHA256, índices nativos, reglas y límites de interpretación.
- `build-catalog.py`: autoría reproducible desde corpus y reglas V2. No ejecutarlo sobre un cuestionario en uso sin planificar migración de respuestas; cambiar el catálogo cambia su digest.
- `../data/quiz-answers.json`: respuestas canónicas, revisión y estado `draft`/`ready`. Se crea cuando el usuario responde; no hay opciones preseleccionadas.
- `../data/quiz-history/`: todas las revisiones aceptadas.
- `../data/quiz-decisions.json`: opciones legibles, matices, tramos y evidencia. No es un plan de render.
- `../data/quiz-brief.md`: resumen legible para la siguiente propuesta.

Leer el estado vigente y los comentarios antes de la próxima propuesta; respetar los pendientes. `ready` significa que Ale dejó las respuestas listas para revisar, no que aprueba el siguiente vídeo. Elegir una referencia no aprueba todos sus recursos. Una preferencia no demuestra una intención del editor original ni equivale a un parámetro medido.

## Comportamiento

Guardado con debounce, copia local mientras está pendiente, revisiones optimistas para evitar sobrescrituras entre pestañas y escritura atómica de respuestas. En conflicto se conserva el borrador y se permite descargarlo; no se sobrescribe silenciosamente una revisión ajena. Los exports se reconstruyen a partir de las respuestas. Las notas y los vídeos de Cutroom no se modifican.

Reproductor con tramo limitado, vídeo completo, velocidades 1×/0,5×/0,25×, consulta de fotograma nativo y anotación de momento en el comentario de la pregunta activa. El timecode durante reproducción es aproximado al fotograma; «Ver exacto» extrae el índice nativo por ffmpeg. Todos los medios proceden de rutas permitidas del corpus y la fuente Birdieballs, sin aceptar rutas de archivo arbitrarias.

El audio de referencia se reproduce para que Ale valore el ejemplo. No se identifican samples automáticamente. No hay generación o render al pulsar «Dejar respuestas listas para revisar».

## Comprobación realizada

`node --test motor-editor/review/quiz.test.mjs`: 4 pruebas; catálogo, validación, procedencia, persistencia, recuperación, export y conflicto simultáneo. Pruebas de navegador sobre una instancia aislada: selección, comentario literal escapado, recarga, exclusión de opciones incompatibles, consulta nativa de Birdieballs, captura de tiempo y entrega como `ready`. Revisado visualmente a 1440×1000 y 390×844; corregido desbordamiento móvil. La instancia real queda sin respuestas de prueba.

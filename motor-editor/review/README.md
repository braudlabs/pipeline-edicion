# Cutroom · revisión local de versiones

Interfaz de revisión del motor de edición. Importa clips y renders, conserva versiones independientes y guarda indicaciones temporales y espaciales en el proyecto. No envía vídeos a servicios externos y no ejecuta cambios de edición por sí sola.

## Abrir

Desde la raíz del proyecto:

```sh
node motor-editor/review/server.mjs
```

Abrir `http://127.0.0.1:4317`. También: `npm run review` desde `motor-editor`.
Requiere Node y ffmpeg/ffprobe en PATH; no necesita instalar paquetes ni compilar frontend.
El servidor escucha solo en loopback. Debe seguir en ejecución mientras se usa la interfaz.

## Revisar un corte

1. **Añadir versión** importa un MP4, MOV, M4V o WebM, conserva el original y calcula sus tiempos y SHA256. Cada nuevo render se añade como otra versión.
2. Espacio reproduce/pausa; las flechas avanzan un frame y Mayús + flecha avanza diez. También se puede escribir el número de fotograma.
3. **Marcar inicio / fin** (I/O) o Mayús + arrastrar en la línea de tiempo selecciona un intervalo. **Solo este frame** vuelve a una indicación puntual. **Tramo** reproduce la selección.
4. **Punto**, **Zona** y **Flecha** dibujan sobre el fotograma pausado. Se pueden añadir marcas en distintos frames de la misma indicación. Los números relacionan el comentario con las zonas.
5. Escribir el cambio y guardar. Las notas conservan versión, intervalo, marcas, imágenes y estado pendiente/resuelto. Los borradores se conservan en ese navegador y versión.
6. **Copiar resumen para el chat** o **Exportar indicaciones** permite solicitar la siguiente edición. El agente también puede leer directamente los archivos guardados. Guardar una nota no inicia automáticamente un turno de IA.

El navegador debe poder reproducir el códec para escuchar/ver vídeo en movimiento. Se recomienda MP4 H.264/AAC para las versiones de revisión. ffmpeg extrae los fotogramas aunque el navegador no soporte el códec; se avisa si la reproducción falla.

## Contrato para quien edita

- Estado: `motor-editor/review/data/project.json`.
- Cada versión tiene ID, SHA256, dimensiones de presentación, cadencia y `frameTimes` reales. Los archivos originales se copian a `data/<versionId>/source.*`.
- Los frames empiezan en **0**. `startFrame` y `endFrame` son **inclusivos**. Para Remotion, convertir el extremo final a exclusivo una vez (`endFrame + 1`) si no cambia la cadencia; en otra cadencia, convertir mediante los tiempos fuente.
- `frameTimes` es el PTS de cada frame decodificado, normalizado al primer frame. Para fuentes VFR se consulta esta tabla; no se calcula el tiempo como `frame/fps`.
- `shapes` contiene tipo, frame y coordenadas normalizadas de 0 a 1 respecto a la imagen visible, sin las bandas del visor. La orientación y proporción de presentación se toman del fotograma decodificado por ffmpeg.
- Cada nota guarda PNGs exactos y SVGs autocontenidos con imagen y marcas. Los enlaces viven en `snapshots`; son relativos a `data/`. La imagen pausada se extrae con selección por índice de frame, independientemente del seek aproximado del reproductor.
- Una nota de V1 no se traslada automáticamente a V2: un corte puede alterar los tiempos. Revisar la versión/huella antes de editar.
- Guardar una nueva versión deja la anterior intacta. El servidor solo permite leer medios de versiones registradas, no rutas arbitrarias del ordenador.

Para incorporar un render desde el motor o desde el agente, con el servidor abierto:

```sh
node motor-editor/review/import.mjs /ruta/render.mp4 "V2 · ajuste de ritmo"
```

La interfaz detecta nuevas versiones sin recargar ni interrumpir la selección actual.

Datos y medios están ignorados por Git, pero persisten en disco. Para conservar o trasladar todo el proyecto, copiar la carpeta `data/`; el JSON exportado por sí solo no contiene los vídeos.

## Comprobaciones realizadas

- Seis pruebas de contratos: tiempos VFR, extremos inclusivos, rangos inválidos, marcas fuera de selección, geometría y exportación.
- Prueba real en navegador con vídeo sintético de 48 frames: importación, reproducción/pausa, avance exacto, intervalo F5–F20, zona en F5 y flecha en F20, guardado con imágenes, persistencia al recargar, resolución/reapertura y aislamiento entre dos versiones.
- Se verificaron también reproducción de selección, peticiones parciales de vídeo, rechazo de notas inválidas, atajos tras usar las herramientas, diseño móvil sin desbordamiento y vídeo con orientación de 90° (fuente 640×360, presentación 360×640).
- Los datos de prueba usan una carpeta temporal separada; no aparecen en el proyecto del usuario.

```sh
node --test motor-editor/review/tests/*.test.mjs
```

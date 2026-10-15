# Birdieballs · V07

Versión completa de 38,005 s, realizada en Remotion. Pendiente del veredicto de Ale.

- **Continuidad:** los subtítulos conservan su ancla durante la lectura y los cambios de plano. Eliminados los saltos de 200 px en «recuperamos» y «originales». Lagos/campos comparten posición y color. Todos los apoyos de la oferta permanecen arriba del 70 % original.
- **Jerarquía:** SF Pro, peso regular en protagonistas como «riñón», y combinaciones compactas. Las frases puente tienen menos movimiento. La variación procede del tamaño, el peso, la acumulación y el ritmo, no de recolocar cada frase.
- **Keyframes:** entradas y salidas separadas; reemplazos directos, entradas suaves, acumulaciones, revelado y énfasis con asentamiento. Las capas de un mismo grupo coordinan sus salidas. La máscara y el contorno de SOLUCIÓN comparten exactamente la misma trayectoria.
- **Referencia ejecutable:** el motor consume el ajuste medido de V8 en los énfasis seleccionados. Se distingue el intervalo observado de los enlaces de inicio/final diseñados. No se identifica ese ajuste con los keyframes originales del editor.
- **Continuidad del anuncio:** mismos 2278 fotogramas, fuente, montaje y mezcla que V06; sin nuevos cortes ni retiming. Renders anteriores conservados.

Motor reutilizable: `motor-editor/src/caption-keyframes/index.ts`. Decisiones de esta pieza: `cues.ts`. Pruebas: `motion-validation.json` y `QA.json`. Comparación visual: `stills/V07-vs-V8.jpg`. Contactos del MP4 final: `stills/final-*.jpg`.

## Revisión realizada

Inspección de 40 estados distribuidos por todo el anuncio y secuencias de entrada de riñón/SOLUCIÓN, más los cortes conflictivos del producto y paisajes. Comparación focal con V8 en continuidad y jerarquía. Decodificación completa sin errores; seis ventanas de audio con desfase medido de 0 ms. Esto no equivale a certificar fidelidad artística global ni a una escucha independiente.

El primer diseño de V07 se corrigió antes de entregar: producto bajado a una zona de más contraste, paisajes en una ancla que deja libre la cara cuando entra el actor, espacio entre «bolas» y «originales», y trazo ligeramente reforzado sobre la oferta.

## Qué falta para mejorar el algoritmo

No hace falta pedir más archivos para esta revisión. El trabajo pendiente del sistema es elegir los recursos según contexto, además de ejecutarlos bien: énfasis de la voz, continuidad de frase, rostro/manos/producto, espacio de lectura y función del plano. Esa selección sigue dirigida manualmente en `cues.ts`; V07 no demuestra un planificador autónomo universal.

Para cada nueva regla general se necesita evidencia comparable, casos donde aplica y contraejemplos; después, una prueba renderizada frente a la referencia y el feedback de Ale. Contar frames, efectos o promedios por sí solo no recupera el criterio del editor. Los proyectos editables, las fuentes y las pistas separadas permitirían conocer con más exactitud curvas, capas y SFX; son material útil opcional, no un bloqueo ni una garantía de réplica perfecta.

## Reproducibilidad

El runtime original tenía archivos locales ilegibles/intermitentes. Se instaló desde la caché, sin red, una copia temporal de las mismas dependencias fijadas por el lockfile, en `/private/tmp/birdie-v07-runtime`. Se usó Chromium ya instalado en la caché de Playwright. `render.mjs` permite indicar ambos mediante `BIRDIE_REMOTION_RUNTIME` y `BIRDIE_BROWSER`. Render completo: 53,103 s. Sin cambio de versiones de dependencias ni instalación global.

# V04 · entrega para veredicto

19,603 s, 1175 fotogramas, 1080×1920 a 60000/1001. El tramo conserva el montaje y el tiempo del original desde cero hasta «Justo ahí». La siguiente frase empieza a 19,62 s y queda fuera. V03 y su historial se conservan.

## Cambios visibles

- Baseline compartida entre «¿Cansado» y «de dejarte un»; segunda línea compacta con contraste serif/lima en los énfasis.
- Gags colocados según el plano, con contraste oscuro sobre agua, arena y cielo. «Me cago en…» queda fuera de la cara.
- Gráfico 12,30–14,92 s: entrada de una esfera fotográfica, apertura a tres, cambio de agrupación y salida. Fondo iluminado con textura, profundidad simulada, sombras y cinco muestras temporales de los objetos para desenfoque de movimiento.
- Flecha dibujada hacia el personaje real en «Justo ahí».
- Audio original continuo con efectos suaves añadidos. No se ha identificado ni copiado un sample exacto de las referencias.

## Auto-pruebas y correcciones

Se renderizaron tres alternativas de gráfico y se eligió C. Se revisaron fotogramas de diseño y hojas de secuencia; se corrigieron separación de líneas, destino de flecha, contraste, texto sobre la cara y dos colisiones entre grupos sucesivos. Las hojas generales preceden a esta última corrección; `stills/qa-final-handoffs.jpg` documenta los ocho fotogramas finales de los dos cambios corregidos.

La reconstrucción de «pagar» de V8 se comparó con seis frames nativos: error máximo de posición 1 px, IoU medio de tinta 0,931. Es una calibración local de una palabra, no validación de todos los subtítulos ni del nuevo gráfico. Comparación en `reference-test/comparison.jpg` y mediciones en `reference-test/comparison.json`. En una muestra el apoyo superpuesto reduce la coincidencia.

Decodificación completa sin errores; correlación del audio original frente a la entrega superior a 0,9997 y desfase detectado 0 ms en tres ventanas. Sonoridad −14,0 LUFS, pico verdadero −0,8 dBFS. Reproducción funcional a 1× comprobada en el navegador hasta el último frame mostrado, sin error de medio. Esa comprobación no constituye escucha independiente ni observación visual continua por el modelo. QA detallada en `QA.json`.

## Alcance pendiente

V04 queda pendiente de Ale. Es una composición específica en Remotion; no acredita la migración completa del planificador V2 ni la reproducción exhaustiva del estilo de las once referencias. El motion de esta prueba está en `Film.tsx`; no hay un proyecto After Effects equivalente entregado.

Los brutos aportados suman 68 vídeos y 10 audios; hay diez pares revisados cualitativamente. Falta alinear exhaustivamente los intervalos y completar las mediciones de todos los eventos, oclusiones y audio. La interfaz `/raw-study` distingue la correspondencia de escena de la alineación exacta.

Activo de bola generado con imagegen, congelado en `assets/golf-ball-photo.png`; prompt y procedencia en `assets/provenance.json`. Es un recorte 2D con profundidad simulada y no una fotografía del inventario comercial.

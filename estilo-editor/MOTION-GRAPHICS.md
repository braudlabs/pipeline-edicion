# Motion graphics: estudio, implementación y límites

Actualizado el 10/10/2026. Sí se han estudiado los motion graphics de las diez referencias, además del montaje y los subtítulos. La cobertura secuencial está completa; la medición nativa es selectiva. No equivale a haber reconstruido todas las escenas ni a conocer el proyecto o herramienta original.

El código está en [motor-editor](../motor-editor/README.md). La primera implementación ofrece doce modos editoriales, diez de ellos con gráficos. El selector usa reglas explícitas; no es un modelo entrenado. Ninguna receta se considera visualmente validada todavía.

## Qué sabemos y qué ejecuta el motor

| Familia | Evidencia conservada | Implementación actual | Qué falta para igualar la referencia |
|---|---|---|---|
| Tipografía por palabra y acumulación | [V1](notas/v1-pagado-A.md), [landing](notas/landing-A.md): modos, permanencias, jerarquía y entradas distintas | `rail`, `accumulate`, tiempos de cada palabra y ajuste con métricas SF Pro | Variantes de composición y acumulación en varias líneas; comprobar tipografía sobre imágenes reales |
| Ascenso con desaceleración | [Gracias, 47 muestras](medidas/landing-A/gracias-position-fit.json); [hooks, trayectoria nativa](medidas/landing-F/ink-hooks-full.tsv) | Curva normalizada de Gracias en `motion.ts` | La duración, distancia y fundido usados por las recetas son adaptaciones. Contraste de la imagen no demuestra alpha. No generalizar esta curva a todo el vídeo |
| Palabra protagonista y oclusión | [Landing](notas/landing-B.md): funcionan detrás de CRT/cabeza; Paid con relleno detrás de cámara/persona y contorno delante | `hero`, `masked-hero`: capas separadas, mismo recorte y trim que el metraje | Extraer y verificar recortes alpha de personas y objetos; resolver encuadres por escena |
| Parpadeo | [BLACK](notas/v6-ads90-rev-A.md), f268–276 a 60 fps: opaco/parcial/ausente/parcial, repetido | `pulse`: reproduce los estados temporales; el estado parcial usa 0,5 como aproximación | El estado parcial fue observado, no medido como alpha exacto; revisar FRIDAY y otras variantes por separado |
| Precio y unidad | [V1](notas/v1-pagado-A.md), f176–225: componentes con beats distintos | `price`: prefijo, importe, unidad, entrada escalonada | Ajustar geometría, color, textura, transformaciones y tiempos a la variante concreta |
| Contador radial | [V1](notas/v1-pagado-A.md), f389–398: 1, 6, 15, 21, 24, 26, 28, 29, 29, 30 | `count`: secuencia discreta y líneas radiales | Textura, puntos exteriores, crecimiento radial y continuidad de cámara hacia «costo mínimo» no están reconstruidos |
| Comparación espacial | [V2](notas/v2-churros-A.md): Tiempo → Dinero | `comparison`: dos conceptos y traslado del conjunto | Coreografía completa, perspectiva, continuidad de objetos y blur medidos |
| Pruebas y capturas | [Landing](notas/landing-A.md): revelados por componentes | `proof`: imagen real con regiones y tiempos declarados | Anotar regiones por recurso; igualar diseño y transiciones concretas |
| Proceso, carrusel y foco | [LaFabrica](notas/lafabrica-v2p1-B.md), [V6](notas/v6-ads90-B.md) | `steps` y `carousel`: adaptaciones con etapas, imágenes y cámara | No son réplicas del sistema de actores, cinta o máquina. Faltan recursos, trayectorias y composición específica |
| Metáforas, engranajes y escenas 3D | [V3](notas/v3-ia-cara-B.md), [V6](notas/v6-ads90-rev-A.md): acciones, orden visual y relación con el discurso | El montaje puede incorporar metraje preparado | No hay generador de modelos, animación de personajes, cámara 3D general ni reconstrucción de esas escenas |
| Destellos y uniones complejas | [V3](notas/v3-ia-cara-B.md): flash del sujeto y corte oculto; otras uniones en notas | Cortes de plano y movimientos internos básicos | Recetas específicas de uniones, flashes por máscara, desenfoque de obturador y su verificación |
| Audio asociado a acciones | Espectrogramas y marcas en las notas; identidades sonoras sin verificar auditivamente | Cues explícitos, ganancias, fades y ducking | Escucha e identificación de sonidos; biblioteca y sincronía de estilo verificada |

## Qué significa «aplicar el mismo estilo»

El motor debe elegir una representación por lo que comunica la frase, darle una composición adecuada, coreografiar sus elementos y unirla al montaje con continuidad. Tener transiciones o letras grandes no basta. La implementación ya separa selección editorial, recursos, plan por fotograma y composición Remotion, con una única fuente de verdad.

Hoy necesita palabras temporizadas, material etiquetado y datos verificables para las escenas. Puede inferir cláusulas e intención con reglas léxicas sencillas, pero no comprende por sí solo todo el metraje ni decide metáforas originales con el criterio del editor de las referencias. Las máscaras, pruebas y escenas 3D deben aportarse.

Para certificar el objetivo faltan comparaciones visuales sobre fragmentos representativos: rail, máscara sobre persona/objeto, contador y salida, prueba, comparación y escena compleja. Deben comprobarse legibilidad, sincronía verbal, geometría, continuidad, aceleración, blur y audio. Esas comparaciones siguen pendientes porque Ale pidió posponer los renders. Pasar pruebas de código no demuestra fidelidad estética.

## Próximo desarrollo concreto

1. Completar las curvas nativas de los eventos prioritarios y asociar parámetros de receta a medidas, conservando incertidumbre.
2. Incorporar transiciones compartidas entre escenas y recursos específicos; mantener una receta aproximada identificada como tal.
3. Añadir ingestión de transcripción y anotación visual, extracción de máscaras y selección de recursos con revisión de confianza.
4. Cuando se retomen los renders, comparar fragmentos con la misma duración y formato, corregir y registrar cuáles pasan. No extender una aprobación local a todas las recetas.

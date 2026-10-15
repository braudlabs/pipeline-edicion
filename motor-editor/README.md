# Estado del motor tras el rechazo de V03

**Avance ejecutable del 14/10/2026:** [selector editorial V2](src/editorial-v2/README.md)
conectado a Remotion, con decisiones por contexto, continuidad de bloques, alternativas
de composición y control de tinta animada. CLI `compile-editorial`; `compile` lo usa
también cuando el Job contiene `editorial`. Pilotos aislados, 64 pruebas técnicas y límites
documentados. El compilador 0.1 sigue disponible para reproducibilidad; no se promueve
su política de números→contadores a la V2.

Nueva relación explícita V2: ventana que cierra y reabre sin aplastar letras, basada en
medidas V8. Incluye filtros de lectura/sincronía y evita mezclar strings por el obturador.
[Prueba y límites](../estilo-editor/notas/relacion-v2-2026-10-14.md).

**Dirección vigente, 14/10/2026:** Remotion es la base de ejecución autónoma del producto;
After Effects se mantiene para producción interna. La comparación previa está en
[MOTION-GRAPHICS-AE-REMOTION](../MOTION-GRAPHICS-AE-REMOTION.md).

Nueva primitiva `src/caption-keyframes/reference-v2.ts`: trayectoria continua en segundos,
escalado por altura, muestreo a fps arbitrarios y separación explícita entre curva ajustada
y enlaces/salida diseñados. `atFrame(frame, fpsRacional, height)` es consumible desde
Remotion, incluidos subframes de obturador. No depende de AE, React ni una interfaz.
La consume ahora el selector editorial V2 cuando el contexto y la geometría lo permiten; el helper histórico se conserva.
Pruebas: `node --test tests/reference-v2.test.ts` desde esta carpeta. Se ha renderizado un piloto de laboratorio con selección y descarte contextual de la primitiva; su fidelidad editorial sigue pendiente.

El planificador actual0.1 es una implementación preliminar, no una réplica validada del editor. La política nueva está en [ALGORITMO-V2](../estilo-editor/ALGORITMO-V2.md); reglas/datos en `../estilo-editor/datos/revision-v2`. Los módulos `forensics/contract.mjs` y `forensics/reference-motion.mjs` validan procedencia/preservación temporal y evalúan curvas medidas; todavía no reemplazan automáticamente las recetas existentes. No presentar un plan antiguo como resultado V2.

# Motor de edición por referencias

Implementación inicial ejecutable en TypeScript y Remotion, separada de los anuncios existentes. Convierte palabras temporizadas, intención editorial y medios en una línea de tiempo con planos, subtítulos, motion graphics, máscaras y audio. Produce un plan JSON único, la composición consume ese mismo plan y cada decisión conserva su evidencia.

La selección automática es un sistema de reglas y puntuaciones. No se ha entrenado un modelo con los vídeos. Las etiquetas y datos de una escena pueden venir de un agente/editor; si solo se entregan palabras, el motor propone cláusulas e intención mediante reglas léxicas y lo marca para revisión. No deduce pruebas, cifras ni modelos 3D ausentes.

## Uso

Desde la raíz del proyecto:

```sh
node motor-editor/cli.ts compile motor-editor/examples/job.json --out motor-editor/examples/plan.json
node motor-editor/cli.ts inspect motor-editor/examples/plan.json
node --test motor-editor/tests/*.test.ts
./node_modules/.bin/tsc --project motor-editor/tsconfig.json
```

`examples/job.json` fuerza recetas para mostrar el contrato. `examples/automatic.json` conserva intención y datos, y deja que el motor elija. Ambos son casos técnicos sin voz/metraje; sus avisos de medios ausentes son esperados. No son anuncios aprobados ni resultados visuales de referencia.

Para un trabajo real, las rutas de medios son relativas al JSON de entrada. `--stage-media` verifica archivos con ffprobe, obtiene dimensiones/duración, guarda SHA256 y copia los medios al public aislado del motor:

```sh
node motor-editor/cli.ts compile /ruta/trabajo.json --stage-media --out /ruta/edicion.json
```

Sin `--stage-media`, los `src` deben ser rutas ya servidas desde `motor-editor/public/`. La salida incluye `edicion.json`, `edicion.props.json` y `edicion.report.json`. El último explica elecciones, candidatos rechazados y problemas de recursos.

La entrada Remotion es `motor-editor/src/index.tsx`, composición `ReferenceEdit`. Al retomar las pruebas visuales, cargar `edicion.props.json` como props. Los comandos de Studio/bundle se ejecutan desde `motor-editor`; los assets se sirven desde su propio public. Por ejemplo, `npm run studio -- --props=examples/plan.props.json` abre el caso técnico; no se ha ejecutado Studio ni un render durante esta implementación. Se usan las dependencias ya instaladas del proyecto padre, sin cambiarlas. El motor requiere Node con soporte de TypeScript sin compilación (22.18+); el adaptador TSX lo compila Remotion.

## Qué hace cada parte

| Archivo | Responsabilidad |
|---|---|
| `src/types.ts` | Contrato de entrada, plan y nodos animados |
| `src/planner.ts` | Segmentación, selección de plano/receta, asignación de palabras, posiciones, huecos y audio |
| `src/recipes.ts` | Doce modos ejecutables con referencias, requisitos y duraciones mínimas |
| `src/motion.ts` | Evaluación determinista, curvas y estados medidos |
| `src/text.ts` + `data/font-metrics.json` | Medición tipográfica SF Pro, kerning y ajuste de ancho |
| `src/Composition.tsx` | Metraje, SVG, perspectiva de recursos, oclusores y mezcla Remotion |
| `src/validate.ts` | Requisitos de medios, intervalos, colisiones y cobertura verbal |
| `cli.ts` | Compilación, fijación de medios e informes |

## Entrada editorial

`words` contiene `id`, `text`, `start`, `end` en segundos y `speaker` opcional. Debe estar ordenado. Dos hablantes pueden solaparse; dos palabras del mismo hablante no. `format.fps` es racional, por ejemplo `{ "num": 30000, "den": 1001 }`.

`clauses` asigna cada palabra una vez y permite `intent`, `focusWordIds`, `recipe`, `data`, `shotId` y `tags`. Las intenciones disponibles son hook, problem, demonstration, result, mechanism, offer, reaction y cta. Omitir `recipe` activa la selección; especificarla la convierte en decisión editorial y sus requisitos se comprueban estrictamente. Una receta explícita imposible da error, no se sustituye silenciosamente.

`shots` referencia un asset de imagen/vídeo, rango utilizable en segundos, etiquetas y hablante opcional. `anchor` es una posición normalizada. `avoid` son cajas normalizadas de rostro/objeto detectadas o corregidas por el editor. El motor mantiene el ancla dentro de la cláusula. `crop` tiene scale y desplazamientos x/y normalizados.

`cutoutAssetId` debe ser el sujeto y/o los objetos ya recortados, con transparencia, en el mismo lienzo y tiempo fuente que el metraje. No es una máscara B/N. El motor aplica la misma transformación y trim a base y recorte; puede añadir contorno delante. La extracción/segmentación del sujeto no está implementada aquí.

`narration` aporta la voz ya temporizada con `words`. No se altera su orden. `music` define gain y duckGain; `sounds` contiene cues explícitos con motivo, tiempo, ganancia y fades. El motor no asigna nombres de SFX a onsets del estudio ni genera audio por su cuenta.

## Selección y coreografía

Cada receta exige datos y tiempo. El selector puntúa la adecuación, penaliza repetir la receta anterior, limita escenas gráficas consecutivas y prioriza rail en CTA. Estos pesos son decisiones de implementación, no frecuencias medidas del editor original. Los planos se eligen por etiquetas/intención y capacidad temporal; un plano sincronizado con labios debe aportarse con su rango correcto.

Una cifra puede promoverse al contador; un importe, a precio/unidad. Una comparación solo se propone cuando están declarados sus dos conceptos. Las pruebas requieren imágenes reales y regiones de revelado. Los pasos y carruseles requieren sus etapas/recursos. El diálogo simultáneo conserva rails independientes y colores diferenciados.

Los intervalos son `[start,end)`, en fotogramas de salida. Se conserva la cadencia racional. Las pausas cortas mantienen el recurso visual hasta la siguiente cláusula; el subtítulo tiene su propio límite de permanencia. Los huecos sin visual se reportan. Ninguna anotación desaparece por un fallo de OCR.

## Motion graphics implementados

| Receta | Lo que ejecuta | Relación con el estudio |
|---|---|---|
| rail | Sustitución por palabra, posición por plano, cuerpo estable con ajuste de palabras largas | Verticales/CTA |
| accumulate | Acumula palabras al llegar sus tiempos | V1 y bienvenida landing |
| hero | Foco verbal grande; otras palabras conservan su rail | V1/V6 |
| masked-hero | Relleno, recorte alpha, contorno opcional | V1 y landing CRT/cámara |
| pulse | Estados opaco/parcial/ausente y asentamiento | BLACK f268–276 a60fps |
| price | Prefijo, importe y unidad con beats independientes | V1 f176–225 |
| count | Numeral discreto, rayos y etiqueta | Valores1,6,15,21,24,26,28,29,29,30 deV1 |
| comparison | Dos conceptos en un espacio; traslado de cámara y pausa | Tiempo→Dinero V2 |
| proof | Revelado de regiones de una prueba según palabras/etapas | Perfiles landing |
| steps | Etapas conectadas con cámara que avanza | Adaptación de proceso LaFabrica |
| carousel | Recursos en perspectiva con desplazamiento entre focos | Selector/resultados V6 |
| silence | Supresión deliberada documentada | Pausas de reacción |

Hay componentes y curvas operativos; eso no certifica todavía que el acabado alcance el original. Las recetas de steps/carousel son adaptaciones. Modelos3D, recursos metafóricos, texturas y escenas de actores se suministran como medios. No están implementados aún un sistema general de cámara 3D con modelos, desenfoque de obturador ni todas las escenas de las diez referencias.

## Estado de validación

Las 25 pruebas funcionales y la comprobación TypeScript pasan y cubren determinismo, voces simultáneas, reemplazo de focos, máscaras requeridas, límites de clips, fps racionales, pausas, estados de parpadeo, contador y ducking. Los dos ejemplos se compilan por CLI y conservan cobertura de sus 22 palabras. También se verificó `--stage-media` con un WAV sintético: ffprobe, duración, copia, SHA256 y auditoría del plan.

Actualización con Birdieballs: el bundle Remotion se completó usando Rspack. Se renderizaron cuatro fotogramas de diseño y un piloto de 601 frames; el render de vídeo tardó 15,7 s con cuatro workers. La comprobación anterior con Webpack había quedado sin concluir. Véase [VALIDACION.json](VALIDACION.json).

La fidelidad visual permanece `unverified_without_visual_comparison`. Ya se ha renderizado el piloto Birdieballs B01 V01 tras la autorización de pruebas cortas; todavía no está aprobado por el usuario. Para validar estilo falta comparar secuencias representativas con sus referencias y ajustar diseño, curvas, blur y encuadres; el código que compila no prueba calidad visual.

## Revisión visual de versiones

La interfaz local [Cutroom](review/README.md) permite importar renders, marcar frames o intervalos y dibujar indicaciones sobre la imagen. Se abre con `npm run review`. Las notas y capturas quedan en `review/data/project.json` y su carpeta de medios. Ale ha autorizado reanudar pruebas de edición con clips cortos; esto actualiza la pausa anterior de renders, sin certificar retroactivamente la fidelidad de las recetas.

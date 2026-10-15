# V03 · feedback aplicado

Duración y montaje: mismos 1.204 fotogramas de V02. Audio conservado. Corrección de los rótulos y del bloque gráfico solicitados por Ale. V01 y V02 se conservan.

- «¿Cansado» y «de dejarte un» comparten x=540, y=1340; no se recoloca la preparación hacia arriba al anticipar una segunda línea.
- «riñón», «solución», «originales», «marcas favoritas» y «a una» reciben crema oliva, contorno verde de 2,5 px y sombra de 4 px. SF Pro se conserva; cambiar de fuente era una posibilidad sugerida, no un requisito.
- La multilínea se distribuye con los límites de tinta de SF Pro Bold medidos en Chromium, incluidas tildes y descendentes. La primera pasada dejó la tilde de «riñón» demasiado cerca de la línea superior; se corrigió antes del render completo. Cada bloque mantiene su ancla superior.
- El bloque de 10–12,62 s sustituye la bola estacionaria por recuperación ascendente, aproximación de detalle en «originales», apertura a dos bolas y salida hacia el siguiente plano. Curvas diferentes según acción; no se introduce un bucle de flotación.
- Material de fondo original con grano determinista, iluminación irregular, bandas suaves y profundidad. Perspectiva sugerida mediante escalas y anillos de recuperación. Las bolas son ilustraciones en 2,5D, no modelos 3D.
- El obturador evalúa ocho subfotogramas en 270°, acumula exposición dentro de una capa aislada y limita las muestras al plano. El blur gaussiano se reserva para foco/velocidad extrema y no es el único desenfoque.

## Cambios del algoritmo

`estilo-editor/FEEDBACK-ALE.md` conserva lo expresado, su alcance y la diferencia entre preferencia explícita y ensayo pendiente. `ALGORITMO.md` y `AGENTS.md` indican leerlo al retomar.

`motor-editor/src/style-rules.ts` implementa compactación y revisión de fondos/quietud; `recipes.ts` lo usa para jerarquías; `planner.ts` incorpora los avisos; `motion.ts` y `Composition.tsx` implementan exposición temporal y sombra. V03 consume las mismas funciones. Los umbrales son ayudas de revisión, no garantías de gusto.

28 tests y typecheck pasan. Fotogramas reales de alineación, multilíneas, entrada, acercamiento, pareja, salida y final inspeccionados. El bundle V03 está separado del bundle anterior. La valoración estética de V03 sigue pendiente de Ale.

# AD3 · V8 — Motion graphics recreados en Remotion

Réplica en Remotion de los gráficos nativos de **AD3-Pipeline-V8**, que en la entrega
original se construyeron y renderizaron en After Effects. El objetivo es poder producir
el anuncio entero sin abrir AE, conservando el mismo lenguaje visual y la misma
editabilidad: cada capa sigue existiendo por su nombre, con su geometría y sus
fotogramas clave como datos.

1080 × 1920 · 48 fps · 2180 fotogramas · 45,417 s.

No se ha tocado el proyecto de V8 ni sus renders. Esta carpeta es independiente.

## Qué se ha reconstruido y qué se reutiliza

**Reconstruido desde cero en Remotion** — las nueve composiciones de gráficos nativos:

| Comp | Contenido |
|---|---|
| `00 - Verde BRAUD` | Fondo oliva: degradado radial + fibra + grano |
| `01 - Se monta solo` · `01A` · `01B` | Pistas editables en 3D, descenso de cámara y entrada a la caja |
| `02 - Una creatividad` | Convergencia de trazos y tipografía |
| `03 - Todo encaje` | Anillo de unión y entrada de las tres palabras |
| `04 - Sistemas Visual Hub` · `04A` | Recorrido por el sistema y las cuatro salidas |
| `05 - Produccion y oferta` | Línea de producción y el bloque de precio con giro radial |

Más las **41 capas de subtítulos nativas** del máster, con su sombra y su contorno.

**Reutilizado sin modificar** (enlazado en duro desde el paquete de V8, sin copia ni
recodificación):

- `Montaje-AD3.mp4` — el montaje de metraje, que ya era un render de Remotion.
- `Mezcla-Final.wav` — la mezcla de audio de V8.
- Las cuatro fotografías de Higgsfield Soul Cinematic y los seis fotogramas `toma-*.jpg`.
- SF Pro Display Bold y Regular.

**Aproximado**: las dos texturas del fondo (`ADBE Fractal Noise` y `ADBE Noise2`) son
efectos procedurales propietarios de AE. Se reconstruyen con el mismo modelo —ruido
fractal de ocho octavas estirado en horizontal, y ruido monocromo recortado— y se
congelan en PNG para que el render sea determinista. El grano resultante tiene la misma
densidad y amplitud, pero no es el mismo patrón píxel a píxel.

## Desenfoque de movimiento

AE renderizó con obturador de 210° y fase −105°: cada fotograma integra 0,583 de
fotograma centrado en él, y por eso los planos se arrastran durante el descenso a la caja
o el recorrido por el sistema. Sin esto la recreación sale nítida y se nota.

Como todo el árbol se evalúa en función del tiempo —y la evaluación es continua—, basta
pedirle tiempos fraccionarios: `Shutter` muestrea ocho veces dentro de la ventana del
obturador y las promedia apilándolas con opacidad 1/(i+1), que compuestas en orden dan
la media aritmética. En el fotograma 800 la diferencia con la entrega baja de 7,62 a 4,33.

Ocho muestras es el óptimo medido; con más, el redondeo de la composición en 8 bits
empieza a estropear el promedio. Se ajusta con `REMOTION_SAMPLES` (1 lo desactiva, útil
para iterar rápido).

## Cómo se obtuvo la definición

La spec de diseño de V4 (`v4/ae/design-refined.json`) **no sirve como fuente**: pasos
posteriores —el refinado de V4, la exportación por partes, la corrección de retenciones,
y los parches de V5 y V7— añadieron capas y cambiaron tiempos directamente sobre el
`.aep`, sin volver a la spec. Usarla produciría un vídeo con bloques descolocados.

Lo que sí es fiable es la secuencia de operaciones que recibió After Effects: cada lote
quedó guardado en `v*/ae/*.json`. `scripts/replay-ae.py` las **vuelve a ejecutar en orden
cronológico** sobre un modelo de datos —4640 operaciones, 13 comps— y emite
`src/design.json` con los fotogramas clave normalizados a puntos de control explícitos.

Tres detalles del comportamiento de AE hubo que modelarlos porque no están en las
operaciones y cambian el resultado:

- Al mover solo el punto de entrada de una capa, AE **conserva su duración**: la capa se
  desplaza en lugar de recortarse.
- Al emparentar, AE **conserva la transformación del hijo**, reexpresando su posición en
  el espacio del padre. Sin esto, la del padre se aplica dos veces — los 39 radios del
  bloque de precio aparecían desplazados 540 × 960 px.
- `keyframe.set_batch` **conserva el suavizado** de las claves que ya existían. Reescribir
  la posición de «Visual Hub» no deshizo su curva de entrada.

## Comprobación

`npm run verify` contrasta la reconstrucción con el volcado que devolvió el propio
After Effects tras el parche de V7 (`v7/ae/patch-results.jsonl`), que es el estado exacto
de la imagen entregada en V8:

```
164 capas contrastadas, 0 discrepancias
```

Coinciden nombre, número de capas, duración de cada comp y entrada/salida de cada capa.

Sobre la imagen, `scripts/compare.py` mide fotogramas contra `AD3-Pipeline-V8.mp4`. La
columna «estructura» compara tras desenfocar, porque el grano es ruido procedural y nunca
coincide píxel a píxel; los fotogramas sin gráficos marcan el suelo de la medida —entre
3,3 y 4,3, que es la compresión del mp4.

De 29 fotogramas repartidos por todo el anuncio, **26 quedan en «cerca» o mejor**, la
mayoría entre 4 y 6. `analysis/hoja-comparacion.png` pone ocho de ellos uno encima de
otro para verlo de un vistazo.

### Limitación conocida

Quedan tres fotogramas por encima del resto: 760 (8,2) y, sobre todo, **1600 y 1660
(13,4 y 11,9), en el bloque Sistemas**, durante el tramo más rápido del recorrido de
cámara. El contenido, la escala, los tiempos y el desenfoque coinciden; el conjunto
aparece desplazado hasta unos 20 px en horizontal.

La causa es el acoplamiento exacto entre el trazado espacial de tangentes automáticas de
AE y su gráfica de velocidad, que Adobe no documenta. Se probaron seis modelos
(Catmull-Rom clásico, acotado y no uniforme, con y sin reparametrización por longitud de
arco, y lineal) midiendo la imagen en cada caso; el implementado es el que menos se
aleja. Sobre el vídeo en marcha no se aprecia, pero conviene saber que está ahí.

La distancia de la cámara implícita de AE (`CAMERA` en `src/ae.tsx`) también está
ajustada por medición, no deducida: `scripts/calibrate.py` barre el rango y el mínimo es
plano entre 1600 y 1800 para una comp de 1080 × 1920.

## Uso

```bash
npm install
npm run replay      # reconstruye src/design.json desde las operaciones de AE
npm run textures    # regenera las dos texturas del fondo
npm run verify      # contrasta con el volcado de After Effects
npm run studio      # abre el editor
npm run render      # anuncio completo -> output/AD3-V8.mp4
```

`npm run render:graficos` entrega solo los gráficos en ProRes 4444 con alfa, para
componerlos sobre otro montaje.

Para revisar un fotograma suelto y compararlo con V8:

```bash
node scripts/still.mjs AD3-V8 1962 && python3 scripts/compare.py 1962
```

El resultado queda en `analysis/compare/1962.png`: referencia, recreación y diferencia.

## Composiciones

`AD3-V8` es el anuncio completo y `AD3-V8-Graficos` solo la capa de gráficos. Además hay
una composición por cada comp de AE, con su nombre, para revisarlas aisladas igual que en
el panel de proyecto.

## Editar

`src/design.json` es la definición completa: capas, transformaciones, fotogramas clave,
formas, textos y efectos. Cambiar un color, un tamaño de letra o un tiempo es editar ese
archivo — pero se regenera con `npm run replay`, así que un cambio permanente va en
`scripts/replay-ae.py`, al final, como un delta con su motivo.

`src/interp.ts` implementa la semántica de AE (curvas de influencia y velocidad,
trazados espaciales, matrices 4×4) y `src/ae.tsx` dibuja cada tipo de capa.

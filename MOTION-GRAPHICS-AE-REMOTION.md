# Motion graphics: After Effects y Remotion

Notas de la recreación de los gráficos de AD3 V8 en Remotion (21/09/2026). Todo lo que
hay aquí está medido o comprobado contra la entrega real, no supuesto. Sirve para decidir
con qué herramienta abordar el siguiente anuncio y, si se vuelve a portar algo, para no
repetir el camino.

El proyecto está en [`ad3-pipeline/remotion-mg/`](ad3-pipeline/remotion-mg/README.md).

## Decisión vigente para el producto · 14/10/2026

Ale confirma que el sistema para clientes debe operar autónomamente por código, sin
necesitar una interfaz de edición. **Remotion es la base actual del producto**; AE sigue
siendo una herramienta de producción interna. No interpretar «otras herramientas» como
un encargo de integraciones con Premiere, Resolve o CapCut. El estudio y el prototipo
anteriores ya justifican continuar desde Remotion, sin reabrir la elección por defecto.

La política editorial y sus evidencias se conservan como datos; Remotion ejecuta el plan.
Las limitaciones de fidelidad y rendimiento de este documento siguen pendientes donde
no exista una prueba posterior. Las cifras de AE y Remotion corresponden a composiciones
distintas: **no constituyen un benchmark controlado entre motores ni permiten prometer
un multiplicador de velocidad**.

---

## 1. La pregunta de fondo: ¿cuál es mejor?

No son la misma herramienta compitiendo. En esta serie AE ya se maneja **por código**, a
través del puente local, enviando lotes de operaciones desde scripts de Python. Así que
la comparación real no es «GUI contra código», sino **dos formas de tener el motion
graphic como dato**.

**AE es mucho más rápido renderizando.** Medido: el piloto BRAUDLABS —67 fotogramas,
1080 × 1920, con desenfoque de movimiento y cámara 3D— se renderizó en **4 segundos**,
unos 17 fps (`braud-style-lab/ae/aerender-delivery.log`). Remotion, sobre la comp más
pesada de AD3, hace 6,8 fps sin desenfoque y 0,86 fps con él. Es decir: **~2,5× más
rápido sin desenfoque y ~20× con él** (§8). La mayor parte de la distancia la explica el
obturador, que en AE está integrado y en Remotion hay que construirlo muestreando.

**AE trae resuelto lo que en Remotion hay que implementar.** Cámara 3D, desenfoque de
obturador, ruido fractal, trazados espaciales con tangentes automáticas, curvas de
velocidad. Cada una de esas cosas costó trabajo y alguna quedó aproximada.

**Lo que Remotion dio a cambio**, y que no es poco:

- El proyecto entero es texto: 329 capas en un JSON de 677 KB y ~1500 líneas de código.
  Versionable, diffeable, revisable.
- Se pudo **contrastar capa a capa** contra el volcado del propio AE: 164 capas, 0
  discrepancias. Con un `.aep` binario eso no se puede hacer.
- Se pudo medir la imagen fotograma a fotograma contra la entrega, automáticamente.
- Renderiza sin licencia, sin GUI y sin que AE esté abierto. Va a un CI.

**Y una cosa que AE hizo mal en esta serie y Remotion no puede hacer mal** — ver §2.

### Cuándo usar cada uno

- **AE** para producir: es más rápido, el desenfoque y el 3D salen bien de fábrica, y
  ya está integrado en el flujo.
- **Remotion** cuando haga falta que el resultado sea reproducible, verificable o
  generado en masa (variantes de un mismo anuncio, piezas parametrizadas por datos,
  render en servidor).
- **Portar de AE a Remotion** solo si hay una razón concreta. Cuesta, y el último 5 %
  de fidelidad es el caro.

---

## 2. El problema que de verdad importa: la spec se desincroniza del `.aep`

Este es el aprendizaje más valioso de la tirada y no va de tipografías ni de curvas.

El proyecto de AD3 se compiló desde una spec declarativa (`v4/ae/design.json`). Pero
**los pasos posteriores parchearon el `.aep` directamente, sin volver a la spec**:
el refinado de V4, la exportación por partes, la corrección de retenciones, y los parches
de V5 y V7. Resultado: la spec y el proyecto real divergieron.

Casos concretos encontrados:

| Capa | En la spec | En AE (real) |
|---|---|---|
| `Entra en` (comp 05) | entra en f63 | entra en f54 |
| `Visual Hub` (comp 05) | sale en f130 | sale en f276 |
| `Giro radial - oferta` | no existe | creada en el refinado |
| `Anillo precio` | no existe | creada en el refinado |

Construir desde la spec daba un vídeo con bloques descolocados. **La fuente fiable eran
los lotes de operaciones**, que sí quedaron guardados: `scripts/replay-ae.py` los
reproduce en orden cronológico —4640 operaciones— y reconstruye el estado real.

**Lección para el futuro, use la herramienta que use:** si se parchea el proyecto y no la
definición, la definición deja de valer. O se regenera siempre desde la definición, o se
acepta que el log de operaciones es la única verdad. En Remotion este fallo no cabe
porque el código *es* el proyecto: no hay dos copias que puedan discrepar.

---

## 3. Comportamientos de AE que no están en las operaciones

Tres cosas que AE hace por su cuenta y que hubo que descubrir midiendo, porque ninguna
aparece en el log de operaciones. Si se vuelve a leer un `.aep` como datos, buscar estas
primero:

**Mover solo el punto de entrada conserva la duración.** `layer.inPoint = t` desplaza la
capa, no la recorta. Se detectó por una discrepancia de 1 fotograma en `SUB 19 - sueltos`
(885 frente a 886).

**Emparentar conserva la transformación del hijo.** Al asignar un padre, AE reexpresa la
posición del hijo en el espacio del padre para que no se mueva. Sin modelarlo, la
transformación del padre se aplica dos veces: los 39 radios del bloque de precio salían
desplazados 540 × 960 px.

**Reescribir fotogramas clave conserva su suavizado.** `keyframe.set_batch` sobre claves
que ya existen mantiene sus curvas. Sin esto, «Visual Hub» llegaba 60 px por debajo,
porque su curva de entrada (influencia 80/15) se había reiniciado a 33/33.

---

## 4. Interpolación: la traducción que hay que tener a mano

Es lo más importante para portar AE a cualquier otro sitio.

AE guarda por cada lado de cada clave una **influencia** (%) y una **velocidad**
(unidades/s). Eso se convierte en una Bézier temporal así:

```
dt = (f1 - f0) / fps              duración del tramo, en segundos
dv = v1 - v0                      cambio de valor (módulo euclídeo si es espacial)

x1 = outInfluence / 100
y1 = (outSpeed · dt / dv) · x1
x2 = 1 - inInfluence / 100
y2 = 1 - (inSpeed · dt / dv) · (inInfluence / 100)
```

La Y del punto de control es la pendiente normalizada escalada por la influencia. Con
velocidad 0 queda una curva plana en los extremos.

**Equivalencias de esta serie:**

| En el proyecto | Influencias | Bézier |
|---|---|---|
| `out` (la de casi todo) | 80 entrada / 15 salida | `cubic-bezier(0.15, 0, 0.20, 1)` |
| `flow` (recorridos) | 33 / 33 + velocidad calculada | depende del tramo |
| `linear` | — | recta |

Ojo: el `out` de esta serie es **mucho más seco** que el `ease-out` de CSS
(`cubic-bezier(0, 0, 0.58, 1)`). Arranca rápido y frena largo. Es buena parte de por qué
el estilo se siente como se siente — «las palabras grandes aparecen desde abajo y frenan
rápidamente».

### Propiedades espaciales

Posición y punto de anclaje **no se interpolan en línea recta**. AE traza una curva suave
que pasa por los puntos, con tangentes automáticas. Esto no es un detalle:

- Con interpolación lineal, un recorrido de cámara de varios puntos se ve anguloso.
- Con Catmull-Rom clásico (tangente = (P[i+1] − P[i−1]) / 6, sin acotar) **se curva entre
  dos claves idénticas**: un tramo que debía quedarse quieto describía un arco de 40 px.

Lo que mejor midió: dirección de P[i−1] a P[i+1], longitud acotada a un tercio de la
distancia al vecino más cercano. La cota es lo que hace que dos claves iguales den un
tramo quieto.

**Lo que no se resolvió:** el acoplamiento exacto entre ese trazado y la gráfica de
velocidad. Se probaron seis modelos (Catmull-Rom clásico, acotado y no uniforme, con y
sin reparametrización por longitud de arco, y lineal), midiendo la imagen en cada caso.
En el tramo más rápido del recorrido por Sistemas queda un desvío de ~20 px. Adobe no lo
documenta y no se dedujo desde fuera.

---

## 5. El 3D

- **Cámara implícita.** Una capa 3D se proyecta aunque no haya capa de cámara. La
  distancia no está documentada; se ajustó por medición (`scripts/calibrate.py`) y el
  mínimo es plano entre **1600 y 1800 para una comp de 1080 × 1920**.
- **Ejes.** AE tiene +Z hacia dentro de la pantalla y CSS hacia fuera: **los giros en X e
  Y cambian de signo, el de Z no**.
- **Orden de transformación:** `translate(pos) · Rz · Ry · Rx · scale · translate(−anchor)`,
  con `transform-origin: 0 0` y `matrix3d`.
- **Emparentado:** componer matrices, no anidar DOM. Anidando se rompe el orden de
  apilado de las capas, que en AE el emparentado no toca.
- **Comps anidadas:** en AE se renderizan planas salvo que se colapsen transformaciones.
  En CSS sale gratis, porque `overflow: hidden` fuerza `transform-style: flat`.

---

## 6. Desenfoque de movimiento: la diferencia visual más grande

AE renderizó con **obturador 210°, fase −105°, 16 muestras**. Cada fotograma integra 0,583
de fotograma centrado en él. Por eso los planos se arrastran en el descenso a la caja o en
el recorrido por el sistema. Sin esto la recreación sale nítida y **se nota mucho**.

Remotion no lo trae. `@remotion/motion-blur` es un efecto de estela, no integración de
obturador.

**Cómo se resolvió**, y es una técnica reutilizable: hacer que todo el árbol sea **función
pura de un número de fotograma** —pasando `frame` como prop en vez de llamar a
`useCurrentFrame()` dentro de cada capa—. Entonces se le pueden pedir tiempos
fraccionarios. Se muestrea ocho veces dentro de la ventana del obturador y se promedian
apilándolas con opacidad **1/(i+1)**, que compuestas en orden dan exactamente la media
aritmética.

Medido en el fotograma 800 (descenso a la caja): diferencia con la entrega **7,62 → 4,33**.

**Ocho muestras es el óptimo.** Con más empeora: el redondeo de la composición en 8 bits
estropea el promedio cuando cada muestra aporta menos del 4 %.

| Muestras | f800 | f1600 | f660 | f1020 |
|---|---|---|---|---|
| 1 | 7,62 | 13,77 | 7,20 | — |
| 4 | 4,46 | 13,42 | 7,06 | 4,85 |
| **8** | **4,33** | **13,35** | **6,98** | **4,74** |
| 16 | 4,42 | 13,43 | 7,08 | 4,75 |
| 24 | 4,68 | 13,68 | 7,35 | 4,97 |

El coste es **×8 en tiempo de render**, medido (ver §8). Es la partida principal de la
factura, así que conviene iterar con `REMOTION_SAMPLES=1` y subirlo solo para la entrega.

---

## 7. Traducciones concretas

**Texto** — es donde más fácil se mete la pata:

- El punto de anclaje de una capa de texto en AE es **el origen de la línea base**. Un
  `<text>` de SVG con `x`/`y` en la línea base y `text-anchor` mapea 1:1. Un `div` de CSS
  no: se pelea uno con `line-height` y el ascendente.
- El tracking de AE son **milésimas de eme**: `letter-spacing = tracking / 1000 × fontSize`.
- Trazo con `strokeOverFill` desactivado → `paint-order: stroke` en SVG.

**Efectos:**

| After Effects | Equivalente |
|---|---|
| Gaussian Blur, desenfoque B | `filter: blur(B/2)` |
| Drop Shadow | `drop-shadow(sin(dir)·dist, −cos(dir)·dist, soft/2)` — la dirección de AE se mide desde arriba, en horario |
| Ramp radial | `radial-gradient`, radio = distancia entre los dos puntos |
| Trim paths | `pathLength=1` + `stroke-dasharray` |
| Fractal Noise, Noise | **sin equivalente** — generar PNG determinista |

**Determinismo.** Remotion renderiza fotogramas en procesos paralelos: cualquier cosa
aleatoria debe ir con semilla y congelada en un archivo, o cada fotograma saldrá
distinto. Las dos texturas del fondo se generan una vez con `numpy` y se guardan en PNG.

**Formas.** Un rectángulo de AE está centrado en el origen del grupo y el compilador le
pone el anclaje en `[−w/2, −h/2]`, de modo que la posición acaba siendo la esquina
superior izquierda. Las elipses y los trazados van centrados en el origen.

---

## 8. Rendimiento, medido

Medido con `npm run bench`, que reutiliza un mismo empaquetado y un mismo navegador para
las dos pasadas, de modo que la diferencia sea solo el obturador. Comp 05, la más pesada:
294 fotogramas, 90 capas.

| | fps | Tiempo |
|---|---|---|
| **AE** · piloto BRAUDLABS, 67 f, con desenfoque y cámara 3D | **~16,8** | 4 s |
| **Remotion** · comp 05, sin desenfoque | 6,83 | 43,1 s |
| **Remotion** · comp 05, 8 muestras | 0,86 | 343,5 s |

El arranque es despreciable cuando se reutiliza: empaquetado 0,9 s y navegador 0,1 s.

Dos lecturas:

- **El obturador cuesta exactamente ×8** (343,5 / 43,1 = 7,97). Era de esperar, pero
  conviene tenerlo medido: es la partida principal de la factura.
- **Incluso sin desenfoque, AE va ~2,5× más rápido**; con desenfoque la distancia se va
  a ~20×. Las comps no son idénticas —el piloto es un gráfico y la 05 tiene 90 capas—
  así que el número exacto no es comparable, pero el orden de magnitud sí.

> Cuidado al medir: una comp corta no sirve. En una primera prueba con la comp 03
> (76 fotogramas, 7 capas) salían 46 s y 44 s con y sin desenfoque, y parecía que el
> obturador era gratis. Era el arranque tapando la señal — y además `render.mjs` no
> pasaba las variables de entorno, así que las dos pasadas usaban 8 muestras.

### Cómo se podría acelerar Remotion

- **No muestrear lo que no se mueve.** Ahora el obturador remuestrea el árbol entero,
  incluido el vídeo de fondo, que sale idéntico en las ocho muestras. Sacarlo fuera del
  muestreo debería acercar el coste al ×8 solo sobre los gráficos. *(Pendiente.)*
- Muestrear solo los tramos con movimiento rápido; en los estáticos el obturador no
  aporta nada.
- `REMOTION_SAMPLES=1` mientras se itera; subirlo solo para la entrega.

---

## 9. Verificación: lo que Remotion sí permite y AE no

Por ser código se pudo:

1. **Reproducir el log de operaciones** y reconstruir el proyecto como datos.
2. **Contrastar 164 capas** contra el volcado del propio AE — nombre, número, duración,
   entrada y salida. 0 discrepancias.
3. **Renderizar cualquier fotograma aislado** en segundos y compararlo con la entrega.

Dos trucos de medida que merece la pena recordar:

- **Comparar píxel a píxel no sirve si hay grano procedural.** El grano nunca coincidirá.
  Hay que comparar tras un desenfoque de caja, que deja la estructura y descarta el ruido.
- **Los fotogramas sin gráficos dan el suelo de la medida.** Aquí salieron entre 3,3 y
  4,3, que es solo la compresión del mp4. Cualquier cosa cerca de ese número es, a
  efectos prácticos, idéntica.

Resultado final: de 29 fotogramas repartidos por todo el anuncio, 26 en «cerca» o mejor.

---

## 10. Tropiezos de operación

- **`tail` retiene la salida.** `node render.mjs | tail -25` no muestra el progreso hasta
  que el proceso termina. Para seguir un render, escribir a un archivo y hacer `tail -f`.
- **`renderMedia` no hereda el entorno.** Hay que pasarle `envVariables` explícitamente;
  si no, `REMOTION_SAMPLES=1 node render.mjs` no desactiva nada y se rinde a 8 muestras
  sin enterarse. Costó una medición equivocada antes de detectarlo.
- **El desenfoque llena el disco.** Remotion escribe JPEG intermedios; con ×8 y el disco
  al 99 % el render murió con `ENOSPC` en el fotograma 739. Conviene comprobar el espacio
  antes de una tirada larga.
- **Enlazar los medios en duro** (`os.link`) en vez de copiarlos a `public/`: mismo
  inodo, cero espacio extra.
- **Renderizar solo lo que se quiere ver.** Para revisar los gráficos no hace falta el
  anuncio entero: una composición que encadene los bloques son 856 fotogramas en vez de
  2180.

---

## 11. Actualización del 10/10/2026: Remotion 4.0.534 y obturador oficial

Lo anterior describe Remotion 4.0.525. Este apartado registra lo que cambió después; nada
de lo que sigue se ha probado con un render, porque el usuario pidió no hacer pruebas todavía.

**Qué se actualizó a 4.0.534**

- La raíz del repo (`remotion`, `@remotion/bundler`, `@remotion/cli`, `@remotion/motion-blur`,
  `@remotion/renderer`).
- `ad3-pipeline/remotion-mg`, donde además se añadió `@remotion/motion-blur`.
- `ad4-creatina/remotion`: comparte `node_modules` con `remotion-mg` por enlace simbólico, así
  que usa la versión nueva; se alineó su `package.json` para que diga lo que hay instalado.

`tsc --noEmit` pasa sin errores en la raíz y en `remotion-mg`. AD4 no tiene `tsconfig.json` y
no se comprobó.

**Qué sigue en 4.0.525**: `ad1`, `ad1-reedit/remotion`, `ad3-pipeline/remotion` (y `v4` y `v7`,
que enlazan a su instalación), `replica-96c1/remotion` y los paquetes de entrega de
`ad3-pipeline/v2` y `v3`. No se tocaron para que las versiones entregadas sigan siendo
reproducibles.

Para volver atrás: fijar `4.0.525` en esos tres `package.json` y ejecutar `npm install`.

**Qué trae de nuevo para el desenfoque**

El §6 dice que Remotion no trae obturador. Ya no es así: `@remotion/motion-blur` exporta
`HtmlInCanvasMotionBlur` desde la 4.0.529 (anidado en el render de servidor desde la 4.0.534).
Según su documentación muestrea tiempos intermedios y los promedia, con 180° y 8 muestras por
defecto, y es la opción recomendada frente a `CameraMotionBlur`, que «puede cambiar colores y
opacidad» al apilar capas. Eso encaja con lo medido en el §6: el promedio por capas apiladas
empeoraba por encima de 8 muestras.

Fuentes: [HtmlInCanvasMotionBlur](https://www.remotion.dev/docs/motion-blur/html-in-canvas-motion-blur)
y [guía de motion blur](https://www.remotion.dev/docs/motion-blur-guide).

**Pendiente**: medir el obturador oficial contra el construido a mano sobre la comp 05 de AD3
(`npm run bench` en `remotion-mg`), en diferencia de imagen frente a la entrega y en tiempo de
render. Hasta entonces no se sabe si sustituye al propio ni cuánto cuesta.

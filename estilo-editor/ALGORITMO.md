# Revisión vigente: V2

El criterio operativo se amplía en [ALGORITMO-V2.md](ALGORITMO-V2.md), con reglas condicionales, procedencia, contraejemplos y parámetros desconocidos explícitos. [Abrir estudio en la interfaz](http://127.0.0.1:4317/study). V03 está rechazada y el montaje de entrada se preserva salvo instrucción específica. **La especificación0.1 que sigue es histórica: su heurística de recetas no acredita fidelidad.**

# Algoritmo de edición · especificación de trabajo

## Prioridad del feedback vigente

Consultar [FEEDBACK-ALE.md](FEEDBACK-ALE.md) al editar o ampliar el motor. Desde Birdieballs V02: conservar el ancla de la primera línea al cambiar de frase o crecer a multilínea; compactar las líneas según su tamaño y revisar sus límites reales; explorar una diferencia sutil de paleta/trazo/sombra en la segunda línea. En motion protagonista, diseñar acciones encadenadas con el guion, fondo con textura e iluminación y desenfoque temporal en desplazamientos rápidos. Evitar el objeto estacionario con texto cambiante como solución por defecto.

Estas reglas se implementan en `motor-editor/src/style-rules.ts`, el planificador, las recetas y el adaptador de render. Los umbrales técnicos propuestos no reemplazan la comparación visual con las referencias ni la valoración del usuario.

Versión 0.1, 10/10/2026. Derivada de diez referencias. El cierre de la revisión está
en `ESTADO.md`; esta especificación conserva reglas respaldadas y propuestas
operativas diferenciadas. La implementación inicial está en [motor-editor](../motor-editor/README.md),
con las diferencias y límites recogidos en [MOTION-GRAPHICS.md](MOTION-GRAPHICS.md).
Esta especificación no es un resultado visual aprobado.

## 1. Qué debe decidir

Para cada frase, decidir qué ve el espectador, qué palabra domina, cómo se relaciona
con el sujeto/recurso, qué evento cambia el foco y cuándo sucede. El resultado es
una línea de tiempo explícita de planos, rótulos, máscaras, gráficos, cámara y audio.
Una secuencia de efectos aleatorios cada N segundos no reproduce estas referencias.

La unidad de planificación es la cláusula/acción, la unidad de ejecución el
fotograma y la unidad de subtitulado suele ser la palabra. Las tres no coinciden
necesariamente: un rótulo puede atravesar un corte y un gráfico puede acumular
varias palabras antes de cambiar de plano.

## 2. Entradas

- Voz/locución con palabras, tiempos e incertidumbre. Anotación corregida cuando
  Whisper falla en nombres, cifras o frases pegadas.
- Material visual con sus rangos utilizables, encuadres y sujetos; recursos reales
  para mostrar las afirmaciones del guion.
- Cláusulas con función: gancho, problema, demostración, mecanismo, resultado, oferta,
  reacción o CTA. Estas etiquetas son decisiones editoriales, no salida del OCR.
- Eventos semánticos: cantidad, negación, contraste, lista, repetición, nombre propio,
  cita, diálogo. Seleccionar foco y verbo dominante antes de escoger un efecto.
- Perfil de estilo por familia y encuadre. Para máscaras, segmentación de sujeto
  por fotograma con el mismo recorte y transformación del metraje.
- Formato, fps racional, zonas ocupadas por sujeto/objeto y márgenes de entrega.

Los porcentajes de los estudios se guardan sobre el ancho/alto del original; las
transformaciones locales se guardan además en px. No copiar los px de una landing
1920×1080 a un reel 1080×1920.

## 3. Orden de decisión propuesto

```text
transcribir_y_corregir_palabras()
segmentar_clausulas_y_marcar_foco()
seleccionar_familia_visual_por_brief_y_material()
para cada clausula:
    elegir plano o representación gráfica que muestre su contenido
    elegir modo: palabra / acumulación / héroe / escena / silencio gráfico
    asignar una sola representación principal a cada palabra hablada
    fijar anclas y tamaños según plano, sujeto y jerarquía
    ubicar cortes y cambios de foco en eventos semánticos
    elegir entrada/salida según modo y evidencia pertinente
    asignar audio a acciones principales; preservar la inteligibilidad de la voz
compilar todo a eventos explícitos con intervalos y keyframes
comprobar conflictos temporales, espaciales y semánticos
```

«Una sola representación principal» evita duplicación innecesaria de subtítulo y
motion. Puede haber nombre/cargo junto a un rail de la frase porque cumplen funciones
distintas, como en landing f519–725.

## 4. Modos tipográficos

| Modo | Uso y comportamiento respaldado | Evidencia / límites |
|---|---|---|
| Palabra ordinaria | Sustituye a la anterior; posición constante dentro de un mismo plano o decisión de layout. Entrada directa frecuente, no rebote por defecto. | V1/V2/V3/V5/V6 según fichas; landing «Buenas» f416 entra íntegra en nativa. |
| Acumulación | Conserva palabras precedentes de una cláusula hasta el remate. La línea pequeña y la dominante tienen tiempos independientes. | V1 líneas pequeñas; landing bienvenida; interludios LaFabrica. No acumular frases arbitrarias. |
| Héroe | Foco verbal/cifra a gran escala; ajuste al ancho disponible. Puede reemplazar rail o convivir con línea subordinada. | V1 «30» detrás del sujeto desde f35; detección OCR lo omite. Anchos 70–76% son referencia frecuente, no mandato universal. |
| Héroe ocluido | Tinta detrás del sujeto, con posible contorno por delante. Mantiene identidad aunque parte de la palabra se tape. | V1 y V3 ganchos; V5; LaFabrica V2 f1648–1653. Contorno no aparece en todos. |
| Escena gráfica | El propio texto/objeto expresa la frase, con jerarquía y coreografía por beat. Suprimir la duplicación ordinaria. | Interludios V1/LaFabrica; fichas para escenas específicas. |
| Diálogo | Diferencia hablante mediante color/posición; la reacción puede ir sin rail cuando la imagen ya explica el gag. | V5 amarillo vs blanco; bloque narrador sin rail. No atribuir cada cambio de color a nueva persona sin contexto. |
| Silencio gráfico | No añadir un subtítulo inventado porque el OCR no encontró el existente. Omitir solo por decisión explícita y documentada. | Omisiones OCR, oclusiones, nombres mostrados en tarjetas y huecos deliberados son fenómenos distintos. |

### Tiempos del rail

Propuesta inicial: `startFrame = round(wordStartSec * fps)` tras la corrección de voz;
`endFrameExclusive = nextWordStartFrame` mientras continúa el rail. Terminar antes
si el layout siguiente representa esa palabra de otra forma; conservar una pausa
solo si la comprensión lo requiere. Nunca extender automáticamente una palabra a
todo un silencio largo. Una pausa escrita en Whisper no demuestra que el editor
dejase el rótulo durante ella.

El desfase mediano cercano a cero respalda sincronía por palabra. No demuestra
exactitud absoluta: los resúmenes antiguos excluían desfases grandes y el inicio
de voz tiene incertidumbre. Confirmar intervalos singulares por evidencia visual.

### Tamaño

Para el héroe vertical de la familia BRAUD, usar como propuesta `targetInkWidth ≈
0.73 * width`, con límites por composición y por legibilidad. Resolver `fontSize`
con la anchura real de la palabra en la fuente cargada y su tracking; medir caja
de tinta además del avance tipográfico. Palabras largas disminuyen de cuerpo.

`fontSize = targetWidth / widthAtUnitSize` solo funciona si el mismo modelo de
kerning/tracking se usa en la medición y en el render. CSS puede incluir espaciado
final diferente al ajuste PIL. SVG usa línea base; no confundir `line-height` con
alto de tinta, ni caja OCR con cuerpo tipográfico. Conservar descendentes y halo.

SF Pro Display Bold es la elección de implementación autorizada por Ale; el
tracking −60/1000 em es una aproximación inicial heredada, no una constante
verificada en todas las referencias. Los controles nativos nuevos de palabras
ordinarias favorecen Helvetica Bold en V2, V5, V6 y LaFabrica: conservar los fits
y su incertidumbre, sin confundir fuente elegida con fuente del original. Otros
pesos y la serif del gancho «IA» son estilos locales. No aplicar Bold a la landing
fina solo por compartir familia.

### Posición

La posición se decide **por plano/layout**, no por fotograma independiente de OCR.
La cara ayuda a detectar espacio ocupado, pero su caja puede bailar y seleccionar
otra cara. No crear un seguimiento nervioso del rail a partir de esas detecciones.

Propuesta de resolución: ofrecer anclas candidatas compatibles con el plano,
evaluar superposición con boca/ojos/objeto principal, y elegir la que conserva
jerarquía y continuidad. Mantenerla hasta el siguiente cambio semántico o de plano.
El original a veces superpone el rail sobre boca o producto (V5/V6); permitirlo
como decisión explícita con motivo, no como fallo automático.
Si hay tracking deliberado, suavizar con keyframes guardados y verificar movimiento.

No imponer y=60%: V1 suele acercarse, V5 ronda 50%, V3 usa rail inferior
y≈73% desde f132, LaFabrica puede colocar texto
arriba sobre recursos, y la landing cambia entre rail inferior, lateral y título.
Una mediana del vídeo que mezcla todos esos layouts no define un ancla universal.

## 5. Planos, cortes y ritmo

Elegir entre cambiar material, variar encuadre, introducir un gráfico, destacar una
palabra o dejar respirar la acción. Las duraciones medidas de planos describen lo
que hizo ese editor; no son un metrónomo para cortar cada 2,4 s.

Un corte próximo al inicio de palabra es frecuente. La mediana cero de algunos
verticales no implica que todos caigan exactamente ahí: los porcentajes de proximidad
son menores de 100%, la tolerancia cambia con fps y existen cortes sin voz. Priorizar
continuidad de acción y sentido de la frase sobre la rejilla del detector.

Separar en el plan:

- `source_cut`: nuevo material/ángulo.
- `reframe_step`: salto de escala del mismo material continuo.
- `overlay_change`: cambia un texto/objeto sin cortar metraje.
- `grade_change`: B/N, oscurecimiento, foco de luz.
- `freeze`: solo si el metraje queda inmóvil por evidencia; B/N por sí solo no basta.
- `single_frame_insert`: incluso 1 f puede ser intención editorial o defecto; conservar
  el hallazgo, no programarlo como recurso obligatorio sin motivo.

Ejemplos que corrigen al detector: V1 f1128 inserto de 1 f entre café/terraza;
LaFabrica V2 f342 negro de 1 f; V3 f1428/1430/1431/1433 muestra silueta
blanca del sujeto y oculta el cambio de plano1431 sin borrar fondo;
V5 f1397 candidato puede ser iluminación del mismo
plano. Los eventos de un solo fotograma son motivo para leer todos los fotogramas.

La cadencia del material y de los gráficos se separa. Si se entrega a 60 fps un
rodaje a 24/25, el vídeo repite imágenes y el texto puede seguir animado a 60.
La estimación del detector a partir de cambios finales no permite cambiar el fps
del original ni interpolar movimiento de persona sin otra decisión.

## 6. Entradas, salidas y curvas

Elegir curva por función: reemplazo directo para rail ordinario; entrada breve con
frenada para palabra protagonista; acumulación/revelado para una frase; recorrido
continuo para relación entre objetos. No heredar la misma entrada para todos.

Guardar primero mediciones por fotograma y después, si se ajusta una curva, el
modelo, parámetros, error y dominio. Un nombre como «ease-out» es insuficiente;
un cubic-bezier ajustado a una referencia no es la clave original de AE.

Ejemplos concretos de esta revisión:

- Landing «Gracias», f9–≈55: sube desde cy≈586 px hacia ≈538 px mientras aumenta
  contraste; ancho de tinta ≈128 px estable. Tabla nativa y ajuste exponencial en `medidas/landing-A/`: 47 muestras,
  RMSE≈0,63px, máximo≈2,22px; es aproximación dentro de f9–55, no easing original.
  Contrasta con «Buenas» f416, que aparece ya íntegra a escala final. No extrapolar
  la animación de la bienvenida a todo el rail.
- Landing «hooks», f4798–4828: top604→570px con ancho405–407px y
  alto118–119px. Es ascenso desacelerado y aumento de contraste; no pop de
  escala demostrado. «Creador» también asciende; su ROI limita medición de ancho.
- V6 «BLACK», f268–276: alternancia opaco / tenue / ausente / tenue / opaco en
  varios ciclos. Reproducir estados de parpadeo explícitos, no aproximarlos con fade.
- V3 gancho: alejamiento prolongado del conjunto y capas detrás del sujeto;
  las medidas exactas heredadas de nativa deben revalidarse tras corregir índices.

Para Remotion, almacenar muestras de transformaciones o keyframes precisos, y
hacer el estado función pura de `frame` (puede ser fraccionario para obturador).
No usar reloj, CSS transitions disparadas al montar ni aleatoriedad sin semilla.
La equivalencia técnica y los límites ya medidos viven en
`../MOTION-GRAPHICS-AE-REMOTION.md`; no convertir sus parámetros del AD3 en los de
estas diez referencias.

## 7. Máscaras, profundidad y pruebas visuales

Orden propuesto de composición de texto ocluido:

```text
metraje de fondo
relleno del título grande
recorte del sujeto y/o objetos oclusores (misma transformación que el metraje)
contorno del título, cuando existe en esa escena
línea subordinada / otros overlays previstos
```

Los oclusores pueden ser personas y objetos: landing funcionan f925/1009 va
detrás de CRT y cabeza sin contorno; Paid f1350 lleva relleno detrás de cámara/persona
y contorno delante. IA f1605 es frontal al CRT: no heredar máscara por proximidad.

El texto puede ser legible aun tapado por el sujeto. El contorno y el sólido no
necesitan compartir exactamente alpha/tiempos; observar cada uno. Evitar un
rectángulo fijo usado como máscara de una persona móvil.

Los recursos de prueba (perfiles, capturas, tarjetas) se anclan a lo que la voz nombra.
En landing f632–666 un perfil aparece por etapas: avatar, cabecera, estadísticas,
bio y botones; no se demuestra solo un escalado uniforme de una captura completa.
El plan debe permitir revelar elementos por separado o una máscara temporal que
reproduzca esa secuencia. No afirmar HTML nativo, 3D real o plugin concreto desde MP4.

Escenas con perspectiva se reconstruyen con matrices/proyección coherentes y
movimiento que revele contexto. Guardar la transformación del conjunto y las
locales; no usar el tamaño cambiante de la cara como estimación exacta de cámara.

## 8. Audio

Preservar voz inteligible, conservar pausas expresivas y vincular efectos a eventos
que lo necesitan. La medición de LUFS/picos describe el mix final; no separa
ganancias de voz, música o efectos. Los picos positivos de referencias no se
adoptan como objetivo de masterización.

No disparar un SFX en cada onset: el detector también marca consonantes y transientes
de música. No asignar beat-sync general a una correlación de tempo del mix. Guardar
`onsetCandidate`, `auditoryIdentification`, `visualAnchor` y `offsetFrames` por separado.
Sin escucha validada, el tipo de sonido queda como hipótesis.

## 9. Contrato de salida propuesto

Cada evento contiene `id`, `kind`, `startFrame`, `endFrameExclusive`, `sourceRange`,
`wordIds`, `clauseId`, `speakerId`, `railId`, `mode`, `layoutId`, `layerOrder`, `keyframes`, `assets`,
`occluderIds`, `evidenceIds`, `confidence` y `overrideReason`. Los intervalos derivados del estudio
se convierten de inclusivos a exclusivos una sola vez al compilar.

La fuente de verdad es una spec única. Un parche debe cambiar esa spec, con log
de decisión y versión; nunca tocar por fuera un proyecto binario o un resultado
que deja desincronizada la definición. Ese fallo ya apareció en AD3.

## 10. Comprobaciones de implementación y reconstrucción

- Cada palabra tiene representación/supresión explícita; ningún fallo OCR genera
  una omisión por accidente.
- No hay duplicaciones innecesarias de la misma frase entre rail y escena.
- Distinguir héroe ajustado al ancho y rail ampliado de cuerpo estable: V7 f33–373
  usa palabras con anchos muy distintos. La caja ancha de una palabra larga no
  basta para clasificarla como héroe. No heredar animación protagonista por tamaño.
- La cara/máscara y el fondo comparten recorte, tiempo y transformación.
- Los cortes están clasificados y no se confunden con flashes, tipografía o luces.
- Los intervalos no pierden 1 f en conversión y respetan fps racional/cadencia.
- La aleatoriedad y las transformaciones son reproducibles por fotograma.
- Cada parámetro preciso enlaza una medida; cada aproximación conserva su incertidumbre.

El motor inicial comprueba contratos, tiempos y cobertura verbal sin hacer los renders que Ale pidió
posponer. La calidad de la reconstrucción se verificará sobre sus imágenes reales
cuando se retomen las pruebas, no se garantiza por tener una spec o datos válidos.

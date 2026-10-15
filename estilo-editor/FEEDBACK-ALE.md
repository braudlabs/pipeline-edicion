# Feedback de Ale · reglas acumulativas

Leer al preparar cada versión. Registrar lo que Ale expresa, su alcance y el estado de la solución. El feedback reciente prima sobre recetas anteriores. Guardar las preferencias en la especificación y, cuando sean ejecutables, en el motor; conservar versiones anteriores para contrastar. Una propuesta aplicada no equivale a aprobación.

## Demo SaaS BRAUD Studio · Claude Avance 05 → 06 · caso y bloques · 2026-10-15

Sobre el Avance 04, Ale dijo: «venga, este estilo mucho mejor, dale». El estilo queda aprobado como dirección: titulares sobre negro, un elemento real por frase y el sistema de la landing.

Sobre el Avance 05 (0–84 s), mirando el segundo 33 (la intención, una retícula de cuatro campos con velos), dice: «No me gustan los ads de ejemplo que has seleccionado y esos bloques son super cutres, pilla el ad de la maquinita».

**Reglas derivadas (hipótesis, sin veredicto del Avance 06):**
- El ejemplo es el anuncio de la maquinita (Ecommerce Andrómeda, el de la lavandería), no las piezas del escaparate (Creatina, Sérum, Moda, PapiCat). La sudadera morada sigue vetada: se eligen y se recortan los planos donde manda la máquina.
- Un formulario de interfaz a tamaño de módulo (texto pequeño, cuatro campos a la vez, velos que lo apagan) se ve cutre. La interfaz se enseña grande, con texto legible (unos 24 px o más en pantalla), un campo cada vez y una cámara que se desliza sobre la interfaz real. Nada de velos grandes que apaguen la imagen. Cuando hay imagen (clips, caras, pantallas), la imagen manda sobre el texto.

## Demo SaaS BRAUD Studio · Claude Avance 03 → 04 · «se ve muy IA» · 2026-10-15

Sobre el Avance 03 (0–31 s), Ale dice: «Es una mierda se ve muy IA tío, hazlo más pro joder». El Avance 03 tenía fondo con brillo cobalto, la interfaz en tema claro ocupando el cuadro detrás de los titulares, recursos dibujados (onda de dictado, abanico, espiral) y, además, capturas hechas en modo desarrollo («DEV», selector «Explorar el inicio», «DESARROLLO / BRAUD»).

**Reglas derivadas (hipótesis, sin veredicto del Avance 04):**
- Nada inventado en pantalla: cada estado de la interfaz es una captura del frontal. Si el producto tiene un estado real (dictado: «Terminar», «Grabando · 0:01», «Transcribiendo…»; «pensando»: la animación thinking-flow), se captura o se reproduce tal cual, en vez de dibujar uno.
- Capturar siempre en modo producción (`?brand=…`, sin `dev=1`). Las marcas de desarrollo delatan prototipo.
- Un foco por frase. El titular va sobre negro y debajo solo el elemento real que la frase nombra (el campo, la conversación, una sección), recortado y ampliado. La ventana entera solo aparece en la presentación del producto.
- Lenguaje de la landing de BRAUD y de El Sistema FINAL: negro casi puro, titulares en degradado blanco→gris, etiquetas mono en píldora, barra de proceso por capítulos, bordes de 1 px con luz desde arriba, sin brillos de color ni rebotes.
- Material de anuncios reales en la apertura (Creatina, Sérum, Moda, PapiCat).

**Comprobación ejecutable:** antes de renderizar, buscar en las capturas «DEV», «Explorar el inicio» y «DESARROLLO»; y comparar el texto dibujado contra la captura real del mismo estado (diferencia 0 en el Avance 04).

## Demo SaaS BRAUD Studio · Claude Avance 02 → 03 · hook y música · 2026-10-15

Sobre el Avance 02, Ale dice: «la música está muy fuerte, y el hook es una mierda». El hook de V02 eran tarjetas de anuncio dibujadas (galaxia, feed de colores, contador); no había ningún material real. Los bloques 2–5 no recibieron comentario. Siguen sin aprobar, pero se conservan.

**Regla derivada (hipótesis):** un hook de producto no se construye con maquetas genéricas si hay metraje real del cliente.

**Música:** unos 7 dB por debajo, más ducking bajo la voz y sin cortes. El frenazo de cinta pasa a ser un filtrado continuo, por la preferencia ya registrada de música que no frene.

## Demo SaaS BRAUD Studio · Claude Avance 01 → 02 · ritmo y «salsa» · 2026-10-15

Sobre el Avance 01 (bloques 1–5, 0–31 s, `video-saas/videos/braud-studio-demo/`), Ale dice: «es un poco cutre,
tiene que ser más rápido, dopamínico, especialmente la apertura, falta salsa». Es la misma queja que hizo sobre
El Sistema V1/V2 («lento, cutre, poco dopamínico») y coincide con el «más salsa» de C04.

Antes, el mismo día: «no pongas esa sudadera cringe, que da pena». La sudadera morada queda fuera del material de
marca y de las referencias. Entre los clips se priorizan los planos donde no protagoniza.

Avance 02 (propuesta, sin veredicto):
- **Cambios cada 0,3–1 s:** palabras que golpean (tamaños mezclados, la clave en píldora, como T1) y un contador
  de semanas que acelera (T3).
- **Contraste de velocidades:** en «ritmo de mes» la imagen se para y se vuelve gris, con un frenazo de cinta.
  Es el único corte de la música; si recuerda a la toma que «frenaba», se quita.
- **Objetos que conectan escenas:** la idea como chispa, el logotipo que vuela a la interfaz y la tarjeta que
  gira y es Studio.
- **Luces atadas a una acción:** barridos y destellos solo en los cortes con causa.
- **Efectos sintetizados en cada acción.**
- **Motion blur solo en movimientos rápidos.** En la interfaz clara, acumular 8 muestras provocaba anillos y
  bordes dobles.

## Ecommerce Andrómeda · Claude C05 → C06 · 144 fps y «upgrade infernal» · 2026-10-15

Sobre C05 a 24 fps, Ale: «Esta versión me la sacas en 144 fps y 1080, luego, haz otra versión
con más efectos aún, haz un upgrade infernal». No corrige nada de C05; se entregó a 144 fps
(1080×1920, 12.300 f, verify TOTAL OK). Tras «más salsa» en C04, vuelve a pedir más densidad de
efectos: preferencia clara en esta serie.

C06 (propuesta, sin veredicto) sube la densidad sin tocar lo aprobado:
- **Cámara digital:** golpes de zoom en las palabras que pesan, escalones en las repeticiones
  («días y días», «meses y meses»), empujes, caída en «caído», temblor en los impactos y barrido
  con desenfoque en el corte a la máquina.
- **Efectos atados a una palabra o acción:** B/N selectivo con la tarjeta en color, ondas,
  chispas, centelleo, rayos detrás de la cabeza en «criterio», haces de los proyectores, fallo
  de imagen en «este mismo ad», flechas en «pincha abajo», y fugas de luz al entrar los
  fundadores y la llamada.
- **Se mantienen:** rótulos libres fijos dentro de x 100–980; nada de motion sobre la pantalla de
  la maquinita (las ondas se recortan por encima); gag en B/N sin subtítulos, ahora con grano y
  viñeta; hook, persiana y «OTRA PUTA VEZ».

Bloque protagonista: dos alternativas con fotogramas reales. Se eligió «aterrizaje»; la otra,
«apagón y haz cenital», apenas se leía sobre un decorado tan claro.

## Ecommerce Andrómeda · Claude C04 → C05 · paleta, márgenes, salsa y música continua · 2026-10-15

Veredicto de Ale sobre C04: «overall no está mal». Por partes: (1) tinta marino + azul BRAUD
sobre la camiseta de los fundadores: «la paleta de colores de los subtítulos no me gusta una
mierda» → solo blanco + azul claro; en fondos claros, halo oscuro difuso (sin caja). (2) Tarjeta
«nuevo ángulo»: «puede quedar más integrado… se ve un poco cutre». (3) Eco en «el doble de
mierda»: «no me gusta, queda cutre». (4) Rótulos «demasiado pegados al lateral… Meta recorta un
poquito los bordes, es importante», y hay más casos → regla ejecutable: toda línea se ajusta
dentro de x≈100–980 automáticamente (también handles y copias decorativas). (5) Música: «no me
gusta nada, es como que frena mucho a la mitad» → la toma paraba al final de casi cada compás y el
montaje añadía silencios; se aprueba una toma nueva continua (sin paradas ni silencios). (6) Pide
«más salsa»: efectos como los del editor —luces en un momento, un objeto importante que refleja—.
Regla derivada: preferir continuidad musical; recursos de luz puntuales atados a una acción o
palabra, nunca como receta por corte. C05 entregada a 24 fps el 15/10 (verify TOTAL OK, copia ligera
enviada); propuesta pendiente de veredicto. 144 y 60 fps, solo tras su visto bueno.

## Ecommerce Andrómeda · Claude C03 → C04 · vídeo completo con música · 2026-10-15

Con la entrega completa del director (17 unidades, 85,417 s), Ale: «ya está todo ready para
terminar el vídeo». C04 extiende C03 (sin rehacer lo anterior) y aplica a 06–15 las reglas ya
registradas: líneas grandes centradas en la zona libre de cada plano, sin tapar caras, manos,
ticket ni pantallas; el recurso de relleno detrás + contorno delante solo en «criterio»
(segundo y último uso tras el hook); nada encima de la maquinita; handles solo en 10.
Propuestas del agente, pendientes de veredicto: la línea que acompaña los acercamientos de
cámara (07/08), la voz de la máquina toda en azul claro (08), «mierda» que cae al cesto y sale
duplicada (09), tinta marino sobre camisetas y mostrador claros (10/15), la pared que se llena
de «creativos» (12). Música: toma 2 de ElevenLabs según la spec funk de 122 BPM que pasó Ale;
el brief del director pide otra pieza (118 BPM, pizzicato/fagot/piano). Se señala la
discrepancia; no se ha elegido por él. Nada escuchado todavía.

## Ecommerce Andrómeda · Claude C02 → C03 · sin recuperar el término anterior · 144 fps · 2026-10-14

Sobre C02, Ale detecta que al volver del gag de la sudadera a «la solución» «hay un frame que
se sigue viendo lo de problema» (la ventana V8 recuperaba «tu problema» ≈f740–757 antes de
cerrarlo). Lo percibe como error: al volver de un corte, no reaparecer un término ya leído
para transformarlo; abrir directamente el nuevo. Regla local aplicada en C03 (la selección
se abre limpia con «la solución»); la relación con recuperación queda como recurso a usar
solo si el término anterior sigue en pantalla, no tras un corte de escena. Pide además la
entrega «en 144 Hz y en 1080»: composición a 144 fps (metraje ×6 sin interpolar, rótulos a
144) conservando la de 24 fps. No implica aprobación nueva del resto.

## Ecommerce Andrómeda · Claude C01 → C02 · subtítulos grandes y centrados · 2026-10-14

Veredicto de Ale sobre C01 (`ecommerce-andromeda-claude/c01/`): «el hook es la polla, lo de
las imágenes también» —capturas del cartel impreso en la persiana («es la misma / MIERDA /
de siempre», f190–237) y del remate condensado «OTRA / PUTA / VEZ.» (f578–610)—; «el resto
de subtítulos, la fuente es muy pequeña, demasiado a los lados (se cortará en meta) y no es
estética». Aprobación local de esos tres recursos; rechazo del rail pequeño (58–64 px) en
columnas pegadas a los bordes (x≈64–72 o alineado a 1036–1044).

Regla para C02 y siguientes: los subtítulos de lectura adoptan el lenguaje del hook —frase
corta en una línea, SF Pro ~800, blanco con acento azul claro, entrada subiendo con
asentamiento— a tamaño grande, centrados en x=540 y con márgenes laterales amplios
(tinta dentro de x≈100–980) para no perderse en recortes o interfaz de Meta. El ancla
vertical sigue eligiéndose por plano en la zona central. Los cuatro recursos aprobados se
conservan sin cambios. Lo demás de C02 es propuesta del agente, pendiente de veredicto.

## Ecommerce Andrómeda V05 · añadir motion fuera de la maquinita · 2026-10-14

Ale responde «bien» a V04 y pide «algún motion graphic». Ante una propuesta en la
pantalla, corrige: «en la maquinita no, mejor en otro sitio». Mantener esa escena y el gag
de sudadera; añadir motion en otro tramo, sin interpretar «bien» como aprobación del
anuncio completo todavía incompleto.

V05 propuesta: calendario de hojas con aceleración de01a07 sobre la pared durante
«días y días» (10,000–11,479s), sin cubrir caras ni duplicar las palabras del subtítulo.
Se comparan tres estados de diseño: hojas, cuadrícula, reloj. Se eligen hojas físicas
por encaje con el material. La selección y la ventana son decisiones del agente, no
preferencias globales de Ale. Referencia T3 para el ritmo; no copiar sus píxeles/audio.
La condición ejecutable de `WaitingMotion` limita el overlay a ese intervalo y devuelve
null fuera de él; la revisión contrasta V04 en maquinita y sudadera. V05 pendiente.

## Ecommerce Andrómeda · pieza paralela de Claude (C01) · hook aprobado localmente · 2026-10-14

Encargo directo a la sesión de Claude, en paralelo a V01–V05 de Codex: «quiero que los
subtítulos sean avanzados dopamínicos, usando bastantes recursos, estético, acorde al
vídeo, mantén el audio nativo de los clips (incluso el del hook)». Pieza independiente en
`ecommerce-andromeda-claude/c01/`; no toca `ecommerce-andromeda/`.

Sobre los fotogramas del estudio del hook, Ale: «este inicio de subtitulación me molaba
mucho». Se refiere a la variante A (`ecommerce-andromeda-claude/c01/stills/hook-A/`):
frases en SF Pro 820 grande detrás de las dos cabezas (relleno blanco recortado con matte
de persona, contorno fino delante), acentos en azul claro («ecommerce», «Andrómeda»,
«semana»), entrada subiendo desde detrás de las cabezas y susurro nativo «más anuncios.
/ más.» pequeño en azul claro sobre el hombro del azul. Aprobación LOCAL del arranque
(0–5,4 s): no aprueba el resto de C01. Se descartan las variantes A2 (relleno azul BRAUD)
y B (rail en el pecho). Regla derivada para C01: conservar esa identidad cromática
(blanco + azul claro) en el resto de rótulos; no usar el relleno azul saturado como
color de héroe. Se aplican también a C01 las correcciones de V04 de Codex: gag de la
sudadera en blanco y negro sin subtítulos y el recurso de relleno detrás/contorno delante
dosificado (en C01 solo en el hook).

## Ecommerce Andrómeda V04 · dosificar recurso y gag limpio · 2026-10-14

Ale: «ahora lo has spameado demasiado», y sobre la sudadera: «más gag, pon blanco
y negro, sin subtítulos». Corrección explícita de V03: reutilizar un recurso no implica
aplicarlo a casi todos los énfasis. Dosificarlo según función y contraste con los tramos
ordinarios. Excepción específica a la cobertura completa anterior: suprimir la frase
«y con la sudadera de este tío» durante el gag; no generalizar esa omisión al resto.

V04 propuesta: contorno/relleno solo en tres momentos —«anuncios nuevos», «mierda»,
«solución»—; esa selección concreta es decisión del agente, pendiente de veredicto.
Blanco y negro y cero subtítulos en frames692–740 de base24fps (28,833–30,875s),
recuperando color con «Vengo a hablarte». Audio nativo y montaje conservados. Regla
ejecutable de densidad mediante lista explícita de frases y comprobación de ausencia
de elementos en el intervalo del gag en `ecommerce-andromeda/v04/edit-decisions.json`
y la revisión de esta versión. V03 no queda aprobada por este feedback.

## Ecommerce Andrómeda V03 · fluidez, cobertura y contorno sobre personaje · 2026-10-14

Feedback directo sobre V02: «se ve como super lag», faltan muchos tramos de subtítulos,
«algo mejor», y pide reutilizar mucho más el recurso de la captura «criterio / visual».
Mejora parcial; V02 no queda aprobada. El recurso mostrado es relleno detrás de la
silueta y contorno por delante, confirmado contra `mercadillo/v01/Film.tsx` y
`mercadillo/v02/ae/criterion.py`; no reducirlo a una tipografía de trazo sin integración.

Aplicación V03: recuperar119/119palabras de narración; no omitir texto para despejar
un gag, resolver su posición. Unidades de lectura completas desde el primer fotograma,
sin fade de baja opacidad ni cascada palabra a palabra en todos los subtítulos. Cadencia
V02 comprobada:920fotogramas con PTS regulares a24fps; ese control no explica por sí
solo la sensación de lag. V03 prueba gráficos a48fps y copia ligera; imagen fuente a24fps
sin interpolar ni retimar. Voz nativa del hook y mezcla de V02 conservadas.

Se reutiliza oclusión con máscaras locales de persona en257fotogramas nativos. La revisión
muestra que en planos de torso lleno desaparece casi todo el relleno; propuesta V03:
resolver con barrido a relleno frontal tras la entrada en esos casos, mantener oclusión
pura en planos con suficiente contraste figura/fondo. Es una adaptación del agente,
pendiente de juicio; no una preferencia nueva atribuida a Ale. El texto del ticket se
ubica bajo las caras hasta el desplazamiento a la máquina; sudadera sobre el estampado,
sin tapar sus ojos/boca. La cobertura exacta y la conservación de audio son comprobaciones
ejecutables en `ecommerce-andromeda/v03/verify.py`. Alcance:38,33s disponibles;06provisional.

## Ecommerce Andrómeda V01 rechazada · animación y voz nativa · 2026-10-14

Ale rechaza la V01: subtítulos feos, animación escasa y poca variedad frente a las
referencias. Pide rehacer con mayor elaboración, manteniendo su corrección anterior de
altura para Meta. La revisión de posición no bastaba para satisfacer la dirección.
Aplicar a V02: coreografía por función, jerarquías y construcciones contrastadas con
secuencias de referencia; conservar V01 como versión rechazada, no como base aprobada.

También señala desincronización de «Más anuncios. Más.» en el hook y pide conservar la
voz nativa del clip. V01 había seguido el brief de entrega: voz externa colocada a1,970s
y ambiente de otro clip. La instrucción directa más reciente sustituye ese criterio.
V02 debe recuperar audio nativo0–130frames del hook, retirar el stem azul externo y la
cama provisional de ese mismo tramo, conservando el narrador original. Verificar que el
render no introduce desfase; no certificar lipsync perceptivo a partir de correlación.

### Aplicación V02 · pendiente de veredicto

V02 renderizada: 40 elementos de coreografía (no40frases nuevas), variación de
Regular/Bold, entradas dirigidas, máscara, impacto y relevo de repetición; anclas por
plano y jerarquías compactas. No se atribuye a Ale aprobación de estas alternativas.
La prueba de audio verifica260000samples del hook contra el original (error máximo
1,19e-7 de escala completa por cuantización) y cero desfase en6ventanas de la mezcla
exportada. Se añadió `ecommerce-andromeda/v02/study/verify-native-audio.py` como
comprobación ejecutable de origen, silencio de cama provisional y ausencia de voz
externa. La preparación usa índices de muestra, sin desplazar el ambiente posterior.
Regla para el motor: cuando se conserva diálogo nativo, fuente, IN y velocidad deben
compartir el reloj de la imagen; un test de correlación contra una mezcla equivocada
no valida la elección de esa mezcla. Mantener separadas ambas comprobaciones.
Estado artístico: propuesta V02, pendiente de Ale. Alcance38,33s;06provisional.

## Ecommerce Andrómeda V01 · altura para anuncios de Meta · 2026-10-14

Ale: «intenta no meterme la subtitulación tan abajo, intenta centrarla un poquito más
sin tapar partes demasiado demasiado críticas, porque esto va para anuncios de Meta».
Preferencia explícita para esta edición y campañas Meta: zona central, ancla por plano,
priorizar caras y acciones esenciales. No resolver colisiones bajando automáticamente
al pie del vídeo. Aplicación en V01: revisar con guía de interfaz, retirar texto cuando
el gag ocupa todo el espacio y documentar el campo protegido. No es aprobación del
primer diseño ni certificación de todas las ubicaciones de Meta.

## Continuación del motor · relaciones visuales · 2026-10-14

Ale pide «sigue refinando». Se amplía el selector V2 con una transformación relacional
basada en la ventana clientes→empleados de V8, ejecutada en Remotion. La auto-prueba
cambia una jerarquía Bold/contexto pequeño por Regular más equilibrada y descubre un
solapamiento de strings provocado por el obturador; se corrige separando movimiento y
sustitución discreta. Son decisiones propuestas y comprobaciones técnicas del agente,
no nuevas preferencias atribuidas a Ale ni aprobación de la pieza. Alcance: laboratorio,
sin cambios en Birdieballs/Mercadillo. Estado y límites en
`notas/relacion-v2-2026-10-14.md`; siguen pendientes oclusión, integración y transferencia.

## Continuación sustantiva del algoritmo · 2026-10-14

Ale pide seguir desarrollando el algoritmo con más criterio y creatividad. Aplicado en
el selector V2 experimental: función semántica antes de receta, comparación de secuencias
para no repetir énfasis idénticos, geometría persistente de bloque y control de colisiones
de tinta durante movimiento. Se conecta a Remotion y se renderiza un piloto aislado;
no se sustituye Birdieballs V08 ni se interpreta este encargo como aprobación del piloto.

Costes de selección, márgenes, opciones de layout y entrada alternativa son propuestas
del agente. La revisión visual hizo rechazar un sobrepaso concreto; no prohíbe todos los
rebotes. Evidencia y límites en `notas/selector-v2-2026-10-14.md`. La generación autónoma
de gráficos relacionales y la validación editorial completa siguen pendientes.

## Producto autónomo por código · 2026-10-14

Ale pide seguir estudiando/refinando el algoritmo y aclara que AE interesa para nuestro
trabajo, mientras el sistema para clientes debe usar «remote o similar», una herramienta
que la IA maneje sin interfaz. Se interpreta Remotion en el contexto del estudio previo;
no es una petición de exportadores a editores de escritorio. Prioridad: plan editorial
verificable y ejecución programática en Remotion. AE no es una dependencia del producto.

Aplicación técnica: `motor-editor/src/caption-keyframes/reference-v2.ts` separa segundos,
fps fuente y dimensiones de salida; mantiene la velocidad del ajuste medido, permite
muestras fraccionarias para obturador y rechaza entradas que invaden la salida en vez de
comprimirlas automáticamente. Entrada/salida diseñadas se identifican como propuestas.
Seis nuevas pruebas de regresión; primitiva disponible para integrar, **todavía no
seleccionada por el planificador ni usada para sustituir renders anteriores**. No
constituye validación visual de estilo ni estudio nuevo completo del corpus.

## Birdieballs V02 → V03 · 10-10-2026

| Regla | Evidencia del usuario | Aplicación y estado |
|---|---|---|
| Ancla estable | «cansado y luego de dejarte un… sale más arriba» | La primera línea mantiene eje y altura. El bloque crece hacia abajo. Aplicado a la pregunta y a la llegada de la solución. |
| Multilínea compacta | «lo más junto y compacto posible» | Interlínea ligada al tamaño de ambas líneas, no posiciones verticales independientes. Comprobar tinta, acentos, descendentes y efectos en fotogramas reales. |
| Diferencia sutil en segunda línea | «puedes probar… otra tipografía… un mini trazo… un mini sombreado… un color que combine» | **Permiso para explorar, no obligación de cambiar de fuente.** V03 conserva SF Pro y prueba crema oliva con trazo y sombra verdes discretos. Tratamiento concreto pendiente de valoración. |
| Motion con acción | «muy dinámico… no… una bola ahí parada cinco segundos» | Rechazo a la sensación de objeto inmóvil. No convertir “cinco segundos” en una medición: la escena V02 duraba 2,62 s y aun así se percibía estática. Usar acciones y cambios de escala ligados a la voz; evitar oscilación ornamental. |
| Fondo producido | «no… un verde ahí plano… un poquito texturizado» | Material con grano, iluminación y profundidad dentro de la paleta. No reciclar el color o el fondo de otra marca. |
| Desenfoque de movimiento | «me tienes que meter motion blur» | Exposición temporal de objetos desplazándose; el desenfoque gaussiano solo expresa foco y no sustituye el obturador. |
| Actualizar el algoritmo | «todo lo que te voy diciendo lo vas añadiendo al algoritmo» | Guardar evidencia, cambiar reglas/helpers/validación cuando proceda, probar y mostrar una nueva versión. No afirmar entrenamiento del modelo. |

Implementación: `motor-editor/src/style-rules.ts` (compactación y controles), `motion.ts` (obturador), `Composition.tsx` (composición temporal y sombra), `recipes.ts` y `planner.ts` (consumo de reglas). V03 utiliza esos helpers, no una nota desligada del render.

Parámetros propuestos por el agente: separación de 6–8 px a 1080 px más 3 px de margen de efectos, límites de tinta medidos en SF Pro Bold (incluyen tildes y descendentes), advertencia de quietud desde 0,65 s, 8 muestras y obturador de 270°. Son ajustes iniciales, no cifras dictadas o aprobadas por Ale. Los controles detectan candidatos a revisión; no certifican calidad artística.

## Rechazo de V03 y alcance del estudio · 10-10-2026

- **V03 rechazada**: ni la subtitulación ni el motion alcanzan la creatividad, composición y producción de las referencias. Los helpers anteriores solo comprueban propiedades técnicas; sus tests no demuestran fidelidad ni aprobación artística.
- **Montaje de entrada bloqueado por defecto**: si un vídeo viene editado, conservar orden, cortes, duración y sincronía. No inferir autorización para recortar de una petición de postproducción. La EDL de Birdieballs usada en V02/V03 no constituye permiso para siguientes versiones.
- El algoritmo debe explicar decisiones condicionales de posición, tamaño, combinaciones, multilínea, entradas/salidas, fuentes, máscaras, motion y sonido. Una lista de efectos y unos porcentajes globales no satisfacen el encargo.
- Estudiar todas las referencias, incluida BRAUDLABS V8, y mostrar evidencias vinculadas a vídeo/fotograma en la interfaz existente. No contar variantes de una misma pieza como pruebas independientes.
- Separar observado, medido e inferido. No llamar exhaustivo a extraer todos los frames, ejecutar OCR o abrir hojas reducidas. No deducir nombre de SFX por un pico ni tipografía exacta por una caja OCR.
- Prioridad actual: estudio y sistema de decisiones. No generar V04 ni reemplazar versiones anteriores durante este trabajo. El usuario exige profundidad y precisión; no optimizar por el número de tokens.
# 10/10/2026 · Auto-pruebas, brutos y nueva versión Birdieballs

Ale pide extraer patrones técnicos con máxima precisión temporal, realizar auto-pruebas comparadas mano a mano y presentar resultados que el agente haya revisado antes de pedir su veredicto. Aporta seis carpetas de brutos como apoyo para distinguir lo generado/filmado de lo añadido al editar. También autoriza expresamente volver a editar Birdieballs mientras continúa ese estudio; esto sustituye la pausa temporal de V04, sin convertir V03 ni el motor anterior en aprobados. Mantener el encargo de aproximadamente20segundos y el montaje original sin nuevos cortes. El muestreo visual se expresa en frames y tiempos racionales; no prometer observación visual a1ms en fuentes de24/60fps.

## V04 rechazada · cuestionario visual solicitado · 10-10-2026

- Ale rechaza el motion gráfico completo de V04 y el tratamiento del personaje saltando. No conservarlos como dirección aprobada ni limitar la siguiente propuesta a pulirlos.
- Prefiere recuperar SF Pro como primaria. Rechaza la secundaria cursiva escogida; la imagen de «de campos…» es un contraejemplo explícito. No inferir rechazo de toda fuente secundaria posible.
- Subtítulos demasiado lineales; rechaza repetir el mismo recurso de multilínea en dos momentos. Variar construcciones por función y composición, sin inventar preferencias concretas aún no respondidas.
- Pide un cuestionario muy detallado dentro de Cutroom, basado en todas las referencias y los patrones documentados, antes de fijar la próxima dirección.
- Respuestas del cuestionario: `motor-editor/review/data/quiz-answers.json`; decisiones derivadas: `quiz-decisions.json`; brief: `quiz-brief.md`. Estos archivos aparecen cuando Ale responde. No marcar las opciones propuestas como preferencias del usuario.
- Se conserva montaje original, bloque de ~20 s y renders anteriores. Esta tarea crea el cuestionario; no autoriza por sí sola una nueva dirección elegida por el agente.

## Cuestionario entregado · revisión 132

Respuestas conservadas en `birdieballs/v05-direction/quiz-answers-revision-132.json`. Dirección interpretada y mapa en `birdieballs/v05-direction/BRIEF.md` y `direction.json`. Ale prioriza humor expresivo, SF Pro variable, construcciones compactas, la combinación de pagar de V8, subtítulos de V1/V5 y producto explicado por el metraje real. Landing, Churros, V6 REV y LaFabrica quedan fuera de la dirección de este anuncio, sin borrarse del corpus. Prohíbe flechas en gags. Pide ver mapa de estructura, blur bajo/medio y propuestas concretas antes de fijar recursos condicionales. Libertad creativa local explícita no convierte «idk», «no sé» o cinco preguntas vacías en aprobación.

## Cambio explícito de herramienta · V05

Ale indica: «lo tienes que hacer todo en remotion». Esta instrucción sustituye para Birdieballs el requisito anterior de motion en After Effects. Montaje, tipografía, efectos y composición final en Remotion; no portar ni generar proyecto AE.

## Birdieballs V06 · rechazo del cambio cromático de V05

Feedback explícito: «no me gusta ese cambio de color, venga acaba el video». Captura del grupo «de LAGOS,» en verde oscuro sobre arena, aproximadamente15,65s. No convertir relleno crema/acento a tinta oscura al cambiar el plano. Mantener identidad cromática por rótulo; resolver contraste con posición y sombra/trazo discreto. Aplicar a V06 y completar la fuente de38s en Remotion, sin alterar montaje. No supone aprobación global de V05.

## Birdieballs V06 · continuidad de subtítulos · 2026-10-11

Ale: «no está mal», pero «un poco cutre» frente a los originales y «los subtitulos cambian DEMASIADO de posición». Valoración parcial; no aprobación. Comparación focal con V8 guardada en `birdieballs/v06/comparison/audit.json`. Fallos comprobados: traslación instantánea de200px en texto ya visible a12,629s y13,247s; apoyos de la oferta pasan de baseline330 a1680. Mantener una misma ancla por bloque semántico, heredarla al reemplazar palabras y reservar traslados para una razón narrativa/visual documentada. Diferenciar entrada animada de recolocación. Variar jerarquía y construcción sin usar la posición como variación automática. Estas correcciones quedan pendientes de aplicar a la siguiente versión; este pase solo compara y conserva V06.

## Birdieballs V06 · calidad de keyframes · 2026-10-11

Ale añade: «los keyframes, se pueden mejorar muchísimo más». Exige mejorar la coreografía, además de estabilizar posiciones. Revisión de implementación: entradas laterales/verticales comparten180ms y ease-out cuártico; aparición35ms; salidas por opacidad lineal sin trayectoria propia; resorte genérico distinto del ajuste medido deV8. Próxima revisión: separar entrada/lectura/salida, definir curva y duración por función, coordinar las capas de cada grupo y aplicar sobrepaso solo al énfasis que lo justifique. Revisar velocidad, frenada, asentamiento y blur en secuencias reales. El ajusteV8 es una trayectoria observada en palabras concretas, no los keyframes originales ni una regla para todas las entradas. No se ha generado una nueva edición en este pase de feedback.

## Birdieballs V07 · aplicación de continuidad y keyframes · 2026-10-11

Ale autoriza realizar la nueva versión completa y avanzar autónomamente con el material disponible. Aplicado en `birdieballs/v07/`: anclas estables por bloque, mismos colores durante lectura, jerarquías SF Pro y entradas/salidas diferenciadas. El motor reutilizable `motor-editor/src/caption-keyframes/index.ts` es importado por el render; consume el perfil medido de V8, con enlaces diseñados explícitos fuera del intervalo observado. Validación ejecutada: saltos de ancla eliminados en f757/f794, continuidad de posición/velocidad en enlaces, sincronía máscara/contorno y posiciones comunes en producto/paisajes/oferta. Render y comparación visual en `birdieballs/v07/stills/`; detalles en `CAMBIOS.md` y `QA.json`.

Estas comprobaciones corrigen fallos concretos y no certifican equivalencia al estilo completo. La selección contextual de recursos sigue dirigida en `cues.ts`; no presentar V07 como un algoritmo autónomo perfecto. Se conserva V06. V07 queda pendiente del veredicto del usuario.

## Birdieballs V07 y nuevo Mercadillo · 2026-10-11

Ale valora V07 como «Not bad», pero «muy muy simple». Es una valoración parcial, no aprobación global. Aporta el paquete de Mercadillo de agencias para empezar una pieza nueva y añade: «a este le tienes que meter una música que cuadra bastante, editalo flow el de la maquinita».

Aplicado en `mercadillo/v01/`: edición completa en Remotion con referencia focal V5, contraste de jerarquías, títulos persistentes, acumulaciones y máscaras selectivas. Música Funky Martian con cambios de nivel ligados a los gags y al diálogo. Cutroom independiente en el puerto 4318. La selección musical, las curvas y esta dirección son propuestas del agente, pendientes de veredicto.

Aprendizaje de las auto-pruebas: trasladar una máscara de V5 a un actor central tapaba demasiado texto. Se conservó la jerarquía y se retiró la oclusión del gancho. En primerísimo plano y en gags visuales se permite omitir texto para no tapar boca/acción. Esto es una decisión contextual probada en esta pieza, no una nueva preferencia explícita de Ale. Evidencia, descartes y límites en `mercadillo/v01/CAMBIOS.md` y `QA.json`.

## Mercadillo V01 → V02 · sincronía, jerarquía y AE · 2026-10-11

Ale detecta subtítulos que parecen «glitched», jerarquías poco cuidadas y desincronización en la abuela y en «Evidentemente». Precisa la puesta en escena: primero se le indica a la abuela que le hable a ChatGPT; entonces ella empieza a hablar al micro. Pide mejorar subtítulos, efectos y probar After Effects. Cambio de herramienta autorizado para esta revisión; no modificar V01.

Diagnóstico medido: 61 contactos de subtítulos de V01 solapaban 25 ms, con mezcla temporal adicional; las marcas de transcripción anticipaban «Hazme» unos 536 ms e «hiperrealista» unos 686 ms. V02 usa alineación forzada local contra el audio, rangos de capas semiabiertos a 24 fps, texto nativo separado y entradas con blur de movimiento espacial. La actividad del indicador de micro sigue la energía real de la voz. Esto documenta correcciones verificables, no una equivalencia global con el editor de referencia.

### Preferencia local: «criterio visual», 58–59 s

Durante la preparación de V02, Ale dice: «en este frame me molaba más la composición de remotion!». Captura aportada del diseño compacto de V02 en el pecho del actor. Se recupera la composición de V01: SF Pro Bold grande, «criterio» / «visual.» en blanco, baselines 655 / 925, tamaños 211 / 287, relleno detrás del personaje y contorno de 1,65 px delante. Conservar los nuevos tiempos de la voz. Esta preferencia afecta solo a ese bloque y no aprueba el resto de V01 ni V02. Renders anteriores preservados.

## Mercadillo V02 → V03 · pausa cómica, empalmes reales y ritmo · 2026-10-11

Ale pide silencio de música/efectos durante «Ya se lo explico yo, Pelillos», imagen en blanco y negro y regreso de todo después. Señala un primer empalme con sensación de overlap y la voz «ChatGPT, e… [abuela] …videntemente» aún cortada. Pide abuela más rápida/dinámica y más efectos en el conjunto.

Regla derivada del fallo comprobado: corregir tiempos de subtítulos no repara un empalme acústico. Revisar la locución original y cortar entre palabras completas; una alineación forzada puede asignar «Evidentemente» a un fragmento «…videntemente» si se le impone el guion. Verificar fonemas de entrada y salida además de la transcripción. V03 reconstruye la palabra desde la fuente y silencia su ataque prematuro.

Aplicación local: pausa de Pelillos con voz sola, cero música/foley/SFX y blanco y negro. Abuela con esperas recortadas, voz ligeramente acelerada conservando tono, remate físico abreviado y acercamientos crecientes. Más acentos visuales/sonoros según acciones, conservando el diseño preferido de criterio visual. Estos cambios son una propuesta renderizada para revisión, no aprobación global. V01 y V02 se preservan.

## Birdieballs V08 en preparación · 70 % · 2026-10-11

Ale rechaza durante la revisión el oscurecimiento/máscara superior añadido sobre el gráfico del 70 %: «la mascara esa del 70% esa una mierdas». Retirar completamente esa capa; conservar el gráfico original visible y resolver los apoyos en la propia tipografía. Rechazo local explícito, no aprobación del resto de V08. Aplicación: operación `offer-clean.json`, capa OFERTA - contraste suave desactivada; siguiente máster debe renderizarse de nuevo.

## Birdieballs V08 · reedición completa en After Effects · 2026-10-11

Ale pide explícitamente volver a editar Birdieballs en After Effects. Esta instrucción sustituye, para la V08 actual, la anterior obligación de usar solo Remotion. Se conserva la dirección del cuestionario132 y el montaje de2278frames. Texto/keyframes/gráficos/matte nativos en AE; 16 acentos sonoros sobre música y voz originales. Diseño y ejecución en birdieballs/v08/ae, con todas las operaciones y parches registrados.

La revisión corrige márgenes del cierre, repeticiones de subrayado y el texto sobre la bola del primerísimo plano. La máscara superior del70% permanece retirada por el rechazo explícito del usuario; no reactivarla al regenerar. QA valida2278frames, sincronía de audio a0ms en seis ventanas, cero fuentes/medios ausentes y reproducción funcional sin frames descartados. No equivale a escucha independiente ni aprobación artística. V08 queda entregada en Cutroom4317 para veredicto.

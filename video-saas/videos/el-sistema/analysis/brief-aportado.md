# Encargo: la película de producto de El Sistema

Este documento es todo el contexto que tienes. Lo ha preparado otra sesión que ha leído el producto por dentro. Lo que doy por comprobado lo está; lo que no pude comprobar lo digo al final.

Carpeta raíz: `/Users/alejandrorubiocamarero/Desktop/El director/`. Todas las rutas de abajo son relativas a ella.

## Qué hay que hacer

Un vídeo de producto estilo SaaS para **El Sistema**: unos 90 segundos, 16:9, con locución en castellano. Es la pieza con la que alguien que no conoce el producto tiene que entenderlo y quererlo. El listón es el de las películas de lanzamiento del mejor software (el registro de Linear, Raycast o Arc): la interfaz real como protagonista, tipografía con aplomo, un cursor que lleva el ojo, cortes clavados a la voz y ni un segundo de relleno.

Lo ve gente que hace anuncios para su marca o para clientes: dueños de ecommerce, media buyers, agencias, freelance. Ya ha probado a generar anuncios con IA y le salen inconsistentes, o depende de creadores y editores que tardan y cuestan. Llega en frío y sin el vocabulario del producto.

Alejandro, el dueño del producto, ha dicho qué tiene que quedar, en este orden de importancia:

1. **El pipeline creativo.** Lo sencillo que es darle tu idea y que el sistema la traduzca en visuales con la calidad que buscas.
2. **Que por dentro hay mucho más de lo que parece.** En sus palabras: «que entiendan que realmente la estructura interna que hay es mucho más compleja de lo que parece, de ahí que esté adaptado para hablarle y que genere». La sencillez de fuera existe porque dentro trabaja un proceso de producción entero.
3. **El pipeline de edición.** Cómo monta esos vídeos para dejarlos listos para publicar.
4. **Ideas y reversiones.** Cómo el propio sistema sugiere ideas y saca nuevas versiones del anuncio hasta dar con conceptos ganadores.

El mensaje, en una frase: **tú le cuentas la idea; del proceso entero, del guion al anuncio montado y a sus versiones, se encarga El Sistema.** Una escena que no empuje esa frase, sobra.

## Qué es El Sistema

Un sistema de producción de creativos publicitarios que vive en una carpeta de tu ordenador y funciona sobre Claude Code. Le hablas con tus palabras, en la terminal o en su dashboard local, y produce la pieza de punta a punta con tus propias cuentas de generación. No es una herramienta que rellenas: es un operador con criterio, que interpreta, produce, se corrige antes de enseñarte nada y aprende de lo que le dices.

Todo lo que sigue es comportamiento real del producto, al nivel de lo que se le cuenta a un cliente. Es tu inventario de verdades: puedes enseñar cualquiera de ellas, y no debes afirmar nada que no esté aquí.

**Lo que pasa por dentro cuando le das una idea (el pipeline creativo):**

1. Lee quién eres: tu negocio, tu marca, tus productos, tus referencias, y lo que ya ha aprendido de ti.
2. Interpreta la idea, la reformula en una o dos frases y te la confirma. Pregunta solo lo imprescindible y pide referencias.
3. Trabaja sobre tu guion: una línea, una escena. Cuenta la duración de cada escena antes de generar.
4. Si la pieza admite varias direcciones, te presenta un abanico de conceptos (título, logline y por qué) y eliges.
5. Parte de referencias reales, cada una con su papel (modelo, producto, estética), y deja bloqueados estilo, personaje y escenario.
6. Genera la imagen base de la primera escena. Aprobada, pasa a ser el frame ancla del que salen todas las demás.
7. Estima el coste antes de cada generación.
8. Elige el modelo que toca en cada escena (imagen: Nano Banana Pro y Soul; vídeo: Seedance, con voz nativa, y Kling) y le escribe prompts muy detallados.
9. Te enseña el moodboard: el mapa completo, escena por escena, antes de animar nada.
10. Tú apruebas las imágenes y solo entonces anima. El vídeo es lo caro, así que se itera en imagen.
11. Contrasta cada resultado con su listón de calidad y corrige la causa antes de enseñártelo. Un vídeo nunca se regenera sin decírtelo.
12. Deja el dossier de la pieza: cada generación con su prompt exacto, modelo, parámetros, referencias, veredicto y coste. Actualiza el registro y la wiki sin que lo pidas.

**Cómo edita (el pipeline de edición):** transcribe en local para tener cada palabra con su tiempo; corta donde el personaje deja de hablar y no hace nada relevante; pone todos los clips a la misma velocidad (1,1× o 1,2×, igual en toda la pieza); subtitula palabra por palabra con cuatro estilos de la casa (pop, karaoke, clean, impact) ajustados a tu marca en color, resalte, tipografía, posición y tamaño; cierra con tu end card, si la tienes; verifica antes de enseñar. Entrega el vídeo final, los subtítulos y el proyecto editable. El motor es un proyecto de Remotion.

**Cómo propone ideas y reversiones:** abanicos de concepto; ganchos; la regla de «un anuncio, un dolor» y baterías de ángulos en paralelo; variaciones de un ganador cambiando gancho, enfoque o formato; producción en lote (`/lote`); y espionaje de la competencia: encuentra en la biblioteca de anuncios de Meta el anuncio del competidor que está rindiendo, lo transcribe, entiende por qué funciona y te propone uno nuevo para tu marca, nunca una copia. Una regla de la casa que el vídeo debe respetar: el guion y la oferta son del cliente; el sistema propone, itera y versiona. No lo cuentes como «te escribe los anuncios de la nada».

**También es verdad, como detalle de fondo:** cinco comandos (`/creativo`, `/lote`, `/espia`, `/feedback`, `/estado`) que son atajos, no requisito; aprende de cada «esto no» y no lo repite; los créditos invertidos se ven pieza a pieza; el dashboard solo escucha en tu ordenador y la transcripción es local; si una herramienta no está conectada lo dice y nunca simula una generación.

## La voz manda

Alejandro graba la locución en ElevenLabs y te la deja en `video-saas/locucion.mp3` (o `.wav`). El texto está en `video-saas/GUION-LOCUCION.md` y, bloque a bloque, en la tabla de abajo. Habla El Sistema en primera persona, como habla el producto en su propia interfaz.

- **La grabación es la verdad, no el guion.** Transcribe lo que de verdad se dice (puede haber retocado frases o quitado un bloque) y construye sobre eso. Si falta un bloque, se cae su escena.
- **La voz es el reloj.** La duración de cada escena y cada revelación salen de los tiempos reales de las palabras: lo que la voz nombra aparece en la palabra que lo nombra. Si una escena necesita aire, sepáralo entre frases; no estires ni aceleres la voz, y no la sustituyas por otra sintetizada.
- **Tiempos por palabra:** transcripción local con un modelo multilingüe en español. El ejemplo de las skills usa `small.en`, que es solo inglés y aquí no sirve. Hay `whisper` instalado. Comprueba la transcripción contra el guion antes de fiarte de los tiempos.
- **Si el archivo aún no está cuando empieces:** avanza todo lo que no depende de él (sistema de diseño, storyboard con duraciones estimadas a unas 2,6 palabras por segundo, material, bocetos) y espera la grabación antes de cerrar tiempos y construir. No generes una voz provisional.
- **Música y efectos:** una base contenida y con pulso por debajo de la voz, sobria, sin épica; sube un punto al entrar en la inmersión y al volver a la superficie. Efectos pocos y causales (un clic, un paso de escena). La voz siempre por encima.
- **Subtítulos:** no los quemes en el máster; el texto diseñado en pantalla lleva las palabras clave y el vídeo tiene que entenderse sin sonido. Entrega un `.srt` aparte.

## Bloque a bloque

La columna central es lo que la pantalla tiene que demostrar: el contenido es obligatorio, el diseño y el movimiento son tuyos.

| # | La voz dice | La pantalla tiene que demostrar | De dónde sale |
|---|---|---|---|
| 01 | Si tus anuncios con IA no salen como los imaginas, el problema no es la herramienta. Es el proceso. | El dolor que ya conoce: el mismo personaje que cambia de cara de un plano a otro, tomas casi buenas, intentos tirados. «Es el proceso» cae como tipografía. | Descartes reales (ver Material). Sin logos ni interfaces de otras herramientas. |
| 02 | Yo soy ese proceso. Soy El Sistema. | El logotipo tal como es en el producto. | Cabecera del dashboard. |
| 03 | Por fuera soy así de simple: me cuentas tu idea, con tus palabras. | La pantalla de inicio real, casi vacía. El cursor llega, hace clic en la barra y se escribe una sola frase: el encargo de la pieza protagonista. | Vista de inicio del dashboard. |
| 04 | Por dentro, pasa todo esto. | Empieza la inmersión: la cámara atraviesa la barra de texto hacia dentro. | Ver «La inmersión». |
| 05 | Entiendo lo que quieres, y te lo confirmo antes de gastar un solo crédito. | El sistema reformula la idea en dos líneas y espera el sí. El coste estimado aparece antes de generar nada. | Estilos de conversación del dashboard. |
| 06 | Convierto tu guion en escenas. | Las líneas del guion se separan en escenas numeradas, cada una con su duración. | Guion real de la pieza protagonista. |
| 07 | Dejo fijos a tu personaje y a tu producto, para que sean los mismos en todos los planos. | Referencias que entran cada una con su papel; un frame ancla del que cuelgan las escenas; misma cara y mismo producto plano tras plano. | `ancla.png` y `frames/` de la pieza; las tres ranuras reales de «Crear una pieza». |
| 08 | Elijo el modelo que mejor resuelve cada escena, y le escribo cada prompt al detalle. | Cada escena se enruta a su modelo. Los prompts se ven largos y densos, pero no se leen. | Nombres de modelo de la sección anterior, en texto. |
| 09 | Te enseño el mapa completo. Tú apruebas, y entonces animo. | El moodboard con todos los fotogramas; un clic de aprobación y cobran vida como clips reales. | `frames/` y `entrega/*.mp4` de la pieza. |
| 10 | Y lo reviso todo contra el listón de calidad. Solo te enseño lo que ya está a la altura de tu marca. | Un control por el que no pasa todo: tomas que se quedan dentro y se repiten, y solo la buena sube. | Descartes reales de la misma pieza, si los hay. |
| 11 | Todo eso, para que tú solo tengas que escribir una frase. | Vuelta a la superficie: la frase del principio y, a su lado, el resultado terminado. Un instante de quietud. | Clip o montaje final de la pieza. |
| 12 | Después, lo monto. Corto los silencios, igualo el ritmo y subtitulo palabra por palabra, con el estilo de tu marca. | Una línea de tiempo con los clips reales: los silencios desaparecen, los clips se igualan, los subtítulos entran palabra a palabra y cambian de estilo y de color de marca. | Los cuatro estilos reales de `Subtitulos.tsx`; finales y `.srt` de `edicion-final/`. |
| 13 | Listo para publicar. | La pieza final en vertical, y su estado avanzando por los nombres reales del registro hasta «publicado». | Estados de `registro.md`. |
| 14 | Y no me quedo en un anuncio. Te propongo ideas, y de cada pieza saco nuevas versiones: otro gancho, otro ángulo, otro formato. | De una pieza salen ramas: tarjetas de concepto (título, logline, por qué) y versiones que cambian una sola cosa cada vez. Una rama puede nacer de «Espiar a la competencia». | Vista de espiar; la variedad de formatos del escaparate; el AD3 tiene versiones reales de la V1 a la V8. |
| 15 | Hasta encontrar el concepto que gana. | Una versión queda marcada como ganadora y se multiplica en lote. Sin cifras de rendimiento. | — |
| 16 | Tú me cuentas la idea. Del proceso me encargo yo. | La barra de texto otra vez, sola. Ahora se intuye debajo toda la estructura. | — |
| 17 | El Sistema. | El logotipo y, si la hay, la llamada a la acción. | — |

**Una pieza protagonista de principio a fin.** Los bloques 03 a 13 siguen a una sola pieza real, de la frase al vídeo publicado: es lo que convierte la explicación en una demostración. Elígela tú viendo el material, con este criterio: que tenga rastro completo en su dossier (fotogramas, clips y montaje), que se entienda sin sonido, y que tenga entre cuatro y seis escenas con el mismo personaje o producto repetido. La frase que se escribe en el bloque 03 es el encargo de esa pieza, redactado como lo diría un cliente.

**El cierre.** El CTA no está decidido. Si Alejandro no lo ha dado, cierra con el logotipo solo y deja preparado el hueco de una línea debajo. No inventes URL, precio ni oferta.

## La inmersión: sencillo por fuera, una productora entera por dentro

Los bloques 04 a 11 son la escena que decide la película. En unos treinta segundos el espectador tiene que pensar «ahí dentro hay muchísimo», y a la vez entender que nada de eso es problema suyo.

En el producto real, mientras trabaja, la interfaz solo muestra una línea: «El Sistema está trabajando…». La inmersión es lo que pasa detrás de esa línea.

- **Contraste de densidad.** La superficie está casi vacía: una barra de texto y mucho negro. El interior es denso, con capas, etapas, ramas y bucles, pero ordenado: una máquina, no un caos.
- **La pantalla enseña más de lo que la voz nombra.** La voz nombra seis cosas; alrededor se ve el resto de la lista de arriba (la identidad que se lee, la memoria, las referencias por papel, el coste estimado, los reintentos, el dossier que se va escribiendo). Esa diferencia es exactamente lo que comunica «más complejo de lo que parece».
- **Un solo viaje de cámara**, no seis diapositivas. Los fotogramas y clips reales de la pieza protagonista viajan por la estructura como lo que se está fabricando, para que la complejidad siempre esté al servicio de un resultado que se ve.
- **La profundidad se siente, no se lee.** Los nombres de etapa y de herramienta se pueden leer. El contenido del método no: ni prompts legibles, ni plantillas, ni criterios de calidad, ni parámetros. Los prompts aparecen como textura (se ve que son largos y precisos, no qué dicen). La razón: el método es lo que se vende, y un vídeo público que lo deje leer lo regala.
- **La vuelta a la superficie es el premio.** Deja un instante de quietud antes de enseñar el resultado junto a la frase.

## Identidad visual

El vídeo tiene que parecer el producto cobrando vida. Estos son los valores reales del dashboard:

- Fondo `#0A0A0B`, texto `#EDEDEA`, texto secundario `#98958D`, un solo acento ámbar `#F2B800` (texto sobre ámbar `#141200`), verde de estado `#7ddb9a`, filete `rgba(255,255,255,.09)`.
- Paneles de cristal: degradado `linear-gradient(160deg, rgba(255,255,255,.045), rgba(255,255,255,.012))`, desenfoque de fondo de 22 px con saturación al 160 %, brillo interior de 1 px, radios de 16 a 18 px y píldoras de 20 px.
- Tipografía Helvetica Neue con mucho contraste de peso: saludo en 200 con el nombre en negrita, etiquetas pequeñas en mayúsculas, peso 800 y tracking abierto.
- Logotipo: «EL SISTEMA» en peso 800 con tracking de 0,24 em, «EL» en color de texto y «SISTEMA» en ámbar.

El ámbar se usa poco y significa algo: lo activo, lo aprobado, lo que gana. Negro, silencio y aire alrededor.

Ninguno de los estilos de serie del flujo es negro con cristal y ámbar. Parte del tipográfico que mejor lleve un fondo negro con un único acento (`broadside` es el más cercano) y remézclalo con estos valores. La interfaz que aparece dentro de los planos sigue al dashboard real, no al estilo de serie.

Lo que lo estropearía: rejillas de iconos de stock, el look «IA» de degradados morados, formas 3D flotando, emojis, diapositivas de viñetas, pantallas inventadas.

## Material real y dónde está

**La interfaz.** `sistema-ale/plataforma/dashboard/public/index.html` es un solo archivo con el CSS dentro, y es la fuente de verdad: reutiliza su marcado y sus estilos tal cual en las composiciones, así la interfaz es exacta y se puede animar. Vistas que existen: inicio («¡Buenas, [nombre]!», «¿Qué tienes en mente hacer hoy?», barra «Cuéntamelo con tus palabras…» y cuatro tarjetas), Crear una pieza (formatos: UGC hiperrealista, Claymation, Photoshoot, B-roll, Estático y Carta blanca; guion línea a línea; ranuras de referencia Modelo UGC, Producto y Estética), Espiar a la competencia, Mis piezas, Créditos, Conexiones y Mejorar. Los textos de interfaz salen de ese archivo, no de tu imaginación.

Arrancarlo es opcional, solo como referencia visual (`node plataforma/dashboard/server.js` dentro de `sistema-ale/`, puerto 8790). Si lo arrancas, solo navega y captura: no envíes nada por la barra de chat ni pulses «Empezar la pieza», «Espiar» o «Aplicar ahora», porque lanzan sesiones reales que pueden gastar créditos o reescribir el propio dashboard.

Dos cosas que ya comprobé de esas vistas: «Mis piezas» abre un «camino» por pieza que lee carpetas `avatar/` y `rondas/`, y ningún dossier las tiene, así que con datos reales sale vacío (si quieres esa pantalla, reconstruye el componente real con fotogramas reales). Y la tabla de piezas enseña costes reales en créditos y una fila de un tercero: deja solo las filas del escaparate propio y avisa en el plan de que se ven costes reales, por si Alejandro prefiere ocultarlos.

**Los subtítulos.** `sistema-ale/plataforma/remotion/app/src/Subtitulos.tsx` tiene los cuatro estilos reales. Léelo para reproducirlos fielmente en la escena de edición.

**Las piezas propias** (todo en `sistema-ale/cliente/creativos/`). Son el escaparate de la casa y se pueden enseñar. Los siete clips que medí son verticales, 1080×1920 a 24 fps (el croché, 1076×1928), de 4 a 7 segundos:

| Dossier | Qué es | Qué tiene |
|---|---|---|
| `2026-09-22-km11-lluvia/` | Zapatilla, cine nocturno | `entrega/`: 5 clips, `ancla.png`, `BRIEF-EDITOR.txt` |
| `2026-09-22-croche-gato/` | Snack de gato, stop-motion de lana | `entrega/`: 5 clips; `montajes-referencia/`: montaje de 16 s con voz |
| `2026-09-22-denim-trucker/` | Moda: prueba de prenda y macros de tejido | `entrega/`: 5 clips, `ancla.png`; `descartados/` |
| `2026-09-21-escaparate-web/` | Cosmética (testimonio), creatina (producto), moda (una prenda, cinco personas) | `entrega/01-cosmetica`, `02-creatina` (con `descartados/`), `04-moda`; `montajes-referencia/00-MONTADO-15s.mp4` |
| `2026-09-12-ad1-churros-cocina/` | Anuncio con avatar | `entrega/`: una veintena de clips; `edicion-final/`: final, `.srt`, proyectos de Remotion y After Effects, hoja de revisión |
| `2026-09-12-ad2-ia-cara/` | Anuncio con avatar | `edicion-final/`: el final y las versiones V2 a V5, con sus `.srt` |
| `2026-09-16-ad3-pipeline-autonomo/` | Anuncio con avatar, montado por el pipeline | `edicion-final/`: versiones V1 a V8, `.srt`, `Revisar.html` |

Casi todas las `entrega/` traen un `BRIEF-EDITOR.txt` (en moda se llama `BRIEF-EDICION.txt`) que dice qué hace cada clip; léelo antes de mirar vídeo. Los anuncios con avatar llevan claims y precios propios: úsalos sin sonido y sin sus cierres.

Para el bloque 01, en `2026-09-12-ad1-churros-cocina/entrega/` hay clips llamados `02-avatar-bueno`, `03-avatar-cambiado` y `04a/b/c-otra-cocinera`. Por el nombre, se rodaron para enseñar la inconsistencia; compruébalo.

**Casi todo el material está en iCloud, no en el disco.** El escritorio se sincroniza con iCloud y más del 80 % de los vídeos e imágenes son marcadores sin datos. Leer uno bloquea hasta que se descarga: `ffmpeg` y `ffprobe` se me quedaron colgados, y `brctl download` no trajo un clip de 7 MB en un minuto con la red funcionando. Antes de tocar un archivo, mira con `ls -lO` si pone `dataless`; pídelo con `brctl download <ruta>` y espera a que desaparezca la marca. Si no baja, dile a Alejandro qué carpetas tiene que descargar desde Finder («Descargar ahora») y sigue con lo demás. Copia dentro del proyecto todo lo que uses, para que el render no dependa de iCloud. Hay 40 GB libres.

## Lo que queda fuera

- **El método.** `sistema-ale/base/` y `sistema-school/m.pack` son la propiedad intelectual del producto. No los necesitas: no los abras, no los cites y no los enseñes. Lo mismo para el texto de los prompts de las piezas (`prompts-*.txt`, `generaciones.md`): nunca legibles en pantalla.
- **La clave.** `CLAVE-METODO-SCHOOL.txt` y `GUIA-INSTALACION-SCHOOL.txt` contienen la clave del método. No los abras.
- **Material de terceros.** La carpeta `generations/` de la raíz y el dossier `2026-09-24-la-maquina/` son trabajos para clientes y leads. Fuera, salvo que Alejandro diga otra cosa.
- **Personas reales.** Las fotos y vídeos de referencia (`referencias/` de cada dossier, `seedance-videoclip/refs/`, `cliente/referencias/`) pueden ser de personas reales. Solo aparece material generado.
- **Nada inventado.** Ni métricas, ni ROAS, ni testimonios, ni logos de clientes, ni cifras de usuarios, ni pantallas o funciones que no existan. Los nombres de modelos y herramientas van en texto, sin logotipos ajenos.
- **Sin gasto.** No lances generaciones de imagen, vídeo ni voz: todo lo que hace falta ya existe. Si crees que falta un plano generado, propónlo con su coste y espera respuesta.
- **Solo lectura.** No modifiques nada dentro de `sistema-ale/` ni de `sistema-school/`.

## Cómo trabajar

Usa `video-saas/` como directorio de trabajo; el proyecto queda en `videos/el-sistema/`.

Entra por `/hyperframes`. La ruta es `product-launch-video`: un producto que se promociona, con brief y guion, sin web pública que capturar. Antes de componer nada carga `motion-doctrine`, que es la ley de movimiento de la casa y manda sobre la guía genérica: la película tiene que sentirse como un único movimiento de cámara. `oversized-cursor` para las escenas de interfaz y `cut-the-curve` y `seam-craft` para las costuras. El viaje hacia dentro y la vuelta a la superficie piden los dos vectores de profundidad que esa doctrina reserva.

La petición ya viene formada, así que no hay ronda de propuestas. Estas son las respuestas a lo que te preguntaría la capa de intención; no vuelvas a preguntarlas:

- **Vender o enseñar:** vender, usando como material la interfaz real y las piezas reales.
- **Mensaje:** tú le cuentas la idea; del proceso entero se encarga El Sistema.
- **Ángulo:** sencillo por fuera, una productora entera por dentro.
- **Público:** quien hace anuncios para su marca o para clientes y ya ha probado la IA.
- **Duración:** la fija la locución; cuenta con unos 90 segundos. Si pasa de 100, recorta aire, no voz.
- **Destino y formato:** web y YouTube, 1920×1080.
- **Idioma:** castellano de España.
- **Locución:** sí, aportada como archivo, texto literal.
- **Captura:** sin captura web; los valores de marca son los de «Identidad visual».
- **Storyboard:** sí. **Flujo:** automatización.

Alejandro prefiere pocas paradas y no que le pregunten dos veces lo mismo. Enseña el plan una vez, con la pieza protagonista que propones y por qué, y dos o tres fotogramas clave ya con el estilo (el de la inmersión entre ellos). Un «dale» o un «lanza» es un sí. Después no pares hasta el preview final. Las únicas preguntas que le corresponden son el CTA, si no lo ha dado, y cualquier cosa que implique gasto.

## Qué entregar

- El MP4 final, con su ruta y su duración real, y el `.srt`.
- La hoja de contactos con los identificadores de cada plano, para poder pedir cambios plano a plano.
- Un informe corto en castellano que separe con claridad: lo que decidiste tú y por qué; lo que comprobaste (lint, check, verificación de costuras, transcripción contra guion) y con qué resultado; y lo que no pudiste hacer o diste por supuesto (archivos que no bajaron de iCloud, material que no llegaste a ver).

Antes de darlo por terminado, pásale estas pruebas: en cualquier segundo que pares hay algo con sentido en movimiento; sin sonido se entiende la historia; todo lo que se afirma en pantalla está en el inventario de verdades de arriba y se enseña con interfaz o material real; ningún plano es una lista de viñetas; y a los tres segundos de entrar en la inmersión ya se nota que ahí dentro hay muchísimo.

## Lo que no pude comprobar

No llegué a ver ningún vídeo ni fotograma, por lo de iCloud: lo que digo de cada pieza sale de sus documentos y de los nombres de archivo, así que la calidad y la elección del material las juzgas tú. Tampoco comprobé cómo adopta el flujo una locución ya grabada en lugar de sintetizarla; si su paso de audio solo sintetiza, registra el archivo como pista de narración y escribe tú los tiempos en el formato que espera el resto del flujo.

# Ecommerce Andrómeda · C01 (Claude) · decisiones y estado

Pieza paralela e independiente de la serie V01–V05 de Codex (`ecommerce-andromeda/`, no
tocada). Encargo de Ale a esta sesión: «quiero que los subtítulos sean avanzados
dopamínicos, usando bastantes recursos, estético, acorde al vídeo, mantén el audio nativo
de los clips (incluso el del hook)». Prueba de 0–38,333 s (920 f, 1080×1920, 24 fps) sobre
el material entregado. **No es el anuncio final**: el plano 06 es PROVISIONAL, faltan 07–15
y la música.

## Qué viene de Ale y qué es propuesta mía

| Origen | Decisión |
|---|---|
| Ale, a esta sesión | Subtítulos ricos y variados, estéticos y acordes al vídeo. Audio nativo de todos los clips, incluido el hook. |
| Ale, a esta sesión | «este inicio de subtitulación me molaba mucho» → hook = variante A del estudio, sin cambios. Aprobación local del arranque, no del resto. |
| Ale, vía feedback de V01 | Subtítulos más centrados (anuncios de Meta), sin tapar partes críticas. |
| Ale, vía feedback de V03/V04 | Relleno detrás + contorno delante sí, pero sin abusar; gag de la sudadera en blanco y negro **sin subtítulos**. |
| Ale, preferencias previas | SF Pro; entradas por un eje; motion blur real (obturador); anclas estables; nada de flechas en gags; no cambiar el color de un rótulo según el plano. |
| Brief de dirección | Cortes e IN/OUT exactos, narrador desde 0, ticket con offset 0,5 s, 03b íntegro, sin música provisional, 06 provisional. |
| Propuesta de Claude | Todas las construcciones por plano descritas abajo, la paleta del resto de escenas, el serif en «tradicional», los SFX y las ganancias. Pendientes de veredicto. |

## Sistema

- **Tipografía:** SF Pro variable del sistema (pesos 560–900; anchura 62 % solo en el remate
  condensado). New York solo para «tradicional».
- **Color (identidad del hook aprobado):** blanco + azul claro `#A9CDFF` para lectura y
  énfasis. Azul BRAUD `#2F5BFF` solo como tinta impresa sobre un objeto (persiana).
  Contraste resuelto con posición y sombra suave, sin cajas negras ni tinta oscura.
- **Movimiento:** cada palabra entra con su sonido (alineación forzada local), por un eje;
  obturador real de 180° con 8 submuestras solo mientras algo se mueve; sobrepaso
  amortiguado reservado a palabras de énfasis. La geometría de cada frase se reserva desde
  el primer fotograma: las palabras nuevas no recolocan las anteriores.
- **Anclas:** una por plano o bloque semántico, elegida sobre fotogramas reales con rejilla;
  la mayoría en la franja central (y≈450–1050) de la guía de Meta.

## Plano a plano

| Tramo | Construcción | Por qué |
|---|---|---|
| 0–130 Hook | Frases grandes detrás de las dos cabezas (matte de persona con Vision), contorno fino delante, acentos azul claro; susurro nativo «más / anuncios.» y «más.» pequeño y tembloroso en el hombro del azul | Variante A elegida por Ale. El acercamiento final al miedo queda limpio |
| 130–190 Ventanilla | Rail a la izquierda sobre su chaqueta; «tradicional» en serif | La empleada baja la persiana (acción causal): el texto se aparta |
| 190–237 Persiana | «es la misma / MIERDA / de siempre» impreso en la persiana cerrada, en su perspectiva (homografía medida) y siguiendo la panorámica (correlación de fase subpíxel) | La persiana cerrada es el remate; el texto se trata como un cartel normal del mundo |
| 237–282 Banco | «días» / «y días» grandes a la derecha; la segunda línea se vence hacia él cuando se desploma | Los estados de espera son el chiste; el texto acompaña sin taparlos |
| 282–350 Mostrador | Columna derecha; «piezas.» en énfasis | Cara, mano y tarjeta pequeña libres para la reacción |
| 350–444 Ticket | Columna derecha estable durante el barrido: «Quieres / testear», «un nuevo / ángulo» (la palabra se inclina 13° con arco de transportador), «semanas» con barra de progreso que casi no avanza, «para ver / el fruto / de eso» | Sin texto sobre cara, tarjeta, estampado, mano que pulsa, ranura ni papel. Sale antes de la reacción |
| 450–552 Apagados | Lista vertical entre las cabezas; «CAÍDO» cae con gravedad, rebota y queda sobre el canto de las pantallas; se apaga con la última pantalla (f537); «los ads antiguos» se apaga antes del corte | Causalidad física: objetos con peso y el mismo apagado eléctrico |
| 552–610 Repetir | Rail arriba a la izquierda y remate condensado «OTRA / PUTA / VEZ.» en columna; quieto mientras mira a cámara | Condensada reservada a un remate; la mirada remata |
| 610–679 Sudadera | Rail en la franja de los cordones; «tu problema» seleccionado con tiradores | Prepara la relación |
| 691–739 Gag | **Blanco y negro, sin subtítulos** | Instrucción de Ale para V04, aplicada aquí |
| 739–782 Solución | Recuerda «tu problema» y la ventana de selección cierra y reabre con «la solución» (separación de tiradores medida en V8, `src/data/v8-selector-width.json`) | Relación problema → solución con lo nuevo del algoritmo |
| 782–840 Máquina | Arriba a la izquierda: «Instalaremos / en tu tienda» → «esta / maquinita» | Pantalla negra libre: define el hardware |
| 840–920 PROVISIONAL | «le pedirás» → «5» que se posa + «ads» → «para un concepto nuevo» → «te los / dará.» | Portable al 06 definitivo; no se añade contador porque el dashboard final enseñará las cinco versiones |

Descartados con fotogramas: variante A2 (relleno azul saturado) y B (rail en el pecho) del
hook; nota sobre la tarjeta blanca del ticket (ilegible); aparte vertical durante el gag
(eliminado por la instrucción de «sin subtítulos»; queda como `AsideDescartado`).

## Audio

Pistas separadas en `src/data/audio.json`: narrador original desde 0 (sin retiming); hook
con su **audio nativo** (voz generada sincronizada «Más anuncios. Más.» + ambiente, ganancia
0,8), sin el stem externo del azul ni la cama del clip 04; ambiente nativo de 01–06 en su IN
exacto (0,6–0,75; el 06 provisional a 0,42 porque su tono de interfaz llega a −13,9 LUFS);
SFX de subtítulos (4 acentos: «CAÍDO» aterriza, selección, reapertura «la solución», «5»);
música vacía y desactivada. Los clips 01–06 no contienen habla (whisper solo devuelve
alucinaciones típicas de ruido) — comprobado por transcripción, no por escucha.

## Verificado y pendiente

`verify.py` comprueba cortes frente al CSV, audio nativo en sus muestras exactas, narrador sin
retiming, ausencia de voz externa, música desactivada, cobertura de todas las palabras 0–118
(salvo el gag) y el máster (formato, 920 f, desfase de audio 0 en 6 ventanas). Resultado en
`QA.json`: todo OK. Mezcla del máster: −17,4 LUFS integrados, pico −2,4 dBFS, LRA 3,3 LU
(medición, no objetivo de loudness). Revisión visual del render real: hoja de contacto a
2 fps y secuencias fotograma a fotograma de «CAÍDO» (516–539) y de la selección
problema→solución (744–775) en `study/qa/`. En la primera pasada la caída duraba 0,57 s y
tapaba parte de una cara; corregido (g=9 px/f², 90 px, dentro del hueco entre caras).

**No verificado:** escucha humana de la mezcla, lipsync perceptivo del hook nativo y
comportamiento real en los placements de Meta. El 06 sigue siendo provisional (seis tarjetas,
interfaz vieja). 07 debe partir del último fotograma usado de 06. Sin aprobación de Ale más
allá del arranque del hook.

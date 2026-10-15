# Ecommerce Andrómeda · C02 (Claude) · cambios sobre C01

C01 se conserva intacta en `../c01/` (render, código y QA). Esta versión aplica el veredicto
de Ale sobre C01:

> «el hook es la polla, lo de las imágenes también, el resto de subtitulos, la fuente es muy
> pequeña, demasiado a los lados (se cortará en meta) y no es estética»

| Se conserva sin cambios (aprobado) | Se rehace |
|---|---|
| Hook 0–130: frases grandes detrás de las cabezas, acentos azul claro, susurro nativo | Todo el rail pequeño (58–64 px) en columnas pegadas a los bordes |
| Cartel impreso en la persiana «es la misma / MIERDA / de siempre» (190–237) | Serif de «tradicional», columna del ticket, arco de transportador, barra de progreso |
| Remate condensado «OTRA / PUTA / VEZ.» (578–610) | Lista vertical entre cabezas en las pantallas y aparte lateral |
| Gag de la sudadera en B/N sin subtítulos (691–739), audio, montaje | |

## Regla nueva (registrada en `estilo-editor/FEEDBACK-ALE.md`)

Los subtítulos de lectura usan el lenguaje del hook: frase corta en **una línea**, SF Pro 800,
blanco con acento azul claro, palabras que suben con asentamiento y salida que se hunde.
Tamaño grande (≈100–190 px), ajustado automáticamente con la fuente real para que la tinta
quede dentro de **x≈100–980**, y centrado en la zona libre del plano (casi siempre x=540).
Componente: `src/captions/Big.tsx` (`BigLines`, medición con `FontsGate`).

## Plano a plano

| Tramo | C02 |
|---|---|
| 130–190 Ventanilla | «Y sabes que» → «de la forma» → «tradicional», centrado sobre el mostrador (y≈1105), bajo las manos que entregan la carpeta |
| 237–282 Banco | «días» → «y días» (se vence 6° cuando él se desploma) → «para que», centrado sobre sus cabezas (y≈592) |
| 282–350 Mostrador | «el editor» → «o una agencia» → «te entregue» → «las piezas.», centrado en la franja del cuello (y≈962), sin tapar caras, tarjeta ni mano |
| 350–386 Selfie | «Quieres testear» → «un nuevo ángulo» impreso en tinta azul en el margen de la tarjeta, que viaja con ella (seguimiento encadenado). Mismo lenguaje que el cartel de la persiana |
| 386–415 Máquina | «y necesitas» → «semanas», grande y centrado **detrás del ticket**: el papel cae por delante y se ve entero (matte de luminancia del papel y la tarjeta) |
| 415–444 Caída | «para ver» → «el fruto» → «de eso» en la zona libre a la izquierda del papel (centro x≈300, dentro de márgenes), también detrás de su borde |
| 450–552 Apagados | Línea grande sobre el canto de las pantallas (y≈752): «y durante» → «todo ese proceso» → «ya se te han» → «caído» (cae con gravedad y rebota en el canto) → «los ads antiguos», que se apaga como las pantallas cuando ya se ha leído |
| 552–578 Repetir | «y venga a» → «repetir», centrado sobre la pared; luego el remate condensado aprobado |
| 610–679 Sudadera | Contexto «No vengo a hablarte de» + selección grande «tu problema» con tiradores; «ya tienes» → «suficiente» → «con eso» |
| 739–782 Solución | Contexto «Vengo a hablarte de» + la ventana V8 cierra «tu problema» y reabre «la solución» a tamaño grande |
| 782–840 Máquina | «Instalaremos» → «en tu tienda» → «esta maquinita», entre su barbilla y la máquina; pantalla limpia |
| 840–920 PROVISIONAL | «le pedirás» → «5 ads» → «para un concepto» → «nuevo» → «te los dará.» sobre la pantalla, a la izquierda del estampado |

Recursos de oclusión: hook (cabezas) y ticket (papel). Se mantiene dosificado.

## Verificación

`verify.py` → `QA.json`: todo OK. Cortes idénticos al CSV, audio nativo en sus muestras
exactas (hook incluido), narrador sin retiming, música desactivada, cobertura de todas las
palabras 0–118 salvo el gag, B/N 691–739 y máster 1080×1920 / 24 fps / 920 f / AAC 48 kHz con
desfase de audio 0 en 6 ventanas. Mezcla: −17,4 LUFS integrados, pico −2,4 dBFS (medición).
Revisión del render real fotograma a fotograma en `study/qa/`: impresión sobre la tarjeta
durante la panorámica (352–383) y «semanas» detrás del ticket (400–431). En la primera
pasada la impresión se salía por el borde de la tarjeta al girar; corregido con seguimiento
de su franja superior, giro medido (≈4°) y texto más bajo. La franja del mostrador se subió
para no rozar la cabeza del estampado.

No verificado: escucha humana, lipsync perceptivo del hook nativo y placements reales de
Meta. 06 sigue PROVISIONAL; faltan 07–15 y la música.

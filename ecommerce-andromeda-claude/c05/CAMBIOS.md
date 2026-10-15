# Ecommerce Andrómeda · C05 (Claude) · feedback de Ale sobre C04

C04 se conserva intacta en `../c04/` (su registro, en `study/CAMBIOS-C04.md`). Veredicto de Ale sobre C04:
«overall no está mal», con seis correcciones. C05 las aplica sin rehacer el resto:

| Ale sobre C04 | C05 |
|---|---|
| «la paleta de colores de los subtítulos no me gusta una mierda» (marino + azul BRAUD sobre la camiseta de 10 y el mostrador de 15) | Siempre blanco + azul claro. Sobre fondos claros, halo oscuro difuso alrededor de la letra (`ink: 'halo'`), sin caja. |
| «lo de nuevo ángulo… puede quedar más integrado, se ve un poco cutre» | La impresión va anclada al canto superior real de la tarjeta (recta ajustada por fotograma, `src/data/card-edge.json`), con su ángulo (≈6° → 4°), recortada dentro del papel y revelada de izquierda a derecha como una impresora; tinta azul impresa (multiplicar, ligeramente blanda). Ya no se sale de la tarjeta cuando esta sale de cuadro. |
| «el doble mierda, mierda… queda cutre» | Sin eco: «de mierda.» normal. |
| «demasiado pegado al lateral… Meta recorta los bordes… hay unos cuantos más» | Regla ejecutable en `Big.tsx`: cada línea (con la palabra que crece) se recoloca para que su tinta quede dentro de x 100–980, con un colchón de 12 px porque la medida del lienzo subestima la tinta real un 3–4 %. También las etiquetas de los handles, las copias de «creativos» y tres elementos aprobados de C03 que se salían: las frases del hook (tamaño limitado a lo que cabe; las que ya cabían no cambian), el susurro «más anuncios.» y «OTRA PUTA VEZ» (de x≈58–66 a x=104). **Auditoría**: composición `AndromedaC05-audit` (solo rótulos sobre negro) + `study/audit-margins.py` → 0 de 1.718 fotogramas con texto fuera de x 100–980 (antes, 271). |
| «la música no me gusta nada, frena mucho a la mitad» | Toma nueva continua (toma 3, aprobada): groove de 122 BPM sin paradas de compás; el montaje ya no mete silencios, solo un apagado corto con paso bajo en la sudadera. Ver `../music/`. |
| «más salsa… luces en algún momento, un objeto importante que lo reflejaba» | `src/fx/Moments.tsx`: reflejo que cruza el ticket al asomar («semanas»), flash cálido en el corte a la máquina (32,583), halo detrás de «Sí», foco sobre la propuesta elegida en «criterio», destello en las lentes de los proyectores al encenderse (f1621) y flash breve con el remate final. |

Sin cambios: montaje (17 unidades, 2.050 f), audio nativo, narrador, hook, persiana, «OTRA PUTA VEZ», gag en B/N y la
colocación del resto de rótulos (salvo el ajuste automático al margen seguro).

## Verificación (24 fps, 15/10/2026)

- Máster `Andromeda-C05-00-85s-24fps-1080.mp4`: 1080×1920, 24 fps, 2.050 f, AAC 48 kHz, 85,42 s.
  `verify.py`: TOTAL OK (51 comprobaciones, `QA.json`); la comprobación de composiciones admite ya
  `AndromedaC05-audit`, que solo sirve para la auditoría de márgenes.
- Sonoridad: −17,6 LUFS integrados, LRA 3,5, pico real −2,2 dBTP.
- Hojas de fotogramas revisadas: paleta blanco + azul claro, tarjeta integrada (f372), «de mierda.» sin eco,
  márgenes, y los momentos de `Moments.tsx` (reflejo del ticket, flash, halo de «Sí», foco y destello).
- Copia ligera para revisar: `Andromeda-C05-24fps-1080-ligero.mp4` (x264 a dos pasadas, 2.400 kb/s; AAC 160 kb/s).

## Pendiente

- Veredicto de Ale sobre C05.
- Escucha de la mezcla con la música nueva.
- Observaciones visuales del director (UI de 06/07/08, proyección de 12, anticipación de 09).
- 144 y 60 fps se renderizan cuando Ale dé el visto bueno al preview de 24 fps.

## Nota técnica

`~/Documents` está en iCloud con «Optimizar almacenamiento»: macOS desaloja archivos (Chrome de Remotion, mattes) y los
renders parecen colgados a 0 % de CPU mientras se descargan uno a uno. Antes de renderizar:
`find <dir> -type f -flags +dataless -print0 | xargs -0 -P 64 -n 20 cat > /dev/null` sobre `node_modules/.remotion` y `public/`.

Con el disco casi lleno, iCloud deja de bajar y subir. Y si `editor/` está marcado «Mantener descargado», al liberar
espacio macOS intenta volver a bajarlo entero (10,7 GB en 69.000 archivos el 15/10) y ninguna otra descarga avanza:
la marca se quitó ese día. El máster de C05 se renderizó desde una copia en `/private/tmp/claude-render/editor`, que
no se desaloja; al copiar, no excluir `*.mp4`, porque los clips de `public/assets/clips` lo son.

# Ecommerce Andrómeda · C06 (Claude) · «upgrade infernal»

Ale, tras recibir C05 a 24 fps: «Esta versión me la sacas en 144 fps y 1080, luego, haz otra
versión con más efectos aún, haz un upgrade infernal». C05 se entregó a 144 fps (`../c05/`) y se
conserva intacta. C06 parte de C05: montaje (17 unidades, 2.050 f), audio nativo, narrador,
música (toma 3) y rótulos son los mismos. C06 añade dos capas nuevas: una cámara digital
(`src/fx/plan.ts`, `src/fx/camera.ts`) y una capa de efectos (`src/fx/Moments.tsx`, `src/fx/Fx2.tsx`).

## Criterio

- **Vocabulario del editor** (`estilo-editor/notas`, recuento de lo anotado: desenfoque 70, zoom 38,
  flash 38, impacto 36, viñeta 22, barrido 22, onda 18, destello 15, reflejos, partículas, RGB).
  Se usan: golpe de zoom, zoom por escalones, empuje, caída, temblor, barrido con desenfoque, onda
  expansiva, chispas, destello en estrella, fuga de luz, viñeta, parpadeo, grano, rayos detrás del
  sujeto, haces de proyector, B/N selectivo y fallo de imagen.
- **Cada efecto atado a una palabra o una acción** (regla de C05); la densidad sube, pero no hay
  receta por corte.
- **Reglas de Ale que se mantienen:** paleta blanco + azul claro (más luz cálida en flashes y fugas),
  rótulos libres dentro de x 100–980 (la cámara no los mueve), nada de motion sobre la pantalla
  de la maquinita (las ondas de «5» y «Sí» se recortan por encima de ella; las chispas de la
  máquina salen a ras de mostrador; el fallo de 13 solo usa franjas por encima), gag de la
  sudadera en B/N sin subtítulos, sin eco, hook / persiana / «OTRA PUTA VEZ» intactos.

## Cámara

Solo escala uniforme ≥ 1 y traslación; la traslación se acota al rango en que la imagen cubre el
cuadro, así que nunca se ve un borde. Si se mueve deprisa dentro del obturador, el metraje se
dibuja en 8 submuestras (desenfoque de movimiento real). Se mueven con ella el metraje y los
efectos anclados al metraje; el cartel de la persiana y la impresión de la tarjeta aplican la
misma transformación a su geometría, y las máscaras de los textos detrás del sujeto, a su
`mask-size`/`mask-position`. Los rótulos libres quedan fijos.

| f | Palabra / acción | Cámara |
|---|---|---|
| 0–130 | hook (aprobado) | empuje muy suave (3 %) y golpe corto en «Andrómeda» (f56) |
| 210 | «MIERDA» en la persiana | golpe + temblor |
| 246, 263 | «días y días» | dos escalones de zoom hasta el corte |
| 396–422 | «semanas», sale el ticket | empuje hacia la ranura |
| 519 | «se te han caído» | caída (la imagen baja y rebota) |
| 579 / 585 / 593 | «OTRA PUTA VEZ» | tres golpes crecientes + temblor en «vez» |
| 740–781 | «Vengo a hablarte de la solución» | empuje hacia el prota |
| 778–786 | corte a la máquina | barrido (desenfoque horizontal) + golpe al aterrizar |
| 823, 856 | «maquinita», «5» | golpes |
| 1199, 1211–1229 | «Sí», «y escalarás» | golpe; empuje en el primer plano |
| 1250, 1268, 1328 | «Pero eh», la bola cae en la cesta, «mierda» | golpe; golpe + temblor; golpe |
| 1367, 1405, 1461/1473 | «melenas», «kiwi», «meses y meses» | golpes; escalones |
| 1478–1584 | «criterio» | empuje lento |
| 1619, 1747, 2038 | «máquina», «maquinita», «ads.» | golpes (+ temblor final) |

## Efectos

| f | Palabra / acción | Efecto |
|---|---|---|
| 363–386 | «un nuevo ángulo» | B/N selectivo (75 %): la tarjeta conserva su color + reflejo que la cruza |
| 404–417 | «semanas» | reflejo en el ticket (C05) + polvo de papel al asomar |
| 519–527 | «caído los ads» | parpadeo de exposición (se va la luz) |
| 577–610 | «OTRA PUTA VEZ» | viñeta |
| 691–739 | gag en B/N | grano y viñeta de cine mudo |
| 782–800 | la máquina aparece | flash (C05) + onda aplanada sobre el mostrador + chispas laterales |
| 823 | «maquinita» | destello en estrella en el botón naranja |
| 856 | «5» | onda breve alrededor de la cifra |
| 1097–1110 | «espectacular» | centelleo alrededor de la frase |
| 1196–1212 | «Sí» | halo (C05) + onda + chispas hacia arriba |
| 1211–1229 | «y escalarás» | partículas que suben |
| 1268 | la bola cae | polvo en la cesta |
| 1340, 1392 | entran los fundadores | fuga de luz cálida y luego fría |
| 1500–1585 | «criterio» | rayos que nacen detrás de su cabeza (recortados con su holdout) + foco (C05) + viñeta |
| 1621–1681 | se encienden los proyectores | destellos de lente (C05) + haces hasta las imágenes, con motas |
| 1729–1731 | «este mismo ad» | fallo de imagen en franjas (azul claro) |
| 1786 | entra la llamada a la acción | fuga de luz fría |
| 1814–1852 | «pincha abajo» | flechas hacia abajo encendiéndose en cascada |
| 2038 | «ads.» | flash (C05) + onda + chispas |

## Bloque protagonista: dos alternativas

Presentación de la máquina (f740–840), con fotogramas reales de ambas
(`stills/film-C06Block-A`, `stills/film-C06Block-B`):

- **A · aterrizaje:** empuje en «la solución», barrido horizontal en el corte, flash, onda y
  chispas cuando la máquina «aterriza».
- **B · apagón y haz cenital:** la viñeta cierra a casi negro en «la solución» y la máquina aparece
  bajo un haz de luz desde arriba.

Elegida **A**: tiene una acción física clara (aterriza) y la energía que pide «infernal»; B apenas
se lee sobre un decorado tan claro. En la primera prueba de A, el flash y el barrido lavaban
demasiado f782 y las chispas cruzaban la pantalla de la máquina: se bajaron a 48 px / 0,32 y las
chispas pasaron a salir a ras de mostrador, con una onda aplanada sobre la superficie.

## Verificación (24 fps, 15/10/2026)

- Máster `Andromeda-C06-00-85s-24fps-1080.mp4`: 1080×1920, 24 fps, 2.050 f, AAC 48 kHz, 85,42 s
  (render de 126 s). `verify.py`: TOTAL OK (51 comprobaciones, `QA.json`): montaje, audio nativo y
  música idénticos a C05, muestra a muestra.
- Márgenes: auditoría de solo rótulos, 0 de 1.718 fotogramas con tinta fuera de x 100–980
  (`study/audit-margins.json`). La cámara no mueve los rótulos libres.
- Sonoridad: −17,6 LUFS, LRA 3,5, pico real −2,2 dBTP (mezcla de C05 sin cambios).
- Hojas revisadas sobre el máster: barrido y aterrizaje de la máquina, onda de «5» y de «Sí»
  recortadas sobre la pantalla, rayos de «criterio», haces, fallo de 13, flechas y remate. Sin
  bordes dobles visibles por el desenfoque de 8 muestras.
- Copia ligera: `Andromeda-C06-24fps-1080-ligero.mp4` (x264 a dos pasadas, 2.400 kb/s; AAC 160 kb/s).
- Desarrollo y render en la copia local `/private/tmp/claude-render/editor/ecommerce-andromeda-claude/c06`
  (iCloud desaloja archivos de `~/Documents`); sincronizada con esta carpeta tras verificar.

## Pendiente

- Veredicto de Ale sobre C06.
- 144 fps de C06 cuando lo pida (la cámara y los efectos ya se evalúan en tiempo fraccionario).

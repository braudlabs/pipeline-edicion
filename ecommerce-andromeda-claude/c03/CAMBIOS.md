# Ecommerce Andrómeda · C03 (Claude) · corrección puntual + salida a 144 fps

C02 se conserva intacta en `../c02/` (y C01 en `../c01/`). Esta versión responde a:

> «justo cuando abres … lo de tu problema, y se abre como la pantalla, es azul … justo entra
> lo de la sudadera y vuelve a lo de la solución, es como que hay un frame que se sigue
> viendo lo de problema … arregla esa pequeñita cosa rápido y me lo pasas en 144 Hz y en 1080»

## Qué cambia

1. **«tu problema» ya no reaparece al volver del gag.** En C02, al salir del blanco y negro
   (f739) la ventana de selección recuperaba «tu problema» y lo cerraba con la curva V8 antes
   de reabrir «la solución» (≈f740–757). Ahora durante «Vengo a hablarte de» solo está el
   contexto, y la ventana azul se abre limpia con «la solución» al decir «la» (f760), con el
   mismo gesto de selección que la primera vez. Clic de interfaz movido a ese instante.
2. **Salida a 144 fps, 1080×1920.** Composición `AndromedaC03-144`: 5.520 fotogramas
   (144/24 = 6 exacto). El metraje no se interpola: cada fotograma fuente se repite ×6; los
   rótulos, entradas, caídas, seguimientos y el obturador (180° del fotograma de salida) se
   calculan a 144 fps. Todo el diseño sigue definido en fotogramas de 24 fps (`src/lib/time.ts`,
   contexto `TimeScale`); `AndromedaC03` conserva la salida a 24 fps.
3. **Golpe de «caído»** alineado con su caída real en la línea (≈100 ms antes que en C02, que
   usaba la fórmula de la caída de C01).

Sin cambios: montaje, audio nativo, hook, persiana, «OTRA PUTA VEZ», gag en B/N y el resto de
subtítulos de C02.

## Verificación

`verify.py` → `QA.json`. Fotogramas de control a 144 fps en `stills/film/` (tablero
`study/board-144.jpg`): f4434–4620 (= 739–770 a 24 fps) sin «tu problema»; hook enmascarado,
persiana, tarjeta, ticket y «caído» correctos a 144.

Nota: 144 fps es la petición explícita de Ale (pantallas de alta frecuencia). Antes de subirlo
a Meta conviene confirmar el máximo de fps que acepta cada ubicación; la composición a 24 fps
sigue disponible para eso.

## Entregas

| Archivo | Formato | Notas |
|---|---|---|
| `Andromeda-C03-00-38s-144fps-1080.mp4` | 1080×1920, 144 fps, 5.520 f, 56,8 MB | metraje ×6 exacto |
| `Andromeda-C03-144fps-1080-ligero.mp4` | igual, 27,8 MB (2 pasadas, ~5,6 Mb/s) | para el móvil |
| `Andromeda-C03-00-38s-60fps-1080.mp4` | 1080×1920, 60 fps, 2.300 f, 45 MB | metraje en cadencia 3:2 (60/24 = 2,5), cortes en fotograma entero |
| `Andromeda-C03-60fps-1080-ligero.mp4` | igual, 27,6 MB | para el móvil |

Ambos másteres pasan `verify.py` (formato, número de fotogramas y desfase de audio 0 en 6
ventanas). Incidencias de render: a 144 fps con concurrencia 6 el compositor se atascó con un
fotograma HEVC (se resolvió con concurrencia 3, timeout 240 s y caché de 3 GB); el primer
intento de 60 fps en paralelo falló porque el servidor local dejó de servir un stem de audio
durante 20 s; en solitario tardó 95 s.

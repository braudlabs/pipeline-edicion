# AD1 · Churros cocina

Montaje vertical de 70,833 s, 1080 × 1920, 48 fps.

## Edición

- El montaje de imagen se prepara en Remotion; After Effects incorpora la mezcla final de voz, música y efectos. Las intervenciones de la cocinera conservan la voz original de los clips 05 y 14 y su sincronización. El clip 13 usa la versión recomendada sin voz.
- Todos los gráficos y los subtítulos son capas nativas editables de Adobe After Effects 2026. No se reutiliza ninguna animación del AD2.
- La dirección visual parte de la cocina: una comanda que acumula intentos, reloj y moneda con giro 3D, platos giratorios con pruebas de Instagram, recetas que se despliegan y una presentación del precio.
- Los subtítulos entran sólo por el eje Y. Texto de punto, sin cajas que recorten descendentes. Línea base a 1220 px, por debajo de las caras y por encima de la zona inferior reservada para la interfaz.
- Música de Mixkit y efectos de la biblioteca local con procedencia declarada Pixabay; véase `CREDITOS.md`. Las pistas de los vídeos de referencia no se han reutilizado.

## Abrir y editar

Abrir `After-Effects/AD1-Churros-Cocina.aep`. La composición principal es **AD1 - FINAL**. Las composiciones **MG - …** contienen los gráficos; **PLATO - …** contienen las cifras y sus capturas. Los subtítulos están nombrados **SUB número | palabra** en la composición principal. Las cámaras, curvas, trazados y textos permanecen editables.

La carpeta `After-Effects/assets` incluye el montaje base, la mezcla final y todas las imágenes utilizadas. La fuente es **SF Pro Display Bold**, instalada en el equipo de edición; su archivo no se redistribuye en este paquete.

En `Remotion`, ejecutar `npm ci` y `npm run render:base` para reconstruir el montaje sin gráficos. Para cambiar cortes o texto: editar `src/timeline.json` y `src/captions.json`, y adaptar las capas correspondientes en After Effects. El `.srt` conserva la transcripción completa, incluido el cierre que el vídeo presenta como cartel de precio.

## Cifras utilizadas

- @notkurtgodel: 83,3 mil seguidores; 7,7 M de visualizaciones **en un solo reel**.
- @notelliotkay: 13,5 mil seguidores; 4,9 M de visualizaciones **en un solo reel**.
- Las cifras corresponden a las capturas aportadas y revisadas para esta edición. Los seguidores y las visualizaciones no son acumulados ni sumados entre cuentas.
- `50 generaciones` reproduce la frase del narrador; la comanda es una metáfora visual y no introduce un coste inventado.
- Precio del cierre: 39 dólares, conforme al audio. No se añade una periodicidad no indicada.

Fuentes de las pruebas de alcance:

- https://www.instagram.com/notkurtgodel/reel/DTkz_BMiFAo/
- https://www.instagram.com/notelliotkay/reel/DUbkE4cCBWo/

Referencias de estilo analizadas: BRAUDLABS — NI ME HAN PAGADO, LaFabrica V2 P3 y LaFabrica V1. Se estudiaron entradas, giros, cambios de escala, pausas y desenfoque fotograma a fotograma; sus recursos gráficos y su música no forman parte del export.

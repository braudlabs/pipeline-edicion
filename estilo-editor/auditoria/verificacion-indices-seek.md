# Verificación: ¿la extracción antigua por tiempo devolvía el fotograma rotulado?

Fecha: 10/10/2026, 17:25. Hecha por la sesión de Claude al retomar el estudio.

## Por qué

`sheet.py` extraía a resolución nativa con un salto por tiempo (`-ss (n − 0,5)/fps` antes de
`-i`). El 10/10/2026 se cambió a `select=eq(n,N)` porque un salto por tiempo puede devolver
`n − 1`. `METODO.md` pide por eso recomprobar las medidas nativas antiguas antes de tratarlas
como fronteras exactas. Esta nota mide cuánto fallaba de verdad el método antiguo.

## Cómo

Para cada vídeo se eligieron hasta 14 fotogramas repartidos por toda su duración, todos con
cambio claro respecto a sus dos vecinos (para poder distinguir `n` de `n ± 1`). Cada uno se
extrajo con el método antiguo y se comparó, reducido, con los fotogramas `n − 1`, `n` y `n + 1`
de `analysis/frames/<slug>/` (decodificación secuencial, la misma numeración que el lector de
texto y que las hojas densas). Gana el índice con menor diferencia media absoluta.

## Resultado

| vídeo | fps | probados | coincide con n | con n − 1 | con n + 1 |
|---|---|---|---|---|---|
| landing | 60 | 3 | 3 | 0 | 0 |
| v1-pagado | 24 | 14 | 14 | 0 | 0 |
| v2-churros | 24 | 14 | 14 | 0 | 0 |
| v3-ia-cara | 24 | 14 | 14 | 0 | 0 |
| v5-maquina | 29,97 | 14 | 14 | 0 | 0 |
| v6-ads90 | 60 | 14 | 14 | 0 | 0 |
| v6-ads90-rev | 60 | 14 | 14 | 0 | 0 |
| v7-ads90-rev | 60 | 14 | 14 | 0 | 0 |
| lafabrica-v1 | 24 | 14 | 14 | 0 | 0 |
| lafabrica-v2p1 | 24 | 14 | 14 | 0 | 0 |

129 de 129 fotogramas devolvieron el índice correcto. En la landing solo hubo 3 candidatos
porque casi no tiene tramos con tres fotogramas seguidos de cambio fuerte (metraje a ~25 fps
en línea de 60); es la muestra más débil de la tabla.

## Qué implica

- Las medidas nativas hechas antes del cambio (ajustes tipográficos de `fontfit.py`, cajas de
  tinta de `inkbox.py`, colores de `px.py`) no muestran desfase de índice en esta muestra.
  No hace falta repetirlas por este motivo.
- El cambio a `select=eq(n,N)` se mantiene: es exacto por construcción y no depende de que el
  contenedor tenga los tiempos regulares. Cuesta más (decodifica desde el principio en cada
  llamada), lo que se nota en rangos altos de los vídeos largos.
- Lo no cubierto: el método por lotes (`load_full_run`) usaba el mismo salto y devolvía
  fotogramas consecutivos a partir del primero, así que hereda el resultado, pero no se probó
  por separado.

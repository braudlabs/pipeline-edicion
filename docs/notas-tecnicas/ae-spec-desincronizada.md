# La spec de diseño de AE se desincroniza del .aep

> En el pipeline de AE por operaciones, la spec de diseño se desincroniza del .aep; la verdad es el log de operaciones

En los anuncios construidos con el puente local de After Effects (ad3-pipeline y
similares), la spec declarativa de diseño **deja de describir el proyecto real** en cuanto
un paso posterior parchea el `.aep` en vez de regenerar desde la spec. En AD3 pasó con el
refinado de V4, la exportación por partes, la corrección de retenciones y los parches de
V5 y V7: dos capas del bloque de precio solo existían en AE, y varias entradas y salidas
diferían.

**Por qué importa:** construir o portar desde la spec da un vídeo con bloques
descolocados, y el fallo es silencioso — no hay error, solo sale mal.

**Cómo aplicarlo:** la fuente fiable es la secuencia de lotes guardados en `v*/ae/*.json`,
reproducida en orden cronológico. `ad3-pipeline/remotion-mg/scripts/replay-ae.py` lo hace
y contrasta el resultado contra el volcado que devolvió el propio AE. Antes de dar por
buena cualquier spec de diseño, comprobar si hay lotes posteriores que la contradigan.

Detalle completo en `MOTION-GRAPHICS-AE-REMOTION.md` (raíz del repo), enlazado desde
`AGENTS.md`. Ver también [Remotion frente a After Effects](remotion-vs-ae-motion-graphics.md).

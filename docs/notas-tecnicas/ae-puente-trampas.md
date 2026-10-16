# Trampas del puente de After Effects

> Trampas del puente local de After Effects: salida H.264, nombres de plantilla, emparentado, ancla de metraje y espera de render

Cinco fallos del puente `fnf-after-effects-mcp` que no dan error y salen mal en
silencio. Aparecieron en AD4 (creatina) y AD5 (gotita).

- **La plantilla de salida H.264 de AE reescribe el contenedor a 50 fps y recorta
  el audio.** En AD5 dejó la imagen un 4 % rápida y 0,79 s corta. Renderizar
  ProRes («Calidad alta») y transcodificar con ffmpeg, mezclando el wav propio.
- **Los nombres de plantilla llevan espacio duro** (`40 Mbps`). Reteclearlos
  falla con «no es un nombre de plantilla válido»: usar la cadena exacta que
  devuelve `render.list_templates`.
- **`layer.set_parent` recalcula la posición del hijo** para conservar su sitio en
  pantalla, aunque se pase `jump=False`. Si las coordenadas ya son relativas al
  padre, hay que reimponer posición y claves DESPUÉS de emparentar.
- **Un metraje importado queda con el ancla en la esquina.** Con la posición en el
  centro de la comp, el vídeo se va a un cuarto de pantalla. Ponerle ancla en
  `[w/2, h/2]` de su propia fuente.
- **`render.start` agota la espera del puente a los 60 s pero AE sigue
  renderizando.** Vigilar el tamaño del archivo y el recuento de fotogramas en
  vez de relanzar. AE suele entregar un fotograma de más que el tramo pedido:
  recortarlo con `-frames:v`.

**Cómo aplicarlo:** verificar siempre el render con `ffprobe -count_frames`
(fotogramas, fps y duración de audio y vídeo) antes de dar una pieza por buena.
Ver también [La spec de diseño de AE se desincroniza del .aep](ae-spec-desincronizada.md) y [Remotion frente a After Effects](remotion-vs-ae-motion-graphics.md).

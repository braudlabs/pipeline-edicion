# AD3 · Pipeline autónomo · V3 editorial

V3 rehace los cinco bloques de motion con la segunda referencia aportada (552657…) como guía visual. V1 y V2 están guardadas por separado. No se insertan fotogramas, objetos, logos ni audio de las referencias.

46,875 segundos · 1080 × 1920 · 48 fps. Montaje base de tomas a 24 fps, motion nativo a 48 fps. Audio comprimido idéntico al de las versiones anteriores.

## After Effects

Abrir After-Effects/AD3-Pipeline-V3.aep, composición AD3 - FINAL V3. After Effects 2026, sin plugins externos. Tipografías instaladas: Didot, Didot Italic, Helvetica Neue y SF Pro Display. Las fuentes no se redistribuyen.

- Ensamblado: página editorial con tipografía y subrayado, fotografía, trazado de la voz y recorrido de cámara.
- Creatividad: retrato circular → escenas → voz → montaje.
- Consistencia: círculos dibujados que se alinean; retratos de la misma persona en tres tomas.
- Sistemas: una curva conecta cuatro salidas; recorrido horizontal y revelado del conjunto.
- Producción: continuidad de la línea con las piezas producidas.

FOTO V3 contiene las fotografías sustituibles. RETRATO V3 contiene la foto con Tinción nativa; se recorta circularmente en cada instancia. ONDA V3 es un trazado obtenido de la voz. PLIEGO / MUNDO agrupan composiciones semánticas; modificar sus contenidos conserva las animaciones de sus instancias. Las palabras y líneas son nativas, no imágenes generadas. Las claves se encuentran en transformaciones, cámara, máscaras y efectos. El diseño tiene posiciones fijas: revisar composición y saltos de línea al cambiar frases por textos mucho más largos.

## Remotion

Montaje base en Remotion: npm ci; npm run studio; npm run render:base. El render base se guarda en After-Effects/assets/Montaje-AD3.mp4. Mantener la estructura de carpetas al mover la entrega.

## Subtítulos

Las palabras del motion sustituyen a los subtítulos inferiores en esos intervalos. El MP4 ya contiene el texto diseñado; no activar además el SRT, que duplicaría la subtitulación. El SRT conserva el guion completo. El susurro inicial sigue sin subtítulo integrado por el primerísimo primer plano, como en V2.

Diseno contiene los estudios y la lectura de las referencias. Verificacion documenta el alcance real de las comprobaciones. La entrega no implica aprobación estética del usuario.

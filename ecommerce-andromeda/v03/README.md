# Andrómeda V03 · 38,33 segundos disponibles

Feedback: V02 mejora parcialmente, pero se percibe lag y faltan subtítulos. Ale pide reutilizar el recurso de «criterio / visual»: texto sólido detrás del personaje, contorno delante. V03 pendiente de veredicto.

## Cambios y límites

- 119/119 palabras de narración, 55 elementos. Se recuperan entrega de piezas, ticket completo y gag de la sudadera. No se añade una segunda pista de subtítulos simultánea para el susurro nativo.
- SF Pro Bold/Regular. Las frases cortas aparecen completas desde su inicio; movimiento pequeño continuo, sin retrasar legibilidad mediante fade, blur o cascada de cada palabra.
- Gráficos a48fps. Montaje original920frames a24fps preservado en1840frames de salida: cada imagen fuente se mantiene dos fotogramas. No se inventa movimiento intermedio ni se retima la voz.
- Oclusión real por silueta en257frames nativos. Se usa el segmentador local Vision ya empleado en Mercadillo, no se reutilizan sus máscaras sobre este anuncio. La máscara se mantiene bloqueada al mismo fotograma que la imagen.
- Primer pase: sobre los dos cuerpos de un plano cerrado, muchas palabras quedaban enteras en contorno y costaba leer. Segundo pase: en esas composiciones se rellena progresivamente por delante tras la entrada, conservando el gesto de contorno/relleno; en las que cruzan un borde de personaje se mantiene la oclusión pura. Adaptación creativa propuesta, no réplica exacta de todas las decisiones originales.
- Ticket: al comienzo todavía se ven las caras y la fotografía; su caption se mantiene bajo las caras, en el borde inferior de la fotografía, y después pasa a la fascia libre de la máquina. Sudadera: caption sobre la frente del estampado, sin cubrir sus ojos ni boca.
- Audio idéntico a V02 corregida: voz nativa del hook, narrador y ambiente posterior; sin música nueva.
- Último plano06 sigue siendo provisional. No es el anuncio completo.

## Qué se ha comprobado

`study/cadence-diagnosis.json` verifica que V02 tenía PTS regulares a24fps: no se ha demostrado un fallo del reproductor ni fotogramas codificados perdidos. La sensación de lag se aborda con menos espera para leer, curvas más continuas y48fps en el grafismo. La copia720p reduce carga de reproducción; estas medidas necesitan el veredicto del usuario.

`verify.py` comprueba cobertura exacta y orden de119palabras, límites temporales, máscaras, hashes de8fuentes y la mezcla, y formato. `study/verify-render.py` contrasta los IN/OUT de8cortes con las imágenes fuente y comprueba desfase del audio codificado frente a la mezcla. El test de audio no certifica percepción de lipsync. Revisión visual de26frames por pase y secuencias de animación exportadas; no se afirma escucha ni reproducción completa independiente.

## Editables y ejecución

`design.py` produce `choreography.json`; `index.tsx` contiene la composición Remotion; `timeline.json` conserva la base24fps. Los assets anteriores son hard links que no deben sobrescribirse. Las máscaras V03 son propias.

```sh
python3 ecommerce-andromeda/v03/design.py
python3 ecommerce-andromeda/v03/study/prepare-mask-inputs.py
birdieballs/v05/segment ecommerce-andromeda/v03/study/mask-input ecommerce-andromeda/v03/public/assets/masks
node node_modules/typescript/bin/tsc --project ecommerce-andromeda/v03/tsconfig.json
node ecommerce-andromeda/v03/render.mjs --bundle
python3 ecommerce-andromeda/v03/verify.py
python3 ecommerce-andromeda/v03/study/verify-render.py
```

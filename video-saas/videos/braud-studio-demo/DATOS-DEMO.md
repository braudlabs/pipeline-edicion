# Qué es real y qué es demo dentro del dashboard del vídeo

El dashboard que sale en el vídeo es el frontal real de BRAUD Studio v0.7. Desde el Avance 04 se captura en **modo producción** (`/?brand=braud`, sin `dev=1`) y en **tema oscuro**. Su estado lo genera `tools/build-state-v2.py` (caso Creatina). Las capturas las hace `tools/snap.mjs shots-v4.json`. `tools/check-snaps.py` falla si alguna captura usada lleva marcas de desarrollo («DEV», «Explorar el inicio», «DESARROLLO / …»).

## Real (Avance 04)

Viene de la producción del escaparate e-commerce del 21/09/2026, en `~/Desktop/El director/sistema-ale/cliente/creativos/2026-09-21-escaparate-web/`, y del montaje final de Creatina:

- **Anuncio terminado de Creatina.** Es `ad4-creatina/output/Creatina-BRAUDLABS-V1.mp4`. Sale en «listo para publicar».
- **Carrusel de la apertura.** Son anuncios y clips reales de Creatina, Sérum, Moda y PapiCat (proxies).
- **Versiones rechazadas y su motivo.** Son los veredictos reales de la producción:
  - CR-Ax: «Cámara demasiado quieta».
  - CR-Bx: «El bote se queda flotando…».
  - CR-M2x y CR-M3x: «otro recipiente».
  - Packshots bote-1 a bote-3: «Texto deformado». El elegido es bote-r2-1.
- **Casting.** Son 12 candidatos de las rondas r6, r5 y r3.
- **Guion.** Son las frases del brief real. La apertura 1 es el hook real.
- **Estados de la interfaz.** Todos son capturas del frontal:
  - el inicio, el agente vacío, con texto, con la conversación y respondiendo;
  - el dictado («Terminar», «Grabando · 0:00 / 0:01 · El texto aparecerá al terminar», «Transcribiendo…», «Transcribiendo el audio…»);
  - las secciones de Mi marca plegadas.

  Los estados del dictado se generan en el DOM con los mismos pasos que `refreshMic()` de `studio.js`. No hubo grabación real.
- **Animación «pensando».** Es el recurso real `assets/thinking-flow-alpha.webp`, de 101 fotogramas a 40 ms. El barrido de luz del texto es el de `theme.css`, en un ciclo de 6 s. En el vídeo se reproduce fotograma a fotograma.

## Contenido de demo, redactado para el vídeo

- **Conversación del agente.** Son dos mensajes que resumen el encargo; no es un chat real.
- **Aperturas 2 y 3.** Son propuestas redactadas.
- **Etiqueta «Leyendo el contexto de tu marca…».** El componente es el de Studio; el texto lo eligió quien montó la demo.
- **Tecleo de la idea en el bloque 4.** Se dibuja en Remotion encima del campo vacío, con la tipografía y el relleno reales del textarea: 14/22,4 px, relleno de 12 y 14 px, -apple-system, #E8E9EC. El último fotograma tecleado coincide píxel a píxel con la captura real del mismo texto (diferencia 0).
- **Marca.** La marca demo del frontal es BRAUD. Su Mi marca describe la instalación de BRAUD, no una tienda de suplementos. Por eso en el Avance 04 solo salen las secciones plegadas «Productos y oferta» y «Públicos y necesidades», que son genéricas. Falta decidir si se crea una marca demo de suplementos o se usa la de un cliente con permiso.
- **Etiqueta «CODEX» en las respuestas del agente.** Está fija en el frontal (`ecom.js`) y se muestra tal cual.

## Fuera del vídeo por decisión de Ale

- **La sudadera morada del caso Andrómeda** («da pena», 15/10). No aparece como material, ni como referencia, ni en los títulos de escena. Además se priorizan los planos donde no protagoniza. El Avance 04 no usa ese metraje.

## Pendiente

- **Pantallas de Meta (bloques 14–16).** No existen en el frontal. Hay que diseñarlas con los componentes de Studio y dejarlas anotadas como recreación, con métricas reales.
- **Música y efectos.** La pista viene de El Sistema y su licencia no consta. Hay que confirmarla antes de la versión final.
- **Capturas de los bloques 6–21** (idea, guion, casting, escenas, montaje). Hay que repetirlas en modo producción. Las actuales llevan «DEV».

## Estado anterior (Avances 01–03, caso Andrómeda)

Venía de `~/Desktop/El director/sistema-ale/cliente/creativos/2026-10-14-ecommerce-andromeda/` y lo generaba `tools/build-state.py`:

- **Clips.** Eran 27 de Seedance 2.5.
- **Guion.** Era la locución del narrador partida en 17 frases.
- **Casting.** El elegido era `frame-elegido-usuario.png`, con 18 exploraciones de Soul 2.0.
- **Rechazos reales.** Hook v1 y cinco ads v1 y v2.
- **Mi marca.** Salía de la guía comercial y la landing de BRAUD. El hook rate del 50,7 % sobre 4 M de impresiones sale de `crm-braud/dist/ecom/resultados.html`.
- **Coste real.** 43,74 € (2.004,72 créditos).
- **Material de demo.** Las aprobaciones de las escenas 06–15 eran de demo.

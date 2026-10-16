# Qué es real y qué es demo dentro del dashboard del vídeo

## Avance 06 · caso de la maquinita

Ale pidió: «pilla el ad de la maquinita». La pieza de Studio es el anuncio Ecommerce Andrómeda («Andrómeda pide más.»).

**Cómo se capturó.**
- El estado es el del caso Andrómeda: `tools/build-state.py`, copiado en `ui-v1/` y servido en el puerto 8812.
- Las capturas son de `shots-v6*.json`, en modo producción (`/?brand=braud`) y tema oscuro.
- `snap.mjs` avisa si encuentra marcas de desarrollo. Las tomas grandes (17 escenas) no guardan el HTML congelado (`noFreeze`).

### Real

- **La pieza en Studio.** Todo viene del estado real de Andrómeda:
  - la conversación;
  - la intención (objetivo, público, tensión, prueba);
  - los tres ángulos;
  - las cinco primeras frases del guion;
  - las tres aperturas («El problema», «La pregunta», «El contraste»);
  - el papel «El azul»;
  - la escena 08 «Cinco ads», con sus cuatro versiones y estados reales: v1 «Miniaturas estáticas» y v2 «Demo sobre blanco» descartadas, v4 por revisar, v5 «Cinco vídeos» aprobada;
  - el montaje provisional de 85,39 s, con la pista de locución.
- **Planos.** Son clips reales del anuncio (V05–V15b), con proxies 1080p.
- **«Listo para publicar».** Se enseña con el plano real de la pantalla de la máquina con los tres anuncios aprobados (V07b, segundos 1,0–3,1).
  El montaje final (C05) lleva la sudadera detrás de la máquina en todo el tramo de la máquina; recortado, pierde los subtítulos.
- **Coste.** La tarifa es de 16 créditos por segundo, medida en las 30 transacciones reales de Seedance 2.5 de Andrómeda (64, 80, 96 y 144). La escena de 5 s sale a 80 créditos. La tarjeta «Cotización del proveedor» es el marcado real de la app.
- **«Usar apertura».** Es un clic real en el servidor de demo. Aplica «La pregunta» y deja el aviso real «Apertura aplicada. El cuerpo y el cierre se conservan.».
- **Meta, la parte real.** Las filas del Administrador de anuncios son capturas de las campañas de BRAUD (`crm-braud/dist/ecom/img/resultados/`). Sus cifras salen de `resultados.html`:

  | Campaña | Hook rate | Hold rate | Coste por registro |
  | --- | --- | --- | --- |
  | LATAM | 52,92 % | 34,73 % | 0,30 € |
  | España | 47,38 % | 28,61 % | 1,86 € |

- **Aprendizaje de Mi marca.** «Hook rate en nuestras cuentas: 50,7 % sobre 4 M de impresiones».

### Recreación o demo (no existe en el frontal v0.7)

- **Meta conectado.** La fila del Taller dice en realidad «Conexión pendiente». En el vídeo pone «Conectado…» y, después, «Nueva versión subida a tu cuenta…». La lectura del agente y la subida automática no existen todavía. La locución las afirma, y falta que Ale confirme que funcionan en producción.
- **Mensaje del agente sobre el hook** («Este anuncio funciona. Pero el hook se cae…»). Es texto de demo, insertado con el componente real de la conversación.
- **Founders Picks.** La demo no trae selecciones. Se insertan tres trabajos reales de BRAUD con su dato real, usando el marcado real de la página:
  - Lemon · Womanizer: n.º 1 por impresiones;
  - Clay · plastilina: 72,8 % de hold rate;
  - V6 · Black Friday: 62,2 % de hook rate el primer día.
- **Tecleo de la idea.** Se dibuja con la tipografía real del campo. Los estados del dictado son los reales del DOM.

### Sudadera morada (veto de Ale)

Aparece en casi todos los planos y en las miniaturas de la interfaz. Para que no salga:
- los clips van recortados hacia la máquina (`src/data/andromeda.ts`);
- la columna de escenas y la pista de miniaturas del montaje quedan fuera de los recortes;
- el casting (todos los candidatos la llevan) se enseña solo con la ficha de texto del papel.

Quedan miniaturas muy pequeñas en la Dirección de la escena y los retratos del perchero.
`tools/check-purple.py` revisa cada render y falla si un fotograma pasa de 300 px morados (a 640×360).

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

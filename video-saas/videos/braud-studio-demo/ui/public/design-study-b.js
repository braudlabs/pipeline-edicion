// Individual study of supplied references 29–50. Every motion below is proposed, not observed in the PNG.
export const studyB = [
  {
    "id": "7da21de5-4720-4b87-a48c-eff8c08b3434",
    "index": 29,
    "title": "Glassy motion · 13 oct · 08.png",
    "assetId": "b6a19f5a-e724-4e9e-b4d6-eefefc939eea",
    "observations": [
      "Panel casi cuadrado con radio moderado, colocado sobre un fondo negro que conserva grandes áreas sin textura.",
      "Un arco azul grisáceo atraviesa diagonalmente el fondo; la zona tras el panel pierde nitidez, pero mantiene su dirección.",
      "Borde gris de un píxel, esquina superior izquierda iluminada y centro translúcido sin brillo blanco uniforme.",
      "Título blanco en tres líneas alineadas a la izquierda; metadatos muy pequeños en las esquinas y flecha circular separada abajo."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Al entrar, revelar el panel en 240 ms y desplazar el arco solo 12 px. En hover, aumentar el brillo de una esquina sin mover el texto."
    },
    "application": {
      "area": "home",
      "component": "Tarjeta editorial de una idea",
      "reason": "Da protagonismo a una idea nueva sin añadir otro bloque denso de información."
    },
    "recipe": {
      "kind": "panel",
      "variant": "night-editorial-pane",
      "accent": "#88b8c7",
      "background": "#070b0e",
      "radius": "24px",
      "blur": "18px",
      "detail": "Una lámina oscura sobre un arco de luz frío; el titular queda completamente nítido."
    },
    "tradeoff": "El fondo necesita espacio; repetirlo en todas las tarjetas convertiría el estudio en una galería de efectos.",
    "verdict": "probar",
    "why": "La jerarquía editorial encaja con el inicio; la luz se limita a una sola pieza.",
    "demo": "<div class=\"study-b b29\"><div class=\"b-orbit\" aria-hidden=\"true\"></div><article class=\"b-pane\"><header><span>BRAUD / ESTUDIO</span><span>Una idea</span></header><h3>Algo que<br>merece ser<br>contado.</h3><p>El concepto empieza en una conversación.</p><footer><button type=\"button\" class=\"b-round\" data-study-toggle aria-label=\"Cambiar la luz del panel\"><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" aria-hidden=\"true\"><path d=\"M5 12h14m-6-6 6 6-6 6\"/></svg></button><span>Concepto en exploración</span></footer></article></div>"
  },
  {
    "id": "461b1ef3-4ea5-41ef-955c-2180654997dc",
    "index": 30,
    "title": "Glassy motion · 13 oct · 09.png",
    "assetId": "c0a79af5-a0b9-494e-a8dd-58bf25952943",
    "observations": [
      "Lienzo negro puro y una única palabra blanca de gran tamaño cruzando el centro.",
      "Dos volúmenes negros orgánicos se superponen a las letras: uno grande asimétrico y otro casi esférico encima.",
      "La silueta se reconoce por reflejos blancos finos; el interior oscurece y deforma visualmente la palabra.",
      "El contraste se concentra en el texto descubierto; no hay tarjetas ni controles secundarios."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Desplazar una lente orgánica entre dos posiciones al pulsar; el titular no escala. Es una interpretación del volumen estático, no una animación observada."
    },
    "application": {
      "area": "home",
      "component": "Cabecera experimental con lente",
      "reason": "Permite estudiar una identidad más escultórica antes de decidir si merece entrar en el producto."
    },
    "recipe": {
      "kind": "panel",
      "variant": "obsidian-title-lens",
      "accent": "#93a6b8",
      "background": "#030405",
      "radius": "46% 54% 57% 43%",
      "blur": "2px",
      "detail": "Lente oscura y orgánica sobre un título; reflejos de borde separados del relleno."
    },
    "tradeoff": "La oclusión perjudica la lectura y exige recrear refracción para resultar convincente. No debe cruzar mensajes ni controles de trabajo.",
    "verdict": "reservar",
    "why": "Útil como portada experimental; demasiado invasiva para la interfaz diaria.",
    "demo": "<div class=\"study-b b30\"><div class=\"b-sculpture\"><span>BRAUD / EXPLORACIÓN</span><h3>Otra mirada.</h3><div class=\"b-lens\" aria-hidden=\"true\"></div><div class=\"b-pearl\" aria-hidden=\"true\"></div><button type=\"button\" class=\"b-sculpture-action\" data-study-toggle>Mover la lente <svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" aria-hidden=\"true\"><path d=\"M5 12h14m-6-6 6 6-6 6\"/></svg></button></div></div>"
  },
  {
    "id": "1e58bb11-92c3-4e88-a6d1-9832d088a53b",
    "index": 31,
    "title": "Glassy motion · 13 oct · 10.png",
    "assetId": "0159acc5-961e-456d-988b-31301edbf136",
    "observations": [
      "Tres placas verticales oscuras superpuestas, desplazadas horizontalmente con radios discretos.",
      "La palabra blanca de fondo aparece nítida en los extremos y muy desenfocada a través de las placas centrales.",
      "Los cantos laterales reciben líneas blancas estrechas; en la cara frontal aparecen reflejos verticales suaves.",
      "Composición monocroma y metadatos diminutos arriba, sin acentos de color."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Abrir las tres láminas en abanico 16 px al pulsar y volver a apilarlas. El texto de cada tarjeta permanece encima del material y legible."
    },
    "application": {
      "area": "library",
      "component": "Pila de colecciones",
      "reason": "La profundidad sugiere conjuntos de referencias sin llenar la biblioteca de marcos pesados."
    },
    "recipe": {
      "kind": "cards",
      "variant": "stacked-smoked-collections",
      "accent": "#ced8e3",
      "background": "#111316",
      "radius": "20px",
      "blur": "14px",
      "detail": "Tres láminas desplazadas, canto fino y fondo tipográfico difuso."
    },
    "tradeoff": "Si se desenfoca el título real o se exagera el abanico, se pierde la identificación del contenido.",
    "verdict": "sutil",
    "why": "Aprovechar las capas para agrupar; mantener títulos y controles fuera de la refracción.",
    "demo": "<div class=\"study-b b31\"><div class=\"b-stack-word\" aria-hidden=\"true\">Ideas</div><div class=\"b-stack\"><i></i><i></i><article><span>BIBLIOTECA</span><h3>Referencias<br>en mente.</h3><p>Una colección antes de decidir la escena.</p><button type=\"button\" class=\"b-link\" data-study-toggle>Explorar las capas <svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" aria-hidden=\"true\"><path d=\"M5 12h14m-6-6 6 6-6 6\"/></svg></button></article></div></div>"
  },
  {
    "id": "8e552009-9ade-4aa5-a138-a90865ac532a",
    "index": 32,
    "title": "Glassy motion · 13 oct · 11.png",
    "assetId": "1f64568a-96f8-4095-b49f-18901e309420",
    "observations": [
      "Modal oscuro compacto, con un radio muy grande y bastante más aire vertical que horizontal entre pregunta y acciones.",
      "La luz cálida desciende desde el centro superior y se apaga antes del pie.",
      "Dos botones de igual anchura, alineados en una fila inferior; texto centrado y sin iconos.",
      "El borde exterior apenas se diferencia del fondo negro azulado."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Abrir y cerrar una confirmación dentro de la muestra con 180 ms de opacidad y 6 px de desplazamiento; sin escala de texto."
    },
    "application": {
      "area": "settings",
      "component": "Confirmación reversible",
      "reason": "Una pregunta breve y dos salidas claras encajan con archivar una conversación o descartar una preferencia local."
    },
    "recipe": {
      "kind": "modal",
      "variant": "warm-compact-confirmation",
      "accent": "#e4d3bf",
      "background": "#060b12",
      "radius": "38px",
      "blur": "20px",
      "detail": "Luz cálida superior y pie de acciones simétrico, sin doble marco."
    },
    "tradeoff": "Un radio tan grande consume espacio. Las acciones necesitan más contraste que en la referencia para diferenciar la principal.",
    "verdict": "probar",
    "why": "La composición es limpia; se prueba con una decisión reversible y texto corto.",
    "demo": "<div class=\"study-b b32\"><div class=\"b-modal-demo\"><div class=\"b-modal-closed\"><span>AJUSTES / VISTA DE PRUEBA</span><button type=\"button\" class=\"b-open\" data-study-toggle>Revisar una decisión</button></div><section class=\"b-confirm\" aria-label=\"Ejemplo de confirmación\"><p>¿Volvemos a la<br>apariencia anterior?</p><div><button type=\"button\" class=\"b-confirm-neutral\" data-study-toggle>Mantener</button><button type=\"button\" class=\"b-confirm-main\" data-study-toggle>Volver</button></div></section></div></div>"
  },
  {
    "id": "31743e72-0027-46e7-8371-2522a9ae0dd9",
    "index": 33,
    "title": "Glassy motion · 13 oct · 12.png",
    "assetId": "f63a01b5-ee7b-439a-aa35-a2b34449079c",
    "observations": [
      "Tarjeta horizontal de grafito con borde doble: un canto exterior fino y un marco interior más oscuro.",
      "Zona principal amplia, casi vacía, reservada a un gesto manuscrito gris.",
      "El pie tiene un tono ligeramente más oscuro y agrupa un avatar a la izquierda y dos acciones a la derecha.",
      "La acción «Write» es blanca; «Continue» queda gris, conservando la misma altura y radio."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Dar foco al campo hace emerger el borde interior en 160 ms; cambiar de acción mueve una cápsula clara sin desplazar el compositor."
    },
    "application": {
      "area": "conversation",
      "component": "Compositor con pie integrado",
      "reason": "Permite distinguir el lugar donde se escribe de las herramientas sin añadir otra tarjeta flotante."
    },
    "recipe": {
      "kind": "composer",
      "variant": "inset-footer-composer",
      "accent": "#b9d0e8",
      "background": "#202226",
      "radius": "28px",
      "blur": "8px",
      "detail": "Caja de escritura espaciosa, pie hundido y una única acción clara."
    },
    "tradeoff": "El ejemplo original tiene poco contraste en el contenido secundario; el prototipo lo eleva y evita imitar una firma.",
    "verdict": "probar",
    "why": "Separa escritura y acciones con una diferencia de superficie, manteniendo el conjunto recogido.",
    "demo": "<div class=\"study-b b33\"><section class=\"b-compose\"><label for=\"study-b33-input\">La siguiente idea</label><textarea id=\"study-b33-input\" placeholder=\"¿Qué quieres contar?\" rows=\"3\"></textarea><footer><span class=\"b-avatar\">b</span><span>BRAUD · borrador de prueba</span><div class=\"b-options \" role=\"group\" aria-label=\"Opciones de la muestra\"><button type=\"button\" class=\"\" data-study-option=\"0\" aria-pressed=\"true\">Pensar</button><button type=\"button\" class=\"\" data-study-option=\"1\" aria-pressed=\"false\">Redactar</button></div></footer></section></div>"
  },
  {
    "id": "46618067-e038-4c97-bde6-473cb8c9a067",
    "index": 34,
    "title": "Glassy motion · 13 oct · 13.png",
    "assetId": "dace7ade-27b2-48ae-84e6-8868d11e2ebc",
    "observations": [
      "Base negra en forma de cápsula, con una depresión interna que refuerza la sensación de objeto físico.",
      "El control móvil ocupa la mitad derecha y su canto tiene un anillo plateado muy marcado.",
      "Aparecen pequeños destellos cromáticos en dos puntos del anillo; el resto es monocromo.",
      "Flecha central gris de trazo ancho y sombra suave debajo de toda la pieza."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Mover el control a través de su carril al pulsar, con 420 ms y frenada suave; el anillo conserva el grosor durante todo el recorrido."
    },
    "application": {
      "area": "navigation",
      "component": "Paso al siguiente bloque",
      "reason": "La metáfora del carril puede hacer tangible continuar entre Idea y Guion, como alternativa experimental al botón plano."
    },
    "recipe": {
      "kind": "button",
      "variant": "chrome-track-arrow",
      "accent": "#a8c4ff",
      "background": "#1a1c1f",
      "radius": "999px",
      "blur": "0px",
      "detail": "Pastilla negra con control cromado y destellos mínimos en el canto."
    },
    "tradeoff": "Es más pesado que los botones actuales y puede parecer un interruptor. El texto debe explicar que solo cambia una vista.",
    "verdict": "reservar",
    "why": "Interesante como gesto aislado; no conviene sustituir todas las acciones por mecanismos tridimensionales.",
    "demo": "<div class=\"study-b b34\"><div class=\"b-track-demo\"><span>IDEA → GUION</span><div class=\"b-track\"><button type=\"button\" class=\"b-chrome\" data-study-toggle aria-label=\"Probar el recorrido del control\" aria-pressed=\"false\"><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" aria-hidden=\"true\"><path d=\"M5 12h14m-6-6 6 6-6 6\"/></svg></button></div><p>Probar el recorrido. La pieza no cambia.</p></div></div>"
  },
  {
    "id": "298a5f47-2a0a-4de7-9222-4fc6813addcd",
    "index": 35,
    "title": "Glassy motion · 13 oct · 14.png",
    "assetId": "cc197419-a895-4880-8f11-6493a5eb9857",
    "observations": [
      "Cápsula transparente sobre un campo azul petróleo desaturado, más claro abajo que arriba.",
      "El borde inferior es una línea luminosa continua; el superior es más oscuro y ancho.",
      "Selección interna más oscura que la base, con radio completo y un pequeño margen alrededor.",
      "Dos rótulos grandes: el seleccionado blanco y el secundario gris, sin iconos ni divisores."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Deslizar una única selección entre las dos mitades en 320 ms, manteniendo fijo el texto. La luz inferior acompaña el borde exterior, no la opción."
    },
    "application": {
      "area": "navigation",
      "component": "Selector Recientes / Por pieza",
      "reason": "Conserva un contenedor reconocible y un recorrido continuo para organizar conversaciones."
    },
    "recipe": {
      "kind": "tabs",
      "variant": "petrol-inner-selection",
      "accent": "#b9e0eb",
      "background": "linear-gradient(150deg,#14252e,#607e87)",
      "radius": "999px",
      "blur": "16px",
      "detail": "Cápsula de cristal, selección oscura y borde inferior claro."
    },
    "tradeoff": "Se necesita comprobar el contraste del texto inactivo; la referencia lo reduce demasiado.",
    "verdict": "probar",
    "why": "La selección interna encaja con el flow actual sin añadir iconografía.",
    "demo": "<div class=\"study-b b35\"><div class=\"b-petrol\"><span>CONVERSACIONES</span><div class=\"b-petrol-track\"><i aria-hidden=\"true\"></i><div class=\"b-options \" role=\"group\" aria-label=\"Opciones de la muestra\"><button type=\"button\" class=\"\" data-study-option=\"0\" aria-pressed=\"true\">Recientes</button><button type=\"button\" class=\"\" data-study-option=\"1\" aria-pressed=\"false\">Por pieza</button></div></div><p>Una lista. Dos formas de encontrarla.</p></div></div>"
  },
  {
    "id": "dba24196-6847-4bb0-bac3-c4a3422b863b",
    "index": 36,
    "title": "Glassy motion · 13 oct · 15.png",
    "assetId": "97545748-03d5-4a32-888c-8f09a4bf0567",
    "observations": [
      "Control de volumen muy ancho sobre una fotografía de tejido oscuro, piel y cielo gris.",
      "El relleno seleccionado no es opaco: conserva la textura trasera, suavizada por el cristal.",
      "La frontera del nivel es una lente redondeada con borde fino claro y un reflejo azulado en su esquina superior.",
      "Icono y número blancos grandes se sitúan dentro de la zona seleccionada, sin marcas intermedias."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Arrastrar un range cambia de forma continua la anchura del relleno y el reflejo de la lente. El número corresponde al control de la muestra, no a un audio real."
    },
    "application": {
      "area": "studio",
      "component": "Nivel de monitorización en Voces",
      "reason": "Prueba una lectura tangible de un valor continuo sin añadir un panel de ajuste separado."
    },
    "recipe": {
      "kind": "slider",
      "variant": "textile-glass-level",
      "accent": "#b3d5ff",
      "background": "#303b43",
      "radius": "999px",
      "blur": "12px",
      "detail": "Lente móvil sobre una textura abstracta; relleno translúcido y valor legible."
    },
    "tradeoff": "Un slider tan alto no cabe en barras densas. Debe poder usarse con teclado y conservar un valor numérico visible.",
    "verdict": "sutil",
    "why": "Aplicable a un ajuste principal de audio, reducido a una altura razonable.",
    "demo": "<div class=\"study-b b36\"><div class=\"b-textile\" aria-hidden=\"true\"></div><div class=\"b-volume\"><label for=\"study-b36-range\">Nivel de escucha · muestra</label><div class=\"b-volume-track\"><i></i><span>◖ <output data-study-output>52</output></span><input id=\"study-b36-range\" data-study-range type=\"range\" min=\"0\" max=\"100\" value=\"52\" aria-label=\"Nivel de escucha de la muestra\"></div><small>Prueba visual; no modifica el audio.</small></div></div>"
  },
  {
    "id": "ea578987-7f0d-40ce-bb1a-a54b2b9bf265",
    "index": 37,
    "title": "Glassy motion · 13 oct · 16.png",
    "assetId": "03d4c4df-8f92-4b42-90b0-2b7efa01445c",
    "observations": [
      "Barra inferior de iconos con cápsula oscura y botón de búsqueda circular separado a la derecha.",
      "La selección es una lente gruesa que rebasa ligeramente la altura de la barra.",
      "La lente introduce bordes verdes, azules y cálidos; deforma los iconos y parte del texto que atraviesa.",
      "Los elementos seleccionados son azul cian y los demás blancos; icono encima y etiqueta debajo."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Trasladar una lente común entre tres opciones en 440 ms. Probar un leve estiramiento al iniciar; los textos de BRAUD permanecen sin distorsión."
    },
    "application": {
      "area": "navigation",
      "component": "Navegación principal de tres destinos",
      "reason": "La referencia permite probar un recorrido de selección verdaderamente continuo entre Estudio, Biblioteca y Actividad."
    },
    "recipe": {
      "kind": "tabs",
      "variant": "refractive-dock-lens",
      "accent": "#34b9ff",
      "background": "linear-gradient(#4c6c7d,#17242c)",
      "radius": "999px",
      "blur": "6px",
      "detail": "Lente móvil que sobresale del carril y recibe un canto cromático mínimo."
    },
    "tradeoff": "La refracción extrema de la captura dificulta leer. En producto solo usaría el canto y el desplazamiento, sin deformar letras.",
    "verdict": "probar",
    "why": "Es una prueba directa del movimiento líquido pedido, con una versión legible.",
    "demo": "<div class=\"study-b b37\"><nav class=\"b-liquid-nav\" aria-label=\"Navegación de prueba\"><div class=\"b-liquid-bar\"><i></i><div class=\"b-options \" role=\"group\" aria-label=\"Opciones de la muestra\"><button type=\"button\" class=\"\" data-study-option=\"0\" aria-pressed=\"true\"><span>▦</span>Estudio</button><button type=\"button\" class=\"\" data-study-option=\"1\" aria-pressed=\"false\"><span>▧</span>Biblioteca</button><button type=\"button\" class=\"\" data-study-option=\"2\" aria-pressed=\"false\"><span>⌁</span>Actividad</button></div></div><button type=\"button\" class=\"b-search\" data-study-toggle aria-label=\"Iluminar búsqueda de prueba\"><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\"><circle cx=\"10\" cy=\"10\" r=\"6\"/><path d=\"m15 15 5 5\"/></svg></button></nav></div>"
  },
  {
    "id": "b3a84fa0-415b-4b3d-96db-bc8b95fa551c",
    "index": 38,
    "title": "Glassy motion · 13 oct · 17.png",
    "assetId": "49298529-8464-45c3-bc59-75702264db0a",
    "observations": [
      "Menú negro sobre negro, visible por un borde blanco muy fino en la esquina superior izquierda y el lateral.",
      "La opción seleccionada tiene una segunda cápsula interior; el borde inferior izquierdo produce un pequeño halo.",
      "Un check precede al texto activo y ocupa la misma columna que el espacio reservado a las demás opciones.",
      "Las opciones inactivas son extremadamente tenues; el panel se desvanece hacia la derecha."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Deslizar la cápsula verticalmente entre tres filas; el punto de brillo viaja con la selección y se apaga al llegar, en 260 ms."
    },
    "application": {
      "area": "conversation",
      "component": "Menú de intención del mensaje",
      "reason": "Una lista compacta sirve para elegir entre foco, borrador y revisión sin convertir el chat en un panel de ajustes."
    },
    "recipe": {
      "kind": "panel",
      "variant": "edge-lit-intent-menu",
      "accent": "#d1dfed",
      "background": "#030507",
      "radius": "22px",
      "blur": "4px",
      "detail": "Seleccionado con doble canto, check estable y pequeño halo lateral."
    },
    "tradeoff": "El contraste inactivo de la imagen es insuficiente. Debe subirse y no ocultarse el borde derecho cuando el menú contiene texto largo.",
    "verdict": "sutil",
    "why": "La luz de borde aporta calidad con pocos recursos si no sustituye a un estado claro.",
    "demo": "<div class=\"study-b b38\"><section class=\"b-edge-menu\"><span>TRABAJAR CON EL AGENTE</span><div class=\"b-edge-list\"><i></i><div class=\"b-options \" role=\"group\" aria-label=\"Opciones de la muestra\"><button type=\"button\" class=\"\" data-study-option=\"0\" aria-pressed=\"true\"><b>✓</b>Poner foco</button><button type=\"button\" class=\"\" data-study-option=\"1\" aria-pressed=\"false\"><b>✓</b>Redactar mensaje</button><button type=\"button\" class=\"\" data-study-option=\"2\" aria-pressed=\"false\"><b>✓</b>Revisar contexto</button></div></div><p>Selecciona una intención de prueba.</p></section></div>"
  },
  {
    "id": "c9f62eaa-89e0-4559-ab16-b98002b1480e",
    "index": 39,
    "title": "Glassy motion · 13 oct · 18.png",
    "assetId": "bfaa1277-2b16-44f0-b429-50d9b4193331",
    "observations": [
      "Dock oscuro de esquinas muy redondeadas sobre una fotografía de montañas al atardecer.",
      "Botón cuadrado casi negro con relieve suave; dentro hay una marca blanca formada por escalones.",
      "Una notificación roja circular se solapa con su esquina superior derecha y proyecta luz roja sobre el dock.",
      "A la derecha aparece una miniatura de contenido con un control circular de pausa, parcialmente recortada."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Encender o apagar un halo de aviso en 200 ms. El aviso no pulsa continuamente: solo cambia al aparecer un estado nuevo."
    },
    "application": {
      "area": "activity",
      "component": "Indicador de revisión pendiente",
      "reason": "Permite estudiar cómo señalar una tarea que necesita criterio sin hacer parpadear todo el panel."
    },
    "recipe": {
      "kind": "status",
      "variant": "review-beacon-dock",
      "accent": "#ff5b64",
      "background": "#24212c",
      "radius": "30px",
      "blur": "16px",
      "detail": "Aviso localizado que tiñe levemente el borde de un dock compacto."
    },
    "tradeoff": "Rojo transmite urgencia; para una revisión creativa normal conviene azul y reservar rojo para errores reales.",
    "verdict": "sutil",
    "why": "Probar el halo localizado con azul; conservar rojo solo como comparación de intensidad.",
    "demo": "<div class=\"study-b b39\"><div class=\"b-beacon-scene\" aria-hidden=\"true\"></div><div class=\"b-beacon-dock\"><div class=\"b-beacon-symbol\">b<i></i></div><div><span>ACTIVIDAD / MUESTRA</span><h3>Tu criterio,<br>en el momento justo.</h3><button type=\"button\" class=\"b-beacon-action\" data-study-toggle>Probar aviso</button></div></div></div>"
  },
  {
    "id": "93b462e7-f95d-4779-a415-edf952fde98f",
    "index": 40,
    "title": "Glassy motion · 13 oct · 19.png",
    "assetId": "d66c6702-84e1-4f09-bd90-69f074d7df92",
    "observations": [
      "Malla muy densa de símbolos cuadrados, cruces y pequeñas barras sobre fondo negro.",
      "Una banda luminosa diagonal combina violeta, azul eléctrico, cian y blanco.",
      "La intensidad se expresa cambiando brillo y tamaño aparente de los glifos, no con una superficie lisa.",
      "Hay textura de píxel y dispersión de color en el contorno; no aparecen componentes de interfaz."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Desplazar una banda luminosa una sola vez al pulsar y luego detenerla. No hacer ruido animado permanente detrás del texto."
    },
    "application": {
      "area": "conversation",
      "component": "Firma visual de una respuesta en preparación",
      "reason": "Una textura propia puede distinguir la actividad del agente del resto de los estados, siempre subordinada a texto explícito."
    },
    "recipe": {
      "kind": "status",
      "variant": "glyph-wave-signature",
      "accent": "#56d9ff",
      "background": "#050a13",
      "radius": "18px",
      "blur": "0px",
      "detail": "Malla de glifos con una onda de color; la etiqueta de estado queda fuera de la textura."
    },
    "tradeoff": "Una trama tan densa puede generar moiré y fatiga. Debe reducirse a una pequeña zona decorativa, nunca ser el único indicador.",
    "verdict": "reservar",
    "why": "Interesante para explorar identidad del agente; demasiado intensa para uso continuo.",
    "demo": "<div class=\"study-b b40\"><div class=\"b-glyph-demo\"><div class=\"b-glyph-field\" aria-hidden=\"true\"><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span><span>▤</span><span>+</span><span>⊞</span><span>▤</span><span>+</span><span>+</span><span>▤</span><span>⊞</span><span>+</span><span>▤</span><span>+</span><span>+</span><span>⊞</span><span>+</span><span>+</span></div><div class=\"b-glyph-caption\"><span>AGENTE · PRUEBA VISUAL</span><h3>La idea toma forma.</h3><button type=\"button\" class=\"b-glyph-action\" data-study-toggle>Recorrer la trama <svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" aria-hidden=\"true\"><path d=\"M5 12h14m-6-6 6 6-6 6\"/></svg></button></div></div></div>"
  },
  {
    "id": "b7b1b2aa-4e54-4a59-997b-d0fbcf1367ca",
    "index": 41,
    "title": "Glassy motion · 13 oct · 20.png",
    "assetId": "7a6a5e97-2f19-48a0-b866-802044da0612",
    "observations": [
      "Botón azul claro aislado en la esquina inferior de un gran panel oscuro.",
      "La forma es asimétrica: izquierda semicircular y esquina superior derecha más cerrada.",
      "Borde blanco luminoso, relleno azul más saturado en el centro y halo lechoso cerca del perímetro.",
      "Texto negro azulado centrado, de tamaño grande y peso regular; no lleva icono."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Al pulsar, comprimir solo el brillo interior durante 100 ms y devolverlo en 220 ms; mantener el tamaño del rótulo."
    },
    "application": {
      "area": "home",
      "component": "Acción principal de empezar una idea",
      "reason": "Una sola acción con material azul puede dar identidad al inicio manteniendo el resto neutro."
    },
    "recipe": {
      "kind": "button",
      "variant": "blue-gel-create",
      "accent": "#367dff",
      "background": "#10151e",
      "radius": "70px 26px 70px 70px",
      "blur": "0px",
      "detail": "Relleno gel azul, borde blanco difuso y silueta asimétrica."
    },
    "tradeoff": "El halo necesita contraste con el fondo y puede parecer demasiado plástico si se repite en cada botón.",
    "verdict": "probar",
    "why": "Una acción dominante admite este tratamiento; conservar los controles secundarios sobrios.",
    "demo": "<div class=\"study-b b41\"><article class=\"b-gel-panel\"><span>BRAUD / NUEVA PIEZA</span><h3>Todo empieza<br>con una idea.</h3><p>Ensayo del botón principal.</p><button type=\"button\" class=\"b-gel-button\" data-study-toggle>Crear</button></article></div>"
  },
  {
    "id": "9db215d0-2099-4433-b4d9-1e2141b55ad3",
    "index": 42,
    "title": "Glassy motion · 13 oct · 21.png",
    "assetId": "79cdd887-3e04-47f1-ba90-ff473630d9dc",
    "observations": [
      "Seis cápsulas azules superpuestas en una columna, con desplazamiento vertical constante.",
      "La escala va de azul marino casi negro a celeste lechoso, conservando la misma geometría.",
      "Cada pieza tiene un brillo concentrado en la esquina superior derecha y borde inferior suave.",
      "Las muestras se identifican con líneas laterales y códigos de color; no se presentan estados funcionales."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Cambiar entre tres intensidades de azul hace variar la superficie de una misma acción en 240 ms; conservar su forma y texto para comparar solo el material."
    },
    "application": {
      "area": "settings",
      "component": "Escala de acento azul",
      "reason": "Sirve para decidir qué azul funciona en acción principal, selección y fondo, sin confundirlos con estados de negocio."
    },
    "recipe": {
      "kind": "button",
      "variant": "blue-depth-scale",
      "accent": "#3781fc",
      "background": "#05080e",
      "radius": "999px",
      "blur": "0px",
      "detail": "Tres profundidades del mismo azul, manteniendo una luz de esquina común."
    },
    "tradeoff": "La lámina no demuestra que todos los tonos mantengan contraste con cualquier texto. Cada combinación necesita comprobación.",
    "verdict": "probar",
    "why": "La escala permite afinar el azul en claro y oscuro sin rediseñar la marca.",
    "demo": "<div class=\"study-b b42\"><div class=\"b-blue-scale\"><span>UN ACENTO / TRES INTENSIDADES</span><div class=\"b-blue-stack\" aria-hidden=\"true\"><i></i><i></i><i></i></div><div class=\"b-blue-choice\">Continuar la idea</div><div class=\"b-options \" role=\"group\" aria-label=\"Opciones de la muestra\"><button type=\"button\" class=\"\" data-study-option=\"0\" aria-pressed=\"true\">Profundo</button><button type=\"button\" class=\"\" data-study-option=\"1\" aria-pressed=\"false\">BRAUD</button><button type=\"button\" class=\"\" data-study-option=\"2\" aria-pressed=\"false\">Suave</button></div></div></div>"
  },
  {
    "id": "70aa6384-d182-44d1-a8f5-666a5d5687fb",
    "index": 43,
    "title": "Glassy motion · 13 oct · 22.png",
    "assetId": "ce5de3c4-ef9c-406b-b2ed-30be4eca478e",
    "observations": [
      "Doce tarjetas oscuras en retícula de tres columnas, todas con la misma proporción horizontal.",
      "Cada tarjeta lleva una banda vertical azul en el borde izquierdo y un halo exterior del mismo tono.",
      "Las variaciones van de azul marino a cian; títulos blancos, código hexadecimal pequeño a la derecha y descripción debajo.",
      "El encabezado es azul saturado y de gran peso; las frases atribuyen cualidades psicológicas que la imagen no demuestra."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Mover una barra azul exterior entre tres filas de escena en 300 ms. El halo sigue la barra, mientras los títulos permanecen quietos."
    },
    "application": {
      "area": "studio",
      "component": "Indicador de escena seleccionada",
      "reason": "Recupera la banda exterior que Jordi pide, más larga que un punto y sin quitar aire al texto."
    },
    "recipe": {
      "kind": "rail",
      "variant": "blue-exterior-scene-rail",
      "accent": "#367dff",
      "background": "#10151d",
      "radius": "16px",
      "blur": "0px",
      "detail": "Barra azul exterior pegada a la tarjeta, con luz breve y margen interior intacto."
    },
    "tradeoff": "Una colección de doce azules sería difícil de interpretar. Para selección conviene un único azul; no adoptar las promesas psicológicas de la lámina.",
    "verdict": "probar",
    "why": "La geometría de la banda sí resuelve una necesidad concreta del rail de escenas.",
    "demo": "<div class=\"study-b b43\"><div class=\"b-scene-rail\"><span>ESCENAS / SELECCIÓN DE PRUEBA</span><div class=\"b-scene-options\"><i></i><div class=\"b-options \" role=\"group\" aria-label=\"Opciones de la muestra\"><button type=\"button\" class=\"\" data-study-option=\"0\" aria-pressed=\"true\"><span>01</span><strong>Apertura</strong><small>El primer momento</small></button><button type=\"button\" class=\"\" data-study-option=\"1\" aria-pressed=\"false\"><span>02</span><strong>Desarrollo</strong><small>La idea avanza</small></button><button type=\"button\" class=\"\" data-study-option=\"2\" aria-pressed=\"false\"><span>03</span><strong>Cierre</strong><small>Lo que permanece</small></button></div></div></div></div>"
  },
  {
    "id": "7619b5f9-b928-49e1-8362-9d22740fed6f",
    "index": 44,
    "title": "Glassy motion · 13 oct · 23.png",
    "assetId": "603903d4-f011-48c0-ade6-530d08a3e653",
    "observations": [
      "Nueve tarjetas en retícula de tres columnas, con franjas verdes alineadas al borde izquierdo.",
      "Variaciones entre verde saturado, pistacho, menta y verde grisáceo; fondos grafito casi idénticos.",
      "Halos del color de la franja se extienden al fondo negro sin afectar la tipografía blanca.",
      "Títulos y códigos mantienen una jerarquía regular; las asociaciones de personalidad son afirmaciones editoriales, no evidencia de uso."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Comparar tres intensidades de una misma señal de validación; pasar de borde neutro a verde en 180 ms, sin rebote ni confeti."
    },
    "application": {
      "area": "studio",
      "component": "Estado de revisión de una versión",
      "reason": "Explora cómo distinguir una decisión validada del azul reservado a la selección actual."
    },
    "recipe": {
      "kind": "status",
      "variant": "sage-review-status",
      "accent": "#9fd8bc",
      "background": "#101714",
      "radius": "14px",
      "blur": "0px",
      "detail": "Verde salvia en un canto breve y un check; no usar verde como acento general."
    },
    "tradeoff": "El verde no debe significar simultáneamente seleccionado, generado y aprobado. La etiqueta explícita es imprescindible.",
    "verdict": "sutil",
    "why": "Sirve para estudiar una aprobación discreta; el azul sigue siendo el color de navegación.",
    "demo": "<div class=\"study-b b44\"><div class=\"b-sage-demo\"><span>ESTADO VISUAL / EJEMPLO</span><div class=\"b-sage-card\"><i><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" aria-hidden=\"true\"><path d=\"m5 12 4 4L19 6\"/></svg></i><div><h3>Revisión de una versión</h3><p>La decisión siempre lleva una etiqueta.</p></div></div><div class=\"b-options \" role=\"group\" aria-label=\"Opciones de la muestra\"><button type=\"button\" class=\"\" data-study-option=\"0\" aria-pressed=\"true\">Salvia</button><button type=\"button\" class=\"\" data-study-option=\"1\" aria-pressed=\"false\">Menta</button><button type=\"button\" class=\"\" data-study-option=\"2\" aria-pressed=\"false\">Verde</button></div><small>Comparación de color; no aprueba ningún recurso.</small></div></div>"
  },
  {
    "id": "0c83c0a0-2f46-486e-9987-bcdac317747e",
    "index": 45,
    "title": "Glassy motion · 13 oct · 24.png",
    "assetId": "2947f0ad-8a36-4c59-ae7f-648dea782d8d",
    "observations": [
      "Doce colores distribuidos en tarjetas oscuras de igual tamaño; cada una tiene franja y halo propios.",
      "El titular combina turquesa y blanco, mientras la retícula ordena colores cálidos, fríos y neutros sin cambiar geometría.",
      "El título de cada tarjeta es blanco y la descripción más pequeña; no se usan iconos para reforzar la diferencia.",
      "El pie contiene una acción turquesa y una línea decorativa; las asociaciones psicológicas son parte del contenido de la lámina."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Conmutar entre acción, aviso y error cambia color, símbolo y etiqueta al mismo tiempo. La transición no debe animar un cambio de significado por sí sola."
    },
    "application": {
      "area": "activity",
      "component": "Paleta de estados operativos",
      "reason": "Ayuda a delimitar azul de acción, ámbar de atención y rojo de error, sin mezclar los estados de producción."
    },
    "recipe": {
      "kind": "status",
      "variant": "semantic-color-swatch",
      "accent": "#53b9f5",
      "background": "#0c1116",
      "radius": "14px",
      "blur": "0px",
      "detail": "Tres señales semánticas con franja corta, texto y símbolo redundantes."
    },
    "tradeoff": "Un arcoíris por sección saturaría Studio. No trasladar afirmaciones culturales o psicológicas como reglas universales.",
    "verdict": "sutil",
    "why": "Útil como prueba de contraste y consistencia, no como invitación a multiplicar colores.",
    "demo": "<div class=\"study-b b45\"><div class=\"b-semantic\"><span>COLOR CON SIGNIFICADO</span><section class=\"b-semantic-card\"><i aria-hidden=\"true\"></i><div class=\"b-semantic-copy\"><h3>Acción disponible</h3><p>El color acompaña a la etiqueta.</p></div><div class=\"b-semantic-copy b-warning\"><h3>Necesita revisión</h3><p>Un aviso explica qué falta decidir.</p></div><div class=\"b-semantic-copy b-error\"><h3>No se ha completado</h3><p>Un error incluye una salida clara.</p></div></section><div class=\"b-options \" role=\"group\" aria-label=\"Opciones de la muestra\"><button type=\"button\" class=\"\" data-study-option=\"0\" aria-pressed=\"true\">Acción</button><button type=\"button\" class=\"\" data-study-option=\"1\" aria-pressed=\"false\">Aviso</button><button type=\"button\" class=\"\" data-study-option=\"2\" aria-pressed=\"false\">Error</button></div><small>Estados de demostración, sin trabajos reales.</small></div></div>"
  },
  {
    "id": "e9f66b95-ce04-49e7-83ab-52e9b14d2931",
    "index": 46,
    "title": "Glassy motion · 13 oct · 25.png",
    "assetId": "e0baaa05-2649-47c6-9b25-067aa3a30034",
    "observations": [
      "Fondo blanco grisáceo con una retícula de líneas casi invisibles.",
      "Mosaico de cinco por cinco cuadrados de cristal con esquinas redondeadas, separados por juntas muy finas.",
      "Una mancha verde y amarilla continua atraviesa varias piezas; cada cristal la desenfoca de forma distinta.",
      "Los extremos del mosaico se funden con el blanco mientras el centro conserva saturación y profundidad."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Mover la mancha de luz bajo el mosaico 40 px al pulsar, sin animar individualmente 25 baldosas. Conservar quietos títulos y límites."
    },
    "application": {
      "area": "library",
      "component": "Portada de una colección de referencias",
      "reason": "El mosaico puede sugerir diversidad visual y relación entre referencias antes de abrir una colección."
    },
    "recipe": {
      "kind": "cards",
      "variant": "frosted-reference-mosaic",
      "accent": "#7eca57",
      "background": "#f1f4f2",
      "radius": "14px",
      "blur": "12px",
      "detail": "Retícula de vidrio sobre una única mancha de color, adaptada también a azul BRAUD."
    },
    "tradeoff": "El verde de la referencia se aleja del acento actual. Probar la estructura con azul y evitar colocar texto encima del punto más brillante.",
    "verdict": "probar",
    "why": "La lógica de muchas ventanas sobre un mismo fondo encaja con Biblioteca.",
    "demo": "<div class=\"study-b b46\"><div class=\"b-mosaic-copy\"><span>BIBLIOTECA / COLECCIÓN</span><h3>Una idea.<br>Muchas pistas.</h3><button type=\"button\" class=\"b-mosaic-action\" data-study-toggle>Mover la luz <svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" aria-hidden=\"true\"><path d=\"M5 12h14m-6-6 6 6-6 6\"/></svg></button></div><div class=\"b-mosaic\"><i class=\"b-mosaic-light\"></i><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></div>"
  },
  {
    "id": "906f19a2-be19-42f4-aa0d-d808dc60f1a4",
    "index": 47,
    "title": "Glassy motion · 13 oct · 26.png",
    "assetId": "cbaa8d8a-724a-4668-86b0-ea7b3c386512",
    "observations": [
      "Campo azul muy pálido con mucho espacio libre en la mitad superior.",
      "Tres arcos grandes nacen desde abajo y se superponen como cúpulas, cada uno más claro en su borde superior izquierdo.",
      "La textura tiene un grano fino visible y transiciones suaves, sin contornos rígidos.",
      "Nombre azul saturado centrado y una línea pequeña encima; tipografía sans geométrica y ligera."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Elevar suavemente los arcos 10 px al activar el compositor; el fondo se detiene cuando el campo pierde el foco. Sin movimiento perpetuo."
    },
    "application": {
      "area": "home",
      "component": "Entrada luminosa a una conversación",
      "reason": "Crea profundidad en un estado vacío sin tarjetas extra y deja una zona limpia para escribir."
    },
    "recipe": {
      "kind": "composer",
      "variant": "pale-blue-conversation-arcs",
      "accent": "#1766b7",
      "background": "#e8f3ff",
      "radius": "50%",
      "blur": "0px",
      "detail": "Arcos concéntricos de luz azul detrás de un inicio de conversación nítido."
    },
    "tradeoff": "El brillo y el grano deben reducirse para no lavar los bordes del compositor. No cambiaría el wordmark oficial por la tipografía de la referencia.",
    "verdict": "probar",
    "why": "Es la alternativa más cercana a una Home clara y tranquila, con suficiente carácter.",
    "demo": "<div class=\"study-b b47\"><div class=\"b-arc b-arc-one\" aria-hidden=\"true\"></div><div class=\"b-arc b-arc-two\" aria-hidden=\"true\"></div><div class=\"b-arc b-arc-three\" aria-hidden=\"true\"></div><div class=\"b-arc-home\"><span>BRAUD / ESTUDIO</span><h3>¿Qué tienes<br>en mente?</h3><label for=\"study-b47-input\" class=\"b-arc-composer\"><input id=\"study-b47-input\" placeholder=\"Empieza con una idea…\" aria-label=\"Idea de prueba\"><button type=\"button\" class=\"\" data-study-toggle aria-label=\"Probar la profundidad azul\"><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" aria-hidden=\"true\"><path d=\"M5 12h14m-6-6 6 6-6 6\"/></svg></button></label><small>Exploración visual · no envía mensajes</small></div></div>"
  },
  {
    "id": "d7f4b772-f702-4032-8fe9-48cc78e59b1c",
    "index": 48,
    "title": "Glassy motion · 13 oct · 27.png",
    "assetId": "7968a5ad-edde-474b-9cac-633c151e2f2d",
    "observations": [
      "Página casi blanca con una nube azul suave que atraviesa el centro en diagonal.",
      "La nube combina lóbulos claros y zonas más saturadas; no presenta borde, marco ni geometría regular.",
      "Una sola frase negra sans serif aparece en el centro, sin jerarquía adicional.",
      "La gran cantidad de blanco superior e inferior evita que la mancha se convierta en un fondo uniforme."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Al alternar la muestra, desplazar dos lóbulos en direcciones contrarias durante 900 ms. La frase y los controles no se mueven."
    },
    "application": {
      "area": "home",
      "component": "Estado vacío conceptual",
      "reason": "Un campo de luz bajo el texto puede dar vida al primer paso sin introducir una imagen que parezca una escena ya producida."
    },
    "recipe": {
      "kind": "panel",
      "variant": "soft-sans-blue-cloud",
      "accent": "#6ba5ff",
      "background": "#fff",
      "radius": "50%",
      "blur": "34px",
      "detail": "Nube azul difusa, tipografía sans limpia y amplias zonas blancas."
    },
    "tradeoff": "No aporta información por sí sola. La intensidad debe bajar cuando haya contenido o el fondo competiría con la idea.",
    "verdict": "sutil",
    "why": "Útil en vacío y bienvenida; se retira al entrar en trabajo detallado.",
    "demo": "<div class=\"study-b b48\"><i class=\"b-cloud b-cloud-a\" aria-hidden=\"true\"></i><i class=\"b-cloud b-cloud-b\" aria-hidden=\"true\"></i><div class=\"b-cloud-copy\"><span>IDEA / PUNTO DE PARTIDA</span><h3>Antes de producir,<br>algo que decir.</h3><button type=\"button\" class=\"b-cloud-action\" data-study-toggle>Dar aire al concepto <svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" aria-hidden=\"true\"><path d=\"M5 12h14m-6-6 6 6-6 6\"/></svg></button><p>Prueba de atmósfera, sin escenas ni personajes.</p></div></div>"
  },
  {
    "id": "8a2a4af3-8a77-4332-afca-b100b9f23fe4",
    "index": 49,
    "title": "Glassy motion · 13 oct · 28.png",
    "assetId": "ca1446e7-0ab3-4587-b610-7c1f7ab8a15f",
    "observations": [
      "Composición hermana de la nube azul anterior, pero con la masa de color más baja y desplazada a la izquierda.",
      "La frase se sitúa en una franja blanca del tercio superior, dejando la nube como apoyo inferior.",
      "Tipografía serif negra fina, con contraste de trazos y un tono editorial más marcado.",
      "El azul se concentra en dos lóbulos; el extremo derecho y la parte superior quedan casi vacíos."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Cambiar entre presentación sans y serif sin mover el encuadre; usar una disolución breve de color para comparar el tono editorial."
    },
    "application": {
      "area": "home",
      "component": "Titular de concepto con voz editorial",
      "reason": "Explora si el concepto creativo puede diferenciarse de los controles de producción mediante una única tipografía de lectura."
    },
    "recipe": {
      "kind": "panel",
      "variant": "editorial-serif-cloud",
      "accent": "#7eaaff",
      "background": "#fff",
      "radius": "50%",
      "blur": "36px",
      "detail": "Titular serif sobre blanco y mancha azul inferior; controles permanecen sans."
    },
    "tradeoff": "Introduce una segunda familia tipográfica que puede romper la coherencia de la v1. No debe propagarse a botones, cifras ni campos.",
    "verdict": "reservar",
    "why": "Probar solo en una portada de concepto; decidir con Jordi si aporta algo frente a la tipografía actual.",
    "demo": "<div class=\"study-b b49\"><i class=\"b-editorial-cloud\" aria-hidden=\"true\"></i><article class=\"b-editorial\"><span>BRAUD / CONCEPTO</span><h3>La idea merece<br>su espacio.</h3><p>Una intención clara antes de buscar su forma.</p><div class=\"b-options \" role=\"group\" aria-label=\"Opciones de la muestra\"><button type=\"button\" class=\"\" data-study-option=\"0\" aria-pressed=\"true\">Editorial</button><button type=\"button\" class=\"\" data-study-option=\"1\" aria-pressed=\"false\">Estudio</button></div><small>El mismo concepto, dos voces tipográficas.</small></article></div>"
  },
  {
    "id": "8ad31f22-e02f-4bc1-9cf1-6a619225453e",
    "index": 50,
    "title": "Glassy motion · 13 oct · 29.png",
    "assetId": "8aea85e7-1e2c-4af4-9ff3-dea2032f45c2",
    "observations": [
      "Cinta azul ultramar ondulada que recorre verticalmente una página blanca y divide el espacio sin línea recta.",
      "Un lado de la cinta tiene borde definido; el otro se dispersa en una sombra azul con textura granulada.",
      "Título y subtítulo serif azules se sitúan arriba a la derecha, con alineación a la izquierda.",
      "Una línea de metadatos gira noventa grados en el margen izquierdo; el centro conserva grandes vacíos."
    ],
    "motion": {
      "observed": false,
      "description": "PNG estático: permite observar composición, material y luz; no documenta una transición.",
      "proposal": "Desplazar la curva como una sola capa 18 px al activar el panel. Evitar que la cinta atraviese el texto o que simule progreso de una tarea."
    },
    "application": {
      "area": "library",
      "component": "Portada de una colección editorial",
      "reason": "Puede dar a una colección de referencias una cubierta reconocible sin convertirla en una escena ni en una métrica."
    },
    "recipe": {
      "kind": "panel",
      "variant": "ultramarine-editorial-ribbon",
      "accent": "#1546e8",
      "background": "#fff",
      "radius": "50%",
      "blur": "16px",
      "detail": "Cinta curva azul con un canto nítido y sombra difusa; título en un área despejada."
    },
    "tradeoff": "La tipografía serif y el texto girado se alejan del estudio actual. Mantener el giro solo decorativo y repetir el rótulo accesible en horizontal.",
    "verdict": "reservar",
    "why": "Interesante para una cubierta ocasional; no para divisores o barras de desplazamiento del trabajo.",
    "demo": "<div class=\"study-b b50\"><div class=\"b-ribbon\" aria-hidden=\"true\"></div><span class=\"b-ribbon-side\" aria-hidden=\"true\">BRAUD / REFERENCIAS</span><article class=\"b-ribbon-copy\"><span>COLECCIÓN VISUAL</span><h3>Una dirección.</h3><p>Imágenes y referencias<br>para encontrar el tono.</p><button type=\"button\" class=\"b-ribbon-action\" data-study-toggle>Recorrer la cinta <svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\" aria-hidden=\"true\"><path d=\"M5 12h14m-6-6 6 6-6 6\"/></svg></button></article></div>"
  }
];

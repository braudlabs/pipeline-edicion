export const studyC = [
  {
    "id": "webild",
    "index": 1,
    "title": "Webild",
    "url": "https://www.webild.io",
    "sourceStatus": "visual",
    "observations": [
      "El paisaje ocupa el fondo completo; el formulario se concentra en una placa de cristal central.",
      "El campo blanco tiene más opacidad que el marco exterior: la escritura mantiene contraste.",
      "Las miniaturas continúan bajo el compositor, separadas por un único divisor.",
      "Azul reservado al envío y a la acción principal; controles secundarios casi monocromos."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "El foco ilumina la placa; el contenido no flota continuamente."
    },
    "application": {
      "area": "home",
      "component": "Inicio con entrada y proyectos en una misma placa",
      "reason": "Une comenzar y continuar sin multiplicar contenedores."
    },
    "recipe": {
      "kind": "composer",
      "variant": "webild-plane",
      "accent": "#347cff",
      "background": "#dce1e7",
      "radius": "28px",
      "blur": "16px",
      "detail": "Paisaje abstracto CSS, placa común y textarea opaca."
    },
    "tradeoff": "No copiar la prueba social, el paisaje ni las promesas de Webild. Esta prueba usa contenido de ejemplo.",
    "verdict": "probar",
    "why": "Une comenzar y continuar sin multiplicar contenedores.",
    "demo": "<div class=\"sc-webild\"><small>ESTUDIO / BRAUD</small><h3>Una idea.<br>Todo lo que puede ser.</h3><div><textarea aria-label=\"Idea de prueba\" placeholder=\"¿Qué quieres crear?\"></textarea><button data-study-toggle>Continuar ↗</button><footer><span>01 · Campaña</span><span>02 · Producto</span><span>03 · Concepto</span></footer></div></div>"
  },
  {
    "id": "behance-0",
    "index": 6,
    "title": "AI Voice Agent",
    "url": "https://www.behance.net/gallery/254610891/AI-Voice-Agent",
    "sourceStatus": "visual",
    "observations": [
      "El proyecto combina bloques blancos redondeados con placas azul noche de gran contraste.",
      "Un haz vertical y un horizonte curvo concentran la atención en un símbolo pequeño.",
      "Los controles de paso son círculos discretos y el contenido ocupa la mayor parte del espacio.",
      "Los acentos cálidos aparecen como luz, no como color de todo el texto."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "El haz se activa una vez al pulsar; nunca indica que un proceso real ha terminado."
    },
    "application": {
      "area": "activity",
      "component": "Resumen de producción con un foco visual",
      "reason": "Un único punto luminoso puede señalar trabajo activo sin convertir el informe en una colección de indicadores."
    },
    "recipe": {
      "kind": "dashboard",
      "variant": "voice-beam",
      "accent": "#347cff",
      "background": "#080d23",
      "radius": "28px",
      "blur": "16px",
      "detail": "Haz vertical, horizonte y ficha operativa legible."
    },
    "tradeoff": "La referencia es de comunicación por voz. No trasladar estadísticas, valoraciones ni resultados inventados.",
    "verdict": "probar",
    "why": "Un único punto luminoso puede señalar trabajo activo sin convertir el informe en una colección de indicadores.",
    "demo": "<div class=\"sc-voice\"><i></i><small>ACTIVIDAD / VISTA DE PRUEBA</small><div class=\"sc-orbit\">✧</div><h3>El estudio, en marcha.</h3><p>Una vista del trabajo que sigue avanzando.</p><button data-study-toggle>Ver enfoque</button></div>"
  },
  {
    "id": "behance-1",
    "index": 7,
    "title": "Hers — Healthcare App Branding",
    "url": "https://www.behance.net/gallery/245019923/Hers-Healthcare-App-Branding",
    "sourceStatus": "visual",
    "observations": [
      "Fotografía orgánica a sangre y blancos cálidos; el verde procede del producto.",
      "Las cápsulas transparentes superponen una línea fina clara sobre una imagen detallada.",
      "El nombre serif es protagonista; los controles y datos usan una sans pequeña.",
      "El contenido alterna mosaicos de fotografía y producto, no una cuadrícula de tarjetas idénticas."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "La cápsula gana opacidad al foco y revela su intención al pulsar."
    },
    "application": {
      "area": "library",
      "component": "Ficha de referencia con etiqueta flotante",
      "reason": "La referencia visual conserva protagonismo y el uso aprobado queda en una cápsula corta."
    },
    "recipe": {
      "kind": "cards",
      "variant": "hers-capsule",
      "accent": "#60774d",
      "background": "#eff0e9",
      "radius": "28px",
      "blur": "16px",
      "detail": "Cápsula sobre volumen abstracto, sin reutilizar fotografía ajena."
    },
    "tradeoff": "La serif se reserva a esta portada experimental; no sustituye la tipografía de formularios.",
    "verdict": "probar",
    "why": "La referencia visual conserva protagonismo y el uso aprobado queda en una cápsula corta.",
    "demo": "<div class=\"sc-hers\"><div class=\"sc-hers-orb\"></div><small>REFERENCIA / EJEMPLO</small><h3>Materia.<br>Luz. Carácter.</h3><button data-study-toggle><span>Dirección visual<small>Color y textura</small></span><b>＋</b></button></div>"
  },
  {
    "id": "behance-2",
    "index": 8,
    "title": "Notis — Smart AI Workspace",
    "url": "https://www.behance.net/gallery/245890113/Notis-Smart-AI-Workspace-UX-UI-Design",
    "sourceStatus": "visual",
    "observations": [
      "El negro dibuja juntas visibles entre módulos crema con radios amplios.",
      "Fotografía desenfocada y textura de grano conviven con fichas informativas limpias.",
      "Los botones son cápsulas pequeñas; no compiten con los titulares.",
      "La paleta alterna lavanda, azul pálido y melocotón; la retícula mantiene la unidad."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "Entrada corta de los módulos; sin parallax mientras se escribe."
    },
    "application": {
      "area": "home",
      "component": "Mosaico editorial con una pieza dominante",
      "reason": "Da ritmo a inicio con tamaños distintos sin cambiar la escala de los controles."
    },
    "recipe": {
      "kind": "cards",
      "variant": "notis-mosaic",
      "accent": "#347cff",
      "background": "#101211",
      "radius": "28px",
      "blur": "16px",
      "detail": "Juntas oscuras de 5 px, cuatro módulos con ritmo 2:1:1."
    },
    "tradeoff": "Las juntas negras son una dirección experimental fuerte; demasiado contraste en los paneles de edición cansaría.",
    "verdict": "probar",
    "why": "Da ritmo a inicio con tamaños distintos sin cambiar la escala de los controles.",
    "demo": "<div class=\"sc-notis\"><section><small>EN TU ESTUDIO</small><h3>Ideas que<br>toman forma.</h3><button data-study-toggle>Explorar ＋</button></section><section><span>01</span><b>Concepto</b></section><section><span>02</span><b>En producción</b></section><section><span>03</span><b>Biblioteca ↗</b></section></div>"
  },
  {
    "id": "e83b1fff-3f88-49dc-bb2f-34483e9010ed",
    "index": 51,
    "title": "Glassy motion · 13 oct · 30.png",
    "assetId": "24997eea-af9b-40bb-8782-b1793380c3fa",
    "sourceStatus": "visual",
    "observations": [
      "Dos cuadrados concéntricos con radios muy amplios y grosor óptico en el borde.",
      "La placa exterior es más transparente; la interior tiene un velo blanco.",
      "El azul está en el fondo diagonal; el signo central es sólido y oscuro."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "Desplazamiento de 6 px entre capas al enfocar."
    },
    "application": {
      "area": "settings",
      "component": "Identidad de marca en capas",
      "reason": "La marca obtiene presencia con dos planos, sin rodear cada ajuste de una nueva caja."
    },
    "recipe": {
      "kind": "panel",
      "variant": "identity-layers",
      "accent": "#347cff",
      "background": "#bad9ee",
      "radius": "28px",
      "blur": "16px",
      "detail": "Dos capas; 1 px de borde y luz diagonal."
    },
    "tradeoff": "Limitarlo a identidad. Duplicarlo en cada control produciría exceso de marcos.",
    "verdict": "probar",
    "why": "La marca obtiene presencia con dos planos, sin rodear cada ajuste de una nueva caja.",
    "demo": "<div class=\"sc-brand\"><div><div><b>braud<sup>®</sup></b></div></div><button data-study-toggle>Ver identidad ↗</button></div>"
  },
  {
    "id": "ee871289-fb68-4825-a294-abf0fceae530",
    "index": 52,
    "title": "Glassy motion · 13 oct · 31.png",
    "assetId": "50be9667-df43-4054-bc59-49e9884ff12c",
    "sourceStatus": "visual",
    "observations": [
      "Seis tarjetas forman una retícula de tres columnas y dos filas.",
      "Una esfera lavanda grande atraviesa el fondo común y tiñe cada panel de forma distinta.",
      "Los logotipos son negros y centrados; las etiquetas técnicas quedan en las esquinas."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "La selección aclara un panel sin mover los vecinos."
    },
    "application": {
      "area": "library",
      "component": "Colecciones bajo una atmósfera común",
      "reason": "La luz compartida hace que la biblioteca se lea como un sistema, no como seis adornos independientes."
    },
    "recipe": {
      "kind": "cards",
      "variant": "shared-orb",
      "accent": "#9a8acb",
      "background": "#cdd0de",
      "radius": "28px",
      "blur": "16px",
      "detail": "Retícula 3×2 con esfera detrás; contenido completamente nítido."
    },
    "tradeoff": "En la biblioteca real cada colección conserva su miniatura; no sustituirla por iconos decorativos.",
    "verdict": "probar",
    "why": "La luz compartida hace que la biblioteca se lea como un sistema, no como seis adornos independientes.",
    "demo": "<div class=\"sc-collections\"><button data-study-option=\"0\"><small>01</small><b>Producto</b><span>↗</span></button><button data-study-option=\"1\"><small>02</small><b>Personajes</b><span>↗</span></button><button data-study-option=\"2\"><small>03</small><b>Luz</b><span>↗</span></button><button data-study-option=\"3\"><small>04</small><b>Textura</b><span>↗</span></button><button data-study-option=\"4\"><small>05</small><b>Ritmo</b><span>↗</span></button><button data-study-option=\"5\"><small>06</small><b>Marca</b><span>↗</span></button></div>"
  },
  {
    "id": "7239c3eb-6a61-4b85-9b16-3a5681feb973",
    "index": 53,
    "title": "Glassy motion · 13 oct · 32.png",
    "assetId": "f36a7dcd-29ae-4e62-8ec7-09e494e5bc66",
    "sourceStatus": "visual",
    "observations": [
      "Tarjeta horizontal oscura con borde luminoso fino.",
      "Dos masas desenfocadas iluminan esquinas opuestas en azul y malva.",
      "Jerarquía de texto blanca con metadatos pequeñas y mucho espacio entre grupos."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "Al ampliar, el pie cambia de énfasis sin escalar el texto."
    },
    "application": {
      "area": "activity",
      "component": "Resumen compacto de una pieza",
      "reason": "Agrupa estado, contexto y siguiente acción sobre una única superficie oscura."
    },
    "recipe": {
      "kind": "dashboard",
      "variant": "night-summary",
      "accent": "#347cff",
      "background": "#222337",
      "radius": "28px",
      "blur": "16px",
      "detail": "Gradiente diagonal, borde de 1 px, texto fuera de las zonas de brillo."
    },
    "tradeoff": "No introducir números de cuenta o métricas ficticias tomadas de la tarjeta bancaria.",
    "verdict": "probar",
    "why": "Agrupa estado, contexto y siguiente acción sobre una única superficie oscura.",
    "demo": "<div class=\"sc-summary\"><small>ESTUDIO / VISTA DE PRUEBA</small><strong>Una pieza.<br>Su siguiente paso.</strong><footer><span>En revisión</span><button data-study-toggle>Ver detalle ↗</button></footer></div>"
  },
  {
    "id": "00df4e75-016c-4cd9-b358-56e2f14e301d",
    "index": 54,
    "title": "Glassy motion · 13 oct · 33.png",
    "assetId": "5af8550d-46c9-4d9d-91f7-6ac2e953e194",
    "sourceStatus": "visual",
    "observations": [
      "La niebla pasa de blanco arriba a azul petróleo abajo y a la derecha.",
      "El símbolo blanco ocupa el centro con mucho espacio vacío alrededor.",
      "Las palabras en mayúsculas están separadas y funcionan como coordenadas.",
      "No hay tarjetas de vidrio: el material es el propio fondo."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "La luz se desplaza lentamente solo durante la entrada, después se detiene."
    },
    "application": {
      "area": "home",
      "component": "Portada atmosférica de inicio",
      "reason": "Una única atmósfera puede dar carácter sin añadir más cajas."
    },
    "recipe": {
      "kind": "panel",
      "variant": "atmospheric-identity",
      "accent": "#347cff",
      "background": "#173b4c",
      "radius": "28px",
      "blur": "16px",
      "detail": "Fondo de niebla azul petróleo, texto nítido y un CTA."
    },
    "tradeoff": "Usarlo en el inicio o un vacío; las páginas de producción necesitan superficies uniformes.",
    "verdict": "reservar",
    "why": "Una única atmósfera puede dar carácter sin añadir más cajas.",
    "demo": "<div class=\"sc-atmos\"><small>BRAUD</small><h3>Da forma<br>a lo que imaginas.</h3><button data-study-toggle>Comenzar ＋</button><small>STUDIO</small></div>"
  },
  {
    "id": "e0a82dde-be02-4473-9545-9a0bda9dbf74",
    "index": 55,
    "title": "Glassy motion · 13 oct · 34.png",
    "assetId": "c41f7b53-6c27-443b-ac47-59c44ff34c65",
    "sourceStatus": "visual",
    "observations": [
      "Plano gris frío con retícula ortogonal muy tenue.",
      "La esquina inferior izquierda tiene un radio desproporcionadamente grande.",
      "Una lente circular transparente se superpone al titular negro y lo distorsiona.",
      "La cruz blanca del círculo repite la pequeña cruz de la retícula."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "La lente recorre 50 px al pulsar, con un único easing de 420 ms."
    },
    "application": {
      "area": "home",
      "component": "Mosaico con lente de entrada",
      "reason": "La retícula ordena las piezas y una sola lente señala dónde empezar."
    },
    "recipe": {
      "kind": "button",
      "variant": "grid-lens",
      "accent": "#347cff",
      "background": "#d6d8df",
      "radius": "28px",
      "blur": "16px",
      "detail": "Retícula 64 px y lente de 100 px. Distorsión aproximada con CSS, no refracción física."
    },
    "tradeoff": "No desplazar ni deformar el texto editable. La lente solo afecta a la decoración.",
    "verdict": "probar",
    "why": "La retícula ordena las piezas y una sola lente señala dónde empezar.",
    "demo": "<div class=\"sc-grid\"><small>ESTUDIO / 01</small><h3>Una idea.<br><span>En movimiento.</span></h3><button data-study-toggle aria-label=\"Activar lente de nueva idea\">＋</button><footer>Concepto&nbsp; / &nbsp;Guion&nbsp; / &nbsp;Producción</footer></div>"
  },
  {
    "id": "f3ecd6fe-52b6-49b4-8f77-8a4cf6f0800d",
    "index": 56,
    "title": "Glassy motion · 13 oct · 35.png",
    "assetId": "de534dd6-1c60-45c5-8ba4-419f381703bd",
    "sourceStatus": "visual",
    "observations": [
      "Botón circular y cápsula larga sobre un plano azul gris.",
      "El volumen se concentra en el borde superior e inferior blanco.",
      "Los iconos finos y el texto permanecen planos dentro de la superficie."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "Presión de 2 px y retorno de 200 ms; sin rebote elástico."
    },
    "application": {
      "area": "studio",
      "component": "Entrada de referencias",
      "reason": "Un botón con material reconocible invita a subir sin crear un panel pesado."
    },
    "recipe": {
      "kind": "button",
      "variant": "upload-optics",
      "accent": "#347cff",
      "background": "#aebac4",
      "radius": "28px",
      "blur": "16px",
      "detail": "Borde interior y luz de 1 px; el centro queda calmado."
    },
    "tradeoff": "En el prototipo no se suben archivos. La integración final conserva el selector nativo y su estado.",
    "verdict": "probar",
    "why": "Un botón con material reconocible invita a subir sin crear un panel pesado.",
    "demo": "<div class=\"sc-upload\"><small>REFERENCIAS EN MENTE</small><div><button data-study-toggle aria-label=\"Probar carga circular\">↑</button><button data-study-toggle>↑ <span>Añadir referencia</span></button></div><p>Una imagen, un enlace, una dirección.</p></div>"
  },
  {
    "id": "82b87eeb-cd2a-4fbc-9c7f-91c7dfd8441e",
    "index": 57,
    "title": "Glassy motion · 13 oct · 36.png",
    "assetId": "523e21d6-2f7e-4891-95e3-6e84429ff84e",
    "sourceStatus": "visual",
    "observations": [
      "Un círculo se une a una cápsula alargada mediante un cuello cóncavo.",
      "La retícula del fondo permanece visible a través de la forma.",
      "El borde concentra brillo y una línea cromática muy leve."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "La cápsula y el accesorio comparten 320 ms; accesos con opacity, no salto de altura."
    },
    "application": {
      "area": "conversation",
      "component": "Compositor con accesorio conectado",
      "reason": "Relaciona adjuntar y escribir sin que parezcan herramientas de dos bloques distintos."
    },
    "recipe": {
      "kind": "composer",
      "variant": "connected-glass",
      "accent": "#347cff",
      "background": "#c5c7cc",
      "radius": "28px",
      "blur": "16px",
      "detail": "Dos piezas con cuello visual; no aplicar filtros de fusión al texto."
    },
    "tradeoff": "El efecto de unión se aproxima con geometría CSS. No prometer refraction exacta del render original.",
    "verdict": "probar",
    "why": "Relaciona adjuntar y escribir sin que parezcan herramientas de dos bloques distintos.",
    "demo": "<div class=\"sc-connected\"><button data-study-toggle aria-label=\"Mostrar accesos de la prueba\">＋</button><label><span class=\"sr-only\">Mensaje de prueba</span><input placeholder=\"Piensa, pide, corrige…\"></label><div class=\"sc-tools\"><span>Referencia</span><span>Foco</span></div></div>"
  },
  {
    "id": "ccb4229d-b4ab-4f5e-ad48-719e9655be63",
    "index": 58,
    "title": "Glassy motion · 13 oct · 37.png",
    "assetId": "e5d6f301-ad59-4cbe-8cbf-f458cfc6fc35",
    "sourceStatus": "visual",
    "observations": [
      "Dos opciones amplias dentro de un rail gris redondeado.",
      "La activa es una cápsula transparente con luz superior e inferior.",
      "El contraste procede del peso de la etiqueta, no de una pastilla azul sólida."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "Lente translateX de 320 ms; textos sin transform ni escala."
    },
    "application": {
      "area": "conversation",
      "component": "Orden de conversaciones",
      "reason": "Una lente móvil puede dar continuidad a Recientes / Por pieza manteniendo ambas opciones quietas."
    },
    "recipe": {
      "kind": "tabs",
      "variant": "thread-lens",
      "accent": "#347cff",
      "background": "#bfc2c5",
      "radius": "28px",
      "blur": "16px",
      "detail": "Un indicador compartido desliza bajo dos botones de igual ancho."
    },
    "tradeoff": "En listas muy cortas el cambio puede no alterar el orden; conservar la selección explícita.",
    "verdict": "probar",
    "why": "Una lente móvil puede dar continuidad a Recientes / Por pieza manteniendo ambas opciones quietas.",
    "demo": "<div class=\"sc-thread-tabs\" data-option=\"0\"><i></i><button data-study-option=\"0\" aria-pressed=\"true\">Recientes</button><button data-study-option=\"1\" aria-pressed=\"false\">Por pieza</button></div>"
  },
  {
    "id": "7d95b767-6d59-4bb3-8c68-607bb9d3b496",
    "index": 59,
    "title": "Glassy motion · 13 oct · 38.png",
    "assetId": "7faefdc7-331f-42ed-b0c2-300bbb40c786",
    "sourceStatus": "visual",
    "observations": [
      "Cápsula transparente larga sobre una retícula gris.",
      "Un círculo blanco con más en la izquierda y una cápsula negra de micrófono en la derecha.",
      "Sombras diagonales suaves atraviesan el fondo; cuatro marcas de encuadre delimitan la pieza."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "Borde y micrófono responden en 180 ms, sin animar continuamente el placeholder."
    },
    "application": {
      "area": "home",
      "component": "Entrada compacta con voz diferenciada",
      "reason": "Las dos acciones laterales se reconocen sin necesitar tres filas de herramientas."
    },
    "recipe": {
      "kind": "composer",
      "variant": "framed-input",
      "accent": "#347cff",
      "background": "#c4c7cc",
      "radius": "28px",
      "blur": "16px",
      "detail": "Marco solo en la zona de ejemplo; cápsula con input real."
    },
    "tradeoff": "El micrófono de prueba no graba. En producto el estado debe corresponder al permiso y la captura reales.",
    "verdict": "probar",
    "why": "Las dos acciones laterales se reconocen sin necesitar tres filas de herramientas.",
    "demo": "<div class=\"sc-framed\"><div><button data-study-toggle aria-label=\"Añadir contexto de prueba\">＋</button><input aria-label=\"Idea de prueba\" placeholder=\"Cuéntame la idea…\"><button data-study-toggle aria-label=\"Probar estado de dictado\">ⅡⅠⅡ</button></div></div>"
  },
  {
    "id": "1db2b720-38e1-4f29-9e31-83f60bf7bed4",
    "index": 60,
    "title": "Glassy motion · 13 oct · 39.png",
    "assetId": "b3d37634-0353-4c79-8527-6e1ed275d8c2",
    "sourceStatus": "visual",
    "observations": [
      "Degradado vertical de crema claro a gris azulado oscuro con transición muy larga.",
      "Una línea blanca delgada conecta la marca superior con el contenido inferior.",
      "La jerarquía combina titular sans, frase serif y párrafo corto."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "La línea se revela una vez de arriba abajo al pulsar."
    },
    "application": {
      "area": "home",
      "component": "Vacío editorial de un estudio nuevo",
      "reason": "La línea puede unir la idea inicial con el primer paso sin llenar la pantalla de instrucciones."
    },
    "recipe": {
      "kind": "panel",
      "variant": "editorial-line",
      "accent": "#347cff",
      "background": "#aab5bf",
      "radius": "28px",
      "blur": "16px",
      "detail": "Línea de 1 px y un único párrafo; la altura se adapta al contenido."
    },
    "tradeoff": "No copiar el gran vacío vertical en pantallas de trabajo: retrasaría el acceso al compositor.",
    "verdict": "reservar",
    "why": "La línea puede unir la idea inicial con el primer paso sin llenar la pantalla de instrucciones.",
    "demo": "<div class=\"sc-editorial\"><small>BRAUD / STUDIO</small><i></i><h3>Empieza donde estás.</h3><p>Una intuición ya es un punto de partida.</p><button data-study-toggle>Dar forma a la idea ↗</button></div>"
  },
  {
    "id": "a1ca200e-b8ec-47a0-978d-b2e3e3350e7e",
    "index": 61,
    "title": "Glassy motion · 13 oct · 40.png",
    "assetId": "e11d9688-517c-41e2-8f3c-bb10da01515e",
    "sourceStatus": "visual",
    "observations": [
      "Fotografía azul gris oscura con mucho grano y zonas desenfocadas.",
      "Arcos de gran radio y trazo fino recorren toda la composición.",
      "El título es enorme mientras los tres grupos de texto son pequeños y alineados en una columna."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "Solo el arco decorativo rota 8 grados al explorar."
    },
    "application": {
      "area": "library",
      "component": "Portada de una colección de referencias",
      "reason": "Los arcos conectan elementos visuales sin recurrir a una cuadrícula de marcos repetidos."
    },
    "recipe": {
      "kind": "panel",
      "variant": "editorial-arcs",
      "accent": "#347cff",
      "background": "#172f3a",
      "radius": "28px",
      "blur": "16px",
      "detail": "Arcos de baja opacidad sobre atmósfera, no encima de controles."
    },
    "tradeoff": "El texto original es muy pequeño: en BRAUD se eleva a 14 px como mínimo.",
    "verdict": "reservar",
    "why": "Los arcos conectan elementos visuales sin recurrir a una cuadrícula de marcos repetidos.",
    "demo": "<div class=\"sc-silence\"><i></i><i></i><h3>Enfoque.</h3><div><small>COLECCIÓN / EJEMPLO</small><p>Un lugar para las referencias que definen la intención.</p><button data-study-toggle>Ver colección ↗</button></div></div>"
  },
  {
    "id": "06479e7f-9f5f-42cd-9b23-2f7bbd8891e4",
    "index": 62,
    "title": "Glassy motion · 13 oct · 41.png",
    "assetId": "9841ffc5-4c30-446e-b900-336fb3c907dd",
    "sourceStatus": "visual",
    "observations": [
      "Cuatro tonos explícitos: White Cloud #F2F2F2, Dark Fog #C5C6CB, Graphite #30333C y Onyx #131313.",
      "La paleta se integra en un paisaje de agua y un reflejo horizontal blanco.",
      "La separación de temas se construye con luminancia y material, no con muchos acentos."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "Transición de color de 240 ms, anulada con movimiento reducido."
    },
    "application": {
      "area": "settings",
      "component": "Base tonal del tema",
      "reason": "El azul de BRAUD se puede conservar como acento mientras estas cuatro capas ordenan el fondo y los controles."
    },
    "recipe": {
      "kind": "panel",
      "variant": "tonal-system",
      "accent": "#347cff",
      "background": "#f2f2f2",
      "radius": "28px",
      "blur": "16px",
      "detail": "Base neutra por niveles; azul solo en acción y selección."
    },
    "tradeoff": "Dark Fog sobre White Cloud no sirve para texto pequeño: es un color de superficie, no de lectura.",
    "verdict": "probar",
    "why": "El azul de BRAUD se puede conservar como acento mientras estas cuatro capas ordenan el fondo y los controles.",
    "demo": "<div class=\"sc-tones\"><h3>Un acento.<br>Cuatro planos.</h3><div><button data-study-option=\"0\" style=\"--tone:#f2f2f2\"><i></i><span>Cloud</span><small>#f2f2f2</small></button><button data-study-option=\"1\" style=\"--tone:#c5c6cb\"><i></i><span>Fog</span><small>#c5c6cb</small></button><button data-study-option=\"2\" style=\"--tone:#30333c\"><i></i><span>Graphite</span><small>#30333c</small></button><button data-study-option=\"3\" style=\"--tone:#131313\"><i></i><span>Onyx</span><small>#131313</small></button></div><button class=\"sc-tones-action\" data-study-toggle>Azul BRAUD ↗</button></div>"
  },
  {
    "id": "52c255ea-b298-4cca-8223-a4caa4a1c718",
    "index": 63,
    "title": "Glassy motion · 13 oct · 42.png",
    "assetId": "aef223dd-72ed-4595-ae3e-18022c1aefc1",
    "sourceStatus": "visual",
    "observations": [
      "Fondo negro casi puro con una retícula visible solo en la mitad inferior.",
      "Una cápsula negra con borde fino contiene más y una palabra blanca.",
      "El cursor vertical proyecta un cono de luz que disuelve el texto a su derecha.",
      "La luz crea dirección horizontal; no hay múltiples sombras de tarjeta."
    ],
    "motion": {
      "observed": false,
      "description": "La fuente inspeccionada es estática; no permite deducir su animación original.",
      "proposal": "Haz corto al activar el foco; termina en un estado estable."
    },
    "application": {
      "area": "conversation",
      "component": "Foco explícito en el compositor",
      "reason": "Un pequeño haz puede indicar el contexto seleccionado sin convertirlo en un mensaje automático."
    },
    "recipe": {
      "kind": "composer",
      "variant": "focus-beam",
      "accent": "#347cff",
      "background": "#08090a",
      "radius": "28px",
      "blur": "16px",
      "detail": "Haz decorativo separado del texto y del cursor real."
    },
    "tradeoff": "No hacer ilegible el nombre del foco. El resplandor vive por detrás y se limita a una franja.",
    "verdict": "probar",
    "why": "Un pequeño haz puede indicar el contexto seleccionado sin convertirlo en un mensaje automático.",
    "demo": "<div class=\"sc-beam\"><small>CONTEXTO DE LA CONVERSACIÓN</small><button data-study-toggle><b>＋ Poner foco</b><i></i><span>Apertura del guion</span></button><p>Escribe tu indicación con este contexto.</p></div>"
  }
];

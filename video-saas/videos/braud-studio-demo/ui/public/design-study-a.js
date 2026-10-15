// Each fragment is an isolated visual experiment. Native controls never call Studio actions.
const sources={
 2:['design-1','Exploración visual 1','design-1'],3:['design-2','Exploración visual 2','design-2'],4:['design-3','Exploración visual 3','design-3'],5:['design-4','Exploración visual 4','design-4'],
 9:['design-ref-5','Entrada flotant sobre paisatge','design-5'],10:['design-ref-6','Cercador liquid glass','design-6'],11:['design-ref-7','Botó de vidre','design-7'],12:['design-ref-8','Selector Inbox / Draft','design-8'],13:['design-ref-9','Navegació sobre blau','design-9'],14:['design-ref-10','Frosted / Clear / Blur','design-10'],15:['design-ref-11','Control de volum','design-11'],16:['design-ref-12','Gestos i moviment','design-12'],17:['design-ref-13','Estat Thinking','design-13'],18:['design-ref-14','Panell de contingut','design-14'],19:['design-ref-15','Navegació vertical','design-15'],20:['design-ref-16','Dock flotant','design-16'],21:['design-ref-17','Panell sobre paisatge','design-17'],
 22:['bdfd3bc8-86ae-41c7-8ac5-ec5abb42690a','Glassy motion · 13 oct · 01.png','7a133bb8-a712-402b-a4f1-bfc43ea2fa64'],23:['2245b52b-5e2b-48e4-801a-189531ca6a16','Glassy motion · 13 oct · 02.png','c048ed97-a120-4ed9-aec5-a3d2a5a97028'],24:['d8f75b90-5523-40c7-8648-a8e0c71f4963','Glassy motion · 13 oct · 03.gif','7be20d1f-9952-4200-b153-e73d83136161'],25:['7a6e1431-26bd-40ef-8ce2-8fad0ab3f469','Glassy motion · 13 oct · 04.png','93377af6-c0b3-4514-964b-279b6ae7ebb7'],26:['ec3cc1a3-f0c1-4ac2-a8c4-cfb7ce4fe201','Glassy motion · 13 oct · 05.png','322c1555-eaa4-4674-8115-f35f9fc7088f'],27:['9410663f-6e3c-4b6f-a491-80dd13b4bd03','Glassy motion · 13 oct · 06.png','cee7928a-fbbf-483f-9863-4aee7c7b0152'],28:['fe6339e6-09e6-4275-8253-f8a57a25417f','Glassy motion · 13 oct · 07.png','8283255a-aae0-4b4e-88c8-625ed2e0648c']
};
const glyph={plus:'<path d="M12 5v14M5 12h14"/>',up:'<path d="m5 10 7-7 7 7M12 3v18"/>',search:'<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',mic:'<rect x="9" y="3" width="6" height="12" rx="3"/><path d="M6 10v2a6 6 0 0 0 12 0v-2M12 18v3M8 21h8"/>',home:'<path d="m3 10 9-7 9 7v11h-6v-7H9v7H3Z"/>',film:'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 3v18M17 3v18M3 8h4M3 16h4M17 8h4M17 16h4"/>',folder:'<path d="M3 7V4h7l3 3h8v14H3Z"/>',voice:'<path d="M3 10v4M7 6v12M12 3v18M17 7v10M21 10v4"/>',person:'<circle cx="12" cy="7" r="4"/><path d="M4 22v-3a8 8 0 0 1 16 0v3"/>',clock:'<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',settings:'<path d="M3 6h18M3 12h18M3 18h18"/><circle cx="8" cy="6" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="9" cy="18" r="2"/>',volume:'<path d="M3 9h4l5-4v14l-5-4H3ZM16 8a6 6 0 0 1 0 8M19 5a10 10 0 0 1 0 14"/>',play:'<path d="m8 4 12 8-12 8Z"/>',arrow:'<path d="M3 12h18m-6-6 6 6-6 6"/>',check:'<path d="m4 12 5 5L20 6"/>'};
const icon=name=>`<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">${glyph[name]||glyph.plus}</svg>`;
const choices=(n,labels,icons=[])=>`<div class="dsa-choices" role="group" aria-label="Opciones de la demostración">${labels.map((label,i)=>`<label class="dsa-choice"><input type="radio" name="dsa-${n}" value="${i}" ${i===0?'checked':''} aria-label="${label}, demostración"><span>${icons[i]?icon(icons[i]):''}<b>${label}</b></span></label>`).join('')}</div>`;
const switcher=(n,label)=>`<label class="dsa-toggle"><input class="dsa-switch" type="checkbox" name="dsa-toggle-${n}" aria-label="${label}, solo demostración"><span>${label}</span></label>`;
const input=(label='Escribe una idea para BRAUD…')=>`<input class="dsa-input" type="text" placeholder="${label}" aria-label="${label} (demostración, no se envía)">`;
const staticMotion=proposal=>({observed:false,description:'Imagen estática: no permite verificar trayectoria, duración ni respuesta al gesto.',proposal});
const make=(index,details)=>({id:sources[index][0],index,title:sources[index][1],assetId:sources[index][2],...details,demo:`<div class="dsa-demo" data-demo-only="true">${details.demo}<small class="dsa-caption">Vista de prueba · BRAUD</small></div>`});
const recipe=(kind,variant,accent,background,radius,blur,detail)=>({kind,variant,accent,background,radius,blur,detail});

export const studyA=[
 make(2,{
  observations:['Una única placa apaisada ocupa casi todo el encuadre; su perímetro fino y redondeado se distingue del fondo azul desenfocado.','La luz entra por abajo y a la derecha; el azul profundo permanece arriba y a la izquierda.','El titular blanco se divide en dos líneas desplazadas, con una pequeña etiqueta de contorno junto a la primera.','Navegación mínima en una cápsula superior derecha y acción circular aislada en la esquina inferior izquierda.'],
  motion:staticMotion('Al abrir el estudio, revelar la placa con opacidad y 8 px de desplazamiento en 320 ms; la tipografía permanece estable.'),
  application:{area:'home',component:'Portada de bienvenida en una sola placa',reason:'Permite ensayar jerarquía editorial y un único contenedor, evitando repetir tarjetas dentro de tarjetas.'},
  recipe:recipe('panel','clarity-single-plate','#2e72d7','#123c83','34px','20px','Borde blanco fino, luz lateral y titular escalonado; navegación pegada a la esquina superior.'),
  tradeoff:'El gran campo azul compite con las portadas del estudio; conviene reservarlo a una bienvenida o portada puntual.',verdict:'reservar',why:'La jerarquía de la placa es aprovechable; el color protagonista no debería invadir todas las vistas de trabajo.',
  demo:`<div class="dsa-plate"><header><strong>braud</strong><span>ESTUDIO / IDEAS</span></header><h3>Una idea.<em>Una dirección.</em></h3><p>De la intención a la próxima pieza.</p><details><summary aria-label="Abrir entrada de prueba">${icon('arrow')}<span>Abrir estudio</span></summary>${input()}</details></div>`
 }),
 make(3,{
  observations:['El fondo pasa de blanco en la parte superior a azul medio y cobalto en la inferior, sin bordes de tarjetas.','Dos columnas difusas de azul dejan una zona de luz vertical cerca del centro.','El texto serif es diminuto, blanco y centrado; los números laterales amplían el eje horizontal.','La información ocupa muy poca superficie y el desenfoque funciona como protagonista visual.'],
  motion:staticMotion('Desplazar la luz de fondo muy lentamente solo en una bienvenida; detenerla en cuanto el usuario empiece a escribir.'),
  application:{area:'home',component:'Estado inicial sin piezas',reason:'El espacio negativo permite que una primera pregunta sea el único punto de entrada.'},
  recipe:recipe('panel','blue-atmosphere-empty','#2877dc','#edf8ff','18px','40px','Atmósfera abierta sin tarjeta; pequeña composición centrada y una entrada desplegable.'),
  tradeoff:'El texto blanco pequeño pierde legibilidad en la parte clara; necesita una zona de contraste controlada.',verdict:'sutil',why:'Conviene probar el fondo como atmósfera de baja intensidad, no copiar la escala casi ilegible del texto.',
  demo:`<div class="dsa-atmosphere-copy"><span>ESTUDIO</span><h3>¿Qué quieres<br>hacer sentir?</h3><details><summary>Empezar una idea ${icon('plus')}</summary>${input('Cuenta lo que tienes en mente…')}</details></div>`
 }),
 make(4,{
  observations:['Una mancha horizontal casi negra cruza en diagonal un fondo blanco cálido.','El halo exterior azul eléctrico es más ancho en la parte superior y se disuelve hacia los bordes.','La textura granulada evita que el degradado parezca una superficie digital completamente lisa.','Solo aparece una línea de texto blanco, pequeña y centrada sobre la zona más oscura.'],
  motion:staticMotion('Usar una respiración muy lenta del halo mientras el agente está activo; el núcleo y el texto no se desplazan.'),
  application:{area:'conversation',component:'Estado de trabajo del agente',reason:'Concentra la actividad en una forma pequeña que puede vivir cerca del texto de estado.'},
  recipe:recipe('status','analog-ink-halo','#175de5','#f3f1e8','55% 40% 48% 42%','18px','Núcleo oscuro alargado, halo cobalto y grano visual muy fino.'),
  tradeoff:'Una mancha grande parece una ilustración de marca y no un estado; debe reducirse y conservar una etiqueta legible.',verdict:'probar',why:'El contraste entre núcleo y halo tiene una traducción clara a un indicador de actividad compacto.',
  demo:`<div class="dsa-analog"><span>Una dirección toma forma.</span></div>${switcher(4,'Probar respiración del halo')}`
 }),
 make(5,{
  observations:['La composición vertical combina fondo crema con una masa azul de bordes muy difusos.','Un pliegue oscuro en forma de S produce la impresión de dos superficies que se rozan.','El azul se ilumina arriba a la izquierda y vuelve a aparecer detrás de la curva inferior derecha.','No hay texto ni controles: la referencia describe volumen, atmósfera y contraste, no una interfaz.'],
  motion:staticMotion('Al cambiar de familia de referencias, desplazar el pliegue unos pocos píxeles; no animarlo continuamente.'),
  application:{area:'library',component:'Separación entre inspiración y recursos propios',reason:'El pliegue puede aportar profundidad a una portada de biblioteca sin competir con cada miniatura.'},
  recipe:recipe('cards','organic-fold-library','#307fe4','#f2ece2','32px','28px','Pliegue azul oscuro sobre crema y dos áreas editoriales transparentes, sin ilustraciones inventadas.'),
  tradeoff:'La forma es decorativa y ocupa espacio; no ayuda a comparar recursos ni debe reemplazar miniaturas reales.',verdict:'reservar',why:'Tiene valor como introducción o separación de categorías, no como fondo de una biblioteca densa.',
  demo:`<div class="dsa-fold" aria-hidden="true"></div><div class="dsa-fold-copy"><small>BIBLIOTECA</small><h3>Todo empieza<br>mirando.</h3>${choices(5,['Inspiración','Recursos propios'])}<p>Elige qué parte de tu biblioteca quieres explorar.</p></div>`
 }),
 make(9,{
  observations:['La entrada horizontal flota sobre la línea del horizonte de un paisaje verde y azul.','El botón más queda separado a la izquierda; el envío es un círculo blanco dentro del extremo derecho.','La cápsula desenfoca el paisaje de fondo, pero conserva su mezcla de colores verde y cielo.','Texto blanco, una única línea y ausencia de controles secundarios refuerzan la sensación de ligereza.'],
  motion:staticMotion('Abrir el adjunto desde el botón exterior sin cambiar el eje ni la anchura de la cápsula; animar solo el pequeño menú.'),
  application:{area:'conversation',component:'Entrada compacta con adjunto exterior',reason:'Separa el texto principal de los materiales y despeja el extremo de escritura.'},
  recipe:recipe('composer','horizon-floating-input','#7a9b65','#b3d4db','999px','18px','Más independiente, campo transparente y envío circular interior; fondo abstracto de dos planos.'),
  tradeoff:'Una línea resulta insuficiente para instrucciones largas; al crecer debe abrirse hacia arriba sin esconder los controles.',verdict:'probar',why:'La organización del adjunto y el envío es útil incluso eliminando el paisaje de la aplicación real.',
  demo:`<div class="dsa-horizon" aria-hidden="true"></div><div class="dsa-floating-entry"><details class="dsa-attach"><summary aria-label="Mostrar materiales de prueba">${icon('plus')}</summary><p>Referencia · Documento · Audio</p></details><div class="dsa-pill">${input()}<label class="dsa-send"><input type="checkbox" aria-label="Probar estado listo, no envía mensajes">${icon('up')}</label></div></div><p class="dsa-ready">Texto preparado. Esta prueba no envía mensajes.</p>`
 }),
 make(10,{
  observations:['Una cápsula exterior gruesa rodea una segunda entrada clara y más pequeña.','El borde exterior tiene un reflejo blanco intenso arriba y un contorno verdoso abajo, como una lente de gran espesor.','Lupa a la izquierda y micrófono a la derecha viven dentro del campo; el avatar queda fuera de él, dentro de la carcasa.','El campo interior es más opaco que la cubierta, de modo que mantiene legibilidad sobre el paisaje.'],
  motion:staticMotion('Conservar la carcasa inmóvil al enfocar; iluminar solo el borde del campo y desplegar el contexto junto al avatar.'),
  application:{area:'library',component:'Búsqueda con contexto de marca',reason:'La doble capa diferencia la consulta del contexto en el que se está buscando.'},
  recipe:recipe('composer','nested-search-shell','#6b8b61','#c5d9d9','999px','14px','Carcasa biselada, campo interior casi opaco y contexto circular separado.'),
  tradeoff:'El doble borde consume ancho; en móvil el contexto debe abrirse como menú y no reducir el texto a unos pocos caracteres.',verdict:'sutil',why:'La separación entre búsqueda y contexto es más valiosa que el espesor exagerado del vidrio.',
  demo:`<div class="dsa-search-shell"><div class="dsa-search-field">${icon('search')}<input type="search" placeholder="Buscar en mi biblioteca" aria-label="Buscar en la demostración">${icon('mic')}</div><details class="dsa-brand-context"><summary aria-label="Contexto de marca de prueba">B</summary><p>BRAUD<br><small>Recursos de esta marca</small></p></details></div>`
 }),
 make(11,{
  observations:['El fondo gris azulado y la placa son próximos en luminosidad: el relieve procede de los contornos, no del color.','El círculo de subida y la cápsula de texto comparten el mismo doble bisel.','El brillo es blanco en el arco superior y en el borde inferior; una línea oscura exterior dibuja el grosor.','La flecha y el texto parecen ligeramente elevados por un reflejo interior, sin ser iconos rellenos.'],
  motion:staticMotion('Al pulsar, reducir el relieve durante 120 ms y devolverlo en 180 ms; mantener fijos el texto y el contorno externo.'),
  application:{area:'library',component:'Añadir referencias',reason:'Da una acción reconocible a la entrada de materiales sin recurrir a una gran zona de subida vacía.'},
  recipe:recipe('button','smoked-upload-bevel','#d8e9ef','#586973','999px','8px','Disco y etiqueta unidos visualmente por un bisel blanco/oscuro de dos líneas.'),
  tradeoff:'Un borde demasiado brillante parece cromado y pesa más que las acciones principales azules.',verdict:'probar',why:'El relieve puntual puede enriquecer acciones secundarias manteniendo una paleta neutra.',
  demo:`<details class="dsa-upload"><summary aria-label="Abrir opciones de referencias de prueba"><span>${icon('up')}</span><b>Añadir referencias</b></summary><div class="dsa-upload-options">${choices(11,['Enlace','Imagen','Documento'])}${input('Pega un enlace de referencia…')}</div></details>`
 }),
 make(12,{
  observations:['El selector tiene dos opciones iguales dentro de una carcasa horizontal muy redondeada.','La selección es más oscura y parece hundida; el texto activo blanco contrasta con el inactivo gris.','El brillo más fuerte está en el borde inferior, mientras la parte superior es casi transparente.','La forma seleccionada ocupa casi media anchura con un pequeño margen uniforme al perímetro.'],
  motion:staticMotion('Deslizar una misma superficie seleccionada de lado a lado en 300 ms; evitar fundir dos fondos independientes.'),
  application:{area:'conversation',component:'Recientes / Por pieza',reason:'El estado seleccionado puede ser claro sin añadir un relleno azul intenso a toda la opción.'},
  recipe:recipe('tabs','inset-two-way-selector','#b8dce4','#213942','999px','10px','Cápsula oscura con selección hundida y luz continua en el borde inferior.'),
  tradeoff:'El texto inactivo de la referencia es demasiado tenue; debe mantener contraste incluso sin estar seleccionado.',verdict:'probar',why:'Encaja con la navegación actual y permite mejorar el movimiento sin alterar el contenido.',
  demo:`${choices(12,['Recientes','Por pieza'])}<div class="dsa-tab-content"><p class="dsa-first">Conversaciones, en el orden en que las retomas.</p><p class="dsa-second">Cada conversación junto a su pieza.</p></div>`
 }),
 make(13,{
  observations:['Una barra transparente de cinco iconos flota sobre un fondo azul eléctrico con grandes pliegues.','Cada icono tiene una etiqueta pequeña debajo; el espacio entre opciones es regular.','El fondo parece atravesar la barra, con una distorsión luminosa especialmente visible en el extremo derecho.','La cápsula no tiene relleno blanco: su silueta se reconoce por bordes finos y reflejos localizados.'],
  motion:staticMotion('Mover una luz de selección entre opciones y mantener los iconos inmóviles; el fondo no necesita animarse.'),
  application:{area:'navigation',component:'Navegación principal con icono y etiqueta',reason:'Puede hacer más reconocibles las áreas sin depender únicamente de símbolos.'},
  recipe:recipe('tabs','cobalt-transparent-nav','#6488ff','#071a72','999px','5px','Cinco zonas iguales y un reflejo elíptico en un extremo de la barra.'),
  tradeoff:'El fondo de alto contraste distorsiona la lectura; el vidrio debe conservar un mínimo de opacidad bajo las etiquetas.',verdict:'sutil',why:'Conviene ensayar la barra y sus etiquetas, manteniendo el gran fondo azul fuera de las vistas de trabajo.',
  demo:`<div class="dsa-blue-fold" aria-hidden="true"></div>${choices(13,['Estudio','Biblioteca','Taller','Actividad','Mi marca'],['home','folder','film','clock','person'])}`
 }),
 make(14,{
  observations:['La comparación utiliza una misma escena de fondo y tres materiales distintos, no tres diseños de tarjeta.','Frosted ocupa la franja superior y suaviza el detalle manteniendo las masas de color.','Clear deja ver el contenido con deformación evidente cerca de los bordes; Blur disuelve casi toda la información.','Los tres paneles mantienen radios grandes y texto blanco centrado, por lo que se puede comparar solo la superficie.'],
  motion:staticMotion('Permitir cambiar de transparencia sin mover el panel; interpolar únicamente opacidad y desenfoque en 220 ms.'),
  application:{area:'settings',component:'Intensidad del material de interfaz',reason:'Hace visible el equilibrio entre transparencia y lectura en un mismo contexto.'},
  recipe:recipe('panel','material-comparison','#b3bd8e','#484e3c','28px','16px','Una única muestra alterna entre suave, transparente y opaca sin cambiar su geometría.'),
  tradeoff:'CSS backdrop-filter aproxima el desenfoque; no reproduce por sí solo la refracción de Clear.',verdict:'probar',why:'Es una comparación útil para elegir cuánto vidrio necesita cada panel, antes de extenderlo a toda la aplicación.',
  demo:`${choices(14,['Suave','Transparente','Opaco'])}<div class="dsa-material-scene"><div class="dsa-material-stripes" aria-hidden="true"></div><div class="dsa-material-panel"><small>DIRECCIÓN</small><h3>La intención,<br>siempre legible.</h3><p>Un mismo contenido. Tres superficies.</p></div></div>`
 }),
 make(15,{
  observations:['El control se presenta como una cápsula horizontal larga y oscura, con una segunda cápsula que ocupa aproximadamente la mitad.','La parte activa tiene borde claro, una reflexión azulada en su esquina superior derecha y texto blanco.','El volumen se expresa con icono y número dentro del área activa, no encima del carril.','El fondo textil permanece reconocible fuera del control y difuso dentro de él.'],
  motion:staticMotion('Al arrastrar, desplazar el límite de la superficie activa sin escalar el icono; la transición desaparece durante el gesto para seguir el dedo.'),
  application:{area:'studio',component:'Mezcla de voz y música en Montaje',reason:'Un control ancho y táctil puede facilitar un ajuste gradual sin añadir ventanas.'},
  recipe:recipe('slider','glass-volume-track','#d2e6ed','#343a3e','999px','12px','Carril ancho ahumado, pulgar de vidrio y etiquetas laterales para voz/música.'),
  tradeoff:'No conviene imitar un número que no se actualiza; la muestra usa un rango nativo sin porcentaje ficticio.',verdict:'probar',why:'La forma tiene relación directa con un control continuo real del estudio.',
  demo:`<div class="dsa-volume-title"><span>Mezcla de la pieza</span><small>Solo prueba visual</small></div><label class="dsa-volume">${icon('volume')}<input type="range" min="0" max="100" value="52" aria-label="Balance entre voz y música, demostración"></label><div class="dsa-volume-ends"><span>Más voz</span><span>Más música</span></div>`
 }),
 make(16,{
  observations:['La referencia es casi negra, con manos tridimensionales iluminadas en blanco y gris.','El dedo apunta a un punto blanco luminoso aislado; el segundo encuadre muestra un gesto sobre una tableta.','El texto es pequeño y desplazado a la derecha, dejando que la dirección de la mano explique la acción.','Es una imagen fija sobre gestos: no permite saber qué animación ocurre entre pulsar y expandir.'],
  motion:staticMotion('Al abrir el chat, expandir el mismo rectángulo desde su borde; el contenido se revela después y no se escala como una fotografía.'),
  application:{area:'conversation',component:'Ampliar y recoger el agente',reason:'Traduce el gesto a una relación clara entre el origen del control y la superficie que aparece.'},
  recipe:recipe('panel','gesture-origin-expansion','#eff4f7','#0b0c0f','26px','0px','Punto de origen luminoso y panel que cambia de espacio sin manos ni ilustraciones ajenas.'),
  tradeoff:'La escena gestual completa es demasiado decorativa; lo útil es el origen del movimiento, no reproducir las manos.',verdict:'sutil',why:'Puede guiar una transición coherente del agente sin añadir ruido permanente.',
  demo:`${switcher(16,'Ampliar conversación')}<div class="dsa-gesture-stage"><span class="dsa-origin" aria-hidden="true"></span><section class="dsa-gesture-panel"><small>AGENTE / BRAUD</small><h3>¿Qué revisamos?</h3><p>La misma conversación, con más espacio.</p>${input('Escribe en esta vista de prueba…')}</section></div>`
 }),
 make(17,{
  observations:['Dos pequeñas esferas translúcidas se superponen a la izquierda del estado Thinking.','El punto de contacto entre ambas concentra una luz blanca intensa y un halo suave.','El panel oscuro tiene una gran esquina redondeada y una línea de luz muy fina en el borde.','Una cuadrícula de puntos apenas visible queda detrás; la entrada de texto mantiene un contraste bajo y uniforme.'],
  motion:staticMotion('Hacer que los dos orbes orbiten lentamente durante el trabajo real; detenerlos al terminar y ofrecer una versión estática con movimiento reducido.'),
  application:{area:'conversation',component:'Indicador de actividad junto al texto',reason:'Un símbolo pequeño puede dar vida al estado sin desplazar el historial ni simular progreso.'},
  recipe:recipe('status','twin-glass-thinking','#dce8f3','#121315','24px','6px','Dos esferas de vidrio superpuestas, luz en el contacto y una etiqueta estable.'),
  tradeoff:'No debe mantenerse animado cuando el agente está inactivo ni prometer un porcentaje de avance que no existe.',verdict:'probar',why:'Es una de las referencias más trasladables al chat con poco espacio y sin alterar su estructura.',
  demo:`<div class="dsa-thinking"><span class="dsa-orbs" aria-hidden="true"><i></i><i></i></span><span>Preparando una dirección…</span></div><div class="dsa-dark-entry">${input('Puedes seguir dando indicaciones…')}</div>${switcher(17,'Ver movimiento propuesto')}`
 }),
 make(18,{
  observations:['Un panel horizontal verde oliva se superpone a una imagen de naturaleza y recoge su color.','La parte superior integra cerrar y tres pestañas; no hay una cabecera separada por otro contenedor.','La miniatura está a la izquierda, la descripción en el centro y dos acciones apiladas a la derecha.','Todos los elementos comparten una superficie mate; el volumen es menor que en las cápsulas de vidrio brillante.'],
  motion:staticMotion('Aparecer desde el borde inferior del visor en 260 ms, sin mover el vídeo; al cambiar pestaña solo cambia el contenido central.'),
  application:{area:'studio',component:'Información y dirección sobre la vista previa',reason:'Permite revisar una escena y sus decisiones sin abandonar el contexto visual.'},
  recipe:recipe('panel','olive-media-inspector','#bdc99e','#34412d','24px','22px','Panel mate con pestañas superiores y una fila de miniatura, texto y acciones.'),
  tradeoff:'Superponer demasiada información puede tapar la escena; debería ser plegable y ocupar solo una franja del visor.',verdict:'probar',why:'La organización del panel aporta una alternativa concreta a una columna lateral demasiado alta.',
  demo:`<div class="dsa-media-panel">${choices(18,['Dirección','Versiones','Notas'])}<div class="dsa-media-body"><div class="dsa-media-preview">${icon('film')}<small>Vista previa</small></div><div><h3>Esta escena</h3><p class="dsa-media-direction">Qué debe sentir quien la mira.</p><p class="dsa-media-versions">Las versiones conservan su dirección.</p><p class="dsa-media-notes">Una nota precisa antes de continuar.</p></div><details><summary>Revisar ${icon('arrow')}</summary><p>Solo abre esta muestra.</p></details></div></div>`
 }),
 make(19,{
  observations:['Un rail vertical muy redondeado contiene tres iconos grandes, sin etiquetas visibles.','La selección inferior es un disco de vidrio dentro de la cápsula principal.','La paleta gris cálida recoge la luz de una habitación; el fondo se suaviza de forma uniforme.','Los iconos blancos tienen rellenos suaves y reflejos, más cercanos a objetos que a trazos planos.'],
  motion:staticMotion('Deslizar el disco de selección en vertical con la misma curva en ambos sentidos; iconos y panel permanecen fijos.'),
  application:{area:'library',component:'Rail compacto de tipos de recurso',reason:'Sirve para alternar materiales sin ocupar una segunda fila de pestañas.'},
  recipe:recipe('rail','warm-vertical-orbit','#ede8db','#6b655c','999px','16px','Cápsula vertical cálida, tres opciones y disco interno continuo.'),
  tradeoff:'Solo iconos obliga a aprenderlos; necesita nombres accesibles y etiquetas visibles al enfocar o pasar el cursor.',verdict:'sutil',why:'Útil como navegación secundaria de biblioteca, menos claro como navegación principal de toda la aplicación.',
  demo:`<div class="dsa-vertical-layout">${choices(19,['Piezas','Personajes','Referencias'],['film','person','folder'])}<div class="dsa-rail-copy"><small>BIBLIOTECA</small><h3>Lo que buscas,<br>más cerca.</h3><p>Cambia de tipo de recurso.</p></div></div>`
 }),
 make(20,{
  observations:['Un dock horizontal oscuro y translúcido atraviesa una imagen de piedra sobre fondo negro.','Siete iconos mantienen el mismo tamaño y separación; el activo recibe un círculo de relleno algo más claro.','La búsqueda se separa en un botón circular a la derecha, con una distancia visible respecto al dock.','El material es satinado y discreto: el contorno es tenue y no hay un borde blanco intenso.'],
  motion:staticMotion('Mover el círculo activo entre opciones; expandir la búsqueda desde su propio botón sin estirar el dock.'),
  application:{area:'navigation',component:'Dock contextual de trabajo',reason:'Agrupa las áreas frecuentes y mantiene la búsqueda como una acción independiente.'},
  recipe:recipe('rail','graphite-detached-search','#c1c6cc','#101114','999px','18px','Dock satinado con selección circular y búsqueda separada.'),
  tradeoff:'Un dock solo de iconos tiene poca capacidad para etiquetas; en móvil debe reducir opciones y conservar acceso claro a las restantes.',verdict:'probar',why:'El tono y la separación de búsqueda encajan mejor con una herramienta de producción que una barra muy brillante.',
  demo:`<div class="dsa-dock-row">${choices(20,['Estudio','Biblioteca','Actividad','Ajustes'],['home','folder','clock','settings'])}<details class="dsa-dock-search"><summary aria-label="Expandir búsqueda de prueba">${icon('search')}</summary>${input('Buscar una pieza…')}</details></div>`
 }),
 make(21,{
  observations:['Una gran superficie translúcida agrupa una imagen principal arriba a la izquierda y datos editoriales a la derecha.','La fila inferior combina un recorrido lineal con una tarjeta de perfil más opaca.','El fondo de montañas y atardecer continúa visualmente a través de las capas.','Los radios son moderados, las separaciones estrechas y el texto negro o blanco cambia según el área de contraste.'],
  motion:staticMotion('Al abrir una pieza, conservar el marco y actualizar solo el panel seleccionado; evitar que cada módulo entre con un retraso distinto.'),
  application:{area:'studio',component:'Resumen visual de una pieza',reason:'Puede reunir dirección, etapa y material dentro de una misma composición sin convertirlo en un panel de métricas inventadas.'},
  recipe:recipe('dashboard','landscape-piece-overview','#6f9ba8','#4a6570','22px','18px','Dos columnas y una franja inferior de etapas, con un único marco exterior.'),
  tradeoff:'La referencia mezcla muchos niveles de opacidad; hay que limitarla para no perder jerarquía entre contenido y acciones.',verdict:'reservar',why:'Merece probarse como resumen de proyecto, no sustituir directamente la vista de escenas que ya funciona.',
  demo:`<div class="dsa-dashboard"><div class="dsa-dashboard-preview">${icon('film')}<span>Tu pieza</span></div><section><small>ESTUDIO</small><h3>Del concepto<br>a la entrega.</h3><p>Una misma intención atraviesa cada paso.</p><details><summary>Ver dirección</summary><p>La dirección reúne lo decidido en el chat.</p></details></section><div class="dsa-dashboard-steps">${choices(21,['Idea','Guion','Casting','Escenas'])}</div></div>`
 }),
 make(22,{
  observations:['Una forma orgánica tridimensional está construida con miles de puntos, sin superficie sólida.','Las hileras curvadas cambian de densidad y hacen legible el volumen como una malla.','El azul cian domina la zona superior; aparecen violeta y magenta en las ondulaciones inferiores.','La figura ocupa el centro de un fondo negro y no contiene texto ni controles.'],
  motion:staticMotion('Ondular muy suavemente una malla reducida solo durante una actividad real; evitar girar una esfera rígida que perdería el carácter de tela.'),
  application:{area:'conversation',component:'Exploración de indicador de generación',reason:'El punto puede convertirse en una señal ligera, siempre a escala pequeña y junto a un estado textual.'},
  recipe:recipe('status','particle-mesh-presence','#65b7ff','#050709','46%','0px','Malla de puntos cian con ondulación violeta en el borde inferior.'),
  tradeoff:'Una simulación completa aumenta consumo y distracción; la demo usa un SVG determinista y movimiento CSS contenido.',verdict:'reservar',why:'Tiene identidad visual fuerte, pero sería excesiva como animación continua del chat.',
  demo:`<div class="dsa-particle-state"><svg class="dsa-particles" viewBox="0 0 240 180" aria-hidden="true">${Array.from({length:16},(_,r)=>Array.from({length:24},(_,c)=>{const x=20+c*8.6+Math.sin(r*.45)*10,y=18+r*8.6+Math.sin(c*.38+r*.25)*10;return `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="1.8" fill="${r>11?'#ad85e5':'#72c5ff'}" opacity="${(.5+.5*Math.sin((c+1)/25*Math.PI)).toFixed(2)}"/>`}).join('')).join('')}</svg><p>Una idea se está formando.</p></div>${switcher(22,'Probar movimiento de la malla')}`
 }),
 make(23,{
  observations:['La pantalla negra presenta una esfera azul luminosa arriba y un saludo centrado debajo.','La esfera combina trazos curvos finos con una zona de luz más ancha en su lado derecho.','El compositor se sitúa muy abajo, sobre un halo azul que ilumina el borde inferior de la pantalla.','La entrada es una cápsula transparente con un icono de voz a la derecha y sin una gran botonera.'],
  motion:staticMotion('Reservar la luz inferior al foco de escritura; dar al orbe una respiración leve y pausarla al empezar una conversación.'),
  application:{area:'conversation',component:'Bienvenida de una conversación vacía',reason:'Refuerza que el espacio es un chat y dirige la mirada hacia el campo donde empezar.'},
  recipe:recipe('composer','bottom-lit-agent-welcome','#4399ff','#030a13','28px','12px','Orbe compacto arriba y halo azul limitado al borde inferior del compositor.'),
  tradeoff:'La separación vertical de la referencia funciona en móvil, pero desperdicia espacio en un lateral de escritorio.',verdict:'probar',why:'La iluminación inferior puede ayudar al descubrimiento del chat sin añadir otra tarjeta.',
  demo:`<div class="dsa-welcome-orb" aria-hidden="true"><i></i><i></i></div><div class="dsa-welcome-copy"><small>AGENTE / BRAUD</small><h3>¿Qué hacemos hoy?</h3></div><div class="dsa-bottom-composer">${input('Una idea, una pregunta…')}${icon('voice')}</div>`
 }),
 make(24,{
  observations:['El GIF contiene 101 fotogramas de 40 ms: un ciclo completo dura 4,04 segundos.','Una cinta extremadamente estrecha de luz blanca y cian atraviesa el centro sobre negro.','A lo largo del ciclo se curva hacia arriba y hacia abajo; alterna qué extremo se ensancha y qué zona se ve de perfil.','Un halo azul y violeta acompaña la torsión; la etiqueta Loading permanece quieta debajo.'],
  motion:{observed:true,description:'En las muestras a 0, 480, 1000, 1480, 2000, 2520, 3000 y 4000 ms, la cinta pasa de una punta ancha a una curva inferior, se estrecha de perfil y vuelve a abrirse con el extremo contrario. El texto no se mueve.',proposal:'Probar una interpretación CSS/SVG de 4,04 s con la misma alternancia de anchura y curvatura. No es una reproducción exacta de la simulación del GIF.'},
  application:{area:'activity',component:'Estado de tarea en preparación',reason:'La silueta horizontal consume poca altura y puede acompañar el nombre de una tarea sin simular un progreso numérico.'},
  recipe:recipe('status','edge-on-light-ribbon','#75e9ff','#02040c','50%','9px','Cinta horizontal blanca/cian con halo violeta, torsión alterna y texto inmóvil.'),
  tradeoff:'El brillo blanco del original es muy intenso; a pequeña escala necesita menor halo y una alternativa sin movimiento.',verdict:'probar',why:'El movimiento observado aporta un patrón específico y más ligero que otro indicador circular.',
  demo:`<div class="dsa-ribbon-stage"><svg class="dsa-ribbon" viewBox="0 0 320 90" aria-hidden="true"><path d="M10 45C90 40 135 10 200 30S275 56 310 45C225 51 100 50 10 45Z" fill="#bffcff"/><path d="M10 45C100 46 195 60 310 45" fill="none" stroke="#5774ff" stroke-width="3"/></svg><span>Preparando tu pieza…</span></div>${switcher(24,'Reproducir ciclo de 4 segundos')}`
 }),
 make(25,{
  observations:['Casi todo el encuadre es negro; un haz azul muy saturado nace cerca del centro y se abre hacia abajo.','Un punto blanco pequeño marca el origen de la luz, con una breve línea de texto debajo.','La composición está organizada por un eje vertical y grandes márgenes vacíos.','Hay trazos y ruido azul muy tenues en las zonas oscuras, sin formar controles reconocibles.'],
  motion:staticMotion('Al cambiar el foco entre dos fragmentos, trasladar el origen del haz en 280 ms; apagarlo al quitar el foco.'),
  application:{area:'conversation',component:'Contexto concreto que está mirando el agente',reason:'El haz puede dar una relación visual entre el foco elegido y el contenido, sin convertirlo en una selección permanente.'},
  recipe:recipe('status','cobalt-focus-beam','#244aff','#01020a','18px','20px','Punto de origen, cono estrecho azul y dos destinos de foco locales.'),
  tradeoff:'Un gran haz de color roba atención al texto; en producción debería limitarse a un indicador o borde de contexto.',verdict:'reservar',why:'Útil para estudiar el foco, pero demasiado escénico para una conversación larga.',
  demo:`${choices(25,['Guion','Casting'])}<div class="dsa-beam-stage"><i class="dsa-beam-source" aria-hidden="true"></i><div class="dsa-beam" aria-hidden="true"></div><h3>Una decisión a la vez.</h3><p>El foco cambia. La conversación continúa.</p></div>`
 }),
 make(26,{
  observations:['Una diagonal suave separa gris verdoso claro arriba a la izquierda y negro azulado abajo a la derecha.','El grano es uniforme y visible en el campo claro, sin degradados de varios colores.','La marca y los textos blancos están centrados en una columna estrecha.','La composición utiliza distancias verticales amplias y un pequeño símbolo final como cierre.'],
  motion:staticMotion('Revelar el contenido de marca sin animar el fondo; como máximo, desplazar el plano diagonal 6 px al abrir el panel.'),
  application:{area:'settings',component:'Contexto de marca y cuenta',reason:'Puede dar presencia a una pantalla institucional sin añadir ilustraciones ni métricas.'},
  recipe:recipe('panel','diagonal-studio-signature','#b8d3d0','#1a353b','24px','26px','Campo gris verdoso diagonal, columna centrada y tipografía blanca contenida.'),
  tradeoff:'El tratamiento de póster no sirve para formularios densos; debe quedarse en una cabecera o estado de bienvenida.',verdict:'sutil',why:'La paleta gris y la jerarquía centrada pueden enriquecer un panel pequeño sin alterar el lenguaje del estudio.',
  demo:`<div class="dsa-signature"><strong>braud<span>®</span></strong><p>Tu marca.<br>En cada decisión.</p><details><summary>Ver el contexto ${icon('folder')}</summary><p>Identidad · Producto · Referencias</p></details><span class="dsa-signature-star" aria-hidden="true">✳</span></div>`
 }),
 make(27,{
  observations:['Una cuadrícula de líneas grises delimita una celda central sobre fondo negro.','La huella dactilar está dibujada con contornos finos, casi invisibles por encima de una línea blanca horizontal.','La línea de escaneo rebasa los lados de la celda y proyecta una luz suave hacia abajo.','Pequeños ángulos blancos marcan las esquinas del área enfocada.'],
  motion:staticMotion('Al revisar un recurso, recorrer su tarjeta con una única línea de arriba abajo y dejar después una marca textual de revisión; la imagen no demuestra este recorrido.'),
  application:{area:'library',component:'Revisión de un recurso por el agente',reason:'La delimitación de la celda puede señalar con precisión qué referencia está siendo inspeccionada.'},
  recipe:recipe('status','outlined-resource-scan','#eceff4','#07080a','0px','8px','Celda cuadrada con esquinas abiertas, dibujo de documento y línea de luz horizontal.'),
  tradeoff:'No debe sugerir reconocimiento biométrico ni que el recurso fue validado realmente; la demo indica únicamente una revisión visual propuesta.',verdict:'sutil',why:'La celda y la línea aportan un estado localizado; la huella se sustituye por un documento para evitar un significado incorrecto.',
  demo:`<div class="dsa-scan-stage"><div class="dsa-scan-document">${icon('folder')}<span>Referencia en revisión</span></div><i class="dsa-scan-line" aria-hidden="true"></i></div>${switcher(27,'Probar recorrido de revisión')}`
 }),
 make(28,{
  observations:['Dos puntos blancos altos forman los extremos de una línea horizontal muy fina.','Desde ambos extremos cae una luz triangular que se solapa en el centro.','La palabra FOCUS aparece negra, espaciada y centrada dentro de la parte iluminada.','El resto del plano es negro absoluto, de modo que la iluminación hace de contenedor sin dibujar una tarjeta.'],
  motion:staticMotion('Encender los dos focos al elegir un contexto y recogerlos al quitarlo; transición de 240 ms sin parpadeo ni bucle.'),
  application:{area:'conversation',component:'Aviso breve de foco aplicado',reason:'Permite estudiar una confirmación de contexto que aparece y desaparece sin empujar el historial.'},
  recipe:recipe('status','paired-light-focus','#f1f3f6','#030405','14px','22px','Dos haces blancos forman un único área de foco; el texto no se mueve.'),
  tradeoff:'El texto negro requiere una luz mínima; cuando el foco está apagado debe seguir existiendo una etiqueta accesible y legible.',verdict:'reservar',why:'Es expresivo para una confirmación breve, pero demasiado teatral para mantenerlo fijo en el chat.',
  demo:`${switcher(28,'Poner foco en esta idea')}<div class="dsa-focus-stage"><i class="dsa-light left" aria-hidden="true"></i><i class="dsa-light right" aria-hidden="true"></i><span class="dsa-focus-word">IDEA EN FOCO</span></div><p class="dsa-focus-help">El contexto se prueba aquí. No cambia ninguna conversación.</p>`
 })
];

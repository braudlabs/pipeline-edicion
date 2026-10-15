// Source videos were inspected locally at multiple timestamps. No source media is embedded.
export const studyLinks=[
 {
  id:'75684635-9e2f-4035-874b-0945c0a33fcc',index:64,title:'Glassy motion · Enlace 01',
  url:'https://v1.pinimg.com/videos/iht/hls/1a/fa/4b/1afa4b131991c127457ac6af01743a4c.m3u8',sourceStatus:'visual',
  sourceNote:'Vídeo de 42,283 s, 714 × 504, 60 fps. Revisados 12 momentos del recorrido y 16 fotogramas entre 2 y 8,5 s.',
  observations:['La superficie pasa de una gota redondeada a una barra con iconos; después se convierte en un menú vertical.','Entre 7,5 y 8 s la barra y el botón de cierre se separan. El borde de luz conserva la sensación de un mismo material.','El montaje también muestra switches, deslizadores y lentes transparentes sobre fondos grises y de color.'],
  motion:{observed:true,description:'La geometría cambia de tamaño y proporción; los contenidos aparecen al asentarse la superficie. Los controles se unen y se separan, sin permanecer como tarjetas rígidas.',proposal:'Conservar la transformación de un único contenedor para desplegar herramientas del compositor. En esta prueba el vidrio se ensancha y revela las acciones; no simula la refracción física completa.'},
  application:{area:'conversation',component:'Herramientas del compositor',reason:'Permite reunir las acciones secundarias sin ocupar una fila permanente ni mover el campo donde se escribe.'},
  recipe:{kind:'composer',variant:'morphing-tool-capsule',accent:'#367dff',background:'#b8bec7',radius:999,blur:16,detail:'Contorno iluminado, sombra estrecha y anchura interpolada; los iconos aparecen con un pequeño retraso.'},
  tradeoff:'El morph completo de gota a menú exigiría más complejidad y puede alterar los objetivos de clic. Aquí se limita a una expansión horizontal accesible.',verdict:'probar',why:'Es una transición útil para el chat, además de un acabado de material.',
  demo:`<div class="sld-demo sld-morph"><div class="sld-morph-backdrop" aria-hidden="true"></div><label class="sld-morph-control"><input type="checkbox" aria-label="Desplegar herramientas de la muestra"><span class="sld-tool-capsule"><span class="sld-tool-plus" aria-hidden="true">+</span><span class="sld-tool-items" aria-hidden="true"><span>Imagen</span><span>Archivo</span><span>Voz</span></span></span></label><p class="sld-hint">Pulsa la cápsula para abrir y recoger.</p></div>`
 },
 {
  id:'2b518a77-12e8-471f-a52a-4438e9129df3',index:65,title:'Glassy motion · Enlace 02',
  url:'https://v1.pinimg.com/videos/iht/expMp4/07/18/00/071800b4702b5ea5880bd1cddb3a0e64_720w.mp4',sourceStatus:'visual',
  sourceNote:'Vídeo de 10 s, 720 × 720, 25 fps. Revisados 12 fotogramas entre 0 y 9,9 s.',
  observations:['Una esfera luminosa azul, cian y magenta ocupa el centro de un fondo negro.','Los filamentos interiores cambian de curvatura y el contorno alterna zonas muy brillantes con zonas casi apagadas.','Hacia 7–8 s queda apenas un punto y un arco tenue; al final recupera su volumen. No hay controles ni texto.'],
  motion:{observed:true,description:'La esfera pulsa, se contrae y se reconstruye; la luminosidad se desplaza por el interior y el borde. El volumen visible cambia mucho durante los diez segundos.',proposal:'Reservarlo para una vista de voz activa. La recreación usa capas de luz y contracción; la etiqueta permanece visible aunque la esfera se atenúe.'},
  application:{area:'conversation',component:'Indicador de escucha por voz',reason:'La intensidad y el volumen pueden expresar actividad de audio sin animar el texto del mensaje.'},
  recipe:{kind:'status',variant:'breathing-light-orb',accent:'#70beff',background:'#080a11',radius:999,blur:12,detail:'Esfera con filamentos superpuestos, halo y cambio de escala. La animación se activa expresamente.'},
  tradeoff:'Es demasiado protagonista para acompañar cada respuesta escrita. La demostración es decorativa: no representa audio real ni un porcentaje de progreso.',verdict:'reservar',why:'Tiene sentido como estado de voz, no como decoración permanente del estudio.',
  demo:`<div class="sld-demo sld-orb-stage"><div class="sld-orb-space" aria-hidden="true"><span class="sld-orb"><i></i><i></i><i></i></span></div><label class="sld-control"><input type="checkbox"><span>Animar luz</span></label><p class="sld-hint">Prueba visual de escucha · sin micrófono</p></div>`
 },
 {
  id:'f81bb611-72d1-4d65-909b-705c4f28a8d0',index:66,title:'Glassy motion · Enlace 03',
  url:'https://i.pinimg.com/originals/a0/44/f0/a044f0d638deba9e4e072270caf1d120.gif',sourceStatus:'visual',
  sourceNote:'GIF de 4,04 s, 800 × 600, 101 fotogramas. Revisados 12 momentos del ciclo.',
  observations:['Una línea blanca muy fina atraviesa el fondo negro, rodeada de luz azul y cian.','El punto más brillante se desplaza de un lado a otro y la línea pasa de una curva ascendente a una descendente.','El texto pequeño «Loading…» permanece inmóvil debajo. No aparece un avance medible.'],
  motion:{observed:true,description:'El brillo recorre una cinta estrecha, que se inclina y ondula mientras cambia el grosor luminoso. El ciclo dura unos cuatro segundos.',proposal:'Usar una versión tenue y breve como actividad indeterminada del agente. La prueba conserva el recorrido y la ondulación, sin presentarlo como barra de progreso.'},
  application:{area:'conversation',component:'Actividad del agente',reason:'Ocupa poca altura y deja estable la línea de texto que explica qué está haciendo el agente.'},
  recipe:{kind:'status',variant:'luminous-ribbon',accent:'#59d9ff',background:'#070911',radius:999,blur:7,detail:'Una cinta estrecha y un núcleo luminoso recorren el mismo eje; el texto no se mueve.'},
  tradeoff:'El blanco intenso y el halo original distraerían durante una lectura larga. Conviene reducir el brillo y detenerlo cuando termina la operación.',verdict:'sutil',why:'Su huella pequeña encaja mejor que un spinner grande, siempre ligado a una actividad real.',
  demo:`<div class="sld-demo sld-ribbon-stage"><div class="sld-ribbon-space" aria-hidden="true"><span class="sld-ribbon"><i></i></span></div><p class="sld-ribbon-label">Preparando la respuesta</p><label class="sld-control"><input type="checkbox"><span>Reproducir recorrido</span></label><p class="sld-hint">Muestra de actividad indeterminada</p></div>`
 },
 {
  id:'926663d6-1bbb-421c-9c98-3076085a590b',index:67,title:'Glassy motion · Enlace 04',
  url:'https://v1.pinimg.com/videos/iht/hls/92/33/44/923344d88f63c33207c41d739d9b9590.m3u8',sourceStatus:'visual',
  sourceNote:'Vídeo de 5 s, 720 × 720, 30 fps. Revisados 12 fotogramas entre 0 y 4,9 s.',
  observations:['Un icono de casa permanece fijo dentro de un botón circular, junto al texto «Home».','Un anillo fino contiene destellos azules, amarillos, rojos y blancos. El destello más intenso recorre la circunferencia.','La cápsula oscura exterior y el texto permanecen estables mientras cambia la iluminación del anillo.'],
  motion:{observed:true,description:'Los reflejos giran alrededor del botón durante el ciclo de cinco segundos; el icono central no gira.',proposal:'Aplicar un único recorrido de luz al enfocar o activar un acceso principal. En la prueba se puede mantener el recorrido para observarlo; la versión de producto debería detenerse.'},
  application:{area:'navigation',component:'Acceso activo',reason:'Señala una acción sin desplazar ni reescalar su etiqueta.'},
  recipe:{kind:'button',variant:'orbiting-prismatic-rim',accent:'#77b6ff',background:'#0b0c10',radius:999,blur:5,detail:'Anillo de luz independiente del icono, núcleo oscuro y cápsula exterior estable.'},
  tradeoff:'El arcoíris original compite con el azul de marca. Probar primero un reflejo azul/blanco y reservar varios colores para esta exploración.',verdict:'sutil',why:'El movimiento en el borde puede aportar respuesta táctil sin modificar la geometría del control.',
  demo:`<div class="sld-demo sld-orbit-stage"><div class="sld-home-capsule"><span class="sld-home-gem" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M3 11 12 3l9 8v10h-6v-7H9v7H3Z" fill="currentColor"/></svg></span><span>Inicio</span></div><label class="sld-control"><input type="checkbox"><span>Recorrer el borde</span></label><p class="sld-hint">El icono y el texto permanecen quietos.</p></div>`
 },
 {
  id:'eb11202a-8936-4835-b23a-69a342ea783c',index:68,title:'Glassy motion · Enlace 05',
  url:'https://v1.pinimg.com/videos/iht/hls/84/cd/6c/84cd6c4bdc427adb5aa68bc9e53fe4dd.m3u8',sourceStatus:'visual',
  sourceNote:'Vídeo de 8 s, 704 × 506, 30 fps. Revisados 12 momentos y 16 fotogramas alrededor de los cambios de estado.',
  observations:['La misma pastilla muestra «Thinking…», después «Searching…» y finalmente «Planning…».','Thinking contiene una onda multicolor; Searching muestra reflejos oscuros y grises; Planning enfrenta una zona cian con otra roja.','El contorno y el tamaño permanecen estables. Los cambios de estado son rápidos, cerca de 2,5 y 5,5 s; no se observa un morph largo entre ellos.'],
  motion:{observed:true,description:'Dentro de cada estado hay un flujo lento de luces o fronteras de color. Al cambiar el rótulo cambia también el material interior, sin mover la cápsula.',proposal:'Distinguir los estados reales del agente con una sola pastilla de tamaño fijo. Esta adaptación suaviza el cambio de material y usa el azul de marca; no atribuye al original esa transición.'},
  application:{area:'conversation',component:'Estado del agente',reason:'Permite diferenciar pensar, buscar y preparar sin añadir bloques ni desplazar la conversación.'},
  recipe:{kind:'status',variant:'state-material-pill',accent:'#367dff',background:'#12171c',radius:999,blur:10,detail:'Tres materiales contenidos en una cápsula fija; selección nativa y cambio de luz de 450 ms.'},
  tradeoff:'No deben aparecer «Buscando» o «Preparando» si el sistema no está realizando esas acciones. El color complementa al texto, nunca lo sustituye.',verdict:'probar',why:'Es directamente aplicable a estados existentes y conserva el lugar de lectura.',
  demo:`<div class="sld-demo sld-state-stage"><div class="sld-state-pill"><span class="sld-state-light" aria-hidden="true"></span><span class="sld-state-text sld-think-text">Pensando…</span><span class="sld-state-text sld-search-text">Buscando…</span><span class="sld-state-text sld-plan-text">Preparando…</span></div><fieldset class="sld-state-options"><legend class="sld-a11y">Estado de la muestra</legend><label><input type="radio" name="study-link-68-state" value="think" checked><span>Pensar</span></label><label><input type="radio" name="study-link-68-state" value="search"><span>Buscar</span></label><label><input type="radio" name="study-link-68-state" value="plan"><span>Preparar</span></label></fieldset><p class="sld-hint">Selecciona un estado de muestra.</p></div>`
 },
 {
  id:'48cbd8ca-4fc9-4cd0-a265-807320246440',index:69,title:'Glassy motion · Enlace 06',
  url:'https://v1.pinimg.com/videos/iht/hls/22/cf/a3/22cfa3e4b003e1d086a55ba49e89e0bc.m3u8',sourceStatus:'visual',
  sourceNote:'Vídeo de 12,183 s, 696 × 672, 60 fps. Revisados 12 momentos y 16 fotogramas de la transición, incluidos intervalos de 0,1 s.',
  observations:['Un pequeño control translúcido con símbolo de luz descansa sobre la esquina curva de una tarjeta.','Al pasar al modo oscuro el control recorre el arco hasta el lateral derecho; vuelve arriba al recuperar el modo claro.','La pista queda insinuada por un borde y una estela violeta. El fondo y la tarjeta cambian juntos de gris claro a azul oscuro.'],
  motion:{observed:true,description:'El control sigue un recorrido curvo, no una diagonal recta. En el primer cambio se ve el desplazamiento entre 1,1 y 1,4 s, acompañado por el cambio de tema.',proposal:'Probar un selector de apariencia contenido en su propia tarjeta de ajustes. La demostración cambia solo esta tarjeta y mueve el control por un arco; no altera el tema del estudio.'},
  application:{area:'settings',component:'Selector de apariencia',reason:'Relaciona la posición del control con el cambio de luz sin introducir un elemento flotante sobre el contenido.'},
  recipe:{kind:'slider',variant:'corner-arc-theme-switch',accent:'#9b91e3',background:'#d9dbdf',radius:70,blur:9,detail:'Control que rota alrededor de la esquina; contrarrotación del símbolo, pista y fondo sincronizados.'},
  tradeoff:'Una trayectoria curva es menos convencional que un switch. Debe conservar etiqueta, acceso por teclado y estados claro/oscuro explícitos.',verdict:'reservar',why:'Tiene personalidad como ajuste puntual; no conviene repetir este gesto en todos los controles.',
  demo:`<div class="sld-demo sld-corner-stage"><label class="sld-corner-control"><input type="checkbox" aria-label="Cambiar la apariencia de esta muestra"><span class="sld-corner-card" aria-hidden="true"><span>studio</span><i></i><i></i><i></i></span><span class="sld-corner-track" aria-hidden="true"></span><span class="sld-corner-arm" aria-hidden="true"><span class="sld-corner-knob"><span>☼</span></span></span><span class="sld-corner-label"><span class="sld-corner-light">Claro</span><span class="sld-corner-dark">Oscuro</span></span></label><p class="sld-hint">Pulsa el control · solo cambia esta muestra.</p></div>`
 }
];

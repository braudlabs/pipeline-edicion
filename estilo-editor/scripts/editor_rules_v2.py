#!/usr/bin/env python3
"""Curated hypotheses, evidence and counterexamples. Weights are NOT learned."""
import json
from pathlib import Path
from common import DATOS
O=DATOS/'revision-v2';O.mkdir(exist_ok=True)
def save(name,x):(O/name).write_text(json.dumps(x,ensure_ascii=False,indent=2))
E=[]
def ev(a,b,kind,name,note,level='overview_sampled'):
 E.append(dict(slug='v8',f0=a,f1=b,tipo=kind,nombre=name,nota=note,evidence_level=level,tramo='v8',source_note='notas/v8-revision-v2.md'))
ev(0,97,'enfasis','Si tienes una + agencia de contenido en arco','Frase superior acumulada; caracteres lima recorren arco alrededor de la cabeza. OCR rompe la frase curvada. Intervalo del plano, no primer píxel certificado de cada glifo.')
ev(112,166,'subtitulo_excepcion','Rail alto','Cada / vez / que / entran, alrededor y25%; no y50 universal. Bordes proceden de OCR; se ha inspeccionado muestreo del plano.')
ev(173,327,'enfasis','Nuevos clientes = Nuevos empleados','Primer Nuevos tenue f173; f172 limpio en ROI. Revisión continua168–327. Selección azul con máscara de texto independiente; pelo delante. Separación de tiradores810px f230→2px f255–257→810px f300, centro≈539px. Nuevos sale antes que clientes; = aparece durante cierre; Nuevos vuelve antes que empleados. Ver curvas nativas y grafo de fases en G03; no equivale a escalar horizontalmente la palabra.','native_sequence_measured')
ev(328,451,'enfasis','ESTÁS / MÁS / JODIDO / QUE MI / TÍO / JERRY','Tipografía ultracondensada vertical blanca/lima, detrás del casco. Se ha visto secuencia nativa cada6f, no cada frontera de palabra.','native_sampled')
ev(452,491,'texto','Porque → contratar','Porque f452–462; contratar f463. Entran ya legibles en el mismo ancla central, sin un deslizamiento comparable al héroe. Control nativo continuo450–469.','native_verified')
ev(545,619,'enfasis','no es solo / pagar / otro sueldo','No tenue f545; es f548; pagar primerf550; solo entra551; otro558; sueldo561. Pagar asciende y luego desciende al asentarse; apoyo por palabra con desfases. Tamaño mayor ≠ única animación. Fin por OCR pendiente borde nativo.','native_entry_verified')
ev(643,918,'texto','Rail central sobre primeros planos y acciones','Narración alrededor y50%, incluso sobre boca. La regla evitar toda cara no reproduce este estilo. Intervalos OCR con vacíos y cortes.')
ev(919,1134,'diálogo','Dos voces: narración alta + protesta lima','Narración y20%, diálogo DEJADME/EN/PAZ/JODER! en y50% desde1040 según OCR. Mantener speakerId, color y rango independientes; texto de ropa es diegético.')
ev(1183,1294,'subtitulo_excepcion','Trabajo de encima: rail alto','El contenido físico de caja/personajes ocupa el centro; narración y25%. Hipótesis de espacio narrativo, no causalidad demostrada.')
ev(1497,1598,'diálogo','LET’S GO NENA! diagonal','Lima diagonal arriba a derecha, simultáneo a blanco central; atraviesa paso a B/N. No confundir con una segunda línea de la misma voz.')
ev(1647,1725,'enfasis','el sistema de / Braudd','El empieza1647 tenue; sistema1650; Braudd1653; de1653. Palabras pequeñas ascienden independientemente y se alinean; marca crece en contraste y tiene asentamiento vertical. Cabeza cruza borde inferior del título.','native_entry_verified')
ev(1727,1810,'efecto','B/N en instalación','Plano de maletín/personajes en blanco y negro. No se infiere congelado por desaturación.')
ev(1969,2071,'demostración','Vídeo dentro de móvil','Recurso de teléfono sobre fondo gris iluminado y sombra; narración central continúa. Apariencia no revela si el editor usó 3D o composición2D.')
ev(2112,2272,'superposicion','pone la idea en arco sobre bombilla','Rótulo sigue al objeto al elevarlo, tomarlo y lanzarlo. Revisión global cada30f; inicio2112 es inicio de ventana de búsqueda, no primer píxel exacto.')
ev(2156,2246,'enfasis','y / dirige / el resultado','Lima protagonista con apoyo blanco, convive con arco superior y bombilla. OCR divide dirige/dinge; no dos palabras editoriales diferentes.')
ev(2396,2562,'superposicion','Primera versión: carrusel de resultados','Narración se coloca arriba y≈23.5%; carrusel ocupa centro. Motion muestra resultado/iteración del sistema, no adorno periódico.')
ev(2563,2672,'enfasis','Pregunta construida en seis líneas','¿Que entra directo con corte2563; el cliente entra directo2570. Luego quiere/probar/otro/enfoque?, alterna blanco/lima. Alineación izquierda, cubre intencionalmente rostro. Nativo2558–2585 verifica solo dos primeras entradas.','native_entry_verified')
ev(2690,2780,'enfasis','puedes crear / nuevas / versiones','Jerarquía de tres niveles, lima central. No tiene que ser doble línea; apoyo anterior y posterior separados.')
ev(2788,2928,'enfasis','sin volver a / organizar / una producción desde cero','Jerarquía elevada para dejar carrusel debajo; persona ocluye parte de línea inferior. OCR fragmenta por máscara; no reducir font para reparar falsa lectura.')
ev(2929,3262,'texto','Respuesta y formación: vuelve el rail','Blanco central frente a narración literal. La pista Por fusionada3130–3220 no demuestra que toda frase esté representada: revisión manual necesaria.')
ev(3276,3327,'enfasis','qué / pedir','Héroe lima. Entrada inicial solo OCR; salida3324–3327 ascendente y pierde contraste revisada nativa.','native_exit_verified')
ev(3328,3362,'enfasis','qué / sirve','Primer sirve tenue3328 por abajo mientras pedir aún se desvanece arriba;3330claro;3331alto; luego desciende/asienta. Apoyo qué tiene salida/entrada propia. No reemplazo sin solape ni easing monótono.','native_entry_verified')
ev(3363,3449,'enfasis','y qué hay que / corregir','Apoyo blanco arriba, héroe lima, cambia de plano durante lectura. Tamaño de palabra larga inferior al de pedir; falta identificar fuente exacta.')
ev(3568,3634,'enfasis','el equipo que ya tienes en arco','Arco sobre cabeza en retrato próximo; después composición se revela como foto Team of the Year. Ventana aproximada, no trayectoria medida.')
ev(3635,3708,'demostración','Foto de equipo','Retirada de cámara a fotografía física; rail central. No inferir escala 2D exacta de un efecto de cámara.')
ev(3766,4190,'cta','CTA con rail estable y acción final','Narración central sobre salida del grupo; agencia permanece durante salto final. Negro desde4191 a verificar frontera nativa, sin justificar nuevos cortes en el vídeo del usuario.')
save('v8-events.json',E)
R=[]
def evidence(slug,a,b,observation,level='prior_review'):
 return dict(slug=slug,f0=a,f1=b,observation=observation,level=('this_revision_qualitative' if slug=='v8' and level=='prior_review' else level))
def rule(id,category,title,when,observed,inference,action,exceptions,examples,params=None):
 R.append(dict(id=id,category=category,title=title,when=when,observed=observed,inference=inference,action=action,exceptions=exceptions,evidence=examples,parameters=params or {},status='conditional_hypothesis' if inference else 'observed_constraint',productionValidated=False))
e=evidence
rule('C01','Posición','El ancla pertenece a una composición y a una función','Antes de colocar el primer subtítulo de un bloque.',
 'La narración cambia entre posiciones altas, centro, laterales y baja según plano/capas; se mantiene localmente aunque se mueva la cámara.',
 'La función verbal y la jerarquía del plano explican más que una altura global por marca.',
 'Definir layoutId persistente, railId y coordenadas normalizadas; evaluar zonas durante todo el bloque. Cambiar solo al variar función, plano o competencia entre capas.',
 ['No seguir el centro de la cara cuadro a cuadro.','Una ausencia de colisión no basta para justificar la composición.'],
 [e('v8',919,1134,'Narración y20%; protesta y50%'),e('landing',4738,5077,'Lista izquierda; rail pasa derecha y vuelve tras corte'),e('lafabrica-v2p1',1559,1623,'Derecha50%→centro26% sin corte')])
rule('C02','Posición','El rostro no es una zona prohibida universal','Hay texto sobre el sujeto.',
 'El rail puede cruzar boca/cuerpo; titulares pueden quedar detrás de cabeza, delante de ella o con contorno frontal.',
 'La legibilidad y el efecto de profundidad son decisiones distintas; no resolver ambos con evitar caras.',
 'Separar avoidSemanticObject, allowFaceOverlap y occlusionPolicy; validar máscara por letras/objeto visible.',
 ['No inferir máscara por intersección de cajas OCR.','No usar una elipse genérica como sustituto del pelo/casco.'],
 [e('v8',734,844,'Rail sobre boca en primer plano'),e('landing',913,944,'Funcionan detrás de cabeza y CRT, sin outline'),e('v6-ads90-rev',2120,2220,'Q4 delante, no máscara demostrada')])
rule('C03','Tamaño','Escala de lectura y escala de titular son sistemas distintos','Se decide tamaño de una palabra.',
 'El rail conserva tamaño local aunque cambie la longitud; términos protagonistas alcanzan gran ancho, y palabras largas pueden reducirse.',
 'Rol, énfasis y espacio condicionan escala; número de letras solo impone el ajuste final.',
 'Elegir primero rol y cuerpo óptico de bloque; después shrink-to-fit limitado. No estirar cada palabra al mismo ancho. Registrar tinta real y métricas de fuente por separado.',
 ['Automáticamente grande en ancho puede seguir siendo rail.','No promover cifras automáticamente: dependen del argumento.'],
 [e('v7-ads90-rev',33,373,'Te≈229px vs entrega≈745px dentro del mismo rail grande'),e('v5-maquina',690,723,'Automáticamente≈717px, rail'),e('v5-maquina',2099,2120,'Personalmente reducido para caber')])
rule('C04','Tamaño','No convertir OCR en fontSize','Se ajustan tamaño o fuente a una referencia.',
 'Caja de tinta, caja OCR y cuerpo nominal difieren; máscaras/acentos/fondo alteran mediciones.',
 None,'Ajustar render de glifos sobre ROI nativa, comparar varias palabras no ocluidas, guardar fuente candidata, tracking y error. fontSize=null mientras no esté calibrado.',
 ['Dos fuentes parecidas pueden producir ajustes casi equivalentes.'],
 [e('v5-maquina',390,390,'Montamos: Helvetica Bold IoU .905 frente SFPro .815 en ajuste anterior'),e('v6-ads90-rev',2350,2350,'Analizaremos: Helvetica .910 frente SFPro .800')],{'exactFontRecovered':False,'SFPro':'Decisión de implementación previa, no fuente universal identificada'})
rule('C05','Multilínea','Apoyo + núcleo semántico + remate','Una frase contiene un término que lleva la promesa/coste/acción.',
 'Pequeña línea de contexto, palabra principal grande y a veces complemento inferior; el complemento puede anclarse a izquierda del héroe.',
 'La jerarquía sintáctica permite retener contexto mientras enfatiza el concepto principal.',
 'Segmentar unidades sintácticas, no partir por caracteres. Layout de dos/tres niveles ligado a cajas de tinta. Guardar alignTo=hero.left/center y offsets medidos.',
 ['No toda frase larga se convierte en multilínea.','El apoyo no debe saltar de ancla por cambiar de una a dos líneas sin una transición diseñada.'],
 [e('v8',545,619,'no es solo / pagar / otro sueldo'),e('v8',2690,2780,'puedes crear / nuevas / versiones'),e('v1-pagado',117,137,'ni me han / pagado')])
rule('C06','Multilínea','Compactación sin un interlineado universal','Se compone un bloque con tamaños distintos.',
 'Las líneas forman unidades compactas; algunos apoyos llegan a solapar ópticamente partes de glifos durante entrada.',
 'La masa tipográfica cuenta más que un line-height fijo del contenedor.',
 'Medir gap de tinta por pareja de líneas y por frame, acentos/descendentes, sombra y blur. Proponer gap relativo a altura óptica y comprobarlo visualmente. No copiar 6–8px de V03 como ley de las refs.',
 ['No corregir el movimiento de entrada con un ancla que desplace todo el bloque.','Las composiciones que rodean un objeto no obedecen stack vertical.'],
 [e('v8',550,575,'Apoyos entran separados y se compactan alrededor de pagar'),e('lafabrica-v1',106,121,'Dos flancos alrededor del megáfono')])
rule('C07','Multilínea','Acumulación editorial, no salto automático de línea','Se enfatiza una pregunta, enumeración o demostración verbal.',
 'La pregunta V8 construye seis filas; lista Landing conserva cuatro términos; una frase ordinaria puede reemplazar una palabra cada vez.',
 'Retener términos permite comparar o materializar una idea completa.',
 'Definir grafo de dependencias: aparecer, mantener, sustituir, reubicar; cada palabra lleva tiempos propios. Mantener las ya asentadas si no hay reflow observado.',
 ['No reanimar todas las filas al entrar la siguiente.','No limitar el sistema a máximo dos líneas.'],
 [e('v8',2563,2672,'Pregunta de seis filas, alternancia blanco/lima'),e('landing',4738,5076,'planos/escenas/hooks/visuales persistentes'),e('lafabrica-v2p1',1515,1558,'Frase gráfica refluye al añadirse palabras')])
rule('C08','Multilínea','Dos voces son dos pistas, no una multilínea','Narración y diálogo se superponen.',
 'V8 narra arriba y protesta en lima central; V6rev narra blanco y diálogo amarillo abajo.',
 'Color/posición permiten separar emisores simultáneos.',
 'Asignar speakerId y railId con in/out independientes; alinear cada voz con su frase. Conservar pausa de un hablante mientras sigue el otro.',
 ['La versión original V6 no tiene la misma pista amarilla.'],
 [e('v8',1040,1134,'DEJADME/EN/PAZ/JODER!'),e('v6-ads90-rev',961,1088,'Quiero un UGC... amarillo y completo blanco'),e('v7-ads90-rev',978,1033,'Retiming distinto al V6rev, no offset global')])
rule('A01','Entradas','Sustitución directa del rail','La palabra sirve a lectura continua.',
 'Porque y contratar en V8 aparecen legibles de una vez; Landing la reemplaza es sin fundido visible.',
 'La animación reducida preserva el flujo cuando la imagen ya lleva acción.',
 'Evento replace at frame, sin desplazar el ancla, sin añadir bounce por defecto. Comprobar el frame previo y el primero visible.',
 ['No aplicar a titulares por analogía.'],
 [e('v8',450,469,'Porque452 / contratar463, control continuo','native_review_this_revision'),e('landing',4317,4324,'La4321 sustituye es'),e('v7-ads90-rev',374,385,'¿Pero ya firme en374')])
rule('A02','Entradas','Ascenso desacelerado sin escala probada','Un término protagonista o una fila nueva toma foco.',
 'Gracias y hooks en Landing ascienden con ancho y altura casi constantes; aumenta contraste.',
 'Entrada espacial breve destaca el término sin hacer un pop de escala.',
 'Separar translationY, scale, contrastProxy; ajustar curva a la serie de tinta y guardar dominio/error, no escoger spring por costumbre.',
 ['El contraste medido no es alpha.','OCR temprano puede subestimar caja y simular crecimiento.'],
 [e('landing',9,55,'Gracias: desplazamiento≈48px; ajuste exponencial RMSE .627px'),e('landing',4798,4808,'Hooks: top604→585px; alto118–119, ancho405–407')],{'fitExample':'cy=537.035+46.350*exp(-0.0859*(f-9)), válido f9–55 a60fps; no easing original recuperado'})
rule('A03','Entradas','Ascenso, sobrepaso y asentamiento son fases separadas','Héroe lima en V8 con apoyo escalonado.',
 'Pagar sube entre550–554 y después desciende al asentarse. Sirve entra abajo3328–3331 y desciende después. Los apoyos tienen su propia fase.',
 'El golpe tipográfico usa un sobrepaso controlado; no todos los títulos comparten la curva monótona de Landing.',
 'Modelar preentrada→ascenso→extremo→asentamiento→lectura. Medir extrema y retorno; no reconstruirlo con un fade sin desplazamiento.',
 ['Una sola caja inicial y final oculta el sobrepaso.','No atribuir el nombre de un plugin/spring sin el proyecto.'],
 [e('v8',544,575,'Pagar y apoyos, control continuo','native_review_this_revision'),e('v8',3319,3346,'Pedir sale mientras sirve entra, control continuo','native_review_this_revision')])
rule('A04','Entradas','Parpadeo es un patrón discreto','Un titular usa encendido intermitente.',
 'BLACK tiene opaco/parcial/ausente/parcial; FRIDAY repite el patrón.',
 'Un golpe gráfico estacional puede usar pulsos en lugar de fundido.',
 'Guardar secuencia de estados por fotograma y luego sostener. Mantener fps fuente al convertir tiempos; no interpolar como fade.',
 ['No generalizar a cada titular ni cada corte.'],
 [e('v6-ads90-rev',268,287,'BLACK268opaco269parcial270ausente271parcial272opaco; FRIDAY283–287')],{'period_source_frames':4,'source_fps':60,'period_ms':66.667})
rule('A05','Entradas','Desenfoque direccional y desenfoque de foco no son equivalentes','Una palabra/grupo llega con estela.',
 'Megáfono usa desplazamiento lateral desenfocado; semanas y negaciones muestran arrastre vertical; otros títulos entran con bordes definidos.',
 'Dirección y velocidad del gesto condicionan estela; añadir GaussianBlur global no reconstruye el recurso.',
 'Medir vector del centro, extensión de estela y fase de enfoque. Guardar técnica como desconocida si no puede distinguirse obturador/filtro.',
 ['No introducir blur en una entrada directa nítida.','No inferir ángulo exacto de obturador del MP4.'],
 [e('lafabrica-v1',106,121,'Texto lateral alrededor del megáfono'),e('lafabrica-v2p1',981,995,'3/semanas con arrastre vertical'),e('landing',4798,4808,'Hooks nítido: contraejemplo')])
rule('A06','Entradas','El texto sobre una curva necesita trayectoria por glifo','La frase describe una idea/objeto/sujeto identificado.',
 'Arcos rodean bombilla, cabeza y medalla; cada letra cambia orientación a lo largo del camino.',
 'El texto puede actuar como etiqueta espacial del concepto, no como subtítulo rectangular.',
 'Representar path normalizado, avance por glifo, tangentRotation, startOffset(t), revelado y vínculo a objectId. Separar movimiento del objeto del desplazamiento sobre path.',
 ['No rotar la frase entera como un bloque.','No usar OCR como geometría del arco.'],
 [e('v8',0,97,'Agencia de contenido'),e('v8',2112,2272,'Pone la idea sigue bombilla'),e('lafabrica-v2p1',1245,1289,'60 días de soporte en medalla')])
rule('A07','Salidas','Solapamiento entre eventos y salida autónoma','Entra la frase siguiente o cambia la palabra protagonista.',
 'Gracias y Te coexisten; pedir se desvanece arriba mientras sirve aparece abajo; otros textos salen con corte.',
 'La continuidad verbal puede enlazarse con continuidad espacial sin borrar todo entre palabras.',
 'Guardar lastPixel de saliente y firstPixel de entrante; permitir overlap controlado con prioridades de lectura. No establecer exit=startNext por defecto.',
 ['El caso A PAGAR→APAGAR tiene1f vacío y sustitución; no morph.'],
 [e('landing',86,96,'Te86 y Gracias hasta89'),e('v8',3324,3330,'Cruce de pedir/sirve'),e('v5-maquina',1794,1803,'1797vacío1798APAGAR')])
rule('T01','Tipografía','Cambio de voz tipográfica por bloque semántico','Un remate o una palabra clave requiere otro tono.',
 'V8 usa ultracondensada para Jerry y sans para explicación; V3 usa serif para costes/proceso/resultado/negocio, pero otros énfasis son sans.',
 'La fuente distingue la función dramática del bloque; no cambia aleatoriamente por palabra.',
 'Catalogar familia visual, proporciones, peso, caja, tracking, color y efectos por función. Buscar fuentes por ajuste de glifos y declarar candidatas.',
 ['No afirmar nombre exacto sin ajuste suficiente.','No asumir que lima significa siempre serif.'],
 [e('v8',328,451,'Remate condensado muy alto'),e('v3-ia-cara',717,823,'QUÉ/PROCESO/RESULTADO serif'),e('v3-ia-cara',1192,1275,'Generaciones/consistencia/artificiales sans lima')])
rule('T02','Tipografía','El color codifica rol o foco dentro de la paleta','Se decide segundo color.',
 'Blanco es frecuente en lectura; lima/verde/amarillo pueden marcar palabra principal, hablante o alternancia de conceptos.',
 'Color tiene función local, no correspondencia global fija.',
 'Asignar colorRole por layout y speaker; mantener coherencia dentro del bloque y contraste con vídeo real. Extraer muestras de interior de glifos, no bordes mezclados.',
 ['No copiar lima a Birdieballs sin adaptar paleta.','No interpretar cada cambio de RGB del MP4 como animación de color.'],
 [e('v8',2563,2672,'Blanco/lima por fila'),e('v8',1040,1134,'Lima para otra voz'),e('v1-pagado',476,496,'Mejor verde')])
rule('M01','Máscaras','Relleno detrás y contorno delante requieren capas distintas','Un texto conserva silueta sobre la cabeza.',
 '30 y curso tienen relleno ocluido pero contorno delante; funcionan de Landing no muestra ese outline.',
 'El contorno conserva reconocimiento sin perder profundidad.',
 'Componer fondo→relleno→recorte sujeto→contorno opcional→apoyos frontales. Máscara comparte frame,crop,transform y blur del metraje. Medir oclusión efectiva por palabra.',
 ['Contorno no es sombra.','No aplicar máscara a todos los objetos claros del set.'],
 [e('v1-pagado',35,88,'30 tras cabeza y outline frontal'),e('v1-pagado',1272,1320,'Curso'),e('landing',913,944,'Sin outline'),e('v3-ia-cara',1410,1434,'CLIENTES tapa softbox pero no cabeza')])
rule('M02','Máscaras','La máscara puede aplicarse a un rail grande','La narración completa se integra en escena.',
 'Oficina de V5 y almacén de V6rev usan palabra a palabra grande detrás del sujeto con contorno.',
 'Modo de lectura y profundidad son ejes independientes.',
 'Permitir maskPolicy por layout además de hero; no codificar masked como una única receta de palabra clave.',
 ['V7gancho grande delante: tamaño no implica máscara.'],
 [e('v5-maquina',1546,1666,'Rail gigante máscara+contorno'),e('v6-ads90-rev',1511,1687,'Almacén grande con máscara'),e('v7-ads90-rev',33,373,'Grande frontal')])
rule('G01','Motion','El disparador es una función narrativa','Se decide insertar una representación gráfica.',
 'Precio, coste acumulado, comparación, pasos y demostración tienen tratamientos propios. Hay extensos bloques sin interludio gráfico.',
 'La gráfica aparece cuando vuelve visible una relación que la persona/escena no expresa por sí sola.',
 'Etiquetar función cuantificar/comparar/explicar_proceso/demostrar/reencuadrar_concepto. Exigir evidencia pertinente y objeto narrativo antes de proponer escena.',
 ['No poner un icono por sustantivo.','No confundir objeto dentro del metraje con overlay creado por el editor.'],
 [e('v1-pagado',176,225,'Precio300€'),e('v1-pagado',383,449,'30variantes→coste mínimo'),e('lafabrica-v2p1',343,504,'Sistema y comparación'),e('v8',2396,2562,'Resultados y primera versión')])
rule('G02','Motion','No hay periodicidad universal demostrada','Se distribuyen escenas gráficas.',
 'Los intervalos entre inicios anotados varían por pieza. LaFabrica concentra tarjetas semanales cercanas; V5 cuenta mediante escena física.',
 'La cadencia responde a estructura del argumento y medio de representación, no a un temporizador fijo.',
 'Calcular distribuciones por familia y función; separar interludio,overlay,UI en escena,VFX y cámara. Conservar intervalos de origen y denominador del censo.',
 ['Cero eventos etiquetados no prueba cero motion.','V6/V6rev/V7 no son tres muestras independientes.'],
 [e('lafabrica-v2p1',996,1289,'Semanas1/2/3 + soporte'),e('v1-pagado',176,449,'Dos gráficos tempranos'),e('v5-maquina',0,2290,'Escenificación, no interludios independientes anotados')])
rule('G03','Motion','Coreografía causal con fases','Se diseña una gráfica de varios conceptos.',
 '30 crece, aparece variantes, el grupo viaja y cede foco a mínimo; reloj sale y hucha entra en un mismo desplazamiento. V8 contrae una selección, recorta clientes, presenta = y reabre para empleados, con timings independientes.',
 'La transformación de un elemento prepara el siguiente y guía la mirada.',
 'Definir estado inicial, cambio de información, vector compartido, relevo de foco, asentamiento y salida. Todo movimiento debe cambiar posición, jerarquía, relación o legibilidad.',
 ['Sostener una cifra puede ser correcto mientras otra capa cambia.','No añadir wobble para cumplir un límite de quietud arbitrario.'],
 [e('v1-pagado',383,449,'Contador y viaje arriba-izquierda'),e('v2-churros',760,793,'Tiempo/reloj→Dinero/hucha'),e('v3-ia-cara',760,823,'Proceso→Resultado con relevo diagonal'),e('v8',196,327,'Clientes→igualdad→empleados: tiradores medidos y secuencia nativa continua','native_sequence_measured')])
rule('G04','Motion','Material, luz y profundidad forman parte del diseño','Se crea un fondo gráfico.',
 'Hay oliva texturizado/viñeta, charcoal, gris iluminado con sombras y naranja con medalla. El material depende de la escena.',
 'La coherencia entre objetos, luz, textura, cámara y tipografía produce calidad; no la suma de filtros.',
 'Guardar mapa de luz/grano, escala de textura, sombras de contacto/proyectadas, material del objeto, profundidad y vector cámara. Validar frame quieto y transición.',
 ['El fondo lima plano V3existe: textura no es ley universal de toda referencia.','Para Birdieballs el usuario sí rechazó fondo verde plano.'],
 [e('v1-pagado',383,449,'Oliva, textura y viñeta'),e('v8',1969,2071,'Gris iluminado, móvil y sombra'),e('v3-ia-cara',1135,1176,'Fondo lima con rail negro: contraejemplo')])
rule('G05','Motion','Contadores: curva del valor y cámara separadas','Se anima una cantidad.',
 '30usa incrementos decrecientes; contador monetario Landing avanza≈84/85€ por frame en tramo final y tiene dígitos fantasma.',
 'El redondeo numérico y la transformación espacial cumplen funciones distintas.',
 'Guardar value(t),rounding,format,oldDigitTreatment,objectTransform,cameraTransform. Ajustar curva al segmento completo antes de generalizar.',
 ['No reconstruir easing de toda subida con solo cola lineal.'],
 [e('v1-pagado',389,398,'1,6,15,21,24,26,28,29,29,30'),e('landing',2213,2317,'€ tarjeta con sombra y arrastre de cifras')])
rule('G06','Motion','UI y objetos en escena no son captions','OCR detecta pantallas, ropa, logos o controles.',
 'BRAUD en monitor sigue perspectiva; V8 tiene texto en caja/ropa y carrusel con controles diminutos.',
 None,'Clasificar cada objeto textual: caption,hero,dialogue,label,diegetic,UI,noise. Mantener unknown cuando no se haya verificado. Nunca contar todos los tracks OCR como subtítulos.',
 ['Un logo legible no demuestra capa3D editada independientemente.'],
 [e('v6-ads90-rev',563,642,'Marca en monitor'),e('v8',1372,1464,'BRAUDD en caja'),e('v8',2420,2562,'Controles carrusel')])
rule('E01','Efectos','Efecto ligado a argumento, gesto o cambio de registro','Se selecciona un efecto sobre imagen.',
 'Recuadros señalan errores de cara/manos; damero representa recorte; B/N acompaña remate; silueta blanca oculta cambio de plano.',
 'Los efectos hacen visible el significado o marcan un registro narrativo.',
 'Registrar trigger exacto, ámbito del efecto, duración, capas afectadas y evidencia. Distinguir imagen completa/persona/objeto/texto.',
 ['B/N no prueba freeze.','Un flash de sujeto no autoriza un flash global.'],
 [e('v2-churros',209,239,'Errores señalados cara/manos'),e('v3-ia-cara',1428,1434,'Silueta blanca solo persona'),e('v7-ads90-rev',374,416,'B/N con movimiento')])
rule('E02','Tiempo','El caption puede atravesar un corte','La frase sigue al cambiar plano.',
 'Servicio, voilà,10 y palabras ordinarias empiezan antes o persisten después de cortes.',
 'Continuidad semántica domina sobre la división física del metraje.',
 'Mantener eventos de texto en tiempo maestro, independientes de clips. Corte no reinicia automáticamente animación ni frase.',
 ['Un nuevo plano puede justificar otro layout, pero requiere una decisión explícita.'],
 [e('v6-ads90-rev',1191,1262,'Voilà entra antes1197'),e('landing',4506,4679,'Variaciones/probar/diferentes atraviesan planos'),e('v8',3363,3449,'Corregir cruza a plano de equipo')])
rule('E03','Tiempo','Hay omisiones y pausas deliberadas','La imagen o reacción ya lleva la información.',
 'Hay tramos sin rail con voz o reacción; el nombre ya visible en la pantalla puede sustituir al rail.',
 'La ausencia de subtítulo puede evitar duplicación y dejar leer acción.',
 'Etiquetar omissionReason y rango; no considerar todo hueco OCR como omisión. Comparar audio/transcripción y evidencia nativa.',
 ['No suprimir palabras solo porque falló OCR.'],
 [e('v5-maquina',802,1031,'Narración/acción sin rail ordinario'),e('v6-ads90-rev',1263,1307,'Reacción sin rail'),e('landing',3976,4312,'Making-of y producto')])
rule('S01','Sonido','Detectar cuándo no identifica qué sonido','Se estudia sonido de una exportación mezclada.',
 'Los análisis disponibles contienen onsets y bandas espectrales; no identificaciones auditivas verificadas.',
 None,'Usar waveform/STFT para proponer ventanas; escuchar/contextualizar, clasificar familia y contrastar candidatos de biblioteca. Guardar unknown y confianza si no hay evidencia.',
 ['Fricativas, golpes de voz y percusión confunden detector.','No asignar whoosh a todos los onsets.'],
 [],{'stft_window':2048,'sample_rate':44100,'hop':441,'temporal_step_ms':10,'frequency_bin_hz':21.533,'identificationComplete':False})
rule('S02','Sonido','Familia acústica y sample exacto son niveles distintos','Se necesita imitar el sonido.',
 'La forma espectral no lleva el nombre del archivo original.',
 None,'Clasificador/embeddings sugieren familia y vecinos; fingerprint/correlación buscan coincidencia en biblioteca conocida; confirmar ataque,cuerpo,cola,pitch,time-stretch,mezcla. Sin candidato no emitir assetId exacto.',
 ['Separación de fuentes puede crear artefactos.','Con stems/proyecto original la identificación puede ser directa.'],
 [],{'levels':['onset_window','perceptual_family','catalog_candidate','verified_sample'],'primarySources':['https://github.com/LAION-AI/CLAP','https://github.com/dpwe/audfprint','https://github.com/Audio-AGI/AudioSep']})
rule('Q01','Validación','Conservar la edición de entrada','El material del usuario ya está montado y no pide cortes.',
 'Ale rechaza los cortes añadidos a Birdieballs.',
 None,'Usar una base continua con sourceFrameMapping1:1. Bloquear reorder,trim,speedRamp y transiciones que alteren tiempo salvo autorización específica. Probar duración,orden,PTS y continuidad del audio.',
 ['Se puede elegir una ventana de20s para prueba sin alterar el orden dentro de ella.'],[],{'authority':'Feedback explícito de Ale','default':'preserve_source_timing'})
rule('Q02','Validación','Una prueba debe contener edición final del tramo','Se presenta un fragmento para feedback.',
 'Ale pide20s completos con subtítulos, efectos,motion y sonido integrados.',
 None,'Diseñar y validar una unidad completa corta; conservar versiones y vincular feedback por frame. No presentar solo subtítulos como edición final.',
 ['La tarea actual es estudio; no renderizar otra propuesta antes de trasladar el criterio.'],[])
rule('Q03','Validación','No certificar estilo con tests de geometría','Se valida una nueva receta/motor.',
 'V03pasó pruebas técnicas y fue rechazada por calidad y semejanza.',
 None,'Separar testsfuncionales, comparación perceptual por recurso y aprobación del usuario. Evaluar temporalidad,paleta,fuente,masa,oclusión,causalidad y audio a velocidad real.',
 ['Más reglas y más tokens no sustituyen la comparación visual.','Una aprobación parcial no aprueba toda la pieza.'],[])
rule('G07','Motion','Separar metraje de base y aportación de edición','Hay acceso al bruto de la misma escena.',
 'En V8 la bombilla flotante ya está en el bruto; el arco de texto se añade. El teléfono con fondo gris no está en el bruto. En V5 la máquina y tarjetas en vuelo ya están presentes.',
 'La dirección del motion añadido debe aprenderse separada de la escenificación/generación de los clips.',
 'Vincular SHA del bruto y del editado, alinear cada intervalo, modelar recorte/color/tiempo y anotar baseVisual,addedText,addedGraphic,addedEffect,unknown. Construir máscara por diferencia solo tras verificar alineación. Excluir objetos del bruto al calcular cadencia de motion añadido.',
 ['Nombres de archivo y similitud no prueban correspondencia.','El tiempo puede variar dentro de un mismo anuncio; no aplicar un único offset global.','Landing y LaFabrica no tienen bruto correspondiente identificado en la nueva entrega.'],
 [e('v8',2160,2160,'Bombilla presente en bruto; pone la idea/dirige añadidos','raw_edited_pair_reviewed'),e('v8',1980,1980,'Metraje dentro de teléfono añadido','raw_edited_pair_reviewed'),e('v5-maquina',120,120,'Máquina/tarjetas y blur presentes en bruto','raw_edited_pair_reviewed')],
 {'pairs':'datos/raw-comparison/pairs.json','rawManifest':'datos/raw-comparison/manifest.json','ui':'http://127.0.0.1:4317/raw-study','alignment':'scene-correspondence reviewed; exact temporal mapping pending'})
fontfile=O/'v8-font-calibration.json'
if fontfile.exists():
 fonts=json.loads(fontfile.read_text());r=next(r for r in R if r['id']=='C04')
 r['parameters']['V8_multiword_font_fit']=[{'text':w['text'],'frame':w['frame'],'bestCandidate':w['candidates'][0]['font'],'IoU':w['candidates'][0]['iou'],'size':w['candidates'][0]['size'],'trackingPx':w['candidates'][0]['trackingPx']} for w in fonts['words']]
 r['parameters']['V8_caution']='SF Pro Display Regular is a strong local candidate for these two heroes, not universal font identification. Size/tracking are calibrated fits, not original project values.'
fitfile=O/'v8-motion-fit.json'
if fitfile.exists():
 fit=json.loads(fitfile.read_text());r=next(r for r in R if r['id']=='A03');r['parameters']={'measuredProfile':'datos/revision-v2/v8-motion-fit.json','formula':fit['model'],'decayPerSourceFrame':fit['decayPerSourceFrame'],'omegaRadiansPerSourceFrame':fit['omegaRadiansPerSourceFrame'],'trainingRMSEpx':fit['trainingRMSEpx'],'trainingSamples':fit['trainingSamples'],'heldOutEntryRMSEpx':fit['heldOut']['entryPhaseReview']['rmsePx'],'heldOutFullRangeRMSEpx':fit['heldOut']['rmsePx'],'caution':'Posición solamente. Ajuste a pagar/Braudd; sirve coincide durante entrada pero diverge al salir. Separación exploratoria por fases, no validación del estilo completo.'}
selectorfile=O/'v8-selector-curves.json'
if selectorfile.exists():
 selector=json.loads(selectorfile.read_text());r=next(r for r in R if r['id']=='G03')
 r['parameters']={
  'measuredProfile':'datos/revision-v2/v8-selector-curves.json',
  'coordinates':'1080×1920; source60000/1001fps; handle medians, not glyph bounds',
  'handleSeparationPx':{str(row['frame']):row['threshold70']['separationX'] for row in selector['rows'] if row['frame'] in [230,235,240,250,255,256,257,258,265,270,280,290,300]},
  'midpointXRangePx_196_326':[538.5,540.5],
  'thresholdSensitivityPx_196_326':{'median':0,'maximum':1},
  'observedPhaseGraph':[
   {'frames':[196,230],'state':'Nuevos + clientes; texto recortado por pelo delantero; selección abierta'},
   {'frames':[231,257],'state':'Nuevos sale; caja se cierra; clientes conserva forma de glifos mientras máscara estrecha área visible; = toma el contexto superior'},
   {'frames':[255,257],'state':'Separación horizontal≈2px; = visible, sin palabra central legible'},
   {'frames':[258,265],'state':'Selección reabre; Nuevos regresa antes de empleados'},
   {'frames':[266,299],'state':'empleados aparece desde abajo dentro de máscara que sigue abriendo; sus extremos aún recortados'},
   {'frames':[300,326],'state':'Lectura Nuevos empleados; cabeza vuelve a ocluir borde inferior'},
   {'frames':[327,328],'state':'Nuevos y tirador superior ya no visibles327; empleados y tirador inferior persisten327; corte328'}
  ],
  'requiredIndependentTracks':['selectionLeftX','selectionRightX','selectionFill','upperContext','centralTextTranslateY','centralTextClip','foregroundSubjectMask'],
  'caution':'El grafo es observación localizada; no recupera alpha, fuente o easing original. Hitos de legibilidad revisados en hojas reducidas, no primer píxel certificado de cada letra.'
 }
save('rules.json',R)
print(len(R),'conditional rules;',len(E),'V8 observations')

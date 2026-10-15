# V8 · revisión V2

Fuente: BRAUDLABS - V8.mp4, 1080×1920, 60000/1001fps,4290frames. SHA256 en `datos/referencias.json`. No se modificó el vídeo. Audio original conservado; **sin identificación auditiva certificada de SFX**.

## Cobertura real

- Vision nativo:4290/4290frames.371pistas OCR; incluyen texto de ropa/caja/controles y errores del texto curvado. No son371subtítulos.
- ASR:224palabras; necesita corrección de marca, diálogo superpuesto y frases como sacarle/sin ti.
- Auditoría nativa por hash:99frames idénticos al anterior. La heurística legacy omitía1708frames no idénticos; no usarla como equivalencia exacta.
- Seis panorámicas vistas: f0..4260 cada30frames. Esto es muestreo general, no lectura de cada frame.
- Recortes obtenidos a resolución nativa, vistos en hojas reducidas: f168–327,544–575,1640–1667,2558–2585,3319–3346,450–469,3349–3364 sin saltos. Ventana324–455 vista cada6frames. Detalles230/240/256/270 ampliados en selector-detail.
- Medidas cromáticas automáticas nativas:549–619,1652–1725,3328–3361; no sustituye inspección de todos esos cuadros.
-26observaciones en `datos/revision-v2/v8-events.json`; inicios/fin aproximados se distinguen de fronteras inspeccionadas.

## 1. Layout y texto

Gancho: Si tienes una arriba, agencia de contenido en arco lima rodeando al personaje. La curva hace que Vision lea fragmentos, rotaciones espurias y palabras inventadas. Luego cada/vez/que/entran en y≈25%. No extraer de ello un cuerpo universal ni mover el ancla por cara cada frame.

f173primer Nuevos visible tenue en el recorte inspeccionado;172sin texto discernible. Selector azul comienza como línea/tirador y se abre hacia los lados; clientes queda detrás del pelo. El marco no aparece como rectángulo completo de golpe. La equivalencia clientes→empleados usa **recorte de palabras dentro de selección que se contrae y expande**, no escala horizontal del texto. Ver medida de tiradores abajo. No se ha recuperado alpha/fuente ni cada primer píxel de apoyo.

### Selección clientes → empleados: capas y fases

Secuencia196–327 revisada sin saltos en tres hojas nativas reducidas. La palabra clientes conserva la forma de los glifos mientras desaparecen los extremos y queda una franja central; detalle240 muestra el recorte. Empleados entra desde abajo mientras la ventana se abre; sus extremos siguen recortados en270. El pelo pasa por delante de selección y texto; no es solo una máscara rectangular de layout.

- Lectura hasta230: Nuevos encima de clientes, selección abierta.
-231–257: Nuevos sale primero; clientes cae mientras la selección se cierra hacia su centro; el signo igual ocupa la línea superior. No convertir esto en un morph clientes→empleados.
-255–257: selección casi cerrada, separación horizontal de tiradores≈2px; signo igual legible.
-258–265: empieza reapertura y vuelve Nuevos, antes que empleados.
-266–299: empleados entra dentro de la ventana que sigue ensanchándose; el bloque se asienta.
-300–326: lectura sostenida; el sujeto vuelve a tapar parte inferior.327ya no se distingue Nuevos ni círculo superior; palabra y tirador inferior persisten hasta corte328.

`measure_v8_selector.py` mide medianas de máscaras azules en dos bandas de altura fija. Distancia entre tiradores:810px f230;574f235;202f240;22f250;2f255–257;127f260;458f265;614f270;758f280;806f290;810f300. Centro x538,5–540,5px en196–326. Dos umbrales dan diferencia mediana0px y máxima1px. Medida de control de selección, **no ancho de texto, fontSize ni alpha original**. f327se rechaza por pérdida de círculo superior. La apertura inicial no se declara totalmente medida porque el segundo tirador aún no supera el criterio de píxeles fiables en varios frames.

Curvas completas en `datos/revision-v2/v8-selector-curves.json`; gráfico en `v8-selector-comparison.svg`; fases y pistas independientes en G03. Cierre y reapertura tienen duraciones diferentes; no copiar la salida invirtiendo la entrada.

f328–451, remate: ESTÁS/MÁS/JODIDO/QUE MI/TÍO/JERRY en tipografía ultracondensada, alto contraste vertical. Lima en JODIDO, blanco en resto observado. Casco oculta parte inferior; los personajes laterales pueden quedar atravesados por glifos. Esto no se reproduce cambiando simplemente el fontSize de la fuente del rail.

f452Porque entra nítido con plano nuevo. Se mantiene hasta462;463contratar sustituye directamente. No hay un bounce visible equivalente a pagar. Coordenadas de rail≈x50%,y50%.

f545no tenue;548es;550pagar;551solo;558otro;561sueldo. Los apoyos entran desde abajo por palabra y se reagrupan, mientras pagar asciende/sobrepasa/asienta. Otro sueldo se instala a izquierda bajo el héroe, no centrado como bloque independiente. El blanco no debe contabilizarse dentro de la selección de tinta lima.

Rail en primer plano puede cruzar boca. Desde919la narración ocupa y≈20%; protesta lima desde1040en y≈50%. Color no es decoración arbitraria: representa otra voz en este caso. En1497+LET’S GO NENA aparece diagonal arriba/derecha mientras la narración sigue en centro y el metraje cambia a B/N.

Marca: el1647tenue, sistema1650, Braudd1653, de1653. Los apoyos entran individualmente y se alinean arriba. Braudd tiene entrada vertical con sobrepaso, no un fundido inmóvil. La cabeza ocluye borde inferior según avanza el plano.

Bombilla: pone la idea recorre un arco que sigue la bombilla; al cogerla y lanzarla cambian tanto el objeto como el texto. Al mismo tiempo y/dirige/el resultado ocupa tres niveles abajo. Se necesitan transformaciones de objeto y de texto local separadas.

Pregunta2563–2672: seis líneas alineadas a izquierda. ¿Que aparece directo con corte2563; el cliente aparece directo2570, sin la entrada de pagar. Las filas posteriores se acumulan. Blanco/lima alternan. No se evita sistemáticamente el rostro del personaje de derecha.

Puedes crear/nuevas/versiones: tres niveles, lima grande. Sin volver a/organizar/una producción desde cero: bloque alto que deja sitio al carrusel. La cabeza tapa fragmentos de la línea inferior; una caja OCR cortada no justifica encoger la fuente.

Pedir→sirve: el apoyo qué sale y vuelve con su timing. Pedir asciende y pierde contraste3324–3327; sirve aparece desdeabajo3328, claro3330. Hay solape. Entrada y salida no son un reemplazo instantáneo ni un morph de letras.

Salida de sirve revisada3349–3364: palabra empieza a divergir de la curva de asentamiento antes de desaparecer; corte de plano3359, todavía hay texto;3360–3362se desvanece,3363ya solo y qué/hay del siguiente apoyo. La salida atraviesa el corte.

## 2. Medida nueva: trayectoria compartida de héroes

Máscara cromática nativa: G−R>c,R−B>c,R>85,G>125; comparar c15/c30; caja percentil0,2–99,8. Se amplió ROI inicial porque recortaba el extremo superior: aquellas medidas iniciales se descartaron. La nueva ROI contiene el desplazamiento completo. Persisten incertidumbre de compresión/umbral/solapes.

Pagar, umbral30: ancho834–835px desde edad2 en gran parte del tramo. Top970px en552,935en556,988en565/566; vuelve a969en575–577. No es una escala que crece hasta ancho final: la anchura es estable y la posición oscila.

Braudd: ancho808px; top408en1655,374en1659,427en1669,407en1679. Las mismas fases ocurren a las mismas edades desdeprimerframevisible:6fextremo alto,16fextremo bajo,26fextremo alto menor. T≈20f=333,67ms entre extremos deigualsigno; amplitud decrece.

Ajuste conjunto a pagar/Braudd, edades2–60,118muestras:

`y = offset_layout + exp(-0.099*a) * (37.833776*cos(0.313*a) - 60.958008*sin(0.313*a))`

`a`=edad en frames del origen60000/1001fps. Offset de pagar973,9069px; de Braudd412,3815px. RMSE entrenamiento0,3551px. Ajuste de posición de tinta; **no recuperación del plugin ni easing original, alpha o fuente**.

Contraste sirve con curva fija y un único offset calibrado enedad2:
- Edad2–23:RMSE1,2324px,máximo1,7633px.
- Todo2–32:RMSE14,2953px,máximo56,2558px; contiene salida/cambio deestado.
- División de fases exploratoria tras revisar residuos y salida nativa, no benchmark predeclarado. Se conserva el error completo del rango válido. Frame3361excluido porque la máscara conserva solo263píxeles frente a≈99.000durante lectura; sus medidas fragmentadas siguen guardadas como rechazadas. Esto respalda reutilización de trayectoria de entrada dentro de V8, no certifica equivalencia entre vídeos.

Valores y filas en `datos/revision-v2/v8-motion-fit.json`. Evaluador determinista en `motor-editor/forensics/reference-motion.mjs`, con extrapolación prohibida por defecto fuera del dominio medido.

## 3. Motion y sonido

Móvil sobre fondo gris iluminado con sombra1969–2071; bombilla y arco2112–2272; carrusel de resultados2396–2562ysegunda iteración2820+; equipo que ya tienes en arco3568+ y retirada a fotografía3635+. En distintos casos el recurso está integrado con metraje; la apariencia no revela backend3D/2D ni autoría separada del editor.

No se puede concluir periodicidad universal. Los focos se agrupan en promesa, mecanismo, objeción/respuesta y formación. La lista de eventos sigue abierta; no contar cero interludios con etiqueta literal grafico como cero motion.

Audio:180onsetsautomáticos, sonoridad medida−13,5LUFS,pico+0,5dBTP. Esas métricas no identifican un whoosh ni demuestran ducking. No usar el estimador de tempo/graves o los valores internos de ducking como propiedades editoriales certificadas. Falta escucha semántica/identificación de biblioteca.

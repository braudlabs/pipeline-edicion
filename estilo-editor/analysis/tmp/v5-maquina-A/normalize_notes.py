from pathlib import Path
import json
BASE=Path('analysis/notas')
def ev(tipo,a,b,nombre,texto='',detalle=''):
 return dict(tipo=tipo,f0=a,f1=b,nombre=nombre,texto=texto,detalle=detalle)
def write(id,slug,a,b,fps,sections,events):
 cov=json.loads((BASE/(id+'.coverage.json')).read_text())
 header=f'# {slug} · f{a}–f{b} · {id}\n\nEstado: **partial**. Pasada densa y suplementos completos; revisión nativa de eventos parcial. {fps:g} fps, 1080×1920. Rango {(a/fps):.3f}–{((b+1)/fps):.3f} s. Fotogramas inclusivos; t=f/fps. Digest completo leído. Nombres exactos de hojas, rangos nativos y espectros en cobertura adjunta.\n\n'
 header+='Las hojas densas originales omitían similitudes JPEG, no solo duplicados exactos; los suplementos restituyen las exclusiones no idénticas. La extracción nativa aquí citada usa select por índice corregido. dapi probe falló EPERM localhost; audio no escuchado ni retranscrito.\n\n'
 titles=['Planos','Cortes y transiciones','Subtítulos base','Palabras de énfasis y tipografía cinética','Escenas gráficas (motion graphics)','Superposiciones y efectos sobre la imagen','Sonido','Ritmo','Reglas que se deducen de este tramo','Dudas y lo que no se pudo verificar','Láminas guardadas']
 text=header+'\n\n'.join(f'## {i+1}. {title}\n\n{s}' for i,(title,s) in enumerate(zip(titles,sections)))
 text+='\n\nLos sucesos siguientes son un inventario visual de los eventos principales; no un certificado de verificación nativa exhaustiva. f0/f1 son límites de lo observado, con incertidumbres explícitas en detalle.\n\n```json\n'+json.dumps(sorted(events,key=lambda e:(e['f0'],e['f1'])),ensure_ascii=False,indent=2)+'\n```\n'
 (BASE/(id+'.md')).write_text(text)
common_doubt='La pasada completa por hojas no resuelve la precisión de todos los bordes de entrada/salida, ni curva/easing o RGBA exactos. Solo los rangos nativos enumerados en coverage se controlaron a resolución original. No atribuir SFX por espectro ni fps del metraje por +k. La relación con words.json tiene error ≈±50 ms. Cortes y tamaños leídos en miniatura conservan incertidumbre; no reconstruir trayectorias 3D ni separar cámara física de zoom digital sin evidencia.'
write('v5-maquina-A','v5-maquina',0,801,30000/1001,[
'''| Fotogramas | Duración | Imagen y movimiento |
|---|---:|---|
|0–139|140f /4,671s|Picado: hombre gafas rojas, chaqueta naranja/camisa morada/pantalón beige izquierda, máquina derecha, estudio gris. Cámara retrocede; cara14,7→6,8%H.|
|140–172|33f /1,101s|Piernas y tarjetas al suelo, color.|
|173–196|24f /0,801s|Perfil junto máquina; tres tarjetas en suelo.|
|197–403|207f /6,907s|Cambio toma/escala mismo lugar; máquina multiplica tarjetas delante cuerpo.|
|404–494|91f /3,037s|Recurso máquina sola lanzando tarjetas.|
|495–521|27f /0,901s|B/N máquina, geometría aparentemente retenida; ver límite de congelado en§6.|
|522–801|280f /9,343s|Personaje rodeado de montón de tarjetas. Se atenúa al final.|''',
'''Secos visibles f140(4,671s),173(5,772s),197(6,573s, salto toma mismo lugar),404(13,480s, máquina sola),522(17,417s, vuelve color al personaje enterrado). f495(16,517s) cambio B/N, tratado como efecto antes que nuevo escenario. Una f402 atraviesa corte404; segundo f506–522 cruza retorno color522. No renovación automática del rail en cada corte.''',
'''Una palabra sustituye anterior. Lima x≈28%,y≈42% en59–113: imagina59–74/tener75–83/una84–90/máquina91–106/que107–113. Tras énfasis, Ahora197/hazme207/10 (dígito)216/anuncios225/más238/para244/mi249–252/producto253–272. Sin caption273–350,78f=2,603s.

Narrador blanco centrox50/y50 desde Sí351/eso365/es375–376/lo377–379/que380–382/montamos383–401/Una402–412/put*413/máquina422/de430/fabricar434/creativos447/para462/tu468/negocio474–494. B/N eh495–497/un498–505/segundo506–522; después sin rail523–552.

Personaje lima x42/y44: Venga553–573/ahora574/súbeme587/todo599/esto606/a615/Meta616–632/y633–639/gestióname640/todas659/las667/campañas675/automáticamente690–723;724vacío;Que725/yo733/no739/tengo743/ni755–757/idea758–783. OCR omite palabras cortas y a veces asigna180° a texto derecho. No hay «loca» nueva al caer tarjeta781+.

Fontfit nativo f390 «montamos»: ROI312,910,767,1020; thr245, tinta438×68px. Helvetica Bold IoU0,905,cuerpo99,tracking−76 milésimas; SF Pro Display Bold0,815,cuerpo104,−83. Es ajuste de una muestra, no identificación inequívoca de fuente. El primer recorte cortaba parte superior y fue descartado. Se conserva decisión de implementación SF Pro−60; esta muestra requiere matizar la homogeneidad de fuente.''',
'''Gancho lima acumulativo Si1/eres11/dueño20–25/de un31–34/e-commerce40, conjunto hasta58. Sólido detrás persona y contorno delantero. Nativa f8–14: f11eres ya tamaño casi final translúcido;12↑opacidad,13↑,14firme, leve descenso, no curva numérica medida. Nativa47–59: salida colectiva progresiva47–58;58sin título,59imagina. No asumir ancho OCR completo cuando sujeto oculta letras.

¿Qué174 línea pequeña y coj***s? grande abajo. Nativa178–187:180primer rótulo translúcido ya ancho grande;181afirma,182desciende/asienta,183–187estable. Hasta196;197Ahora sustituye. «automáticamente»690–723 ocupa≈717px sin convertirse en titular: la palabra larga cabe al rail.''',
'''No interludio gráfico completo independiente. Las tarjetas que expulsa máquina son parte visible de escena; no clasificar como overlay ni deducir CGI/práctico. Salen111+, vuelven271+, proliferan283–333; giro, sombras suelo y blur cuando pasan primer plano.''',
'''En gancho detrás+contorno, oclusión cambia con cuerpo. f495 B/N: nativa493–498 confirma494color→495B/N con misma geometría de máquina hasta498. Suplementos499–521 también parecen retenidos. **Lectura: congelado aparente**; esta revisión no midió hashes de fuente para certificar igualdad geométrica exacta. f784+se atenúa imagen, rail sale antes del fin del tramo (ausente789+). Tarjeta hombro cae781–788.''',
'''Espectros000–032 vistos. Base grave/tonal persistente compatible con música, actividad de voz; no escucha. Banda ancha3,7–5,3s y9,2–11,2s compatible con acciones tarjetas, sin identidad de efecto. Onsets junto cortes:140→4,750s≈+2f;197→6,630≈+2f;404→13,510≈+1f;495→16,540≈+1f;522→17,440≈+1f. f173sin ataque alto exacto. No concluir cada corte tiene golpe.''',
'''Gancho compuesto≈1,9s; rail cambia59–113; primeras tarjetas111. Sin rail273–350 hay abundante movimiento de tarjetas, no pausa visual. El intermedio B/N495–521 separa voz del narrador y reencargo al personaje. No se computó tasa exhaustiva de cambios ni intervalo máximo de imagen inmóvil.''',
'''Gancho acumula y usa profundidad por máscara(1–58); rail se coloca lateral al personaje(59–113), cambia a blanco/centro para narrador(351+), y lima para personaje(553+). Caption cruza cortes404/522. Anchura larga no basta para promover automáticamente un énfasis(690–723).''',
 common_doubt+' Congelado495–521 pendiente auditoría hash/imagen de parent. Color numérico y sombras del texto no medidos.',
'''laminas/v5-maquina/v5-maquina-A-entrada-eres.jpg; -fundido-gancho.jpg; -enfasis-cojones.jpg; -bn.jpg; -rail-fontfit.jpg/.txt. Las cuatro primeras son secuencias corregidas, no extracción vieja por seek.'''
],[ev('enfasis',1,58,'gancho acumulativo con máscara','Si eres dueño de un e-commerce','eres primero11; fundido colectivo47–58, sólido detrás y contorno delante'),ev('superposicion',111,139,'tarjetas en escena','','no atribuir origen overlay'),ev('corte',140,140,'corte a piernas'),ev('corte',173,173,'corte perfil'),ev('enfasis',174,196,'pregunta censurada','¿Qué coj***s?','nativa primera palabra gigante180 translúcida, estable183'),ev('corte',197,197,'salto toma mismo escenario'),ev('subtitulo_excepcion',273,350,'hueco sin rail','','78f mientras tarjetas proliferan'),ev('corte',404,404,'corte máquina sola','Una','caption atraviesa'),ev('efecto',495,521,'B/N y retención aparente','','nativa493–498; igualdad exacta congelado no certificada por este agente'),ev('corte',522,522,'regreso color personaje','segundo','caption dura primerframe'),ev('subtitulo_excepcion',523,552,'hueco sin rail'),ev('efecto',784,801,'atenuación progresiva imagen','','últimos frames del tramo')])
write('v5-maquina-B','v5-maquina',802,1585,30000/1001,[
'''|Fotogramas|Duración|Imagen|
|---|---:|---|
|802–987|186f/6,206s|Personaje entre tarjetas, atenuado, pose retenida visualmente; no certificar freeze.|
|988–1011|24f/0,801s|Plano más cercano frontal B/N: manos y pelo cambian.|
|1012–1062|51f/1,702s|Vuelve color en mismo montón; Okay! lima.|
|1063–1183|121f/4,037s|Macro moneda en dedos, barrido derecho y retroceso picado hacia máquina.|
|1184–1304|121f/4,037s|Actor se aproxima y cámara baja tarjetas/vuelve a rostro.|
|1305–1545|241f/8,041s|Ring oscuro azul izq/rojo der, dos hombres; protagonista levanta tarjeta, rival cae. Cámara acerca.|
|1546–1585|40f/1,335s|Oficina verde, actor naranja y papeles.|''',
'''f988(32,966s) seco a primer plano B/N;1012(33,767s) color original;1063(35,469s) macro moneda;1184(39,506s) salto toma actor;1305(43,544s) ring;1546(51,585s) oficina. Barrido cámara1074–1088 con metraje borroso pero rail limpio; retrocede1096–1111. f1397candidato detector coincide iluminación tarjeta/foco, no nuevo escenario en secuencia nativa1394–1400. Precisión de continuidad de toma pendiente control fullframe.''',
'''Sin rail802–1031 salvo Okay!1032–1062 lima centrox51,7/y50,5. Locución durante atenuación no se escribe completa. Desde1063 blanco central espero, está1109,maquinita1117; después pequeñas a/un/coste/ridículo entre titulares. y1200/el1206/visual1211–1227; ya1228/lo1236/estás1240/viendo1247–1263 crecen≈200px; Hoy1264/en1272/día1274/compites1280/con1296/el1301 vuelven pequeños.

Ring rail y≈24%: mismo1305/producto1313/o1331/uno1334/casi1341/idéntico1350/por1364/el1370/mismo1375/cliente1383/que1397/tu1400/competencia1404/Sabes1430/que1442/te1446/diferencia1448/ahí1466. El1478–1485 pasa x57/y44,6, después y/el/visual/tradicional1504+centro50. No justifica regla fija y60.''',
'''produce1134–1199 blanca arriba x58/y30,w≈740,h≈200; creativos1146–1199 debajo x46/y66,w≈804,h≈165. No máscaras: rail a/un/coste/ridículo entre ellas. Nativa1132–1141:1132/33sin produce;1134primer rótulo translúcido casi ancho final;1135más fuerte;1136–1141asienta con leve caída. No1133 ni1135 como primerframe. Ambas palabras persisten sobre salto1184 y desaparecen juntas1200.

visual1486–1503 gigante≈800×280 central entra con opacidad; fondo se atenua1478+. Oficina desde1546 rail gigante≈700–780px ancho,y36: cuesta1546/mucho1549;1557vacío;dinero1558/tiempo1569–1583/y1584. Texto sólido detrás del sujeto y contorno por delante. OCR180°falso.''',
'''Ring no es interludio tipográfico completo; dos personas, manos, tarjeta y caída rival dentro escena. Tarjeta eleva1394+, brillo1395+, cono al suelo1396–1397. Rival gris colapsa1458–1481. Cámara se acerca1480–1545; tarjeta vira recuadro rectangular brillante.''',
'''B/N988–1011 conserva movimiento de manos/pelo: no congelado. Fondo se oscurece1478–1485 durante respuesta El visual; caption blanco conserva contraste. Blur cámara1074–1088 no afecta texto. Oficina1546+máscara+contorno.''',
'''Espectros024–056 vistos para la intersección del tramo. Base grave persiste incluso pausa voz32,76–35,26s, no silencio total. Onset988→33,040≈+2f;1012sin ataque fuerte exacto;1063→35,480≈0f;1397→46,600≈0f pero evento iluminación;1546→51,650≈+2f. Muchos trazos son compatibles con consonantes/voz; no identificar cash register, golpe o whoosh como escuchado.''',
'''Retención visual atenuada802–987 sobre frase larga sin rail. Sistema dual de titulares produce/creativos deja pequeña frase en medio. Cambio de escena ring1305 y respuesta visual1486; oficina1546 muestra caption grande sucesivo en lugar de frase acumulada. No tasa de cambios calculada.''',
'''Hold puede tener locución sin rail(802–1031). Dos grandes palabras persisten mientras rail menor sigue(1134–1199). Oscurecer imagen precede énfasis central(1478–1503). Rail grande puede usar máscara en oficina(1546+), y caption puede cruzar salto1184.''',
 common_doubt+' Hold802–987 pendiente prueba exacta. Corte1397 no se confirma como montaje; se interpreta iluminación con alcance nativo recortado. Entradas creativos/visual no tienen curva nativa medida.',
'''laminas/v5-maquina/v5-maquina-B-produce.jpg; v5-maquina-B-foco.jpg.'''
],[ev('subtitulo_excepcion',802,1031,'locución sin rail principal','','Okay comienza1032'),ev('corte',988,988,'corte B/N cercano'),ev('efecto',988,1011,'B/N con movimiento','','manos/cabello cambian, no freeze'),ev('corte',1012,1012,'regreso color'),ev('enfasis',1032,1062,'exclamación lima','Okay!'),ev('corte',1063,1063,'macro moneda'),ev('camara',1074,1111,'barrido y retroceso','','rail conserva nitidez'),ev('enfasis',1134,1199,'doble titular','produce / creativos','produce1134, creativos1146; pequeña frase intermedia; atraviesa1184'),ev('corte',1184,1184,'salto toma actor','produce creativos'),ev('corte',1305,1305,'ring oscuro'),ev('efecto',1394,1400,'iluminación tarjeta y suelo','','nativa; no certificar corte1397'),ev('efecto',1478,1485,'atenuación fondo'),ev('enfasis',1486,1503,'palabra gigante','visual'),ev('corte',1546,1546,'oficina verde'),ev('enfasis',1546,1585,'rail gigante con máscara','cuesta mucho dinero tiempo y','una palabra sucesiva, hueco1557')])
write('v5-maquina-C','v5-maquina',1586,2290,30000/1001,[
'''|Fotogramas|Duración|Imagen|
|---|---:|---|
|1586–1786|201f/6,707s|Oficina verde, naranja golpea máquina; tiras largas papel invaden y enterramiento. Cámara gira/baja sobre papel.|
|1787–1918|132f/4,404s|Emergencia roja, casco y extintor hacia llamas izquierda. Cámara pasa cuerpo completo1826 a cara1918.|
|1919–2028|110f/3,670s|Picado montón tarjetas, mano sobresale; personaje escala fuera1968–1992.|
|2029–2149|121f/4,037s|Máquina expulsa tarjetas, hombre alto sobre montón con taza; cámara revela escena.|
|2150–2261|112f/3,737s|Almacén iluminado, máquina palet fondo, personaje izquierda, cámara retrocede.|
|2262–2290|29f/0,968s|Negro sin marca.|''',
'''f1675(55,889s) cambio brusco a detrás hombro en movimiento: posible corte oculto, no confirmado en nativa. f1787(59,626s) seco oficina→extintor rojo;1919(64,031s) seco montón tarjetas;2029(67,701s) seco hombre arriba máquina;2150(71,738s) seco almacén;2262(75,475s) negro. A PAGAR cruza1787; quieres cruza2029–30; tienda cruza2150–2163.''',
'''Oficina rail gigante blanco y≈36%,sólido detrás+contorno delante: dolores1587–1598/de1599–1601/cabeza1602–1619/cuando1620–1629/intentas1630–1644/escalar1645–1666. Luego pequeño centro50: y1693/cuando1696/escalar1705/significa1718/sí1739/o1745/sí1748/Contratar1756–1774/o1775–76/delegar1777–1796.

Rojo: Ay1826/maquinita1839/Y1865/ahora1870/quién1877/recoge1884/todo1896/esto?1908. Tarjetas: Bueno1919/nos1931–1936/tenemos1937/que1948/ir1952/Si1961/ya1968/inviertes1973/en1986/anuncios1991/cada2002/mes2009/y2018/quieres2021–2030/acabar2031/como2042/Deivid2049/pincha2063/abajo2075/y2087/vemos2091/personalmente2099–2120/si2121/encaja2127/con2137/tu2142/tienda2147–2163. personalmente reduce cuerpo para caber≈800px ancho/tinta120px. No fusionar nos/tenemos por error OCR.

Almacén: La2164/máquina2170/te2181/la2184/instalamos2188/dentro2205/de2215–2218/tu2219/negocio2224–2246; sin rail2247+. Rail centro50 puede cubrir cara/objeto, no banda inferior reservada.''',
'''A blanco1668 x23/y20; PAGAR rojo1675/76, grupo A PAGAR≈885px ancho,centro50/y20 hasta1796. La aparición roja exacta1675 frente1676 sigue pendiente control nativo. Lectura: visualiza «a pagar», juego verbal con apagar.

Nativa1794–1803(59,860–60,160s):1794–96A PAGAR;1797todo título ausente1f;1798APAGAR ya nueva geometría roja final translúcida;1799↑,1800↑,1801–03firme. **Sustitución con 1f vacío**, no morph continuo de letras. APAGAR permanece hasta1918. Rail menor continúa debajo.''',
'''No interludio gráfico completo. Papel y fuego pertenecen imagen de escena; no consta backend ni generación. Máquina lanza tarjetas mientras personaje revela posición.''',
'''Texto grande detrás+contorno en oficina. Luz roja del techo pulsa en extintor, no caption parpadeante. Push1826–1918 en metraje; título permanece fijo respecto pantalla. Cámara en oficina muy agitada y rail legible aunque blanco sobre papel. No freeze demostrado en este tramo.''',
'''Espectros048–077 para intersección vistos. Base grave/voz. Onset55,940≈+1f respecto PAGAR1676 (inicio aún ±1f). Banda ancha60–61s durante humo; no separar efecto del audio voz/base.1787sin ataque alto exacto;60,220≈+18f;1919→64,220≈+6f;2029sin ataque alto exacto;2150→71,670≈−2f y71,890≈+5f. Imagen negra75,475s y cola tonal decae≈76,4s: no silencio instantáneo.''',
'''Titular sostenido A PAGAR/APAGAR mientras rail cambia durante≈8,4s. Cortes1919/2029/2150 cambian escenario, caption conserva continuidad verbal. Sin rail2247–2261 durante despedida gestual y negro final. Tasa exhaustiva no calculada.''',
'''Juego verbal puede sostener titular varias frases(1668–1918). Cambio de palabra no exige morph(1797–1801). Caption cruza corte a siguiente contexto(1787,2029,2150). Palabra larga se reduce para caber(personalmente2099–2120).''',
 common_doubt+' Barrido/corte1675 y primera aparición PAGAR1675/76 pendientes nativa. No controles nativos exhaustivos de todos cortes, máscaras ni reducción personalmente.',
'''laminas/v5-maquina/v5-maquina-C-apagar.jpg, secuencia1794–1803 corregida.'''
],[ev('enfasis',1587,1666,'rail gigante con máscara','dolores de cabeza cuando intentas escalar'),ev('enfasis',1668,1796,'juego verbal','A PAGAR','A1668, PAGAR1675/76 pendiente±1f; no confundir con APAGAR posterior'),ev('corte',1787,1787,'emergencia roja','A PAGAR','titular cruza'),ev('transicion',1797,1801,'sustitución con hueco','APAGAR','1797sin título,1798nueva forma roja translúcida,1801firme; nativa'),ev('enfasis',1798,1918,'titular rojo','APAGAR'),ev('camara',1826,1918,'aproximación cuerpo a rostro'),ev('corte',1919,1919,'montón tarjetas','Bueno'),ev('corte',2029,2029,'hombre sobre tarjetas','quieres','caption continúa hasta2030'),ev('corte',2150,2150,'almacén','tienda','caption continúa2163'),ev('subtitulo_excepcion',2247,2261,'despedida sin rail'),ev('corte',2262,2262,'negro final','','sin logo; cola audio persiste')])
write('v6-ads90-rev-A','v6-ads90-rev',0,904,60,[
'''|Fotogramas|Duración|Imagen|
|---|---:|---|
|0–199|200f/3,333s|Radial crema/rosa, escalones turquesa,suelo brillante. Caja centro abre1–14; cabeza15,torso18,actor azul de pie23–39;salta40–49,aterriza50–59;aproximación49–103.|
|200–417|218f/3,633s|Americano presentador azul, luego acercamiento extremo313–328 y rostro estable.|
|418–516|99f/1,650s|Corbata/móvil, azul entra433+ y tira teléfono435–445, toma cara.|
|517–562|46f/0,767s|Grupo camina hacia cortinas rojas/neones.|
|563–642|80f/1,333s|Máquina pantalla Braud, aproximación.|
|643–834|192f/3,200s|Mano BOSS frente hueco máquina/portátil, cae663–675; cámara baja720–810 a cámaras/frasco.|
|835–904|70f/1,167s|Monitor carrusel de avatares; mano señala; card aumenta891+.|''',
'''Secos visibles200(3,333s),418(6,967s),517(8,617s),563(9,383s),643(10,717s),835(13,917s). Otros493–520 cruza517. Candidatos64(1,067s, escala aterrizaje) y818(13,633s, frasco cambia tamaño) sin control nativo para discriminar cambio toma/zoom/continuidad. No inventar corte por marca detector.''',
'''Sin rail0–115. Línea ¿Eres116/dueño133/de145/un154; e-commerce166–199 debajo mayor. La transcripción ¿Eres≈98 implica diferencia≈18f=300ms, pero marca acústica ±50ms y no escuchada.

Tras corte200 residual ¿Eres dueño unframe; ¿Lo201/tienes206/todo223/listo237/para254/el264–267, blanco pequeño y36. Titular BLACK/FRIDAY268+. Se retira313 y hasta349no rail; ¿Menos350/los372/anuncios381–417 pequeño y72.

Desde418 rail blanco centro50: Pues418/se433/acabó440/depender457/de485/otros493–520/Te524/presento536–561/el562/sistema569/de593–602. Sin rail603–642 mientras máquina avanza. Pones747/tu759/producto769/eliges812–840/el841/estilo848–890/y891–900/el901. Caption conserva geometría sobre cámara móvil; y ya visible891 en dense, suplementos muestran892–899 (OCR897 tarde).''',
'''Gancho acumulativo blanco ¿Eres dueño de un116–199 y46, e-commerce166segunda línea mayor. Sin máscara discernible en este gancho. Titular BLACK268/FRIDAY283 hasta312. Nativa266–287(4,433–4,783s): BLACK268opaco/269semi/270ausente/271semi/272opaco/273semi/274ausente/275semi/276+opaco. FRIDAY283opaco/284semi/285ausente/286semi/287opaco. Entrada parpadea con período4f=66,7ms, no fundido monótono. No se deduce easing de flash.

Así677/de701/fácil706: tres líneas grandes blancas x37y35/x28y51/x40y67, inclinación≈−5°; todas hasta746 y se retiran747. Geometría pantalla permanece aunque cámara baja al interior. No es el mismo sistema de palabra única de rail.''',
'''Braud563–642 es texto dentro pantalla de máquina: perspectiva sigue imagen, no demostrar capa3D tipográfica ni interludio gráfico. Carrusel835+ es UI dentro monitor. Tarjeta elegida aumenta891+,otras desaparecen; no enumerar texto ambiente como captions.''',
'''Partículas blancas al salir caja, dentro material visible. Corbata personaje sostiene móvil y azul lo aparta, no cursor. Rail permanece nítido durante cambios cámara. Titulares Así/de/fácil superpuestos a descenso del metraje, no warp evidente a cámara.''',
'''Espectros000–016 para este tramo vistos. Base tonal/grave sostenida compatible con música;0–1,6s actividad banda ancha acompañando salto/partículas; no SFX identificado por escucha. Pausa voz10,1–11,2s conserva fondo. No correlación onset→corte exhaustiva calculada en este tramo.''',
'''Actuación inicial≈1,6s precede primera voz transcrita≈1,63s. Rail empieza1,933s. Alterna gancho acumulativo, palabras pequeñas, parpadeo del titular, caída objeto y demostración máquina. Dos huecos313–349 y603–642 tienen metraje activo. No medir como slides estáticos por ausencia de caption.''',
'''Acción puede abrir antes de locución y caption(0–115). Caption cambia altura por bloque(y46→36→72→50). Entrada de título puede parpadear y quedar fija(268–287). UI/logo dentro pantalla no basta para inferir overlay independiente(563+).''',
 common_doubt+' F64/F818 candidatos no resueltos. Primera opacidad de ¿Eres y resto palabras acumulativas no controlada a nativa. OCR del cuerpo no es fontSize exacto.',
'''laminas/v6-ads90-rev/v6-ads90-rev-A-black-friday.jpg,266–287 corregido.'''
],[ev('camara',0,103,'salida caja y aproximación','','cámara/material, física vs digital indeterminada'),ev('subtitulo_excepcion',0,115,'acción sin rail'),ev('enfasis',116,199,'gancho acumulativo','¿Eres dueño de un e-commerce?','entrada primera116 observada dense, no curva nativa'),ev('corte',200,200,'americano presentador'),ev('enfasis',268,312,'titular parpadeante','BLACK FRIDAY','BLACK268;FRIDAY283;nativa opaco/semi/ausente/semi cada4f'),ev('camara',313,328,'acercamiento rápido rostro'),ev('subtitulo_excepcion',313,349,'hueco sin rail'),ev('corte',418,418,'actor corbata y móvil'),ev('corte',517,517,'grupo cortina','otros','caption atraviesa hasta520'),ev('corte',563,563,'máquina pantalla Braud','el','marca integrada metraje'),ev('subtitulo_excepcion',603,642,'máquina sin rail'),ev('corte',643,643,'frasco sobre máquina'),ev('enfasis',677,746,'tres líneas acumulativas','Así de fácil','ligera inclinación, pantalla fija sobre cámara'),ev('corte',835,835,'carrusel avatares'),ev('efecto',891,904,'crecimiento tarjeta UI','','continúa siguiente tramo')])
write('v6-ads90-rev-B','v6-ads90-rev',905,1784,60,[
'''|Fotogramas|Duración|Imagen|
|---|---:|---|
|905–947|43f/0,717s|Avatar aumenta dentro pantalla.|
|948|1f/0,0167s|Frontal micrófono/actor corbata borroso. Inserto aislado nativo.|
|949–1073|125f/2,083s|Ángulo oblicuo micrófono/actor corbata, rostro se aproxima.|
|1074–1102|29f/0,483s|Macro dedo enter.|
|1103–1150|48f/0,800s|Frasco dentro máquina, luces.|
|1151–1196|46f/0,767s|Monitor blanco rueda/barra cargando.|
|1197–1306|110f/1,833s|Selfie hombre camiseta verde, perfume.|
|1307–1406|100f/1,667s|Presentador azul radial, aproxima rostro1335–1353.|
|1407–1510|104f/1,733s|Dos hombres ante portátil/máquina;oscurece1463+.|
|1511–1687|177f/2,950s|Corbata sin pantalones, rosa,café, pies mesa y monitor, almacén.|
|1688–1748|61f/1,017s|Teclado enter cian oscuro.|
|1749–1784|36f/0,600s|Corbatado café en almacén, aproximación1755–1767.|''',
'''Nativa946–952: pantalla947→frontal borroso948(15,800s)→oblicuo949(15,817s). produce permanece en los3. Inserto1f no figura detector; **intención no inferida** y no promoverlo a recurso de montaje. Parent observa también original, pero esta nota no audita igualdad hash entre variantes.

Otros secos1074(17,900s),1103(18,383s),1151(19,183s),1197(19,950s),1307(21,783s),1407(23,450s),1511(25,183s),1688(28,133s),1749(29,150s). Candidatos1116/1143 coinciden iluminación misma máquina, no cambio escena claro;1176cambio UI del mismo monitor. El titular no es un servicio cruza1407.''',
'''Blanco y50: sistema908/produce929–956/y957–964/edita965/el982/anuncio989/completo1009–1088. Amarillo segunda voz y71: quiero961/un978/UGC989–1039/de1040/este1057/avatar1064–1085; en1087/1088blanco completo aún visible, amarillo ausente. No unir dos voces/rail como una cadena global. Ambos cruzan1074.

Le1091primero poco visible (OCR omite),das1107,a1120 acumulan pequeña línea x47/y45. generar1127 debajo. ¡Y atención!1308–1353 unidad media y69;que1354–1370 pequeño y51. En almacén rail grande y30:Lo1511/instalamos1514–1541/en1542–1549/tu1550/negocio1557/y1581/lo1586/usas1593/cuando1612/quieres1632–1687. Se ve **quieres**, transcripción dice quieras; no corregir visual hacia transcripción. Sólido detrás cabeza+contorno delante en negocio/cuando/quieres. No180°real.

Las1689 pequeña/veces1693 grande/que1705/quieras1711 pequeña acumulan tres niveles hasta1748,y45/53/60. Caption sigue nítido sobre oscuro.''',
'''generar1127–1164. Nativa1126–1135(18,767–18,917s):1126limpio;1127primer translúcido;1128geometría≈final,w801h209,x48/y53;1129/30afirma;1131/32casi firme;1133+asentado. No medir valores de opacidad exactos. Le das a arriba; cruza1151.

voilà1191primer semitransparente sobre UI, cruza1197 y llega1262, giganteh≈276centro52/50.1263–1307sin rail pese YVO≈1284.

no1372x27/y45,es1384/un1391 acumula línea;servicio1398bajo≈754×229,grupo hasta1444;1445sin texto. Es1446x47/y44;fondo oscurece1463–74,tuyo1472translúcido→1477firme,≈728×368hasta1510, frente ambos sin máscara.

¿1primero1750semi,1755firme;anuncio?1759se añade horizontal sobre cifra; combinado numeralh≈466. Persiste a siguiente tramo hasta1805.''',
'''Loading1165–1196 «Generando creativo…» y rueda/barra son UI del monitor, no rail. No declarar gráfico tipográfico completo separado. Composiciones de titulares sobre metraje: generar/voilà/no es un servicio/tuyo.''',
'''Dos railes diferenciados color/altura durante simulado avatar(961–1085). Oscurecimiento1463–1474 prepara palabra tuyo. Máscara+contorno en almacén; caption continúa delante después de ocultarse sólido. Keyboard enter1688cian; no asumir flash de corte en1116/1143.''',
'''Espectros008–032 vistos para intersección. Base grave/tonal conserva energía durante pausa20,2–21,4s; no silencio. Ataque18,13s coincide dedo f1088 sobre enter, no audio escuchado que permita llamarlo clic. Onsets de voz abundantes; no clasificación exhaustiva de efectos.''',
'''Dos carriles contienen frases simultáneas y duran de forma distinta; completo se retiene mientras habla rail amarillo. Cuadro tipográfico generar dura≈0,63s,voilà≈1,2s. Hueco1263–1307con selfie y tránsito al presentador. No calcular máximo tramo sin cambio a partir de pose aparente.''',
'''Otra voz puede tener rail amarillo separado(961–1085). Caption puede continuar por cortes1074/1151/1197/1407. Opacidad puede entrar durante≈6f a escala casi final(generar1127–1133); OCR da primerframe legible tarde. Máscara+contorno también se usa en rail gigante palabra a palabra(1511–1687).''',
 common_doubt+' Inserto948 intención incierta y comparativa hash parent pendiente. Entradasvoilà/servicio/tuyo/¿1 no controladas en nativa completa. Gran máscara de almacén sin medidas de espesor exacto.',
'''laminas/v6-ads90-rev/v6-ads90-rev-B-generar.jpg; v6-ads90-rev-B-inserto-948.jpg.'''
],[ev('corte',948,948,'inserto frontal de un frame','produce','nativa; intención indeterminada'),ev('corte',949,949,'oblicuo tras inserto','produce'),ev('subtitulo_excepcion',961,1085,'segunda voz con rail amarillo','quiero un UGC de este avatar','y71 frente blanco y50; blanco completo continúa hasta1088'),ev('corte',1074,1074,'macro enter','completo / avatar','rail atraviesa'),ev('corte',1103,1103,'frasco máquina'),ev('enfasis',1127,1164,'palabra gigante acumulativa','Le das a generar','nativa1127semi,1133asentado; atraviesa1151'),ev('corte',1151,1151,'monitor blanco','generar'),ev('enfasis',1191,1262,'palabra gigante','voilà','primera semi UI; cruza1197'),ev('corte',1197,1197,'selfie verde','voilà'),ev('subtitulo_excepcion',1263,1307,'hueco sin rail'),ev('corte',1307,1307,'presentador radial'),ev('enfasis',1372,1444,'línea pequeña y palabra gigante','no es un servicio','servicio1398; cruza1407'),ev('corte',1407,1407,'dos hombres máquina','no es un servicio'),ev('efecto',1463,1474,'oscurecimiento fondo'),ev('enfasis',1472,1510,'posesión gigante','Es tuyo','Es1446;tuyo1472semi'),ev('corte',1511,1511,'almacén corbata pies'),ev('enfasis',1511,1687,'rail gigante máscara','Lo instalamos en tu negocio y lo usas cuando quieres'),ev('corte',1688,1688,'teclado cian'),ev('enfasis',1689,1748,'tres niveles acumulativos','las veces que quieras'),ev('corte',1749,1749,'corbata café'),ev('enfasis',1750,1784,'cifra con palabra superpuesta','¿1 anuncio?','continúa tramo C hasta1805')])
write('v6-ads90-rev-C','v6-ads90-rev',1785,2649,60,[
'''|Fotogramas|Duración|Imagen|
|---|---:|---|
|1785–1798|14f/0,233s|Corbata,café, almacén.|
|1799–1866|68f/1,133s|Azul aparece detrás/lado portátil almacén.|
|1867–1909|43f/0,717s|Selfie hombre gris perfume.|
|1910–1959|50f/0,833s|Rubia baño perfume.|
|1960–2019|60f/1,000s|Barba/gafas coche perfume.|
|2020–2074|55f/0,917s|Morena cocina acerca perfume hasta cubrir pantalla.|
|2075–2220|146f/2,433s|Corbatado móvil,café,pies mesa primer término.|
|2221–2584|364f/6,067s|Presentador radial;salto de toma2335.|
|2585–2649|65f/1,083s|Negro sin logo.|''',
'''Secos1799(29,983s),1867(31,117s),1910(31,833s),1960(32,667s),2020(33,667s),2075(34,583s),2221(37,017s),2585(43,083s). f2335(38,917s) mismo radial/cambio gesto y framing leve, salto toma visible, control nativo pendiente. Candidatos1904 y2126 son retirada/entrada titular, **no nuevo plano**. ¿1 anuncio? cruza1799;10 versiones cruza1867;para cruza1910;testear cruza1960;esperas cruza2075.''',
'''¿1 anuncio? continúa hasta1805;No…1806–1862 blanco pequeño centro50. Para1904–1918/testear1919–1963/Sin1964/creadores1983/que2010/fallan2020–2045/sin2046/esperas2065–2114.2115–2119sin texto.

Dentro bloqueQ4,en2173 pequeño x65/y61/tus2184/manos2197, bajo titular, sobre actor/taza. CTA radial:Pincha2221–2244/abajo2245/y2271–2278/agenda2279/una2300/llamada2310–2334/Analizaremos2335–2369/tu2370–2376/caso2377–2402/y2403–2410/veremos2411–2431/si2432–2438/el2439–2443/sistema2444/sirve2468/para2487/tu2499/ecommerce2507–2536/Nos2537/vemos2544/dentro2559–2584. y existe aunque OCR omite. Rail centro50;último Nos/vemos/dentro baja51,7→54,1→55% con framing final; no siempre y60.

Fontfit nativo f2350«Analizaremos»,ROI290,910,790,1015,thr230,tinta470×69. Helvetica BoldIoU0,910,cuerpo94,tracking−131milésimas;SF Pro Display Bold0,800,cuerpo95,tracking−112. Ajuste comparativo de una palabra larga, no fuente inequívoca ni regla de tracking global. Se preserva implementación SF Pro−60; prueba exige distinguir decisión de fuente observada.''',
'''10 primer1864semi,h≈606,w≈812;versiones1873horizontal sobre cifra,1879–1903estable;ambos se retiran1904. Voz10 registrada1854→texto1864(+10f=166,7ms), no diferencia acústica certificada por escucha. Cifra delante sujeto, sin máscara.

Tu2120pequeño arriba y11%;Q4 gigante primer2126semi. Nativa2124–2135(35,400–35,583s):2124/25soloTu;2126Q4semi ya tamaño casi final;2127/28↑opacidad;2130+legible;2134firme. W≈730/H≈597,y30,tilt≈−4,7°,no giro180. Tu/Q4hasta2220. No se dispone curva numérica de tinta por frame.''',
'''No interludio gráfico completo independiente. Q4 compuesto sobre corbatado,10 sobre avatares; perfume visible pertenece recurso. Portátil/marca no rail.''',
'''Botella se aproxima2060+ y ocupa cuadro2074, rail blanco sigue crisp. Q4inclinado no señal OCR180°. Cuadro10/Q4delante del sujeto. Gesto de señalar abajo del CTA pertenece actor, no cursor overlay. Negro2585sin outro.''',
'''Espectros024–045 vistos para tramo. Fondo grave/tonal compatible música. Ataques35,26–35,47s juntoTu/Q4 compatibles énfasis, no identidad SFX escuchada. f2585negro43,083s conserva caída/cola tonal: no silencioinstantáneo. Muchos trazos corresponden voz; no medir tempo exacto desde una rejilla estimada.''',
'''Avatares cambian cada43–60f≈0,7–1,0s;frasco móvil aporta gran cambio dentro último plano.10sostenido≈0,67s;Tu/Q4≈1,68s sobre almacén. CTA mantiene rail ordinario, sin escalar cada palabra al ancho70%.''',
'''Caption/título cruza múltiples cortes(1799/1867/1910/1960/2075). Entrada tipográfica puede causar falso candidato corte(2126),salida también(1904). Body del rail no es altura tinta: tinta69pxfontfit2350 no significa fontSize69. CTA retiene escala pequeña mientras título anteriorQ4es gigante.''',
 common_doubt+'10/versiones,No y salto2335 pendientes rangos nativos exhaustivos. Tracking fontfit tiene posible sesgo por palabra/antialias/compresión; dos muestras no justifican ley global nueva.',
'''laminas/v6-ads90-rev/v6-ads90-rev-C-q4.jpg; v6-ads90-rev-C-rail-fontfit.jpg/.txt.'''
],[ev('corte',1799,1799,'presentador almacén','¿1 anuncio?','caption cruza hasta1805'),ev('enfasis',1864,1903,'cifra gigante y texto sobre ella','10 versiones','versiones1873;cruza1867'),ev('corte',1867,1867,'selfie hombre gris','10 versiones'),ev('corte',1910,1910,'rubia baño','para'),ev('corte',1960,1960,'hombre coche','testear'),ev('corte',2020,2020,'morena cocina','fallan'),ev('corte',2075,2075,'almacén pies mesa','esperas','caption hasta2114'),ev('subtitulo_excepcion',2115,2119,'hueco sin rail'),ev('enfasis',2120,2220,'cifra trimestre y rail bajo','Tu Q4 en tus manos','Q4primer2126semi,2134firme,nativa; no corte2126'),ev('corte',2221,2221,'presentador radial','Pincha'),ev('corte',2335,2335,'salto toma mismo radial','Analizaremos','candidato confirmado visualmente framing/gesto;nativa pendiente'),ev('subtitulo_excepcion',2537,2584,'rail desciende al cierre','Nos vemos dentro','y51,7→54,1→55%'),ev('corte',2585,2585,'negro sin marca','','audio cola persistente')])
write('v7-ads90-rev-A','v7-ads90-rev',0,597,60,[
'''|Fotogramas|Duración|Imagen|
|---|---:|---|
|0–373|374f/6,233s|Corbatado mirando móvil y portapapeles,radial rosa/crema/neón;papel cae20–90,asistente headset entra156+ entrega teléfono.|
|374–416|43f/0,717s|Misma escena B/N: actor sigue moviéndose.|
|417–513|97f/1,617s|Color,protagonista azul entra y aparta móvil/cara.|
|514–557|44f/0,733s|Grupo atraviesa cortinas rojas/neón.|
|558–597|40f/0,667s|Máquina pantalla Braud, cámara avanza; sigue fuera tramo.|''',
'''f374(6,233s) B/N instantáneo dentro escena, no freeze. Nativa372–380:374primer B/N,brazo/corbata cambian374–380. f410(6,833s) candidato escala/encuadre en B/N no discriminado a nativa; no certificar corte. f417(6,950s) color de nuevo. Secos514(8,567s)grupo y558(9,300s)máquina. Otros489–519 cruza514;el558 en corte siguiente. Cola parece similar V6rev−5f, equivalencia exacta la audita parent; no declararla duplicada por parecido.''',
'''Gancho una palabra por vez,blanco grande centroy50–52:¿Tu33–40/creador41–63/UGC64–97/te98–104/deja105–121/tirado122–142/a143–147/última148–169/hora?170–199/o200–212/¿te213–219/entrega220–238/algo239–250/que251–260/no261–272/se273–281/parece282–305/en306–310/nada311–327/a328–333/lo334–337/que338–344/pediste?345–373. No acumulación. Rail delante cuerpo/móvil/papel, sin máscara; ancho te≈229px frenteentrega≈745px demuestra que no se fija cada palabra a70%W. Tinta miniatura≈180–265px; no fontSizeexacto98 ni200.

B/Nrail se reduce centro50:¿Pero374–385/qué386–389/es390–397/esto398–416. f374¿Pero ya firme y geometría final nativa. OCRomite es y fusionaesto. Colorrail pequeño Pues417/se429/acabó434–454/depender455–481/de482–488/otros489–519/Te520/presento532–557/el558/sistema564/de588. A/o/de existen aunqueOCRpierde.

TranscripciónTu0frenteprimer¿Tu33=550ms;no sincroníaexacta medida por escucha.0–32tiene otra frase amarilla diagonal.''',
'''Nativa f10 lee amarillo exacto «*¡Yo me piro!*», diagonal superiorizquierda,visible0–32 sobre metraje. Texto simultáneo de otra voz/personaje; no rail blanco todavía. Gancho posterior todo tamaño grande, incluso conectores pequeños. A partir374 reduce radicalmente escala: no unúnico railconstante toda serie.''',
'''Sin interludio gráfico completo en0–597. Braud558+ integrado pantalla,mueve perspectiva con máquina; no clasificar overlay cinético3D. Los papeles son parte de metraje.''',
'''B/N374–416 con movimiento verificado;no congelado. Papel delante/detrás cuerpo no ocluye caption blanco;no reservar banda inferior. Rail ordinario vuelve mientras azul tira móvil,por encimapiel/ropa.''',
'''Espectros000–016 para intersección vistos. Basegrave/tonal continua. Bandaancha0,4–0,7s compatible papel,actividadvoz≈1–6,2s;pausa6,16–6,36conservafondo. Ataques7,41–7,5s durante azul/móvil,no identificables como SFX escuchado. No audición ni identificación timbre.''',
'''Gancho un plano continuo6,23s con papel,asistente,teléfono y cambioscada palabra. B/Ncorta tratamiento y escala rail durante0,717s. Secosgrupo8,567s/máquina9,300s abre demostración. No confundir frecuencia rail con frecuencia corte.''',
'''Gancho puede elevar toda cadena palabra única(33–373),sin llenar mismoancho porpalabra. Textoamarillo puede ocupar comienzoenvezprimerrail(0–32). B/Nnoimplicacongelado(374–416). Caption atraviesacortes514/558 y UIenmetraje no overlay demostrable.''',
 common_doubt+' Candidato410 y entradas de rail grande no controlados nativamente todos. Amplitud tamaño se estima desde tinta/OCR, nofontSizefinal. Equivalencia variantes pendiente auditoría parent; s006suplemento contiene622/639fueraalcance, visto entero sin adjudicar cola.',
'''laminas/v7-ads90-rev/v7-ads90-rev-A-amarillo.jpg; v7-ads90-rev-A-bn.jpg.'''
],[ev('subtitulo_excepcion',0,32,'segunda frase amarilla diagonal','*¡Yo me piro!*','nativa10;sin blanco¿Tu hasta33'),ev('enfasis',33,373,'gancho rail grande sucesivo','¿Tu creador UGC te deja tirado a última hora? o ¿te entrega algo que no se parece en nada a lo que pediste?','palabra única,cuerpo grande,ancho variable;sin máscara'),ev('efecto',374,416,'B/N con movimiento','','nativa372–380 demuestra movimiento, no freeze'),ev('subtitulo_excepcion',374,416,'reducción rail','¿Pero qué es esto?','¿Pero374yaopaco;es390–397OCRomite'),ev('efecto',417,417,'retorno color'),ev('corte',514,514,'grupo cortinas','otros','captioncontinúahasta519'),ev('corte',558,558,'máquina pantalla Braud','el','marcaenmetraje,nocapa3Dindependientedemostrada')])

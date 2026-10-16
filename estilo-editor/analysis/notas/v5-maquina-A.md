# v5-maquina · f0–f801 · v5-maquina-A

Estado: **partial**. Pasada densa y suplementos completos; revisión nativa de eventos parcial. 29.97 fps, 1080×1920. Rango 0.000–26.760 s. Fotogramas inclusivos; t=f/fps. Digest completo leído. Nombres exactos de hojas, rangos nativos y espectros en cobertura adjunta.

Las hojas densas originales omitían similitudes JPEG, no solo duplicados exactos; los suplementos restituyen las exclusiones no idénticas. La extracción nativa aquí citada usa select por índice corregido. dapi probe falló EPERM localhost; audio no escuchado ni retranscrito.

## 1. Planos

| Fotogramas | Duración | Imagen y movimiento |
|---|---:|---|
|0–139|140f /4,671s|Picado: hombre gafas rojas, chaqueta naranja/camisa morada/pantalón beige izquierda, máquina derecha, estudio gris. Cámara retrocede; cara14,7→6,8%H.|
|140–172|33f /1,101s|Piernas y tarjetas al suelo, color.|
|173–196|24f /0,801s|Perfil junto máquina; tres tarjetas en suelo.|
|197–403|207f /6,907s|Cambio toma/escala mismo lugar; máquina multiplica tarjetas delante cuerpo.|
|404–494|91f /3,037s|Recurso máquina sola lanzando tarjetas.|
|495–521|27f /0,901s|B/N máquina, geometría aparentemente retenida; ver límite de congelado en§6.|
|522–801|280f /9,343s|Personaje rodeado de montón de tarjetas. Se atenúa al final.|

## 2. Cortes y transiciones

Secos visibles f140(4,671s),173(5,772s),197(6,573s, salto toma mismo lugar),404(13,480s, máquina sola),522(17,417s, vuelve color al personaje enterrado). f495(16,517s) cambio B/N, tratado como efecto antes que nuevo escenario. Una f402 atraviesa corte404; segundo f506–522 cruza retorno color522. No renovación automática del rail en cada corte.

## 3. Subtítulos base

Una palabra sustituye anterior. Lima x≈28%,y≈42% en59–113: imagina59–74/tener75–83/una84–90/máquina91–106/que107–113. Tras énfasis, Ahora197/hazme207/10 (dígito)216/anuncios225/más238/para244/mi249–252/producto253–272. Sin caption273–350,78f=2,603s.

Narrador blanco centrox50/y50 desde Sí351/eso365/es375–376/lo377–379/que380–382/montamos383–401/Una402–412/put*413/máquina422/de430/fabricar434/creativos447/para462/tu468/negocio474–494. B/N eh495–497/un498–505/segundo506–522; después sin rail523–552.

Personaje lima x42/y44: Venga553–573/ahora574/súbeme587/todo599/esto606/a615/Meta616–632/y633–639/gestióname640/todas659/las667/campañas675/automáticamente690–723;724vacío;Que725/yo733/no739/tengo743/ni755–757/idea758–783. OCR omite palabras cortas y a veces asigna180° a texto derecho. No hay «loca» nueva al caer tarjeta781+.

Fontfit nativo f390 «montamos»: ROI312,910,767,1020; thr245, tinta438×68px. Helvetica Bold IoU0,905,cuerpo99,tracking−76 milésimas; SF Pro Display Bold0,815,cuerpo104,−83. Es ajuste de una muestra, no identificación inequívoca de fuente. El primer recorte cortaba parte superior y fue descartado. Se conserva decisión de implementación SF Pro−60; esta muestra requiere matizar la homogeneidad de fuente.

## 4. Palabras de énfasis y tipografía cinética

Gancho lima acumulativo Si1/eres11/dueño20–25/de un31–34/e-commerce40, conjunto hasta58. Sólido detrás persona y contorno delantero. Nativa f8–14: f11eres ya tamaño casi final translúcido;12↑opacidad,13↑,14firme, leve descenso, no curva numérica medida. Nativa47–59: salida colectiva progresiva47–58;58sin título,59imagina. No asumir ancho OCR completo cuando sujeto oculta letras.

¿Qué174 línea pequeña y coj***s? grande abajo. Nativa178–187:180primer rótulo translúcido ya ancho grande;181afirma,182desciende/asienta,183–187estable. Hasta196;197Ahora sustituye. «automáticamente»690–723 ocupa≈717px sin convertirse en titular: la palabra larga cabe al rail.

## 5. Escenas gráficas (motion graphics)

No interludio gráfico completo independiente. Las tarjetas que expulsa máquina son parte visible de escena; no clasificar como overlay ni deducir CGI/práctico. Salen111+, vuelven271+, proliferan283–333; giro, sombras suelo y blur cuando pasan primer plano.

## 6. Superposiciones y efectos sobre la imagen

En gancho detrás+contorno, oclusión cambia con cuerpo. f495 B/N: nativa493–498 confirma494color→495B/N con misma geometría de máquina hasta498. Suplementos499–521 también parecen retenidos. **Lectura: congelado aparente**; esta revisión no midió hashes de fuente para certificar igualdad geométrica exacta. f784+se atenúa imagen, rail sale antes del fin del tramo (ausente789+). Tarjeta hombro cae781–788.

## 7. Sonido

Espectros000–032 vistos. Base grave/tonal persistente compatible con música, actividad de voz; no escucha. Banda ancha3,7–5,3s y9,2–11,2s compatible con acciones tarjetas, sin identidad de efecto. Onsets junto cortes:140→4,750s≈+2f;197→6,630≈+2f;404→13,510≈+1f;495→16,540≈+1f;522→17,440≈+1f. f173sin ataque alto exacto. No concluir cada corte tiene golpe.

## 8. Ritmo

Gancho compuesto≈1,9s; rail cambia59–113; primeras tarjetas111. Sin rail273–350 hay abundante movimiento de tarjetas, no pausa visual. El intermedio B/N495–521 separa voz del narrador y reencargo al personaje. No se computó tasa exhaustiva de cambios ni intervalo máximo de imagen inmóvil.

## 9. Reglas que se deducen de este tramo

Gancho acumula y usa profundidad por máscara(1–58); rail se coloca lateral al personaje(59–113), cambia a blanco/centro para narrador(351+), y lima para personaje(553+). Caption cruza cortes404/522. Anchura larga no basta para promover automáticamente un énfasis(690–723).

## 10. Dudas y lo que no se pudo verificar

La pasada completa por hojas no resuelve la precisión de todos los bordes de entrada/salida, ni curva/easing o RGBA exactos. Solo los rangos nativos enumerados en coverage se controlaron a resolución original. No atribuir SFX por espectro ni fps del metraje por +k. La relación con words.json tiene error ≈±50 ms. Cortes y tamaños leídos en miniatura conservan incertidumbre; no reconstruir trayectorias 3D ni separar cámara física de zoom digital sin evidencia. Congelado495–521 pendiente auditoría hash/imagen de parent. Color numérico y sombras del texto no medidos.

## 11. Láminas guardadas

laminas/v5-maquina/v5-maquina-A-entrada-eres.jpg; -fundido-gancho.jpg; -enfasis-cojones.jpg; -bn.jpg; -rail-fontfit.jpg/.txt; -rail-fontfit.metadata.json; -rail-source.png. Las cuatro primeras son secuencias corregidas, no extracción vieja por seek.

Los sucesos siguientes son un inventario visual de los eventos principales; no un certificado de verificación nativa exhaustiva. f0/f1 son límites de lo observado, con incertidumbres explícitas en detalle.

```json
[
  {
    "tipo": "enfasis",
    "f0": 1,
    "f1": 58,
    "nombre": "gancho acumulativo con máscara",
    "texto": "Si eres dueño de un e-commerce",
    "detalle": "eres primero11; fundido colectivo47–58, sólido detrás y contorno delante"
  },
  {
    "tipo": "superposicion",
    "f0": 111,
    "f1": 139,
    "nombre": "tarjetas en escena",
    "texto": "",
    "detalle": "no atribuir origen overlay"
  },
  {
    "tipo": "corte",
    "f0": 140,
    "f1": 140,
    "nombre": "corte a piernas",
    "texto": "",
    "detalle": ""
  },
  {
    "tipo": "corte",
    "f0": 173,
    "f1": 173,
    "nombre": "corte perfil",
    "texto": "",
    "detalle": ""
  },
  {
    "tipo": "enfasis",
    "f0": 174,
    "f1": 196,
    "nombre": "pregunta censurada",
    "texto": "¿Qué coj***s?",
    "detalle": "nativa primera palabra gigante180 translúcida, estable183"
  },
  {
    "tipo": "corte",
    "f0": 197,
    "f1": 197,
    "nombre": "salto toma mismo escenario",
    "texto": "",
    "detalle": ""
  },
  {
    "tipo": "subtitulo_excepcion",
    "f0": 273,
    "f1": 350,
    "nombre": "hueco sin rail",
    "texto": "",
    "detalle": "78f mientras tarjetas proliferan"
  },
  {
    "tipo": "corte",
    "f0": 404,
    "f1": 404,
    "nombre": "corte máquina sola",
    "texto": "Una",
    "detalle": "caption atraviesa"
  },
  {
    "tipo": "efecto",
    "f0": 495,
    "f1": 521,
    "nombre": "B/N y retención aparente",
    "texto": "",
    "detalle": "nativa493–498; igualdad exacta congelado no certificada por este agente"
  },
  {
    "tipo": "corte",
    "f0": 522,
    "f1": 522,
    "nombre": "regreso color personaje",
    "texto": "segundo",
    "detalle": "caption dura primerframe"
  },
  {
    "tipo": "subtitulo_excepcion",
    "f0": 523,
    "f1": 552,
    "nombre": "hueco sin rail",
    "texto": "",
    "detalle": ""
  },
  {
    "tipo": "efecto",
    "f0": 784,
    "f1": 801,
    "nombre": "atenuación progresiva imagen",
    "texto": "",
    "detalle": "últimos frames del tramo"
  }
]
```

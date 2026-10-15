# v1-pagado · f0–f642 · v1-pagado-A

> Revisión en curso de Codex, 10-10-2026. Dense A completo (16/16); nativo parcial. Falta revisión nativa exhaustiva; suplemento de cuadros omitidos completo. 24 fps, 1080×1920. Probe dapi no disponible (EPERM local); metadatos de probe.json. SF Pro Display Bold −60 se conserva como decisión del estudio, no reidentificado por estas hojas.

## Bitácora verificable
- f0–f88 (0–3,667 s): una mujer en cocina, camiseta blanca y camisa azul caída de un hombro, toma selfie vertical, cámara natural con cabeza cambiando de posición. Subtítulos blancos palabra a palabra, sin fondo, centrados en x≈50 %; su y cae de 62,5 % («Esta») a ≈60 % a lo largo del inicio. La observación de esta deriva afecta al rótulo, no es un valor universal fijo.
- f35 (1,458 s) aparece «30» gigante blanco sobre la zona superior; la parte llena queda detrás de la cabeza y un contorno fino de las mismas cifras delante del cabello/cara. f34 no tiene cifra; f35 tenue y f36 más opaco; corrección nativa registrada. Persiste hasta f88; coexiste con «anuncios», «para», «mi», «marca», «de», «ecommerce» pequeños. OCR no lo detectó como pista: evento añadido por inspección.
- f89 (3,708 s): desaparece todo el «30» y cambia la pose del sujeto; candidato de corte NO marcado. Debe verificarse nativo antes de certificar corte, pero la continuidad cambia aquí, no en la ráfaga f92–96.
- f98–100 «lo» visible aunque falta en OCR. f101–112 «mejor?». f113–116 «Que». f117 «ni» tenue, f118 «ni» más opaco; f119–120 «ni me» y f121–137 «ni me han» acumulativo. No atribuir la cadena OCR «nimehan» a ausencia de espacios diseñados sin nativo.
- f124 (5,167 s): «pagado» gigante debajo entra tenue; f125–127 gana opacidad, alcanza lectura fuerte. Dos líneas pequeñas+grande permanecen hasta f137. OCR mide mediana grande w832 h280 cx48,9 % cy68,9 %; medidas de caja OCR, no cuerpo de fuente.
- f138 (5,75 s): color→B/N, desaparecen textos y cambia al gesto sonriente. f138–140 no inmóviles entre sí a tamaño miniatura; f141–150 imagen B/N se aleja/reencuadra y parece tarjeta fotográfica. No llamarlo congelado verdadero sin comparar píxeles y transformación.
- f151 (6,292 s): corte a busto más abierto en salón iluminado con ventana a izquierda; rectángulo fino cuadrado alrededor cara. f151–154 todavía sin palabras periféricas. f155–159 «porque» vertical siguiendo lado derecho del recuadro, revela caracteres con ritmo escalonado.

## Dudas abiertas
Detalles de opacidad, blur y curva de «30», «pagado», salida B/N y panel cara requieren nativo. La descripción de cortes f89/f138 es candidata visual, no corte certificado.

### Segunda tanda d004–d007 (f160–322)
- f160–175: línea de frase «porque no soy real» progresa por el lateral derecho de la cara, girando en curva hacia abajo, no rail convencional; rectangular fino permanece. f162 soy se incorpora, f164 real. La persona está en movimiento real.
- f176–179: corte seco al gráfico, fondo blanco con gris/vineta periférica; 4 f sin texto. f180 «no» tenue y ligeramente bajo, f181 no sube/aclara; f182 «necesito» todavía borroso a la derecha, f183 se asienta. f187 «300€» empieza tenue abajo, f188 casi lleno, f189 lleno. f193 «c/pieza» empieza tenue bajo cifra, f194 se estabiliza. No son 300 palabras pequeñas: cifra grande y etiqueta de abreviatura sustituyen esa voz.
- f194–225: composición entera deriva/escala suavemente hacia un punto más bajo/derecha; el texto tiene perspectiva leve (extremo derecho algo mayor). f226 corte seco a persona del salón; subtítulo «como» ya lleno en primer fotograma.
- f261 corte seco/jump de postura en mismo salón, no transición; f261–262 «y», f263–265 «no» aunque OCR omitió ambos. f266–275 necesito rail normal.
- f276 entra cifra «2» blanca arriba del pecho; f277–279 se estabiliza. f280 entra semanas gigante bajo 2; los dos coexisten f280–292. f276–285 rostro se ilumina conforme movimiento de cámara/sol: no certificar fuga de luz artificial.
- f293 cambia a otra pose/frase en mismo salón, «para» (2 f), f295 entregar; f303 unos visible pese lectura OCR invertida «soun», f310 anuncios. No rotación 180° real en «unos»: es error OCR.

### Contraste nativo exacto
El script sheet.py original desplaza −1 f por seek; las láminas *-exact usan select between(n) decodificando desde inicio.
- «30» rectificado tras auditoría: f33 y34 sin cifra; f35 primera cifra tenue; f36 más opaca; f37/38 blanca. La frase anterior que asignaba cifra a34 era lectura de celda equivocada y se descarta. Sin desplazamiento/escala evidente en35–38; aclarado y borde son evaluación visual, no curva alpha exacta.
- «pagado»: f123 ausente; f124 semitransparente y borroso a y≈1345, f125 más blanco y un poco más alto, f126 más, f127/128 blanco con bordes nítidos. Movimiento hacia arriba continúo posterior: la entrada no equivale a una palabra estática desde primer OCR.
- La línea «ni me han» se ve realmente muy apretada, con hueco mínimo; no corregir su tipografía para reproducirla. Cabeza y torso cambian bajo el texto; no se pudo extraer alpha exacta sin base original sin overlay.

### Limitación de cadencia
Root auditó que repeats.json usa umbral maxblock<3 sobre JPG reducido, no igualdad exacta. +3 en f176 es una omisión visual potencial. Cobertura dense no certifica todos los originales; revisar hojas suplementarias cuando existan.

### Tercera tanda d008–d010 (f323–442)
- f323 limpio; f324 «que» tenue; f326 «que luego», f330 añade «ni». f334 entra «funcionan» gigante gris/transparente, f335 aclara, f336–338 blanco; texto grande queda bajo línea acumulativa y sale junto con ella en f351.
- f351–382: corte al plano sentada junto portátil Mac, luz solar diagonal; mano apoyada, sin subtítulos hasta f371 «Pruebo». Pausa de voz de 1,06 s coincide con recurso gestual.
- f383 gráfico de verde oliva con nube/textura y viñeta, sin texto hasta f389; f386 se revela círculo/radios finos, f387 crecen/radialmente abren, f389 1, f390 6, f391 15, f392 21, f393 24, f394 26, f395 28, f396–397 29, f398 30. Etiqueta «variantes» desde f394 tenue, f396 nítida. No contador lineal: subida acelera hasta 21 y frena hasta 30 en 9 f.
- f398–415 30 variantes con círculo radial de líneas finas con puntos externos; deriva muy suave de escala/posición, sin reiniciar objeto.
- f412 entra «a», f413 un, f415 costo debajo/derecha del círculo. f418 mínimo grande debajo; f416–424 cámara traslada/agranda composición hacia arriba-izquierda, 30 empieza blur evidente f416 y abandona cuadro por arriba; mínimo crece hasta ocupar zona central hacia f425. f428 «de producción» debajo. Cámara usa perspectiva: rótulos inclinados con tamaños no iguales entre extremos; pendiente medir.

### Corrección de índice pendiente
Nativo exacto select(n) confirma f34 SIN cifra, f35 primer «30», mientras dense d000 etiqueta f34 con cifra. Hay discordancia low/dense↔original, no asumir desfase global hasta auditoría root. Todas referencias de bitácora son índices dense salvo las marcadas nativo exacto. Se revoca afirmación nativa anterior de 30 en f34. El original f34 es un fotograma sin subtítulo ni cifra, detalle ausente en hoja dense. Esto demuestra por qué no basta la revisión dense.

### Cuarta tanda d011–d013 (f443–562)
- f443–449 mínimo permanece en centro, nube/viñeta, círculo cortado por arriba. f450 corte seco vuelta portátil; y f450–451 (omitida OCR); me452–456; quedo457–466.
- f467 «con» fuera centro x≈35 %, f470 «con el», f472 «con el que». f476 mejor gigante verde bajo línea; f477–480 crece/aclara. f481 funciona pequeño blanco debajo, empieza tenue. f481–488 «mejor» tiene oscilación ondulada/rotación de glifos (OCR 180° es artefacto pero la distorsión sí existe). f489–496 casi asentado verde.
- f497 corte seco a mujer sentada en sofá con almohadón/frazada, contraluz/luz solar; misma ropa. ¿Al f497–498, principio f499–510; mi511–513; jefe514–519; pensaba520–529; que530–532; el533–534; público535–543; no544–548 (omitido OCR); reaccionaría549–563. Rail cambia de cara/pecho en montaje pero siempre centro ≈60 %.

### Quinta tanda d014–d015 (f563–642): dense A completo
- f570–572 «a» ausente de OCR. f573–581 videos; f582 limpio; f583 hechos con fundido tenue, fija en línea superior más a izquierda; f588 con grande debajo, f589 añade IA formando con IA. f590–600 blanco pleno. Las dos líneas parecen crecer un poco juntas; pendiente medir nativo.
- f601 desaparecen líneas y empieza pero. f604–613 adivina; f614–619 qué; f620 corte seco dentro misma toma sofá a pose sonriente más abierta. Que en f620; la621–622; gente623–628; no629–632; compra633–640; f641 limpio; f642 por.

### Bitácora: Sonido observado en espectrogramas
Se miraron cuatro paneles 0–8, 8–16, 16–24, 24–32 s. No se escuchó audio. Voz dominante con armónicos ascendentes/descendentes y sibilantes anchas: no clasificar onsets automáticos como SFX. No se puede separar música base de voz en estas imágenes con certeza.
- 5,75 s (f138) inicio de B/N coincide onset z11,7 y pausa tras pagado, caída de voz hasta≈6,08. Es el mejor candidato de acento editorial; tipo no confirmado acústicamente.
- 14,44–15,50 voz calla durante portátil; varios transitorios agudos 14,49;14,72;14,89;14,96;15,03;15,18;15,43. El espectro muestra impulsos y no voz clara durante esa pausa; lectura: probable ambiente/efecto/música, no adjudicar todos a quién/qué.
- 16,25–16,6 contador presenta onsets pero algunas cifras caen entre ellos; no demuestra una cifra por golpe.
- Cortes f176,226,383,450,497 no requieren golpe alto z≥6 en mismo f. Norma «SFX cada corte» no respaldada.

### Bitácora: Ritmo
Cortes visuales densos candidatos 89,138,151,176,226,261,293,351,383,450,497,620. Cadena gráfica 383–449 incluye transición por cámara interna. El silencio 351–370 permite gesto; la animación llega sobre la reentrada Pruebo/30. No confundir ausencia de subtítulo con imagen quieta.

### Bitácora: Reglas deducidas provisionales
- La cifra o remate relevante desplaza al rail a una línea superior: ni me han/pagado f117–137; que luego ni/funcionan f324–350; con el que/mejor/funciona f467–496; hechos/con IA f583–600.
- El gráfico económico elimina rail pequeño duplicado: 300€/c/pieza f176–225; contador de variantes/mínimo f383–449.
- Cuando cambia de idea, corte de gesto/escenario y reinicio al rail: f226,450,497.
- Los onsets OCR omiten 1 f limpio y palabras cortas; secuencia visual prueba que textos no son exhaustivos como anotación de guion.

### Bitácora: Pendiente
Nativo de cada evento, alpha/color exactos, curvas de gráfico/perspectiva, cortes originales y revisión de omitted_frames. No puede marcarse forense completed.

### Bitácora: Láminas
Nativas parciales en analysis/tmp/v1-pagado-A; todavía sin láminas finales seleccionadas.

### Rectificación final de auditoría
Root contrastó low32–36, dense34 y original select(n), coinciden. Mis afirmaciones de 30 f34 fueron error de lectura de celda: el primer 30 es f35 (1,458 s); f34 limpio. Descartada hipótesis desfase global. La bitácora es índice válido pero algunos onsets descritos como candidatos requieren nativo.

Auditoría suplemento: s000_f00177-f00179.jpg visto completo. Tres cuadros blanco/viñeta sin textos, variación muy leve de fondo; no evento nuevo legible.

## 1. Planos

|Fotogramas|Duración|Tipo/escenario y movimiento|
|---|---|---|
|f0–f150 (0.000–6.250s)|151f / 6.292s|Cocina selfie; incluye candidato89 y B/N138–150; rail62.5→60%|
|f151–f175 (6.292–7.292s)|25f / 1.042s|Salón más abierto, recuadro cara y texto lateral|
|f176–f225 (7.333–9.375s)|50f / 2.083s|Gráfico gris/blanco con300€ y pieza; perspectiva y deriva|
|f226–f382 (9.417–15.917s)|157f / 6.542s|Mujer Mac/café; rail central50%; no banda reservada|
|f383–f449 (15.958–18.708s)|67f / 2.792s|Gráfico verde; contador30 y variantes; cámara sale arriba/izquierda|
|f450–f582 (18.750–24.250s)|133f / 5.542s|Busto con recursos; rail con acumulaciones|
|f583–f642 (24.292–26.750s)|60f / 2.500s|Sofá, rail hechos/con IA|

La tabla agrupa bloques narrativos; los cortes internos y sus dudas se conservan en bitácora y eventos. Cadencia del recurso inferior a timeline posible; similitud JPG reducida no certifica fotograma idéntico.

## 2. Cortes y transiciones

f176 (7.333s): salón a gráfico; f226 (9.417s): gráfico a persona; f383 (15.958s): persona a gráfico verde; f450 (18.750s): gráfico a persona. Descripciones por cuadro y voces en bitácora. Ningún SFX se asigna a un corte por onset automático solo.

## 3. Subtítulos base

Rail blanco sin fondo; cambia altura según plano. Acumulaciones ni→ni me→ni me han; con→con el→con el que. No es siempre una palabra ni siempre y60%.

## 4. Palabras de énfasis y tipografía cinética

30 f35–88 detrás de cabeza con contorno delante; pagado f124–137; funcionan f334–350; mejor f476–496 verde y funciona f481. Ver rectificación f34 vacío/f35 primer30 en bitácora.

## 5. Escenas gráficas (motion graphics)

300€ f187–189 alpha; por pieza f193–194. Variantes389–398 contador1,6,15,21,24,26,28,29,29,30. Variantes394tenue396plena. Movimiento416–438 recorta30 por arriba.

## 6. Superposiciones y efectos sobre la imagen

B/N138–150 conserva sonrisa/movimiento. No congelado probado.

## 7. Sonido

Todas las hojas pertinentes constan en coverage.json. Voz y consonantes dominan; hipótesis de fondo grave según notas específicas de bitácora. No audición; no certificar whoosh, impacto, ni tick por cada cifra. Marcas amarillas pueden ser sílabas. Desfase de transcripción ±50ms: no convertirlo en offset exacto del montaje.

## 8. Ritmo

Cambios de palabra frecuentes y cambios de jerarquía sobre núcleos de frase. Los bloques de la tabla muestran respiración; el sostenimiento de un título coexiste con movimiento vivo del metraje, gesto o deriva gráfica. No se ha medido el máximo global sin cambio visual ni se infiere de repeats.

## 9. Reglas que se deducen de este tramo

Lectura: cifra y promesa se promueven a gigante; pequeño rail puede acumular. Los interludios hacen deriva en perspectiva durante lectura. Evidencia en los intervalos arriba y JSON. SF Pro −60 sigue decisión del estudio; fuentes serifs ythin requieren catálogo propio.

## 10. Dudas y lo que no se pudo verificar

Cobertura dense completa y suplemento pertinente completo, espectrogramas pertinentes completos; revisión nativa SELECTIVA, aún no cada evento ni cada transición base. Véase native_ranges para lista exacta. No declarar completed forense. No afirmar todos los contornos/curvas medidos a partir de miniaturas ni cuerpo universal98px. Las entradas nativas heredadas de Claude en V3-A conservan procedencia. Queda medición exacta de alpha, curva de movimiento, máscaras por cuadro y posible corte de pose no confirmado cuando bitácora lo indica. No separar SFX con certeza sin audición/stems.

## 11. Láminas guardadas

- laminas/v1-pagado/v1-pagado-A-01-30-exact.jpg

```json
[
  {
    "tipo": "enfasis",
    "f0": 35,
    "f1": 88,
    "nombre": "cifra detrás de cabeza",
    "texto": "30",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "efecto",
    "f0": 89,
    "f1": 89,
    "nombre": "candidato salto pose no confirmado nativo",
    "texto": "",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "subtitulo_excepcion",
    "f0": 117,
    "f1": 137,
    "nombre": "acumulación pequeña sobre pagado",
    "texto": "ni me han",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "enfasis",
    "f0": 124,
    "f1": 137,
    "nombre": "gigante con rail acumulativo",
    "texto": "pagado",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "efecto",
    "f0": 138,
    "f1": 150,
    "nombre": "blanco y negro vivo",
    "texto": "",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "efecto",
    "f0": 138,
    "f1": 138,
    "nombre": "candidato salto pose B/N no confirmado nativo",
    "texto": "",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "corte",
    "f0": 151,
    "f1": 151,
    "nombre": "salón busto más abierto",
    "texto": "",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "superposicion",
    "f0": 151,
    "f1": 175,
    "nombre": "recuadro cara y texto lateral curvo",
    "texto": "porque no soy real",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "corte",
    "f0": 176,
    "f1": 176,
    "nombre": "salón a gráfico",
    "texto": "",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "grafico",
    "f0": 176,
    "f1": 225,
    "nombre": "precio",
    "texto": "300€ por pieza",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "corte",
    "f0": 226,
    "f1": 226,
    "nombre": "gráfico a persona",
    "texto": "",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "corte",
    "f0": 261,
    "f1": 261,
    "nombre": "salón salto postura",
    "texto": "",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "enfasis",
    "f0": 276,
    "f1": 292,
    "nombre": "2 superior y semanas abajo",
    "texto": "2 semanas",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "corte",
    "f0": 293,
    "f1": 293,
    "nombre": "salón nueva pose/frase",
    "texto": "",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "subtitulo_excepcion",
    "f0": 324,
    "f1": 350,
    "nombre": "acumulación pequeña sobre funcionan",
    "texto": "que luego ni",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "enfasis",
    "f0": 334,
    "f1": 350,
    "nombre": "remate gigante",
    "texto": "funcionan",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "corte",
    "f0": 351,
    "f1": 351,
    "nombre": "Mac recurso sin rail inicial",
    "texto": "",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "corte",
    "f0": 383,
    "f1": 383,
    "nombre": "persona a gráfico verde",
    "texto": "",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "grafico",
    "f0": 383,
    "f1": 449,
    "nombre": "contador y cámara en perspectiva",
    "texto": "30 variantes",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "camara",
    "f0": 416,
    "f1": 438,
    "nombre": "salida arriba izquierda",
    "texto": "",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "corte",
    "f0": 450,
    "f1": 450,
    "nombre": "gráfico a persona",
    "texto": "",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "subtitulo_excepcion",
    "f0": 467,
    "f1": 496,
    "nombre": "dos líneas subordinadas con gigante",
    "texto": "con el que mejor funciona",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "enfasis",
    "f0": 476,
    "f1": 496,
    "nombre": "verde con verbo pequeño",
    "texto": "mejor",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "corte",
    "f0": 497,
    "f1": 497,
    "nombre": "sofá",
    "texto": "",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  },
  {
    "tipo": "subtitulo_excepcion",
    "f0": 583,
    "f1": 600,
    "nombre": "acumulación",
    "texto": "hechos con IA",
    "detalle": "Ver bitácora y secciones para capas/entrada por cuadro. Nativo solo donde coverage lo registra."
  },
  {
    "tipo": "corte",
    "f0": 620,
    "f1": 620,
    "nombre": "salto pose sofá",
    "texto": "",
    "detalle": "Inspección completa dense. Ver bitácora; nativo selectivo en coverage."
  }
]
```

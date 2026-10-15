# Algoritmo V2 · sistema de decisiones basado en evidencia

10-10-2026. **Especificación y estudio abiertos; no motor de imitación certificado.** Sustituye el criterio simplificado de elección de recetas de V0.1. No sustituye los renders existentes. Las reglas estructuradas están en `datos/revision-v2/rules.json`, la evidencia en `events.json` y la geometría completa en `<slug>-tracks.json`. La interfaz se abre en http://127.0.0.1:4317/study.

**Implementación parcial 14/10/2026:** el selector V2 ya ejecuta una ventana relacional
con clip independiente de los glifos, curva de tiradores V8 y filtros de lectura/voz.
Se evita mezclar textos discretos por muestras del obturador. Tipografía, alfa y
traslación siguen diseñadas; no se ha reconstruido la oclusión. Ver
`notas/relacion-v2-2026-10-14.md`. Esta primitiva no acredita el repertorio completo.

## 1. Qué falló y qué cambia

El estudio anterior reunió material, notas y medidas selectivas, pero el motor lo redujo a recetas con anclas por familia, tamaños por ancho y puntuaciones léxicas. Por ejemplo, `planner.ts` asigna puntos a `hero`, `price` o `count` según palabras/datos, y la elección de ancla usa unas posiciones candidatas. Eso no modela la sintaxis visual, la intención de la frase, la evolución del plano ni las diferencias entre entradas. Un listado de efectos tampoco lo soluciona.

La V2 exige **un grafo temporal de elementos y decisiones justificadas**, con geometría, movimiento, oclusión y audio independientes. El resultado de cada decisión debe incluir casos pertinentes, alternativas descartadas, parámetros medidos frente a parámetros propuestos y una prueba de reconstrucción. Las 34 reglas actuales son hipótesis condicionales y restricciones documentadas, no pesos aprendidos ni la afirmación de haber recuperado la mente del editor.

## 2. Invariantes del encargo

1. Material ya editado: tiempo, orden y cortes bloqueados; una ventana de prueba conserva mapeo1:1 dentro del tramo. Ninguna heurística semántica puede autorizar cortes.
2. Feedback actual > versión vigente > preferencias > hipótesis del corpus. Birdieballs V03 está rechazada. Los parámetros propuestos de V03 no son parámetros del editor.
3. Versiones anteriores inmutables. Una aprobación parcial no se propaga al resto de la pieza.
4. Instantes de origen con fps racional e índice0. Las notas usan fin inclusivo; ejecución usa fin exclusivo. Convertir en el límite, una sola vez.
5. Nunca llamar exacto al primer frame OCR, al cuerpo tipográfico estimado, a la curva ajustada o al archivo SFX candidato.
6. Probar un tramo significa acabado integrado: texto, efectos, motion, mezcla. La tarea actual es estudio, no otro render de Birdieballs.

## 3. Ontología: separar lo que antes se mezclaba

Cada elemento tiene ejes independientes:

| Eje | Estados / datos |
|---|---|
| Función verbal | lectura, foco, contexto, remate, diálogo, etiqueta, enumeración, nombre/cargo, omisión justificada |
| Representación | palabra sustituida, acumulación, stack, lista, arco, texto en objeto, UI, contador, diagrama, escena física |
| Papel narrativo | gancho, problema, coste, prueba, mecanismo, comparación, demostración, objeción, respuesta, CTA, reacción |
| Plano/capas | sujeto, segundo hablante, producto, manos, objeto de acción, fondo, gráfico previo, luz, cámara |
| Profundidad | frontal, relleno detrás, detrás+contorno delante, integrado por perspectiva, desconocido |
| Movimiento | directo, traslación, sobrepaso, asentamiento, pulso discreto, trayectoria por glifo, reflow, relevo, cámara |
| Audio | voz, música, diálogo, SFX, sonido de escena, mezcla desconocida |
| Evidencia | preferencia explícita, observación panorámica, secuencia nativa, medida, ajuste, inferencia, reconstrucción validada |

Un rail puede ser grande y estar enmascarado. Un titular puede ir delante. Un gráfico puede tener texto de lectura pequeño. Un texto diegético no se convierte en subtítulo porque el OCR lo detecte.

## 4. Ficha mínima de un evento

Identidad: referencia SHA256, familia independiente, clip, layoutId, elementId, speakerId, objectId, versión de anotación y procedencia.

Lenguaje: transcripción corregida, palabras vinculadas, función sintáctica, foco de frase, relación con imagen, segmento narrativo y justificación de omisión/paráfrasis si la hay. ASR es una propuesta que se corrige; en V8 `Brawl` no certifica el nombre de marca, ni `sacarlas en ti` la frase pronunciada.

Tiempo: frame anterior limpio, primer píxel visible, primer estado legible, fin de entrada, extremo de sobrepaso, inicio/fin de asentamiento, intervalo de lectura, inicio de salida, último píxel, siguiente estado. Cada hito puede ser `unknown`; deben conservarse intervalos de incertidumbre, no solo un entero ficticio.

Geometría: x/y de ancla, tipo de ancla, caja de tinta, baseline, ancho/alto, giro, escala, recorte, márgenes, espacio disponible, relación a otras líneas, tamaño relativo al rostro/objeto y superposición permitida. Coordenadas locales y de pantalla separadas.

Tipografía: familia candidata, peso, tamaño nominal si está calibrado, tracking, kerning, altura de mayúsculas/x, proporción de glifos, caja, alineación, color interior, trazo, sombra y orden de capas. La caja OCR no rellena automáticamente esos campos.

Movimiento: muestras x/y/escala/ángulo por frame, trayectoria de glifos si procede, velocidad/aceleración, extremos, normalización temporal, función ajustada, dominio y error. Opacidad, contraste observado, nitidez y estela son campos distintos. El fondo y cámara tienen su propia transformación.

Combinación: dependencias `appearsAfter`, `persistsThrough`, `replaces`, `reflows`, `occludedBy`, `outlineAbove`, `anchoredTo`, `releasesFocusTo`. No limitarse a agrupar todas las palabras que aparecen simultáneamente.

Audio: ventana original, onset y pico candidatos, familia perceptiva, sample candidato, método de identificación, confianza, desfase frente a acción, ganancia frente a voz, panorama, pitch/velocidad, ataque/cola, y estado de escucha. `sampleId=null` mientras no esté identificado.

## 5. Cómo decidir la posición

Primero escoger **layout completo**, después situar palabras dentro. Entradas: recorrido del sujeto/objeto durante toda la frase; zonas de interés; espacio negativo; movimiento de cámara; elementos ya activos; hablantes; dirección de lectura.

Generar candidatos pertinentes a referencias cercanas, no una lista global de y posibles. Un candidato incluye anclas de rail, héroe y apoyos, además de política de profundidad. La puntuación debe separar:

- Lectura: área de tinta legible a lo largo del tiempo y contraste local sobre fotogramas reales.
- Competencia semántica: ocultar producto, gesto o demostración cuando son el foco tiene más coste que cruzar ropa.
- Jerarquía: foco correcto, diferencia entre protagonista y apoyo, masa equilibrada.
- Continuidad: desplazamiento innecesario del bloque, saltos entre layouts y conflicto con el frame previo/siguiente.
- Correspondencia: similitud con ejemplos de misma función y geometría, descontando variantes derivadas.

Las ponderaciones necesitan calibración. No se presentan números arbitrarios como si fueran aprendidos. Los límites de permiso son filtros duros anteriores a cualquier puntuación.

C01/C02/C08 recogen evidencia. V8 cambia y≈50%→20% para narración cuando entra protesta central. Landing cambia rail a derecha cuando la lista ocupa izquierda. LaFabrica cambia posición dentro de un mismo plano. No se deduce una regla universal de «evitar cara».

## 6. Cómo decidir tamaño y fuente

Secuencia: rol→familia visual pertinente→masa óptica→ajuste al espacio→control de texto completo durante movimiento. Para rail, elegir cuerpo coherente de bloque y reducir solo si el ancho excede la zona. Para héroe, establecer prioridad visual y ajustar ancho/alto con glifos reales. No estirar una palabra corta hasta llenar el mismo ancho que una larga.

Medir tamaño con render de fuente candidata sobre ROI nativa no ocluida. Explorar cuerpo/tracking y registrar error de forma/contorno. Usar varias palabras con glifos discriminantes y distintas longitudes. Una buena coincidencia en una palabra no identifica toda la familia. Diferenciar transformación del texto y cambios de caja por máscara o revelado.

T01/T02/C03/C04: V8 cambia a ultracondensada para el remate del astronauta, luego vuelve al sans de explicación; V3 cambia a serif en ciertos conceptos pero mantiene otros énfasis en sans lima. No hay evidencia para «cambia de fuente cada X segundos».

Calibración nueva sobre dos términos V8: SF Pro Display **Regular** alcanza IoU0,952 en pagar y0,924 en Braudd frente a máscaras cromáticas nativas. Los ajustes resultan409/313px de cuerpo y−29,36/−20,88px de tracking, respectivamente. Son parámetros de reconstrucción ajustados; no se ha leído el proyecto original del editor. No trasladar la identidad a todos los estilos. Lámina de diferencias y resultados en `datos/revision-v2/v8-font-calibration.json`.

## 7. Cómo decidir multilínea y combinación

No dividir por número de caracteres. Detectar relaciones: contexto+número; verbo+objeto; negación+núcleo; sustantivo+calificador; pregunta acumulada; lista; dos voces independientes.

Para cada alternativa de agrupación:

1. Conservar unidades sintácticas y orden de comprensión.
2. Elegir núcleo y apoyos; asignar qué continúa visible al añadirse el siguiente.
3. Calcular cajas de tinta con acentos/descendentes y margen de efecto. Evaluar gap entre líneas por frame, no solo line-height CSS.
4. Fijar ancla de primera línea según feedback; cualquier reflow debe estar coreografiado y justificado por referencia.
5. Decidir alineación del complemento respecto al héroe: centro, izquierda, extremo o espacio libre, sin centrarlo todo automáticamente.
6. Diseñar entradas de cada unidad; las palabras de apoyo pueden tener desfases y curvas propias.
7. Evitar duplicar el núcleo en rail y título salvo función deliberada distinta.

Ejemplos: `no es solo / pagar / otro sueldo` tiene tres niveles; `¿Que / el cliente / quiere / probar / otro / enfoque?` seis filas alineadas a izquierda; la protesta verde no forma doble línea con narración blanca. C05–C08.

## 8. Movimiento y curvas

Representar cada propiedad separadamente y evaluar de forma determinista en cualquier frame. Nunca inferir escala creciente de una caja OCR temprana más pequeña. Separar cuatro familias ya documentadas:

- Entrada directa: cambios de rail de V8f452/f463 o Landingf4321.
- Ascenso desacelerado: Gracias de Landingf9–55; ajuste de posición con error medido. No pop de escala probado.
- Ascenso con oscilación amortiguada: héroes lima de V8; curva compartida en estudio cuantitativo. No simplificar a fade.
- Pulso discreto: BLACK/FRIDAY de V6rev; secuencia opaco/parcial/ausente con período4f a60fps.

Para dirección, usar desplazamientos medidos entre muestras con el mismo contenido y sin cambio de máscara; velocidades normalizadas por segundo. Rotación de glifos en un arco ≠ rotación de bloque. Motion blur temporal ≠ desenfoque de foco. Sin información adicional, el nombre del easing/plugin, el shutter exacto y la alpha original son no identificables de forma inequívoca.

Las salidas no se derivan de la entrada invirtiéndola. Medir si corta, desvanece, fragmenta, sale por vector, es ocluido o persiste al nuevo plano. Medir solapes: pedir/sirve en V8 y Gracias/Te en Landing. A01–A07.

## 9. Máscaras y profundidad

Exigir recorte del objeto real con pelo/manos/casco, transformado igual que el metraje. Diagrama de capas explícito. Dos casos distintos: relleno detrás sin contorno; relleno detrás con contorno frontal. Outline y sombra no se intercambian.

Verificar letras antes/durante/después de oclusión y bordes en movimiento. El movimiento del sujeto no cambia necesariamente ancla del texto. M01/M02. Si no hay máscara fiable, ese tratamiento no está listo para producción; un rectángulo/óvalo genérico no es una réplica.

## 10. Motion: elección, cadencia y producción

Separar interludio de diseño, gráfico superpuesto, texto cinético, UI integrada, objeto físico/generado dentro de metraje y efecto de cámara. Los intervalos `grafico` de notas son un subconjunto, no un censo de todo motion.

**Brutos aportados el10/10:**68vídeos y10audios inventariados conSHA256;10pares de escena revisados visualmente. La bombilla de V8 y la máquina/tarjetas volando de V5 ya están en el bruto; la edición añade, entre otras cosas, la tipografía. El móvil con fondo gris de V8 sí se añade. G07 obliga a separar esas atribuciones. Los pares tienen índices nativos exactos dentro de cada archivo, pero aún no una alineación temporal exacta entre ambos. No usar diferencias píxel a píxel como máscaras hasta resolver recorte/retiming/color. Interfaz `/raw-study`.

Desencadenantes candidatos: una cantidad que debe verse; comparación; secuencia de pasos; funcionamiento; transformación; promesa que se demuestra; cambio de concepto. Evaluar si la imagen ya cumple esa función, duración útil para acción/lectura y competencia con información anterior. No insertar recursos por tiempo transcurrido únicamente.

Coreografía: objeto portador, acción inicial, cambio de información, transformación/traspaso de foco, asentamiento legible, salida. En el contador30 de V1 el valor termina antes de que termine la composición; se añade variantes, la cámara viaja y mínimo toma foco. El objeto puede sostenerse si otra propiedad relevante sigue evolucionando. La advertencia de quietud0,65s de V03 no es una ley extraída del editor.

Ejemplo medido de grafo: V8 clientes→empleados. Los tiradores azules pasan de810px separados en230 a2px en255–257 y vuelven a810px en300; centro≈539px. El texto conserva forma y se recorta por la selección: **clipWidth(t) no es scaleX(t)**. Nuevos sale antes que clientes; = ocupa el contexto; Nuevos vuelve antes que empleados. Se requieren pistas independientes para ambos tiradores, relleno, contexto superior, traslación de palabra, máscara del contenedor y máscara frontal del sujeto. G03 contiene el grafo de fases y `v8-selector-curves.json` las medidas por fotograma y sensibilidad al umbral.

Producción: material/textura, escala del grano, iluminación, sombra de contacto/proyectada, perspectiva, oclusión, desenfoque de movimiento, profundidad de foco, transición con escena anterior/siguiente. Una bola trasladándose sobre verde con ruido no cumple por sí sola ese diseño. El recurso tiene que representar el argumento. G01–G06.

## 11. Sonido: metodología y límites actuales

STFT actual: 44.100Hz, ventana2048muestras (~46,44ms), salto441 (~10ms), resolución frecuencial21,53Hz. La localización fina queda condicionada por ventana, mezcla y alineación. Un pico de flujo puede ser una consonante, golpe musical o SFX. El detector no escucha y no identifica.

Para identificar familia: ventanas alrededor de eventos visuales + onsets, escucha del original, separación provisional si ayuda, etiqueta perceptiva y contraste con negativos. Para sample concreto: catálogo de candidatos, embeddings acústicos/semánticos, huellas de picos o correlación, búsqueda de desplazamiento/ganancia/pitch/tempo, escucha comparada de ataque/cuerpo/cola. Separación no certifica identidad.

Fuentes primarias: [CLAP](https://github.com/LAION-AI/CLAP), [audfprint](https://github.com/dpwe/audfprint), [AudioSep](https://github.com/Audio-AGI/AudioSep). Esas herramientas no se han ejecutado en esta revisión. La falta de Diffusion Studio impide usar su análisis semántico en la sesión. No marcar audio como completado.

## 12. Aprender decisiones, no memorizar un único vídeo

Unidad de ejemplo: evento con contexto, tratamiento observado, alternativas disponibles y nivel de evidencia. Construir también negativos: cifra sin héroe, cara cubierta sin máscara, gráfico posible no usado, corte sin SFX, frase larga sin multilínea. La ausencia se verifica visualmente, no por OCR vacío.

Recuperar vecinos por función, sintaxis, composición, objetos, duración y estado previo. Agrupar V6/V6rev/V7 para evitar fuga de evaluación. Separar los tratamientos particulares de una pieza de los repetidos en familias distintas.

Calibrar reglas solo con ejemplos anotados; evaluar dejando una familia fuera. Preguntas de evaluación: ¿predice el papel de cada texto? ¿selecciona layout de geometría comparable? ¿elige la familia de movimiento correcta? ¿produce los hitos y relaciones correctos? ¿distingue cuándo no aplicar el recurso? Un acierto en la curva de tres títulos del mismo vídeo no acredita todo el estilo.

No se ha entrenado un modelo nuevo. La V2 mantiene hipótesis y evidencia con incertidumbre y prepara una política comprobable. No usar supuestas probabilidades80/90% sin evaluación.

## 13. Salida del planificador y contrato de producción

El plan debe contener mapeo de metraje, grafo de capas/eventos, bindings de palabras, layout por bloque, tipografía calibrada, propiedades temporales, máscaras y audio; además, para cada decisión: regla, evidencias, alternativas, razón, valores medidos/propuestos/desconocidos.

El contrato ejecutable está en `../motor-editor/forensics/contract.mjs`: valida preservación temporal, identidad de ejemplos, procedencia y campos necesarios para afirmar reconstrucción verificada. No altera recetas de renders previos. El planificador0.1 todavía debe migrarse a esta política antes de presentarlo como equivalente; su elección heurística no adquiere fidelidad por existir este documento.

## 14. Validación y cierre

Tres comprobaciones separadas:

1. **Técnica:** índices, unidades, intervalos, fuente/asset disponible, determinismo de seek, máscaras con transform idéntico, continuidad base/audio.
2. **Fidelidad:** comparación nativa sincronizada; primer/último píxel; masa/posición; fase y velocidad; solapes; tipografía; oclusión; luz/material; sonido frente a gesto. Inspección de entrada, extremo, lectura y salida a velocidad normal y lenta.
3. **Editorial:** funciona en el nuevo guion, conserva sentido y prioridad, y supera feedback del usuario. No se infiere de tests.

Cierre de una ficha exige pruebas y límites explícitos. Cierre del estudio exige cobertura de todos los eventos y contraejemplos, no solo lectura de todas las hojas. `corpus.json` y `CURRENT-STUDY.json` permanecen `complete:false`: la identidad de fuentes/SFX y la revisión nativa de todas las transiciones aún no están resueltas.


## Preferencias de dirección por proyecto

### Ejecución autónoma y curvas · actualización 14/10/2026

Remotion es la base programática vigente para clientes; AE es una herramienta interna.
Mantener separados decisión editorial, datos del plan y ejecución, sin convertir esa
separación en múltiples integraciones aún inexistentes.

Revisión del ajuste V8 ya medido: «sirve» reproduce la entrada en edades fuente 2–23 con
RMSE 1,2324 px, pero la comparación completa 2–32 da 14,2953 px y llega a 56,2558 px de
desviación. La separación de fases fue exploratoria posterior, del mismo vídeo; no es un
test independiente entre familias. No ocultar el error completo ni declarar universal la
curva. Evidencia: `datos/revision-v2/v8-motion-fit.json`.

Reglas ejecutables nuevas en `motor-editor/src/caption-keyframes/reference-v2.ts`:

- Evaluar en segundos: fps fuente convierte a edad del ajuste; fps salida solo selecciona
  muestras. No comprimir una trayectoria medida para que quepa en una palabra corta:
  escoger un subintervalo revisado o un recurso distinto.
- Escalar desplazamiento por altura sin alterar duración ni velocidad normalizada. Esto
  no resuelve recomposición de layout entre relaciones de aspecto.
- Separar llegada diseñada, tramo ajustado, asentamiento, lectura y salida. Declarar
  procedencia de posición y opacidad por separado: medir posición no mide alfa.
- Empalmar posición y velocidad, permitir tiempos fraccionarios de obturador, usar
  intervalos de visibilidad semiabiertos y evaluación sin estado.
- Rechazar solapamiento entrada/salida, rangos fuera del ajuste o parámetros inválidos.

Estado actualizado en el mismo día: la primitiva ya está conectada al selector experimental
`motor-editor/src/editorial-v2/index.ts`. Su selección depende de función, duración y
colisiones de tinta. Se renderizó un piloto y se corrigió una interferencia observada;
53 pruebas técnicas pasan. Queda validar fidelidad entre familias. Evidencia y límites en
`notas/selector-v2-2026-10-14.md`. Se conserva el helper anterior para entregas históricas.

### Dirección Birdieballs

El cuestionario Cutroom `/quiz` reúne las once referencias y decisiones sobre los patrones documentados. Sus respuestas persistidas en `motor-editor/review/data/quiz-decisions.json` son restricciones de dirección para Birdieballs, con identificadores de pregunta, opciones, comentario, tramos y procedencia. Leerlas antes de una siguiente propuesta. Una respuesta pendiente/aplazada no aprueba un recurso; elegir un ejemplo no certifica el resto de la pieza. Las respuestas no sustituyen mediciones ni implementan automáticamente un planificador. V04 está rechazada; la última evidencia prevalece sobre propuestas antiguas.

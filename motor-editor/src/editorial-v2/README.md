# Selector editorial V2 · piloto ejecutable

Este pase conecta decisiones de contexto con el render Remotion, conservando el compilador
0.1 para reproducir trabajos anteriores. No es una réplica validada del editor ni un modelo
entrenado. El agente aporta una lectura semántica del plano/frase y el compilador la
convierte en una composición verificable; no detecta caras ni entiende vídeo por sí solo.

## Entrada y ejecución

Un Job existente incorpora `editorial.version:2`, una ventana fuente bloqueada y una
anotación por cláusula. Ejemplo ejecutado: `../../lab/editorial-v2/birdie.job.json`.
Las anotaciones explican función, foco, grupo de composición, zonas protegidas temporales
y procedencia de la observación. Para omitir texto exigen una justificación explícita.

Desde la raíz del repositorio:

```sh
node motor-editor/cli.ts compile-editorial motor-editor/lab/editorial-v2/birdie.job.json --out motor-editor/lab/editorial-v2/birdie.plan.json
node motor-editor/cli.ts inspect motor-editor/lab/editorial-v2/birdie.plan.json
node --test motor-editor/tests/editorial-v2.test.ts
```

`compile` también detecta un campo `editorial` y utiliza V2; no lo ignora silenciosamente.
El plan resultante se renderiza mediante la composición existente `ReferenceEdit` y sus
props JSON, sin AE ni interacción con una interfaz. El laboratorio incluye `render.mjs`.

## Decisiones implementadas

1. **Función antes que longitud o cifras.** Un número incidental puede seguir en el rail;
   una palabra ancha no se convierte por ello en titular. Tener un recorte alpha no
   justifica emplearlo. La omisión exige que la acción visual y una razón la justifiquen.
2. **Alternativas a escala de secuencia.** Programación dinámica compara rail, apoyo/foco
   apilado, construcción en una línea, omisión y relación explícita compatible. Penaliza repetir construcciones marcadas
   consecutivas, sin imponer variedad a los rails ordinarios. Costes 0/2/5/7 y mínimos
   temporales son propuestas, no frecuencias recuperadas del editor ni probabilidades.
3. **Geometría antes de aparición.** Reserva las posiciones de las palabras y calcula
   interlínea con métricas de tinta SF Pro. Las nuevas palabras no recentran las anteriores.
   Cada `layoutId` conserva un ancla elegida frente a todas sus frases y regiones protegidas
   pertinentes, también las que aparecen tarde. Si no cabe, falla para rediseñar.
4. **Movimiento condicionado por espacio.** Evalúa tinta animada cada medio frame durante
   los primeros 0,5 s. Prueba la posición ajustada de V8; si invade otra línea, elige una
   entrada monótona diseñada; si esta tampoco cabe, prueba opacidad sin traslación.
   No mueve el bloque entero para remediarlo. Los enlaces, la alternativa y el alfa se
   distinguen del movimiento ajustado. Obturador de 180°, 8 muestras en esos énfasis.
5. **Fuente y trazabilidad.** Una sola ventana de vídeo conserva continuidad y audio de
   origen, incluyendo silencios anteriores/posteriores a los textos. Las decisiones llevan
   alternativas, razones, evidencias y procedencia. La cobertura evita texto duplicado.

## Evidencia y límites

Contraste nuevo de muestras V1 «ni me han / pagado» y La Maquinita «automáticamente»;
originales verificados por SHA256. Secuencias, PNG y manifiesto en
`../../lab/editorial-v2/reference-frames`. No es una revisión nueva completa de las fuentes.

El piloto de Birdieballs dura 270 frames a 60000/1001 fps, conserva el metraje de entrada
y utiliza los tiempos por fragmento de V07. No los convierte en alineación palabra a
palabra: «cada vez que sales» se conserva como una unidad ancha. Se revisaron fotogramas
seleccionados; no se certifica reproducción completa ni escucha independiente.

Faltan: extracción/alineación automática fiable de contexto y palabras, resolución de
diálogo simultáneo en V2, composición entre formatos, contraste óptico completo y
un repertorio amplio de escenas de motion que expliquen relaciones. `explain-relation`
puede ejecutar la ventana de sustitución/igualdad descrita abajo; los casos no soportados
conservan `EDITORIAL_DESIGN_REQUIRED` y un rail provisional, no una entrega terminada.
Las recetas antiguas de contadores/fondos no se reintroducen como sustituto automático.

La fidelidad entre familias y la aprobación artística siguen pendientes. 64 pruebas
técnicas pasan (11 específicas de relación); eso comprueba restricciones, no gusto.

## Ventana relacional · segunda iteración

`Annotation.relation` declara `kind` (replacement/equivalence), `fromWordIds`,
`toWordIds`, contextos opcionales `beforeContextWordIds` / `afterContextWordIds` y
`reason`. Solo se utiliza con función `explain-relation`. Ejemplo reproducible:
`../../lab/relation-v2/job.json`.

El plan incluye un nodo `relation`, renderizado por `RelationView.tsx`: anchura del
recorte independiente de glifos, contexto separado y entrada del segundo término.
La curva de separación proviene de V8 f230–300; la tipografía, alfa, posición vertical y
lectura son diseñadas. Se admite una unidad temporizada por término/contexto. No se
acelera la curva para caber ni se activa por detectar simplemente dos sustantivos.
Se rechazan vínculos incompletos, orden imposible, lectura insuficiente y colisiones.

El obturador toma geometría en subframes y el texto discreto en el frame presentado.
Así una sustitución no mezcla dos strings aunque los tiradores se muevan con blur.
Para relaciones no compatibles queda una advertencia explícita. No hay segmentación
automática del sujeto, identidad de SFX ni aprobación de estilo implícita.

Evidencia, corrección del primer render y límites:
`../../../estilo-editor/notas/relacion-v2-2026-10-14.md`.

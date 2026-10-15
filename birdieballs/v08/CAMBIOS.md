# Birdieballs · V08 · After Effects

Reedición completa de los 2278 fotogramas (38,005 s) en After Effects, solicitada por Ale. El montaje, la locución y la música de origen conservan orden y tiempos. Las versiones anteriores se mantienen. Pendiente de veredicto; no se declara equivalencia global con las referencias.

## Cambios realizados

- Texto nativo editable en SF Pro Regular/Bold. Apoyos compactos, jerarquías construidas y anclas estables por bloque. Entradas con aceleración/frenada específicas, remates breves y lectura quieta. Obturador nativo de 180°.
- Riñón: subida corta y frenada con pequeño asentamiento, seguida del remate en bolas. Solución: una composición en profundidad, relleno detrás del sujeto y contorno delante; misma trayectoria en ambos.
- Producto: bolas/originales en una jerarquía compacta, con trazo de entrada; el metraje real sigue explicando el producto. Revisión: barrido sobre la bola, esquinas de inspección y check dibujado al completar una a una. Se exploraron tres diseños nativos y se eligió el que mantiene más clara la prueba visual.
- Acentos de cámara puntuales en reacción/diálogo/CTA, reflejos breves ligados a la bola limpia y al paquete. Sin nuevos cortes ni retiming.
- Música y voz originales conservadas; 16 acentos sonoros, con su función y ganancia documentadas en study/sound-events.json.

## Correcciones de la revisión

1. Cierre: reducido por menos de208 a192px para dejar margen. Eliminados subrayados repetidos en riñón y nuevas.
2. 22,42–27,04s: un subtítulo tapaba la bola blanca en el macro. Rail de lectura bajado a1640px, apoyo y protagonista final compactos; trazo/sombra ajustados.
3. 27,31–31s: se probó un oscurecimiento superior para el contraste. **Ale lo rechazó expresamente durante el trabajo. Retirado de la versión entregada**, conservando limpio el gráfico original del70%. Se ajusta solo la tipografía de apoyo.

## Editable y reproducibilidad

Abrir ae/Birdieballs-V08.aep, composición BIRDIEBALLS V08 - MASTER. Medios locales en assets; las fuentes SF Pro ya están instaladas y se incluyen las copias empleadas como referencia. El proyecto contiene tres comps de exploración, claramente separadas del máster.

Las operaciones efectivamente ejecutadas y sus respuestas están en ae/*.json y *.jsonl. La secuencia está en study/native-spec.json; los IDs de importación corresponden a esta ejecución, no a cualquier proyecto abierto. Los parches forman parte de la definición final. No recrear el proyecto únicamente desde build.py omitiendo las correcciones posteriores.

## Evidencia y límites

Inspección de estados por todo el anuncio y secuencias de entrada/salida de riñón, solución y revisión, más los cortes del producto/paisajes. Los tiempos están cuantizados a59,94fps, no a una supuesta precisión visual de1ms. QA.json documenta formato, decodificación, sincronía y comprobaciones del proyecto.

La máscara procede de segmentación automática ya usada sobre estos fotogramas, no de rotoscopia manual. La revisión del sonido se limita a sincronía y señal: no se afirma escucha independiente. Las decisiones nuevas son propuestas del agente, no preferencias ya aprobadas.

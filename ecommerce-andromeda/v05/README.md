# Andrómeda V05 · motion en la espera

Ale valora la V04 («bien») y pide añadir motion graphics. Corrige expresamente la primera ubicación propuesta: «en la maquinita no, mejor en otro sitio». La composición final no añade ni reemplaza nada en la maquinita. No modifica el gag de sudadera aprobado en blanco y negro y sin subtítulos.

## Propuesta aplicada

Calendario de hojas sobre la zona libre de pared durante «días y días», frames480–550 de48fps:10,000–11,479s. Una semana pasa en una aceleración de seis cambios de hoja. Fechas/números ilustrativos del paso del tiempo; no representan una medición de plazos reales del servicio.

Se exploran tres mecanismos con fotogramas sobre el material: A, hojas físicas que pasan; B, recorrido por cuadrícula; C, reloj acelerado. Se elige A por encaje con los materiales de la lavandería y lectura inmediata a tamaño móvil. Las alternativas se conservan en `stills/concept-board.jpg`.

`WaitingMotion.tsx` ejecuta geometría editable: hojas con perspectiva, giro alrededor de anillas, sombra, reverso, varias capas de papel, textura procedimental, acento violeta discreto y desenfoque de giro. Las fases se aceleran8/7/6/5/4/4frames sin cambiar el número de la misma hoja durante el movimiento. Entrada9frames, pequeña pausa sobre07, salida10frames. Los subtítulos siguen en su lugar; no se repiten las palabras «días y días» dentro del gráfico.

Referencia consultada: T3 para aceleración de estados y pausa legible. T2 se estudió para la propuesta descartada de pantalla; no se usaron sus píxeles ni su audio. La captura de concepto utiliza una imagen de la V04 propia, no material externo.

No se han añadido sonidos sin revisión auditiva. Voz nativa, mezcla, montaje, velocidades, texto y fuentes de V04 preservados.38,33s disponibles,48fps;06sigue provisional. La nueva pieza está diseñada y revisada por fotogramas/secuencias, pendiente del veredicto de Ale; no se afirma reproducción/escucha completas independientes.

## Reproducir

Desde la raíz: `node ecommerce-andromeda/v05/render.mjs --bundle`. `--concepts` guarda las tres variantes. `--prototype` exporta9,5–11,875s. La composición principal añade solo `WaitingMotion` a V04; no regenerar ni sobrescribir los assets compartidos por hard link.

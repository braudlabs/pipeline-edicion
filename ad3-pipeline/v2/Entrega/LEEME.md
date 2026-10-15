# Visual Hub · Pipeline autónomo · V2

V2 sustituye los cinco bloques de motion de V1. V1 se conserva por separado. Duración y montaje hablado: 46,875 segundos, 1080 × 1920, 48 fps. Imágenes de origen a 24 fps y gráficos animados a 48 fps. Audio del MP4 V1 conservado sin recodificar.

## Abrir y editar

After-Effects/AD3-Pipeline-V2.aep → composición AD3 - FINAL V2. Requiere After Effects 2026. Tipografía SF Pro Display Bold y fuentes del sistema indicadas en las capas; no se redistribuyen fuentes. No se usan plugins de terceros.

- MG V2 - Ensamblado: tres pistas materiales, cierre y resolución al plano siguiente.
- MG V2 - Creatividad: planos independientes convergen en una pieza.
- MG V2 - Consistencia: láminas se alinean en una apertura; la persona mantiene su identidad entre escenarios.
- MG V2 - Sistemas: núcleo y cuatro salidas conectadas, reveladas por cámara.
- MG V2 - Produccion: recorrido entre resultados a distintas profundidades.

Cada composición tiene capas y claves nativas. CAMARA - Recorrido controla el encuadre. FOTO V2 / VENTANA V2 contienen las fotografías sustituibles. CAPA V2 - Texto contiene tres rótulos editables; la onda de CAPA V2 - Voz es un trazado derivado de la voz real. El espaciado de los rótulos usa un layout fijo: al alargar mucho una frase, revisar su tamaño y alineación.

Los cuatro recursos generados (escenario, chasis, marco e iris) son imágenes raster con volumen simulado mediante capas 3D y cámaras de AE: técnica 2.5D. Los materiales y reflejos de estos PNG están integrados en la imagen; posición, escala, orientación y recorrido son editables. Las fotografías proceden de las tomas aportadas. No se han incorporado imágenes de los vídeos de referencia. Arte/prompts.json y Arte/prompt-iris.txt conservan los prompts usados con image_gen integrado; Exploracion-A-B-C.png es el estudio previo, no una animación renderizada.

Remotion contiene el montaje base silencioso. Ejecutar npm ci y npm run studio; npm run render:base exporta a After-Effects/assets/Montaje-AD3.mp4. Los motions se renderizan desde AE. Conservar la estructura de carpetas al trasladar la entrega.

El SRT contiene el guion completo. El MP4 ya incluye el texto diseñado: activar además el SRT duplicaría la subtitulación. La primera frase del susurro no lleva texto integrado por el primerísimo primer plano, igual que V1. Las frases representadas mediante motion no se repiten en un subtítulo inferior.

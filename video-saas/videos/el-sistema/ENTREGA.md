# El Sistema · V2 · La máquina

Vídeo SaaS de 65.167 s, 1920 × 1080, 30 fps. Proyecto y motion graphics nativos de After Effects. Versión para revisión del usuario; no se registra como aprobada.

## Archivos

- `output/El-Sistema-V2.mp4`: H.264, audio AAC estéreo.
- `ae/El-Sistema-V2.aep`: 40 composiciones; texto, formas, claves y planos con perspectiva editables.
- `output/El-Sistema-V2.srt`: subtítulos separados de la película. `El-Sistema-V2.vtt` permite activarlos en la página de revisión.
- `output/Contacto-V2.jpg`: fotogramas numerados y tiempos del resultado.
- `assets/Voz-V2.wav`, `Musica-V2.wav`, `Efectos-V2.wav`: pistas separadas. `Mezcla-V2.wav`: mezcla utilizada.
- `Revisar-V2.html`: reproductor local con capítulos.
- `src/design-v2.json` y `scripts/design-v2.py`: fuente de composición; `scripts/build-ae.py --v2` reconstruye la película en el entorno de trabajo original.

## Decisiones

La última indicación del usuario sustituye Denim Trucker por el anuncio de la maquinita. Se usan los 16 clips aportados de ese anuncio para el mapa y una selección de cinco para el montaje demostrativo. Las voces de esos clips no se mezclan con la locución del SaaS.

La interfaz toma su jerarquía y colores de la plataforma real; se reconstruye y simplifica en capas para la película. Los módulos del interior, revisión, editor y variantes son visualizaciones del funcionamiento. No son una grabación de operaciones ejecutadas en el backend. Los fotogramas del moodboard proceden de los vídeos existentes; no se afirma que fueran sus anclas originales. No se atribuye un modelo generativo concreto a La Máquina ni se inventa un descarte documentado.

Las tres referencias aportadas se estudiaron como dirección visual: aproximación al campo de entrada, montaje de módulos y planos oblicuos. No se han insertado sus fotogramas, logotipos o audio. La geometría utiliza planos 3D de AE y perspectiva; no hay modelos 3D volumétricos de la máquina.

Se han eliminado 3,824536 s del centro de 22 pausas de la locución. Se conservan palabras y velocidad original. El mapa `src/retime.json` gobierna las animaciones y el SRT. Se deja cola tras «El Sistema».

## Sonido

Locución ElevenLabs aportada. Música y efectos de la biblioteca local existente; no se han consumido créditos de generación. Clics, escritura, movimientos y encajes se sitúan en el reloj retimado. Mezcla medida: −16,24 LUFS integrados, pico verdadero de la mezcla −1,50 dBTP. MP4 AAC medido: −16,24 LUFS, −1,38 dBTP y rango de sonoridad 3,9 LU.

## Revisión

Comprobados estados clave de las seis partes, mapas antes/después de animar, clips del editor, márgenes de textos y cierres. Correcciones: orden de entrada de los vídeos, escala de la apertura, margen del botón del mapa, subtítulo Clean y continuidad de los 16 fotogramas al pasar a vídeo. Se comprueban además duración, decodificación, audio y medios enlazados en la entrega. La inspección realizada mediante herramientas se basa en fotogramas y secuencias muestreadas; no se presenta como una aprobación estética ni una escucha humana integral.

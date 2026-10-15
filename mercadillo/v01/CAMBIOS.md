# Mercadillo de agencias · V01 · 11-10-2026

Edición completa de 88,375 s, realizada en Remotion. Cutroom: http://127.0.0.1:4318/ . Versión `1157a9e9-5e30-4fa7-800c-257f1dad1046`. Pendiente del veredicto de Ale.

## Dirección aplicada

Referencia: BRAUDLABS V5 «La Maquinita». Alternancia entre titulares grandes y frases pequeñas; palabras principales que permanecen mientras cambia el apoyo; acumulaciones compactas; máscaras selectivas; silencios tipográficos que dejan ver la acción. Las demostraciones y gags ya están en el metraje. Esta versión los acompaña con tipografía, sonido y un remate en blanco y negro.

- SF Pro Bold/Regular, lima para protagonista/énfasis y blanco cálido para narración. Ancla estable dentro de cada bloque semántico.
- «Precio» y «rápido» permanecen; «premium» une calidad/clientes; «genera/creativos» encierra los apoyos; «bla, bla, bla» acumula y desemboca en «YA».
- Entrada, lectura y salida diferenciadas por función. Curvas Bézier/Hermite reutilizables, exposición temporal de cinco muestras y sobrepaso moderado en énfasis. Son decisiones de esta edición; no se dispone de las claves originales del editor.
- Gancho y «solución» en primer plano: se rechazó la máscara inicial por pérdida de letras. Profundidad selectiva en criterio visual y arte. Primerísimo plano del secreto, gag físico y cameo con espacio sin subtítulos.
- Teléfono visible durante la llamada. Cameo una sola vez, con sus handles originales. Orden, duración y geometría de los 20 clips conservados.

## Música y mezcla

**Funky Martian — Michael Ramir C.**, Mixkit, pista 1029. Fuente: [catálogo funk](https://mixkit.co/free-stock-music/funk/), [licencia](https://mixkit.co/license/), [FAQ de uso](https://mixkit.co/free-stock-music/). El catálogo la describe como jazz/funk, con bajo y batería. La FAQ permite anuncios online. Registro del archivo original y SHA-256: `study/music-sources.json`.

Entrada desde el segundo 2 de la pista, sin cambiar su tempo. Filtros: paso alto 45 Hz, campana de −3 dB en 2,3 kHz para despejar voz y paso bajo 13 kHz. Automatización en `Film.tsx`: bajada en secreto y abuela, casi silencio en «ni de coña», subida durante el gag físico y caída al cierre. Doce acentos gráficos de aire/golpe/resolución, generados localmente. No se extrajo música ni SFX de la referencia.

Narrador alineado al cero, diálogos y foley nativos conservados. Ganancia nativa 0 dB en clips 1–3 y 11–12; −3 dB en clip 4; −6 dB en los demás planos narrados. Mezcla final: −18,54 LUFS integrados, −2,26 dBTP, LRA 4,20. Ocho ventanas de correlación con el stem: desfase de 0 ms.

La revisión de audio es técnica: señales, sincronía y niveles. No se ha hecho una escucha independiente del resultado; no se presenta como mezcla aprobada de oído.

## Revisión

Se compararon fotogramas nativos de V5 y se exploraron tres diseños. Se inspeccionaron 60 imágenes de fuente, 44 stills de composición, una secuencia de movimiento del prototipo y 95 fotogramas del MP4 final, incluidos entradas/salidas y máscaras. Se corrigieron oclusiones, texto sobre la boca y texto sobre el teléfono antes de exportar. Las hojas finales están en `stills/final-complete-*.jpg` y `stills/final-motion-*.jpg`.

Verificación técnica en `QA.json`: 2121 frames a 24 fps, 1080 × 1920, H.264/AAC, decodificación completa sin errores, hashes de los 20 clips iguales a los originales, cameo único y máscaras disponibles. El recorte de cabeza durante la acción de clip 20 ya aparece en la fuente y en su brief.

La temporización de palabras parte de ASR local con correcciones editoriales; no es alineación fonética manual. La segmentación de persona es automática. El ritmo, la elección musical y la fidelidad estética siguen pendientes de valoración.

## Reproducir y editar

Archivo: `Mercadillo-agencias-V01.mp4`. Fuentes: `Film.tsx`, `motion.ts`, `cues.json`, `index.tsx`. No editar V01 una vez recibidas notas: crear V02 y conservar su historial.

Desde la raíz del proyecto: `node mercadillo/v01/render.mjs --bundle`. Usa Remotion 4.0.534 en `/private/tmp/birdie-v07-runtime`; se puede indicar otra instalación compatible con `REMOTION_RUNTIME` y navegador con `BROWSER_EXECUTABLE`. Render completo medido: 59,843 s. Preparación de audio: `prepare-audio.py`; verificación: `verify.py`.

Sala independiente: `PORT=4318 REVIEW_DATA_DIR="$PWD/mercadillo/review-data" node motor-editor/review/server.mjs`. Birdieballs sigue en el puerto 4317.

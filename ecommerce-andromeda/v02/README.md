# Andrómeda V02 · preview 00–38,33 s

V01 rechazada por Ale. V02 pendiente de su veredicto. No es el anuncio completo: faltan los planos posteriores y 06 sigue siendo provisional.

## Corrección de voz

V01 sustituyó el audio nativo del hook por la toma externa colocada a1,970 s, siguiendo el brief antiguo. La instrucción posterior de Ale exige la voz nativa: esa instrucción prevalece. V02 conserva los primeros260000 samples estéreo a48kHz del audio del hook, en su reloj original, sin desplazamiento, estiramiento o doble voz. La narración permanece. La cama provisional se elimina solo durante el hook. El ambiente posterior conserva sus índices exactos de muestra.

La mezcla pasa por un limitador de pico con compensación de latencia. Por eso no se afirma igualdad de amplitud entre la pista aislada y el MP4 mezclado. `study/native-audio-QA.json` comprueba el stem antes de mezclar; `QA.json` comprueba el audio del MP4 frente a la mezcla. La alineación forzada encuentra «más / anuncios / más» en1,883 /2,244 /4,748 s y confirma que cabe antes del corte. No sustituye una escucha ni una evaluación perceptiva del lipsync.

## Subtítulos

SF Pro Regular/Bold. Geometría persistente por frase; anclas por plano y despeje de caras, ticket y pantallas. Las jerarquías de contexto pequeño + palabra principal se alternan con relevos de una línea, entradas laterales, revelados desde abajo, impactos breves y repetición vertical. «Mierda / de siempre» invierte la jerarquía superior/inferior. «Días y días» se releva dentro de una ventana en lugar de acumular otro bloque idéntico.

Entradas de5 frames (208ms), estabilización y salida dirigida de2 frames cuando corresponde; impacto con sobrepaso máximo3%; desenfoque espacial solo mientras se mueve. El revelado y el cambio de palabra se evalúan en el frame de presentación, sin muestras temporales de textos ajenos. El relevo de «días» tiene coexistencia explícita entre texto saliente y entrante durante6 frames (250ms), no un artefacto del obturador. No se emplea el fit posicional de V8 como si recuperase los keyframes originales: estas trayectorias son diseñadas, informadas por las referencias.

Comparación pertinente: V1 «ni me han / pagado» para proporción y acumulación; V8 f550–575 para contraste de tamaños y Regular; V5 «campañas / automáticamente» como contrapeso legible sobre imagen cargada. No son nuevas mediciones exhaustivas de11 vídeos ni prueba de equivalencia artística.

Tres alternativas guardadas para «días»: A acumulación horizontal; B relevo vertical (elegida); C doble línea. B evita repetir otra doble línea y expresa repetición en el mismo ancla. Se revisaron24fotogramas de propuesta,12del MP4 definitivo y24fases de cuatro animaciones. Boards en `study/final-review.jpg` y `study/animation-phases.jpg`.

## Reproducir

Desde la raíz del proyecto:

```sh
python3 ecommerce-andromeda/v02/design.py
python3 ecommerce-andromeda/v02/prepare-native-audio.py
python3 ecommerce-andromeda/v02/build-audio.py
node node_modules/typescript/bin/tsc --project ecommerce-andromeda/v02/tsconfig.json
node ecommerce-andromeda/v02/render.mjs --bundle
python3 ecommerce-andromeda/v02/verify.py
python3 ecommerce-andromeda/v02/study/verify-native-audio.py
python3 ecommerce-andromeda/v02/study/verify-render.py
python3 ecommerce-andromeda/v02/study/review-sequences.py
```

Los medios compartidos con V01 son hard links de solo lectura operativa: nunca sobrescribirlos. Los stems nuevos y la mezcla sí son propios de V02. Música desactivada según la entrega.920 frames a24fps,1080×1920. Ticket conserva IN12;03b conserva58frames. No se cambió el montaje ni se añadieron cortes.

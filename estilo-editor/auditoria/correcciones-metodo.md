# Correcciones del estudio heredado

La auditoría nativa recorre 24.094 fotogramas de diez archivos. El muestreo heredado omitía 4.876 fotogramas que no son idénticos al anterior en el decodificado nativo; se abrieron hojas suplementarias para incluirlos. Una diferencia exacta puede ser ruido de compresión: no significa 4.876 eventos editoriales nuevos. Los manifiestos y sus SHA256 permanecen en datos/ y auditoria/cobertura-fotogramas.json.

El índice se selecciona con `select=eq(n,N)` o `between(n,A,B)` desde la decodificación, base0. Las hojas densas antiguas mantienen su numeración. La nota heredada verificacion-indices-seek.md informa una muestra de129 extracciones antiguas correctas; no certifica lotes que allí reconoce no haber probado. En esta revisión se reextraen por índice las fronteras nativas utilizadas; no afirmar que todo seek antiguo estaba desplazado ni que toda medida antigua está automáticamente verificada.

El contraste de `inkbox.py` no es alpha: en modo bg usa distancia RGB/255, puede superar1 hasta√3; además la caja es por percentiles y depende del umbral/ROI. Un ROI que recorta letras móviles falsea la curva; Gracias fue repetido con región completa. Movimiento y contraste se registran por separado.

Las cajas de OCR miden tinta reconocida o caja aproximada, no fontSize, tracking ni fuente. Los fits selectivos de originales pueden favorecer Helvetica Bold; SF Pro se mantiene por decisión de Ale. Los resultados y crops nativos se conservan fuera de analysis/.

Los resúmenes de sincronía incluyen distribución completa de palabras alineadas y distribución censurada por tolerancia, con tamaño de cada muestra. El subconjunto próximo a cero no demuestra que todo el vídeo sincronice exactamente. `shown=false` puede ser OCR fallido u oclusión, no supresión deliberada.

Las variantes V6 original/revisada comparten2424/2650 fotogramas por hash;226 difieren. V7 comparte visualmente secuencias con anclas−5f, pero el diálogo amarillo tiene retiming local (de1029 frente rev1040). No derivar todos sus eventos por traslación uniforme.

Corte detector, flash, grado de color, zoom/reencuadre e inserto de1f son etiquetas distintas. Los insertos verificados no se convierten en obligación estética. B/N no demuestra imagen fija.

El audio revisado corresponde a espectrogramas del mix: permite describir energía y continuidad, no identidad auditiva de SFX, composición de pistas o ganancias originales. `dapi` no pudo usarse porque Diffusion Studio no estaba activo; no se presentó una escucha que no ocurrió.

La documentación persistente, cobertura y evidencia nativa seleccionada están fuera del directorio ignorado analysis/. La interpretación y las curvas nativas pendientes permanecen explícitas en cada nota y CURRENT-STUDY.json. No se renderizaron anuncios de prueba ni se modificaron composiciones anteriores.

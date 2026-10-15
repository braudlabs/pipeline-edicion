# Revisión forense V2

Datos y estado: corpus.json. Reglas: rules.json. Eventos: events.json. Todos los archivos `*-tracks.json` contienen observaciones OCR, no títulos certificados. Se preservan los datos anteriores.

Reconstruir (desde la raíz del proyecto, con OCR/transcripciones previos disponibles):

```
python3 estilo-editor/scripts/measure_v8.py
python3 estilo-editor/scripts/fit_v8_motion.py
python3 estilo-editor/scripts/plot_v8_motion.py
python3 estilo-editor/scripts/measure_v8_selector.py
python3 estilo-editor/scripts/plot_v8_selector.py
python3 estilo-editor/scripts/editor_rules_v2.py
python3 estilo-editor/scripts/forensic_v2.py
node --test motor-editor/forensics/contract.test.mjs motor-editor/review/tests/*.test.mjs
```

El ajuste depende de los fotogramas originales y conserva medidas descartadas. La comparación de la curva solo valida posición en ejemplos de V8; no fuente/alpha/audio ni generalización a otras piezas.

La API local sirve originales incluidos en el manifiesto y fotogramas exactos por índice; nunca rutas arbitrarias del usuario. El navegador permite comparar reglas y medidas con la referencia. La sección de cobertura expone lo pendiente.

QA realizada: seis vistas sin errores JS; fotogramas nativos1080 y1920px; frame0; cambio de referencia;371pistas V8; reproducción de tramo con audio; espectrograma; HTTP206para vídeos; límites de frame y fuente desconocida rechazados; cuatro versiones y notas originales preservadas.12testsfuncionales pasados. Esta QA no acredita aprobación artística.

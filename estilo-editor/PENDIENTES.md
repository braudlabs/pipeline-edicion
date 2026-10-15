# Prioridad actual: revisión forense V2

**Avance 14/10/2026:** selector V2 parcial ejecutable y conectado a Remotion, descrito en
`notas/selector-v2-2026-10-14.md`. Ya resuelve función/énfasis, secuencia, ancla de grupo y
conflictos de tinta animada. Quedan extracción fiable de contexto, diálogo simultáneo,
más familias de motion relacional y validación entre familias. El piloto de laboratorio no reemplaza una
entrega ni cierra el punto 7. Ventana relacional V8 integrada y probada en laboratorio:
`notas/relacion-v2-2026-10-14.md`. Pendiente aplicar a otro contenido/voz, oclusión,
calibrar alfa/texto y completar apertura/salida; no repetir las medidas de tiradores.

V03 rechazada. Ale ha autorizado una nueva prueba Birdieballs en paralelo al estudio (10 octubre 2026). V04 usó una composición nueva y conservó el montaje original, pero ha sido rechazada; el cuestionario `/quiz` recoge la nueva dirección antes de otra prueba; no reutiliza el EDL de V03 ni acredita el planificador completo. Estado y evidencias en `CURRENT-STUDY.json.revision_v2`, `datos/revision-v2/` y `ALGORITMO-V2.md`.

1. Completar anotación nativa de eventos y contraejemplos; separar OCR físico/UI/ruido de captions. Las11fuentes tienen lectura automática, no revisión forense completa.
2. V8: contracción/reapertura clientes→empleados medida por tiradores; fases196–327 revisadas y añadidas a G03. Falta reconstruir alpha/fuentes, cuantificar apertura inicial y verificar trayectorias de arcos/oclusión y restantes entradas/salidas que aún solo proceden de OCR/panorámicas. Continuar desde `notas/v8-revision-v2.md` sin repetir ventanas ya revisadas.
3. Contrastar la trayectoria compartida de V8 con otras palabras y familias. El ajuste actual solo modela entrada/asentamiento de posición, y su error aumenta al incluir salida. No transferirlo al rail directo.
4. Ajustar fuentes con múltiples glifos no ocluidos; medir multilíneas y capas/contorno. No sustituir medidas por tracking/tamaño global.
5. Completar inventario de motion por tipo, no solo etiquetas legacy grafico; incluir negativos antes de inferir cadencia.
6. Sonido: análisis semántico/escucha y biblioteca disponibles antes de identificar familias o samples. Espectrograma y onset no identifican.
7. Migrar planificador a decisionesV2 y usar contrato de preservación de fuente/tiempo/procedencia. Validar reconstrucciones frente a referencia antes de afirmar fidelidad; La prueba V04 aplica un subconjunto en una composición específica; falta generalizar y validar el planificador completo.

---

# Pendientes concretos del estudio

La cobertura secuencial de las diez referencias está completa en hojas densas y suplementarias; no está cerrada la medición nativa de todos los eventos. `CURRENT-STUDY.json` conserva ambas condiciones por separado. Esta lista evita depender de la conversación para continuar.

1. Recorrer `datos/eventos.json` y cada nota para extraer los rangos nativos aún solo observados en miniatura. Priorizar entradas/salidas tipográficas, máscaras, uniones de gráficos y candidatos de microcorte; incluir frames anteriores/posteriores. Registrar la lista exacta, no marcar un rango entero si solo se abrieron muestras.
2. Medir posición, caja de tinta, contraste y blur por separado, con ROI completa y umbral guardado. Corregir primero las regiones que incluyen piel, reflejos o letras recortadas. Conservar curvas por fotograma antes de ajustar modelos. Los ajustes medidos de Gracias/hooks/Creador no se aplican automáticamente al resto.
3. Resolver microcortes aún dudosos (por ejemplo CTA V6 alrededor2335 y landing alrededor2410). Un cambio rápido de pose puede proceder de corte, cadencia o actuación. Registrar incertidumbre si el MP4 no permite determinarla; no inventar la intención del editor.
4. Completar verificación tipográfica de estilos distintos. Los fits selectivos Helvetica/SF Pro son controles locales; el producto conserva SF Pro por decisión de Ale. Separar cuerpo, tracking, ancho de tinta y distorsión de perspectiva.
5. Escuchar los originales y relacionar sonidos con eventos. Los espectrogramas revisados no identifican SFX ni separan música/voz. Diffusion Studio no estaba activo durante esta revisión; evitar convertir onsets del mix en identidades de sonidos.
6. Al terminar cada tanda, actualizar notas/cobertura y ejecutar `estado.py`, `consolidate.py`, `stats.py`. Auditar evidencias y referencias persistentes. Cerrar `forensic_complete` solo tras revisar todos los eventos del tramo y conservar los límites irreductibles.
7. La implementación inicial Remotion existe en [motor-editor](../motor-editor/README.md), con planificador, recetas, composición y pruebas funcionales. Los renders de comparación siguen pendientes. Completar lo señalado en [MOTION-GRAPHICS.md](MOTION-GRAPHICS.md); `ALGORITMO.md` y `perfil-estilo.json` conservan propuestas separadas de observaciones y no acreditan fidelidad visual.

No se necesitan nuevos briefs para continuar el análisis visual. Los originales se identifican por SHA256 en `datos/referencias.json`; verificar ese digest si se sustituyen o recuperan los archivos.

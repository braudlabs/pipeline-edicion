# Estudio del algoritmo de edición

Estudio de diez referencias de BRAUDLABS y LaFabrica para describir un sistema de edición
reproducible en Remotion. Conserva SF Pro por decisión de Ale. No se están renderizando
pruebas ni alterando anuncios anteriores.

Leer en este orden:

1. [Estado actualizado](ESTADO.md), [cobertura por tramo](CURRENT-STUDY.json) y [pendientes concretos](PENDIENTES.md).
2. [Decisiones y alcance](DECISIONES.md).
3. [Método y límites de medición](METODO.md).
4. [Algoritmo](ALGORITMO.md) y [perfil de parámetros](perfil-estilo.json).
5. [Fichas por vídeo](fichas/), [notas completas](notas/) y [sucesos normalizados](datos/eventos.json).
6. [Estadísticas automáticas](datos/estadisticas.md) y [auditoría del trabajo heredado](auditoria/).

La implementación inicial ejecutable está en [motor-editor](../motor-editor/README.md).
El [mapa de motion graphics](MOTION-GRAPHICS.md) distingue efectos estudiados,
medidas nativas, recetas operativas y reconstrucciones aún pendientes. La calidad
visual del motor todavía no está validada contra las referencias.

Los originales están identificados por SHA256 en [datos/referencias.json](datos/referencias.json).

`analysis/` contiene originales enlazados, JPGs, OCR por fotograma, espectrogramas y
hojas densas; está ignorado por Git y no debe ser el único lugar de la documentación.
`scripts/estado.py` copia las notas en curso a `notas/` y guarda todos los pendientes
en `CURRENT-STUDY.json`. No depende del historial de Claude o Codex para retomarse.

Desde este directorio:

```sh
python3 scripts/estado.py
python3 scripts/consolidate.py
python3 scripts/stats.py
```

La cobertura de miniaturas y la verificación de detalles nativos se registran por
separado. Un estado parcial es información de trabajo, no un estudio completo.

Para incorporar otra referencia, añadirla en `scripts/common.py`, ejecutar el pipeline,
auditar los fotogramas con `scripts/audit_frames.py` y asignar tramos que cubran todo
el original. No reducir el estudio a muestras por segundo.

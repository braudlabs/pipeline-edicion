# Estudio del estilo del editor

> Dónde vive el estudio del estilo del editor profesional (10 vídeos → algoritmo para Remotion) y cómo retomarlo sin depender de una sesión

El estudio de los 10 vídeos del editor profesional (BRAUDLABS y LaFabrica) para derivar un
algoritmo de edición reproducible en Remotion vive en
`estilo-editor/`.

Punto de entrada: `README.md`, y de ahí `ESTADO.md` + `CURRENT-STUDY.json` (cobertura por
tramo), `DECISIONES.md`, `METODO.md`, `ALGORITMO.md`. Notas por tramo en `notas/`, datos
medidos por código en `datos/<slug>/`, herramientas en `scripts/`. `analysis/` son
intermedios pesados ignorados por git.

El usuario pidió el 10/10/2026 que el estudio quede «redactado y actualizado siempre al
último momento» para seguir «sin tener que depender de esta sesión».

**Why:** trabaja el mismo estudio desde Claude y desde Codex; cuando Claude se quedó sin
límite, una sesión de Codex continuó sobre los archivos y reorganizó la documentación.

**How to apply:** al retomar, leer primero `ESTADO.md` y regenerarlo con
`python3 scripts/estado.py`; no fiarse del historial de la conversación. Antes de escribir,
comprobar si otra sesión está modificando la carpeta (`find . -mmin -3`) y no pisar notas
ajenas. Tras cada avance, actualizar los documentos, no solo responder en el chat. El usuario
exige revisión fotograma a fotograma, sin muestrear por segundos. Ver «sf-pro-decidido» (nota interna, no publicada),
«objetivo-comercializar-sin-ae» (nota interna, no publicada) y [Subagentes y límite de uso](subagentes-y-limite-de-uso.md).

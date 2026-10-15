# Ecommerce Andrómeda · C04 (Claude)

Proyecto Remotion editable de la **versión completa 0–85,417 s** del anuncio de ecommerce/Andrómeda
(hombre azul + bigote daliniano, lavandería azul/crema): las 17 unidades del
`MASTER_COMPLETO_24FPS` de la entrega del director (2.050 f a 24 fps), con la locución original
intacta. Independiente de `ecommerce-andromeda/` (serie de Codex). C01–C03 se conservan en
`../c01/`, `../c02/` y `../c03/`. Cambios frente a C03: [CAMBIOS.md](CAMBIOS.md). Comprobaciones: `QA.json`.

**Másteres:** `Andromeda-C04-00-85s-144fps-1080.mp4` (12.300 f), `…-60fps-1080.mp4` (5.125 f) y `…-24fps-1080.mp4`
(2.050 f) — 1080×1920, H.264 + AAC 48 kHz, con subtítulos en las 17 unidades y música.
Render a 24 fps: `render.mjs --render`; a 60 (5.125 f): `--render --60`; a 144 (12.300 f; diseño a 24 fps ×6): `--render --144`.
No es el anuncio final: varias tomas llevan observaciones de UI, beat y proyección del director y la mezcla no
está escuchada. Qué lleva cada render (rótulos, música) y su verificación: CAMBIOS.md.

## Estructura

| Ruta | Contenido |
|---|---|
| `src/index.tsx` | Composiciones `AndromedaC04` (24 fps), `AndromedaC04-144`, `AndromedaC04-60` y `HookStudy` (estudio A/A2/B/F del hook) |
| `src/Film.tsx` | Orden de capas: vídeo, rótulos por escena, audio |
| `src/VideoSpine.tsx` | Montaje bloqueado del máster (IN/OUT exclusivos, ticket +12 f, salida +18 f) y B/N del gag |
| `src/captions/` | `Big` (línea grande centrada; zona por unidad, seguimiento de cámara, tinta oscura), `Hook`, `Scene01`…`Scene14` (Scene14 incluye 15) y `Tag` (handles de 10) |
| `src/lib/` | Curvas, obturador de 8 submuestras, SF Pro variable, homografía, palabras |
| `src/data/words.json` | 274 palabras del narrador completo (85,39 s) alineadas al audio real |
| `src/data/timeline.json` | Las 17 unidades (id, estado, clip, `from`, `dur`, `srcIn`), generado por `build-timeline.py` |
| `src/data/audio.json` | Pistas y ganancias (narrador, hook nativo, ambiente de 01–15, SFX, música) |
| `src/data/shutter-track.json` | Seguimiento de la panorámica sobre la persiana |
| `src/data/v8-selector-width.json` | Curva medida de los tiradores V8 (selección problema → solución) |
| `src/data/card-track.json` | Seguimiento de la tarjeta durante la panorámica del selfie |
| `public/assets/clips/` | Los 17 clips seleccionados (copias idénticas a `01_CLIPS` de la entrega; `source-notes/sha256.txt`) |
| `public/assets/mattes/` | Mattes de persona del hook y del ticket/tarjeta (copia de C03) y `criterio-holdout` (11: Vision + clave de la piel azul) |
| `public/assets/audio/` | Voces originales, stems (`stems/`, incluido `musica.wav` con ducking) y muestras de SFX |
| `source-notes/` | `MASTER_COMPLETO_24FPS` (json y csv), brief y estado de la entrega, hashes |
| `study/` | Solo informes generados (`audio-build.json`, `sfx-build.json`, `comparacion-ensamble.json`, hoja de contacto de cortes, tramos de prueba a 60/144 fps, registros de render) |

## Regenerar

Desde la raíz del proyecto editor:

```sh
python3 ecommerce-andromeda-claude/c04/build-timeline.py
python3 ecommerce-andromeda-claude/c04/build-audio.py
python3 ecommerce-andromeda-claude/c04/build-sfx.py
python3 ecommerce-andromeda-claude/c04/build-music.py      # banda sonora de ../music con ducking bajo el narrador
node ecommerce-andromeda-claude/c04/render.mjs --bundle --render
python3 ecommerce-andromeda-claude/c04/verify.py
python3 ecommerce-andromeda-claude/c04/compare-ensamble.py   # cortes y audio frente al ensamble del director
```

Fotogramas sueltos: `node ecommerce-andromeda-claude/c04/render.mjs --still AndromedaC04 - 120,240,360`.
Tramo suelto de cualquier composición (va a `study/`): `--render --60 --range 3060-3140`.
Usa el Remotion 4.0.534 de la raíz; cargar `@remotion/renderer` tarda ~1 min en esta máquina.
Mattes: `swiftc -O tools/matte.swift -o tools/bin/matte` y
`tools/bin/matte <clip> <salida> <primero> <último> person 1`.

## Pendiente

- **Escucha** de la mezcla completa (narrador, ambientes, música y SFX) en altavoz de móvil y auriculares.
- **Música**: sigue la spec funk de Ale; el brief del director describe otra pieza (ver CAMBIOS.md).
- Observaciones visuales del director sin resolver (UI de 06/07/08, proyección de 12, anticipación de 09).
- Lanzar los renders de uno en uno: dos procesos de Remotion sobre el mismo `build/` rompen la carga de fuentes.

# Ecommerce Andrómeda · C01 (Claude)

> Superada por [C02](../c02/README.md). Se conserva como referencia: Ale aprobó el hook, el cartel
> de la persiana y «OTRA PUTA VEZ»; rechazó el resto de subtítulos (pequeños, a los lados).

Proyecto Remotion editable de la prueba 0–38,333 s del anuncio de ecommerce/Andrómeda
(hombre azul + bigote daliniano, lavandería azul/crema). Independiente de
`ecommerce-andromeda/` (serie de Codex). Decisiones, origen de cada una y pendientes:
[CAMBIOS.md](CAMBIOS.md). Comprobaciones: `QA.json`.

**Preview:** `Andromeda-C01-00-38s-PREVIEW.mp4` — 1080×1920, 24 fps, 920 f, H.264 + AAC 48 kHz.
No es el anuncio final: 06 PROVISIONAL, faltan 07–15 y la música.

## Estructura

| Ruta | Contenido |
|---|---|
| `src/index.tsx` | Composiciones `AndromedaC01` (pieza) y `HookStudy` (estudio A/A2/B/F del hook) |
| `src/Film.tsx` | Orden de capas: vídeo, rótulos por escena, audio |
| `src/VideoSpine.tsx` | Montaje bloqueado del CSV (IN/OUT exclusivos, ticket +12 f) y B/N del gag |
| `src/captions/` | Una construcción por escena: `Hook`, `Scene01`…`Scene05` (+06), `Rail`, `Stack`, `Masked` |
| `src/lib/` | Curvas, obturador de 8 submuestras, SF Pro variable, homografía, palabras |
| `src/data/words.json` | 274 palabras del narrador completo (85,39 s) alineadas al audio real |
| `src/data/timeline.json` | Escenas 00–06 y huecos 07–15 con su estado |
| `src/data/audio.json` | Pistas y ganancias (narrador, hook nativo, ambientes, SFX, música vacía) |
| `src/data/shutter-track.json` | Seguimiento de la panorámica sobre la persiana |
| `src/data/v8-selector-width.json` | Curva medida de los tiradores V8 (selección problema → solución) |
| `public/assets/mattes/hook*` | Mattes de persona del hook (Vision, `tools/matte.swift`) |
| `study/` | ASR, alineación, espectrogramas, fotogramas con rejilla, QA visual |
| `stills/` | Estudio del hook (`hook-A` es la variante elegida por Ale) y revisiones |

## Regenerar

Desde la raíz del proyecto editor:

```sh
/private/tmp/mercadillo-align311/bin/python ecommerce-andromeda-claude/c01/study/align/align.py
python3 ecommerce-andromeda-claude/c01/build-audio.py
python3 ecommerce-andromeda-claude/c01/build-sfx.py
node ecommerce-andromeda-claude/c01/render.mjs --bundle --render
python3 ecommerce-andromeda-claude/c01/verify.py
```

Fotogramas sueltos: `node ecommerce-andromeda-claude/c01/render.mjs --still AndromedaC01 - 120,240,360`.
Usa el Remotion 4.0.534 de la raíz; cargar `@remotion/renderer` tarda ~1 min en esta máquina.
Mattes: `swiftc -O tools/matte.swift -o tools/bin/matte` y
`tools/bin/matte <clip> <salida> <primero> <último> person 1`.

## Siguientes bloques

`words.json` ya contiene toda la locución (hasta «producir ads», 85,39 s) y `timeline.json`
los huecos 07–15. Para añadir un plano: copiar el clip a `public/assets/clips`, añadir la
escena al timeline, regenerar el audio y escribir su construcción en `src/captions/`. Al
sustituir 06, rehacer su escena sin mover las voces; 07 debe empalmar con el último
fotograma usado de 06.

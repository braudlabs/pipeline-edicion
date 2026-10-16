# Puesta en marcha

Cómo reproducir el pipeline de edición en otro Mac. El repo trae el código, los proyectos de After Effects,
los datos ligeros y la documentación del estilo. Los medios no están (ver el apartado 6).

## 1. Requisitos

- macOS con Apple Silicon. Los mattes usan Vision y el puente de After Effects automatiza la app.
- Node 24 o superior (probado con 25.9) y npm.
- Python 3 (probado con 3.14): `pip install -r requirements.txt`.
- ffmpeg y ffprobe: `brew install ffmpeg`.
- Xcode Command Line Tools (Swift), para compilar la herramienta de mattes.
- whisper.cpp (`brew install whisper-cpp`) con el modelo `ggml-large-v3-turbo.bin` en `~/.cache/whisper-models/`,
  para transcribir y alinear palabras.
- After Effects 2024–2026, solo para las piezas que se construyen en AE.

## 2. Dependencias de Node

```bash
npm ci
npx remotion browser ensure
```

La raíz fija Remotion 4.0.534 y React 19. Los `render.mjs` de cada versión resuelven `react` y `remotion`
desde el `node_modules` de la raíz. Algunos proyectos llevan su propio `package.json`
(`ad3-pipeline/remotion-mg`, `ad4-creatina/remotion`…): en esos, `npm ci` dentro de su carpeta.

## 3. Tipografías (no incluidas)

El estilo usa SF Pro Display (Bold y Regular), New York y SF (SFNS). No se incluyen porque su licencia no
permite redistribuirlas:

- SF Pro y New York: <https://developer.apple.com/fonts/>.
- `SFNS.ttf`: viene con macOS, en `/System/Library/Fonts/`.

Cada proyecto las espera en `public/assets/fonts/` con estos nombres: `SFProDisplay-Bold.otf`,
`SFProDisplay-Regular.otf`, `NewYork.ttf` y `SFNS.ttf`.

## 4. Claves

```bash
cp ecommerce-andromeda-claude/music/.env.example ecommerce-andromeda-claude/music/.env
```

Pon tu `ELEVENLABS_API_KEY` en ese `.env`. Git lo ignora y no debe subirse nunca. Cada generación de música
gasta créditos: estima el coste antes de lanzarla.

## 5. Herramientas locales

- **Mattes de persona (Vision):** hay binarios arm64 en `ecommerce-andromeda-claude/c0*/tools/bin/matte`.
  Para recompilar:

  ```bash
  swiftc -O ecommerce-andromeda-claude/c06/tools/matte.swift -o ecommerce-andromeda-claude/c06/tools/bin/matte
  ```

  Revisa el recorte en cada plano: en «criterio» hubo que añadir una clave de color para la piel azul.
- **Puente de After Effects:** es un proyecto aparte con licencia MIT.

  ```bash
  git clone https://github.com/higgsfield-ai/fnf-local-pluging-bridge-mcp .tools/higgsfield-after-effects
  cd .tools/higgsfield-after-effects && npm ci --ignore-scripts && npm run build
  ```

  Los `*/scripts/ae.py` lanzan `.tools/higgsfield-after-effects/dist/index.js` por stdio. `node dist/cli.js
  install-codex` lo registra en Codex. Antes de usarlo, lee `docs/notas-tecnicas/ae-puente-trampas.md`.
- **Alineación forzada (opcional):** torch y torchaudio con MMS_FA. `TORCH_HOME` fija la caché del modelo.

## 6. Medios (no incluidos)

El metraje, los renders, el audio, los fotogramas y los mattes (unos 35 GB) se quedan fuera: GitHub no
admite archivos de más de 100 MB y muchos son material de clientes. Cada proyecto los espera en su
`public/assets/` (`clips/`, `audio/stems/`, `audio/sfx/`, `mattes/`); la lista exacta está en los datos de
cada versión (`src/data/timeline.json`, `src/data/audio.json`). Los mattes se regeneran con la herramienta de
Vision a partir de los clips.

## 7. Variables de entorno opcionales

| Variable | Uso |
|---|---|
| `BROWSER_EXECUTABLE` | Chrome headless distinto del de `node_modules/.remotion` |
| `CONCURRENCY`, `CACHE_MB` | renders con poca memoria (si el swap está lleno, macOS mata el compositor) |
| `EDITOR_ROOT`, `OUT_DIR` | render desde una copia fuera de iCloud |
| `REMOTION_RUNTIME`, `EDITORIAL_REMOTION_RUNTIME`, `BIRDIE_REMOTION_RUNTIME`, `BIRDIE_BROWSER` | runtime de Remotion alternativo |
| `TORCH_HOME` | caché de modelos de torch |
| `STILL_TIMES`, `FRAMES`, `REMOTION_SAMPLES` | fotogramas y muestras de obturador en scripts concretos |

## 8. Comprobación

Con los medios de C06 en su `public/`:

```bash
node ecommerce-andromeda-claude/c06/render.mjs --bundle --still AndromedaC06 - 120,782,1199
```

Para el vídeo entero, pasa `--render` (`--144` y `--60` dan las salidas de alta frecuencia) y verifica
después con `python3 ecommerce-andromeda-claude/c06/verify.py`.

## 9. Dónde está el criterio del estilo

- `AGENTS.md`: instrucciones para los agentes (Codex, Claude Code).
- `docs/direccion-de-arte/`: la guía de dirección de arte (preferencias, ejemplos, decisiones y revisión).
- `estilo-editor/FEEDBACK-ALE.md`: el feedback acumulado de cada versión.
- `estilo-editor/README.md` → `ESTADO.md`: el estudio del estilo del editor (notas, medidas y algoritmo).
- `motor-editor/README.md`: el motor de selección editorial.
- `MOTION-GRAPHICS-AE-REMOTION.md`: las equivalencias entre After Effects y Remotion.
- `docs/notas-tecnicas/`: las lecciones de render, iCloud, el puente de AE y los subagentes.
- El `CAMBIOS.md` de cada versión, por ejemplo `ecommerce-andromeda-claude/c06/CAMBIOS.md`.

## 10. iCloud

Si el repo vive en `~/Documents` con «Optimizar almacenamiento», macOS desaloja archivos y los renders se
cuelgan descargándolos uno a uno. Renderiza desde una copia en `/private/tmp`. Detalle en
`docs/notas-tecnicas/remotion-render-local.md`.

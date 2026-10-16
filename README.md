# Pipeline de edición

Anuncios verticales para Meta: montaje en Remotion, motion graphics en After Effects y Remotion, música con
ElevenLabs, el estudio del estilo del editor de referencia y un motor editorial que lo aplica.

- **Puesta en marcha:** [SETUP.md](SETUP.md). Los medios (metraje, renders, audio, mattes) y las tipografías no
  están en el repo.
- **Criterio de estilo:**
  - [docs/direccion-de-arte](docs/direccion-de-arte/): la guía de dirección de arte;
  - [estilo-editor/FEEDBACK-ALE.md](estilo-editor/FEEDBACK-ALE.md): el feedback acumulado;
  - [estilo-editor/](estilo-editor/README.md): el estudio del editor.
- **Instrucciones para agentes:** [AGENTS.md](AGENTS.md). Notas técnicas en [docs/notas-tecnicas](docs/notas-tecnicas/).
- **Cada anuncio en su carpeta**, con su `CURRENT-VERSION.json` y un `CAMBIOS.md` por versión: `ad1-reedit` (Cocina),
  `ad3-pipeline`, `ecommerce-andromeda` y `ecommerce-andromeda-claude`, `video-saas` (El Sistema, BRAUD Studio),
  `birdieballs`, `mercadillo` y otros. El motor está en `motor-editor/`.

## AD2 «La IA te sale cara» · V5 (proyecto de la raíz)

Anuncio terminado en Remotion 4.0.525, con el bloque de cuentas construido y renderizado en After Effects 2026. Vertical 1080 × 1920, 48 fps, 3160 fotogramas, **65,833333 segundos**. Mantiene las 206 palabras de la locución y elimina 7,708333 s de esperas respecto a V2.

## Abrir y renderizar

```sh
npm ci
npm run studio
npm run render
```

`npm run stills` renderiza fotogramas de revisión. `STILL_TIMES=1,2,3 npm run stills` selecciona segundos concretos. Se necesita Node.js y FFmpeg en PATH. El render funciona con los medios incluidos, sin consultar Instagram.

## Edición

- `src/edl-v3.json`: lista de cortes, con entrada y salida de cada medio en fotogramas. Conserva las uniones continuas 07→08 y 11→12.
- `src/timing-v3.json`: duración y entradas de los gráficos en el montaje final.
- `src/video.tsx`: tomas, recursos, bumper y audio.
- `src/captions-v5.tsx`: subtítulos siempre debajo del rostro. Entradas verticales breves; interlineado 1,28 y desbordamiento visible para conservar g/p/y completas.
- `scripts/reframe-v5.py`: reencuadra los primeros planos conservando proporciones, voz y cadencia. Extiende los bordes periféricos con una caída suave de enfoque. Una viñeta inferior oculta la extensión y mantiene libre la zona de interfaz.
- `public/assets/v5/`: tomas reencuadradas y bloque de cuentas renderizado desde After Effects.
- `ae-v5/Visual-Hub-Cuentas-V5.aep`: proyecto nativo. Composición principal `VH - Cuentas - V5`; composición `WORLD - Camara y conexiones` con cámara 3D real; cuatro precomposiciones con texto y pruebas independientes.
- `src/edit-time.ts`: convierte la escala original de 24 fps a una exportación de 48 fps sin alterar los cortes ni el audio.
- `src/captions-v3.json`: grupos, palabras y sincronía; 206 palabras.
- `src/motion-v4.tsx`: mantiene los gráficos de coste, generación, proceso y precio. El anuncio sustituye su bloque de cuentas por el render nativo de After Effects.
- `public/assets/v3/audio-mix-master.wav`: mezcla final congelada, 48 kHz estéreo.
- `scripts/prepare-v3.py`: reconstruye montaje, subtítulos, recortes literales de capturas y voz. Usa los originales locales y los JSON de transcripción incluidos.
- `scripts/mix-v3.py`: reconstruye música, efectos y máster con NumPy y FFmpeg.

## Dirección de movimiento

La referencia se examinó mediante secuencias consecutivas a 24 fps: tipografía alrededor de 4,2–5,83 s, 10,5–12,13 s y 36,3–37,93 s; recorrido gráfico de 14,5–19,38 s a intervalos de tres frames. Las palabras grandes aparecen desde abajo y frenan rápidamente; las pequeñas tienen entradas mucho más breves. Las curvas se recrean a partir de los fotogramas, no de un proyecto Premiere.

El nuevo bloque de cuentas recorre un mismo espacio: seguidores de Kurt → descenso a sus visitas → desplazamiento horizontal a Elliot → descenso a su reel. Las capturas se conectan a los números mediante líneas dibujadas. Cada cifra permanece legible antes del siguiente movimiento.

Los subtítulos se colocan bajo el rostro, normalmente en y=1130 en los primeros planos. No hay subtítulos sobre la cabeza. La comprobación de 59 frases fuera de los gráficos deja al menos 31 px entre el rectángulo facial detectado y el inicio del texto; el texto no supera y=1219. Se mantiene margen inferior para la interfaz del anuncio.

El bloque de cuentas dura 7,625 s y tiene 366 fotogramas a 48 fps. La cámara de After Effects se aleja, recorre el escenario y se acerca a la siguiente cifra. Usa obturador de 270°, fase −135° y 32 muestras con límite adaptativo de 128. El desenfoque se calcula en After Effects. Las cifras se detienen para poder leerlas. Las tomas de la modelo conservan su cadencia original de 24 fps.

Se utilizó la integración local [Higgsfield use After Effects](https://github.com/higgsfield-ai/fnf-local-pluging-bridge-mcp), siguiendo la propuesta del [artículo aportado](https://www.chaseai.io/blog/gpt-6-astra-after-effects-motion-design). No requiere efectos externos en el proyecto entregado. No se modificaron las preferencias globales de After Effects.

## Editar el bloque en After Effects

Abre `ae-v5/Visual-Hub-Cuentas-V5.aep`. Mantén su carpeta `assets` junto al proyecto. Las cifras son capas de texto con nombre; las capturas se sustituyen desde el panel Proyecto; la cámara tiene fotogramas clave editables. La cola de procesamiento contiene la composición principal. Si cambias de carpeta, selecciona una ruta de salida local antes de renderizar.

Tras modificarlo, renderiza la composición de 7,625 segundos a 48 fps y sustituye `public/assets/v5/accounts-ae.mp4`. `npm run render` recompone el anuncio con los subtítulos y la mezcla de audio. El original ProRes se entrega en el paquete separado de After Effects.

## Métricas y audio

Las cifras reproducen los contadores públicos capturados el 15/09/2026:

- [@notkurtgodel](https://www.instagram.com/notkurtgodel/reels/): **83,3 mil seguidores**; [reel mostrado](https://www.instagram.com/notkurtgodel/reel/DTkz_BMiFAo/): **7,7 M visualizaciones**.
- [@notelliotkay](https://www.instagram.com/notelliotkay/reels/): **13,5 mil seguidores**; [reel mostrado](https://www.instagram.com/notelliotkay/reel/DUbkE4cCBWo/): **4,9 M visualizaciones**.

Las cifras de visitas corresponden a un reel de cada cuenta, no a un total de cuenta. Las capturas completas se incluyen como prueba. Las imágenes se recortan sin alterar sus contadores.

Música: «Tech House vibes», Alejandro Magaña (A. M.), Mixkit #130. Ducking automático durante la voz y 13 acentos de sonido. Voz con su velocidad y tono originales. Fuentes y licencias en `public/assets/v2/CREDITOS.md`. Mezcla final cerca de −14 LUFS, pico real de aproximadamente −1,5 dBTP en WAV y −1,3 dBTP tras la compresión AAC.

La selección de tomas procede del brief de entrega. El prompt genérico aportado sirve de guía de organización; las instrucciones directas del usuario sobre Remotion, recorte de silencios y esta revisión determinan la edición.

## Revisión V5

Comprobaciones del proyecto de After Effects: fuentes y medios presentes, texto editable, cámara nativa, dimensiones y duración coincidentes. Se inspeccionaron las cuatro paradas de cámara y un fotograma en pleno desplazamiento, además del render completo. Las versiones anteriores se conservan.

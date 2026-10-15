# Banda sonora · Ecommerce Andrómeda · comedy-funk de 85,400 s

Pipeline de generación con la API de música de ElevenLabs (`music_v2_5` + `composition_plan`)
y montaje exacto sobre la timeline del vídeo a 48 kHz / 85,400 s (4.099.200 muestras por canal).
Instrumental, 122 BPM, Mi menor. La música va en su propia pista del montaje; la voz y los
sonidos reales se mezclan aparte.

**Estado (15/10/2026):** máster = **toma 3** montada con `edits_take3.json` (plan 3: groove continuo,
5 secciones). Ale rechazó la toma 2 («frena mucho a la mitad»: paraba al final de casi cada compás y el
montaje metía silencios). Pasa las comprobaciones automáticas; falta la escucha.

## Archivos

| Archivo | Qué es |
|---|---|
| `music_pipeline.py` | CLI `--dry-run` / `--generate` / `--conform` (fuente única del plan y de los cues) |
| `composition_plan.json` | Cuerpo exacto de la petición a `POST /v1/music` (15 chunks, 85.400 ms) |
| `cue_timeline.json` | Los 22 tramos del guion con sus límites absolutos y el tratamiento de cada uno |
| `original_music.mp3` | Generación sin tocar que usa el máster (enlace a `original_music_take3.mp3`) |
| `original_music_take3.mp3` | Toma 3 (semilla 85402, plan continuo) tal como la devolvió la API |
| `generation_meta.json` | Formato, semilla y cabeceras de la respuesta de la toma 3 (incluye el id para inpainting) |
| `edits_take3.json` | Montaje de la toma 3: la toma hasta el compás 41, final construido con material propio, tratamiento suave por cue |
| `take2/` | Toma 2 rechazada por Ale (frenaba): plan, montaje, informe y máster |
| `final_soundtrack_85_4s.wav` | Máster: 48 kHz, 24 bits, exactamente 85,400 s, −16 LUFS, pico −1 dBFS |
| `timing_report.json` | Duraciones, montaje aplicado, tratamientos, mediciones, comprobaciones y desvíos |
| `take1/` | Toma 1 descartada (silencio inicial de 7,3 s y una parada por compás) con su plan e informe |
| `conform_v1/` | Primer conformado de la toma 2 (solo ganancia + remate movido); sustituido |
| `study/conform_v2_overview.png` | Envolvente del máster con cues (amarillo), anclas (verde), empalmes (rojo) y notas (magenta) |

## Uso

1. **Clave.** Crea tú `music/.env` con la línea `ELEVENLABS_API_KEY=…` (no se sube ni se imprime;
   también vale exportarla en la terminal).
2. **Validar sin gastar:** `python3 music_pipeline.py --dry-run` (esquema, 15 chunks ≥ 3.000 ms que
   suman 85.400, cues ordenados, ffmpeg/ffprobe, clave presente y coste estimado).
3. **Generar una toma (de pago):** `python3 music_pipeline.py --generate --approve-cost`. Una sola
   llamada; si ya existe `original_music.mp3` exige `--new-take` y guarda `original_music_take3.mp3`.
4. **Montar el máster:** `python3 music_pipeline.py --conform --edits edits_take3.json`.

Coste: ElevenLabs publica Eleven Music por API a **$0,150/min**
([precios](https://elevenlabs.io/pricing/api)): ≈ $0,21 por toma de 85,4 s ($0,30 si redondea al
minuto). Gastado hasta ahora: 3 tomas ≈ $0,64 ($0,90 con redondeo).

## Cómo se monta la toma (sin estirar)

La toma va a 122 BPM desde 0 y coloca cada cambio de sección en su propia barra de compás,
casi siempre con una parada de ~0,4 s antes del tiempo fuerte. Por eso varias entradas llegaban
tarde (la gran reentrada, 0,86 s; la ráfaga, 0,84 s). El conformado:

- **Coloca cada entrada con su ataque medido exactamente en el cue** (5,417 · 23,000 · 25,417 ·
  30,920 · 32,583 · 42,583 · 50,400 · 55,833 · 66,042 · 70,042 · 82,958 · 84,800). Es copia de
  muestras con desplazamiento: los empalmes caen dentro de las paradas naturales, que se
  alargan o acortan. Solo hay tres cortes con material sonando: criterio → ráfaga, un tartamudeo
  de dos tiempos dentro de la ráfaga (para llenar sus 4 s) y ráfaga → revelación.
- **Construye los comentarios graves** que el guion pide (4,85 reacción; 29,70 sudadera; dos graves
  sueltos en «ideas de mierda») con una nota real del bajo de la toma, filtrada y con envolvente
  seca, sobre silencio musical. No hay efectos de dibujos animados.
- **Trata cada cue** con ganancia y paso bajo: casi silencio con bajo tenue en el susurro, retirada
  progresiva por escalones de filtro en los tiempos fuertes (18,75–23,00), cortesía, criterio y
  encaje más suaves. Los microfundidos de 8 ms terminan exactamente en cada límite.
- Normaliza la pista aislada a −16 LUFS con pico ≤ −1 dBFS. El nivel bajo la voz se decide en el
  montaje del vídeo.

**Lo que no hace:** un paso bajo apaga el brillo (charles, púas, ataque de caja) pero no separa
instrumentos; sin stems, el bombo sigue debajo del bajo en las reducciones. El informe lo marca
como escucha pendiente y no lo da por cumplido.

## Si una sección no convence

Se puede reeditar sin gastar: cambiar `edits_take2.json` (segmentos, paradas, notas) y volver a
`--conform`. Si hace falta material que la toma no tiene, la generación se pidió con
`store_for_inpainting: true`: con el id de `generation_meta.json` se puede regenerar solo un chunk
conservando el resto (`source_from`), lo que es de pago y requiere aprobación previa.

## Comprobaciones automáticas

Duración pedida = 85.400 ms · 15 chunks válidos ≥ 3.000 ms · cues ordenados dentro de 0–85,400 ·
WAV con 4.099.200 muestras por canal a 48 kHz · arranque en el tiempo cero · sin silencio inicial ·
sin outro alargado · remate presente en 84,60–84,95 · final sin clic · **cada entrada anclada con
desfase 0 frente a la toma** · **empalmes sin clic** · **notas construidas presentes**. El motivo,
el fagot, las reducciones por filtro y los empalmes con material sonando requieren escucha.

## Nota de dirección

El brief del director (`08_MUSICA`) describe otra pieza: 118 BPM con pizzicato, fagot y piano.
Esta banda sonora sigue la spec funk de 122 BPM que Ale entregó directamente para generarla.

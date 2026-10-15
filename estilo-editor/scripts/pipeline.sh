#!/bin/zsh
# Medición completa de uno o varios vídeos, de cero. Todo local.
#
#   scripts/pipeline.sh                 # todos los vídeos de scripts/common.py
#   scripts/pipeline.sh v1-pagado       # solo uno
#
# Para añadir un vídeo nuevo: darlo de alta en VIDEOS (scripts/common.py) con un slug y el
# nombre del archivo en ~/Downloads, y ejecutar este script con ese slug.
#
# Requisitos: ffmpeg, python3 con numpy y pillow, whisper (openai-whisper, modelo
# large-v3-turbo) y las Command Line Tools de Xcode (swiftc) para el lector de texto y caras.
# Disco: ~1,9 GB de intermedios para los 10 vídeos del estudio, todo en analysis/ (ignorado por git).
set -e
cd "$(dirname "$0")/.."

if [ $# -gt 0 ]; then SLUGS=("$@"); else
  SLUGS=($(python3 -c "import sys; sys.path.insert(0,'scripts'); from common import VIDEOS; print(' '.join(VIDEOS))"))
fi
mkdir -p analysis/{refs,frames,audio,whisper,vision,bin,dense,spectro,notas,tmp} datos laminas fichas notas

echo "== 1. enlaces duros a los originales y metadatos"
python3 - "${SLUGS[@]}" <<'EOF'
import os, sys
sys.path.insert(0, "scripts")
from common import VIDEOS, DOWNLOADS, REFS, probe
for slug in sys.argv[1:]:
    dst = REFS / f"{slug}.mp4"
    if not dst.exists():
        os.link(DOWNLOADS / VIDEOS[slug], dst)      # mismo inodo: no ocupa espacio extra
    i = probe(slug)
    print(f"  {slug:16s} {i['width']}x{i['height']} {i['fps']:.3f} fps {i['frames']} f {i['duration']:.3f} s")
EOF

echo "== 2. todos los fotogramas a baja resolución (360 px de ancho; 640 si es horizontal) y audio"
for s in "${SLUGS[@]}"; do
  mkdir -p analysis/frames/$s
  W=$(python3 -c "import sys; sys.path.insert(0,'scripts'); from common import probe; i=probe('$s'); print(640 if i['width']>i['height'] else 360)")
  VF="scale=${W}:-2:flags=area"
  [ -f analysis/frames/$s/f000000.jpg ] || ffmpeg -v error -i analysis/refs/$s.mp4 -vf "${VF}" -fps_mode passthrough -q:v 5 -start_number 0 analysis/frames/$s/f%06d.jpg
  [ -f analysis/audio/$s.16k.wav ] || ffmpeg -v error -y -i analysis/refs/$s.mp4 -vn -ac 1 -ar 16000 analysis/audio/$s.16k.wav
  [ -f analysis/audio/$s.wav ] || ffmpeg -v error -y -i analysis/refs/$s.mp4 -vn -ar 44100 analysis/audio/$s.wav
done

echo "== 3. locución con tiempos por palabra (Whisper large-v3-turbo)"
for s in "${SLUGS[@]}"; do
  if [ ! -f analysis/whisper/$s.16k.json ] && [ ! -f datos/$s/whisper.json ]; then
    (cd analysis/audio && whisper $s.16k.wav --model large-v3-turbo --language es --word_timestamps True \
       --condition_on_previous_text False --fp16 False --output_format json --output_dir ../whisper --verbose False)
  fi
done

echo "== 4. texto en pantalla y caras en cada fotograma (framework Vision de macOS)"
[ -x analysis/bin/visionscan ] || xcrun swiftc -O -swift-version 5 scripts/visionscan.swift -o analysis/bin/visionscan 2>/dev/null
for s in "${SLUGS[@]}"; do
  if [ ! -f analysis/vision/$s.jsonl ] && [ ! -f datos/$s/vision.jsonl.gz ]; then
    analysis/bin/visionscan analysis/refs/$s.mp4 analysis/vision/$s.jsonl 2>> analysis/vision/run.log
  fi
done

echo "== 5. métricas por fotograma, cadencia, repetidos y cortes"
python3 scripts/framestats.py "${SLUGS[@]}"
for s in "${SLUGS[@]}"; do python3 scripts/cuts.py $s; done

echo "== 6. pistas de texto y cara, palabras, audio, emparejado voz-rótulo, guion anotado"
python3 scripts/tracks.py "${SLUGS[@]}"
python3 scripts/words.py "${SLUGS[@]}"
for s in "${SLUGS[@]}"; do python3 scripts/audio.py $s; done
python3 scripts/align.py "${SLUGS[@]}"
python3 scripts/guion.py "${SLUGS[@]}"

echo "== 7. hojas densas (todos los fotogramas) para la revisión visual"
for s in "${SLUGS[@]}"; do python3 scripts/dense.py $s; done

echo "== 8. copia de los datos caros de recalcular a datos/ (versionable)"
for s in "${SLUGS[@]}"; do
  [ -f analysis/vision/$s.jsonl ] && gzip -9 -c analysis/vision/$s.jsonl > datos/$s/vision.jsonl.gz
  [ -f analysis/whisper/$s.16k.json ] && cp analysis/whisper/$s.16k.json datos/$s/whisper.json
done

echo "== 9. estadísticas cruzadas"
python3 scripts/stats.py
echo "listo. Revisión visual: ver METODO.md. Estado: python3 scripts/estado.py"

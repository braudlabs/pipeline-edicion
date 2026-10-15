#!/bin/zsh
# Mezcla de audio de AD6 «PapiCat Snacks».
# Voz = columna vertebral. Ambiente de cada clip ~18 LU por debajo de la voz.
# El foley sube SOLO en el derrape (hueco de voz 6,940-7,420 s).
# Master: -14 LUFS I, -1,5 dBTP.
set -e
SRC="/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-22-croche-gato/entrega"
W="/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/ad6-gato"
TMP="${TMPDIR:-/tmp}/ad6audio"; mkdir -p "$TMP"

# Ganancias medidas: objetivo de cama -33 LUFS (voz = -15,2 LUFS)
#   A 01 -22,0 -> -11,0 dB | B 02 -31,1 -> -1,9 dB | C 03 -29,0 -> -4,0 dB
#   D 04 -32,0 -> -1,0 dB  | E 05 -59,9 -> 0 dB (tono de sala, inaudible)
# Envolvente del derrape sobre el segmento C (tiempo local = tiempo fuente):
#   <3,183 s: -4,0 dB (0,6310) | 3,183-3,433: rampa a +0,3 dB (1,0351)
#   3,433-3,783: 1,0351 | 3,783-4,060: caida a 0  (cola en L, 0,31 s tras el corte de imagen)
ENV="if(lt(t,3.183),0.6310, if(lt(t,3.433), 0.6310+(t-3.183)/0.250*0.4041, if(lt(t,3.783),1.0351, max(0,1.0351*(1-(t-3.783)/0.277)))))"

ffmpeg -y -v error \
  -i "$SRC/voz-en-off.mp3" \
  -ss 2.875  -t 2.1667 -i "$SRC/01-dormido.mp4" \
  -ss 0.4167 -t 1.5    -i "$SRC/02-bolsa.mp4" \
  -ss 0      -t 4.06   -i "$SRC/03-carrera.mp4" \
  -ss 0      -t 4.7083 -i "$SRC/04-cuenco.mp4" \
  -ss 0      -t 4.0    -i "$SRC/05-producto.mp4" \
  -filter_complex "
    [0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,
         highpass=f=70, apad=whole_dur=16.125, atrim=0:16.125 [voz];
    [1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,
         volume=-11.0dB, afade=t=in:st=0:d=0.03, afade=t=out:st=2.1167:d=0.05,
         adelay=0|0 [a1];
    [2:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,
         volume=-1.9dB, afade=t=in:st=0:d=0.03, afade=t=out:st=1.45:d=0.05,
         adelay=2167|2167 [a2];
    [3:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,
         volume=volume='$ENV':eval=frame, afade=t=in:st=0:d=0.03,
         adelay=3667|3667 [a3];
    [4:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,
         volume=-1.0dB, afade=t=in:st=0:d=0.10, afade=t=out:st=4.6583:d=0.05,
         adelay=7417|7417 [a4];
    [5:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,
         afade=t=in:st=0:d=0.10, afade=t=out:st=3.90:d=0.10,
         adelay=12125|12125 [a5];
    [voz][a1][a2][a3][a4][a5]amix=inputs=6:duration=first:normalize=0:dropout_transition=0 [pre]
  " -map "[pre]" -t 16.125 -c:a pcm_f32le "$TMP/premezcla.wav"

echo "== premezcla =="
ffmpeg -hide_banner -nostats -i "$TMP/premezcla.wav" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|LRA:|Peak:"

# loudnorm dos pasadas
M=$(ffmpeg -hide_banner -nostats -i "$TMP/premezcla.wav" \
      -af loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json -f null - 2>&1 | \
      python3 -c "import sys,json,re; s=sys.stdin.read(); print(json.dumps(json.loads(s[s.rindex('{'):s.rindex('}')+1])))")
echo "medido: $M"
python3 - "$M" <<'PY' > "$TMP/ln.txt"
import sys, json
d = json.loads(sys.argv[1])
print("loudnorm=I=-14:TP=-1.5:LRA=7:measured_I={input_i}:measured_TP={input_tp}:"
      "measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:"
      "linear=true:print_format=summary".format(**d), end="")
PY
ffmpeg -y -v error -i "$TMP/premezcla.wav" -af "$(cat "$TMP/ln.txt")" -ar 48000 -c:a pcm_s24le "$W/output/ad6-mezcla.wav"

echo "== master =="
ffmpeg -hide_banner -nostats -i "$W/output/ad6-mezcla.wav" -af ebur128=peak=true -f null - 2>&1 | grep -A12 Summary | grep -E "I:|LRA:|Peak:"
rm -rf "$TMP"

#!/bin/zsh
# Captura cada toma de un shots.json por separado, con un tiempo máximo por toma.
# El vigilante va con la salida desviada: si comparte la tubería, cada toma espera el máximo entero.
cd /private/tmp/claude-render-braud
f=$1; logs=${2:-/private/tmp/claude-render-braud/out/snap-logs}; mkdir -p $logs
names=(${(f)"$(python3 -c "import json; print('\n'.join(x['name'] for x in json.load(open('$f'))['shots']))")"})
for n in $names; do
  node tools/snap.mjs $f $n > $logs/$n.log 2>&1 &
  PID=$!
  ( sleep 150; kill $PID 2>/dev/null ) > /dev/null 2>&1 &
  WATCH=$!
  wait $PID
  kill $WATCH 2>/dev/null
  echo "$n: $(tail -1 $logs/$n.log)"
done

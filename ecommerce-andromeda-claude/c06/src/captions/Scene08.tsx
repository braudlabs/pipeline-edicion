import React from 'react';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 08 · Optimización (1022–1237) ─────────────
// Plano abierto → acercamiento (f1034–1062) → alejamiento (f1078–1090) → abierto;
// primer plano del azul (f1113–1137); abierto; primer plano del prota (f1207–1229);
// abierto con el botón verde. Cortes medidos por diferencia de fotogramas.
// La cita de la máquina («Hey, … ¿quieres…?») va entera en azul claro: otra voz, sin
// bocadillo ni recuadro. En abierto, la línea queda entre las barbillas y la pantalla.
// «Sí»: la /s/ del narrador empieza en 49,86 s (f1196) y acaba antes del primer plano;
// «y escalarás» empieza en 50,48 s (f1211). La alineación automática los daba algo tarde.
const SCREEN: [number, number][] = [
  [1033, 866],
  [1043, 538],
  [1052, 442],
  [1062, 414],
  [1077, 430],
  [1080, 560],
  [1090, 866],
];
const SI = wf(156) - 3; // f1196: la alineación daba «Sí» 3 f tarde (la /s/ empieza en 49,86 s)
const Y_ESCALARAS = wf(157) - 2; // f1211: «y» empieza en 50,48 s
const ESCALARAS = ws([['y', Y_ESCALARAS], ['escalarás.', wf(158), true]]);
const GROW = {text: 'escalarás.', to: 1.2, frames: 18};

export const Scene08: React.FC = () => (
  <BigLines
    x={540}
    y={866}
    maxWidth={820}
    maxSize={130}
    chunks={[
      {words: ws([['Y', wf(133)], ['luego', wf(134)], ['te', wf(135)], ['dirá:', wf(136)]]), from: wf(133), to: wf(137), yKeys: SCREEN},
      {words: ws([['«Hey,', wf(137)], ['estos', wf(138)], ['dos', wf(139)], ['ángulos', wf(140)]]), from: wf(137), to: wf(141), voice: true, yKeys: SCREEN},
      {words: ws([['han', wf(141)], ['funcionado', wf(142)]]), from: wf(141), to: wf(143), voice: true, yKeys: SCREEN},
      {words: ws([['espectacular.', wf(143)]]), from: wf(143), to: 1113, voice: true, exit: 'cut'},
      // Primer plano del azul: la línea baja al jersey para no cruzar la cara.
      {words: ws([['¿Quieres', wf(144)], ['que', wf(145)], ['te', wf(146)], ['empiece', wf(147)]]), from: wf(144), to: 1138, voice: true, y: 1420, exit: 'cut'},
      {words: ws([['a', wf(148)], ['generar', wf(149)], ['más', wf(150)], ['versiones?»', wf(151)]]), from: 1138, to: wf(152), voice: true},
      {words: ws([['Y', wf(152)], ['tú', wf(153)], ['le', wf(154)], ['dirás', wf(155)]]), from: wf(152), to: SI},
      {words: [{text: '«Sí»', at: SI, key: true}], from: SI, to: 1207, size: 230, y: 884, exit: 'cut'},
      // Primer plano del prota: sobre la sudadera. Al abrirse el plano (corte en f1230) la
      // misma línea pasa a la banda en ese fotograma exacto, sin deslizarse ni repetir entrada.
      {words: ESCALARAS, from: Y_ESCALARAS, to: 1230, exit: 'cut', x: 600, y: 1290, grow: GROW},
      {words: ESCALARAS, from: 1230, to: 1237, exit: 'cut', x: 600, y: 866, grow: GROW},
    ]}
  />
);

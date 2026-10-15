import React from 'react';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 07 · Gestión en campañas (920–1022) ─────────────
// Plano abierto → acercamiento a la pantalla (f933–960) → alejamiento (f996–1008).
// La línea viaja con el canto superior de la pantalla (medido por fotograma): en abierto
// va entre las barbillas y la pantalla (y≈780); en el acercamiento, sobre los torsos
// (y≈406). Los checks verdes de la pantalla se ven limpios: ningún rótulo los repite.
const PUSH: [number, number][] = [
  [932, 780],
  [936, 618],
  [940, 542],
  [944, 486],
  [950, 434],
  [960, 406],
];
const PULL: [number, number][] = [
  [996, 406],
  [1008, 780],
];

export const Scene07: React.FC = () => (
  <BigLines
    x={540}
    y={406}
    maxWidth={820}
    maxSize={130}
    chunks={[
      {words: ws([['Luego', wf(119)]]), from: wf(119), to: wf(120), yKeys: [[923, 780], ...PUSH.slice(0, 2)]},
      {words: ws([['le', wf(120)], ['pedirás', wf(121)]]), from: wf(120), to: wf(122), yKeys: PUSH},
      {words: ws([['que', wf(122)], ['los', wf(123)], ['gestione', wf(124)]]), from: wf(122), to: wf(125), yKeys: PUSH},
      {words: ws([['en', wf(125)], ['las', wf(126)], ['campañas', wf(127), true]]), from: wf(125), to: wf(128)},
      {words: ws([['él', wf(128)], ['mismo,', wf(129)]]), from: wf(128), to: wf(130), yKeys: PULL},
      {words: ws([['te', wf(130)], ['lo', wf(131)], ['hará.', wf(132)]]), from: wf(130), to: 1022, exit: 'cut', yKeys: PULL},
    ]}
  />
);

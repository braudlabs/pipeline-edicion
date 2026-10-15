import React from 'react';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 06 · Cinco ads (840–920), toma v5 ─────────────
// Plano fijo: barbillas a y≈560–600 y canto superior de la pantalla a y≈850. La línea va
// en esa banda, sobre los torsos; la pantalla (con su fila 5 duplicada, pendiente de
// corrección de UI) queda limpia. «5 ads» es uno de los énfasis reservados por el brief.
export const Scene06: React.FC = () => (
  <BigLines
    x={540}
    y={790}
    maxWidth={820}
    maxSize={140}
    chunks={[
      {words: ws([['Le', wf(108)], ['pedirás', wf(109)]]), from: wf(108), to: wf(110)},
      {words: ws([['5', wf(110), true], ['ads', wf(111)]]), from: wf(110), to: wf(112), size: 170},
      {words: ws([['para', wf(112)], ['un', wf(113)], ['concepto', wf(114)]]), from: wf(112), to: wf(115)},
      {words: ws([['nuevo,', wf(115)]]), from: wf(115), to: wf(116)},
      {words: ws([['te', wf(116)], ['los', wf(117)], ['dará.', wf(118), true]]), from: wf(116), to: 920, exit: 'cut'},
    ]}
  />
);

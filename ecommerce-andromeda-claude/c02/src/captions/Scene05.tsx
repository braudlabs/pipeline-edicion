import React from 'react';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 05 · Presentación de la máquina (782–840) y 06 PROVISIONAL (840–920) ─────────────
// 05: franja entre su barbilla (≈600) y el borde superior de la máquina (≈720); la pantalla
//     negra queda limpia (define el hardware; Ale: nada de motion en la maquinita).
// 06: zona libre sobre la pantalla, a la izquierda del estampado (x≈110–750). PROVISIONAL.
export const Scene05: React.FC = () => (
  <BigLines
    x={540}
    y={712}
    maxWidth={860}
    maxSize={124}
    chunks={[
      {words: ws([['Instalaremos', wf(102)]]), from: wf(102), to: wf(103)},
      {words: ws([['en', wf(103)], ['tu', wf(104)], ['tienda', wf(105)]]), from: wf(103), to: wf(106)},
      {words: ws([['esta', wf(106)], ['maquinita', wf(107), true]]), from: wf(106), to: 840, exit: 'cut'},
    ]}
  />
);

export const Scene06: React.FC = () => (
  <BigLines
    x={430}
    y={522}
    maxWidth={640}
    maxSize={170}
    chunks={[
      {words: ws([['le', wf(108)], ['pedirás', wf(109)]]), from: wf(108), to: wf(110)},
      {words: ws([['5', wf(110), true], ['ads', wf(111)]]), from: wf(110), to: wf(112)},
      {words: ws([['para', wf(112)], ['un', wf(113)], ['concepto', wf(114)]]), from: wf(112), to: wf(115)},
      {words: ws([['nuevo', wf(115)]]), from: wf(115), to: wf(116)},
      {words: ws([['te', wf(116)], ['los', wf(117)], ['dará.', wf(118), true]]), from: wf(116), to: 920, exit: 'cut'},
    ]}
  />
);

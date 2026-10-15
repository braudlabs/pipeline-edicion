import React from 'react';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 05 · Presentación de la máquina (782–840) ─────────────
// 05: franja entre su barbilla (≈600) y el borde superior de la máquina (≈720); la pantalla
//     negra queda limpia (define el hardware; Ale: nada de motion en la maquinita).
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

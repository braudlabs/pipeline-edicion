import React from 'react';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 09 · Ideas de mierda (1237–1340) ─────────────
// La línea vive en el interior del cesto (mimbre liso, y≈1250), donde caen los papeles.
// «mierda» cae dentro de la línea con gravedad, como las bolas de papel; en «el doble de
// mierda» sin eco (Ale: «queda cutre»). Sin golpe sonoro: el bloque 09
// se mantiene seco y la caída de los papeles es anterior a «el doble» (observación del brief).
const G = 9; // px/f²
const DROP = 160;
const tFall = Math.sqrt((2 * DROP) / G);
const dropY = (t: number, at: number) => {
  const a = t - at;
  if (a < 0) return -DROP;
  if (a < tFall) return -DROP + 0.5 * G * a * a;
  const b = a - tFall;
  const v = G * tFall * 0.24;
  return -Math.max(0, v * b - 0.5 * G * b * b);
};

export const Scene09: React.FC = () => (
  <BigLines
    x={540}
    y={1250}
    maxWidth={820}
    maxSize={140}
    wordMotion={(w, t) => (w.text === 'mierda' && w.at === wf(166) ? {y: dropY(t, w.at), moving: t >= w.at - 0.5 && t < w.at + tFall + 6} : undefined)}
    chunks={[
      {words: ws([['Pero', wf(159)], ['eh,', wf(160)]]), from: wf(159), to: wf(161)},
      {words: ws([['que', wf(161)], ['si', wf(162)], ['metes', wf(163)]]), from: wf(161), to: wf(164)},
      {
        words: [
          {text: 'ideas', at: wf(164)},
          {text: 'de', at: wf(165)},
          {text: 'mierda', at: wf(166), key: true, noRise: true},
        ],
        from: wf(164),
        to: wf(167),
      },
      {words: ws([['sacarás', wf(167)], ['el', wf(168)], ['doble', wf(169), true]]), from: wf(167), to: wf(170)},
      {words: [{text: 'de', at: wf(170)}, {text: 'mierda.', at: wf(171), key: true}], from: wf(170), to: 1340, exit: 'cut'},
    ]}
  />
);

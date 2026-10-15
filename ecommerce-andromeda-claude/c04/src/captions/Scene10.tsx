import React from 'react';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';
import {Tag} from './Tag';

// ───────────── 10 · Fundadores (1340–1478) ─────────────
// Primer plano de Elliot (hasta f1391), paso a kiwi (f1392–1404), primer plano de kiwi
// (f1405–1423), alejamiento al plano de los dos (f1424–1450). Camiseta blanca y camisa
// azul claro: tinta marino con acento azul BRAUD (un blanco no se leería). Sobre las
// camisetas (y≈1300); en el plano de los dos, sobre los torsos (y≈1060).
// Handles: @notelliotkay sobre Elliot y @notkurtgodel sobre kiwi; en el plano de los dos,
// ambos anclados sobre sus cabezas. Una sola aparición de los fundadores (brief).
export const Scene10: React.FC = () => (
  <>
    <BigLines
      x={540}
      y={1300}
      maxWidth={820}
      maxSize={130}
      chunks={[
        {words: ws([['Pero', wf(172)], ['para', wf(173)], ['eso', wf(174)], ['están', wf(175)]]), from: wf(172), to: wf(176), ink: 'dark'},
        {words: ws([['el', wf(176)], ['melenas', wf(177), true]]), from: wf(176), to: wf(178), ink: 'dark'},
        {words: ws([['y', wf(178)], ['el', wf(179)], ['cabeza', wf(180)], ['kiwi,', wf(181), true]]), from: wf(178), to: wf(182), ink: 'dark'},
        {words: ws([['que', wf(182)], ['llevan', wf(183)], ['haciendo', wf(184)]]), from: wf(182), to: wf(185), ink: 'dark'},
        {
          words: ws([['estos', wf(185)], ['ads', wf(186)], ['con', wf(187)], ['IA', wf(188), true]]),
          from: wf(185),
          to: wf(189),
          ink: 'dark',
          yKeys: [
            [1435, 1300],
            [1450, 1060],
          ],
        },
        {words: ws([['meses', wf(189)], ['y', wf(190)], ['meses.', wf(191)]]), from: wf(189), to: 1478, ink: 'dark', y: 1060, exit: 'cut'},
      ]}
    />
    <Tag text="@notelliotkay" x={880} y={560} from={1346} to={1404} />
    <Tag text="@notkurtgodel" x={540} y={1118} from={1406} to={1431} />
    <Tag text="@notelliotkay" x={345} y={300} from={1452} to={1478} />
    <Tag text="@notkurtgodel" x={720} y={250} from={1452} to={1478} />
  </>
);

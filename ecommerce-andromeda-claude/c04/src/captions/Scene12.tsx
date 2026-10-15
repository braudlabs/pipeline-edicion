import {useT} from '../lib/time';
import React from 'react';

import {clamp, outBack, outQuart} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, typeStyle} from '../lib/type';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 12 · Habitación llena (1585–1681) ─────────────
// Picado alto: personas y máquina abajo a la izquierda, proyecciones de producto que llenan
// la pared desde f1621 (y≈450–800). La línea va en la pared alta (y≈400), a la derecha de
// la ventana y por encima de las proyecciones. En «creativos» la pared se llena también de
// la palabra: copias pequeñas que aparecen escalonadas, como las proyecciones.
export const Scene12: React.FC = () => (
  <>
    <BigLines
      x={680}
      y={400}
      maxWidth={700}
      maxSize={124}
      chunks={[
        {words: ws([['Para', wf(207)], ['que', wf(208)]]), from: wf(207), to: wf(209)},
        {words: ws([['no', wf(209)], ['estés', wf(210)], ['solo', wf(211)]]), from: wf(209), to: wf(212)},
        {words: ws([['contra', wf(212)], ['una', wf(213)]]), from: wf(212), to: wf(214)},
        {words: ws([['máquina', wf(214)]]), from: wf(214), to: wf(215)},
        {words: ws([['que', wf(215)], ['te', wf(216)], ['puede', wf(217)]]), from: wf(215), to: wf(218)},
        {words: ws([['llenar', wf(218)]]), from: wf(218), to: wf(219)},
        {words: ws([['la', wf(219)], ['habitación', wf(220)]]), from: wf(219), to: wf(221)},
        {words: ws([['de', wf(221)], ['creativos.', wf(222), true]]), from: wf(221), to: 1681, exit: 'cut'},
      ]}
    />
    <Swarm />
  </>
);

// Copias de «creativos» en la pared libre (fuera de caras, ventana y proyecciones).
const COPIES: {x: number; y: number; size: number; rot: number; delay: number; a: number}[] = [
  {x: 470, y: 205, size: 64, rot: -4, delay: 3, a: 0.62},
  {x: 860, y: 175, size: 56, rot: 3, delay: 5, a: 0.5},
  {x: 640, y: 120, size: 46, rot: -2, delay: 7, a: 0.42},
  {x: 930, y: 290, size: 50, rot: 5, delay: 8, a: 0.46},
  {x: 410, y: 300, size: 44, rot: 2, delay: 10, a: 0.38},
  {x: 780, y: 250, size: 40, rot: -6, delay: 11, a: 0.34},
];

const Swarm: React.FC = () => {
  const frame = useT();
  const at = wf(222);
  if (frame < at || frame >= 1681) return null;
  const moving = (t: number) => COPIES.some((c) => t >= at + c.delay - 0.5 && t < at + c.delay + 6);
  const render = (t: number) => (
    <>
      {COPIES.map((c, k) => {
        const age = t - (at + c.delay);
        if (age < 0) return null;
        const s = outBack(1.6)(clamp(age / 5));
        return (
          <div
            key={k}
            style={{
              ...typeStyle({size: c.size, weight: 780, tracking: -0.035, color: k % 2 ? INK.white : INK.sky, shadowKind: 'soft'}),
              position: 'absolute',
              left: c.x,
              top: c.y,
              opacity: c.a * outQuart(clamp(age / 2)),
              transform: `translate(-50%, -50%) rotate(${c.rot}deg) scale(${0.6 + 0.4 * s})`,
            }}
          >
            creativos
          </div>
        );
      })}
    </>
  );
  return <Shutter render={render} moving={moving} />;
};

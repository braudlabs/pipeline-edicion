import React from 'react';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 13 · Metagag (1681–1786) ─────────────
// Perfil → mira a cámara (f1694–1724) → se gira hacia la pantalla (f1725–1748) → la
// pantalla con la recreación del hook y el azul detrás (desde f1749). Nada encima de la
// pantalla (Ale: nada de motion en la maquinita). Primero sobre la sudadera, a la
// izquierda de la pantalla; con el giro, la línea sube a la franja libre sobre el canto
// de la pantalla (y≈560), por un solo eje.
export const Scene13: React.FC = () => (
  <BigLines
    x={330}
    y={1000}
    maxWidth={560}
    maxSize={120}
    chunks={[
      {words: ws([['Me', wf(223)], ['olvidaba,', wf(224)]]), from: wf(223), to: wf(225)},
      {words: ws([['este', wf(225)], ['mismo', wf(226)], ['ad', wf(227), true]]), from: wf(225), to: wf(228)},
      {words: ws([['lo', wf(228)], ['ha', wf(229)], ['hecho', wf(230)]]), from: wf(228), to: wf(231)},
      {
        words: ws([['la', wf(231)], ['maquinita', wf(232), true]]),
        from: wf(231),
        to: wf(233),
        yKeys: [
          [1744, 1000],
          [1753, 560],
        ],
      },
      {words: ws([['de', wf(233)], ['la', wf(234)], ['que', wf(235)]]), from: wf(233), to: wf(236), x: 600, y: 560, maxWidth: 760},
      {words: ws([['te', wf(236)], ['hablo.', wf(237)]]), from: wf(236), to: 1786, x: 600, y: 560, maxWidth: 760, exit: 'cut'},
    ]}
  />
);

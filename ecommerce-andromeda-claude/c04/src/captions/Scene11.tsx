import React from 'react';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 11 · Criterio (1478–1585) ─────────────
// Plano fijo: el gesto de apartar dos propuestas y elegir una debe leerse, así que nada
// baja a las manos ni a los papeles. Las frases van detrás de las cabezas (relleno
// recortado con el matte + contorno fino delante), el lenguaje del hook A aprobado por
// Ale; segunda y última vez que se usa en el vídeo. «criterio» es el único acento. Centro
// desplazado a x=450 para que la cabeza del prota (x≈620–920) solo tape el final de cada línea.
// Matte: personas de Vision + clave de color de la piel azul (Vision no recorta la
// cabeza del azul en este plano); ver CAMBIOS.md.
const BEHIND = {dir: 'criterio-holdout', sceneFrom: 1478, srcIn: 0, first: 0, count: 121};

export const Scene11: React.FC = () => (
  <BigLines
    x={450}
    y={322}
    maxWidth={880}
    maxSize={132}
    weight={820}
    tracking={-0.045}
    behind={BEHIND}
    outline={0.9}
    chunks={[
      {words: ws([['E', wf(192)], ['instalarán', wf(193)]]), from: wf(192), to: wf(194)},
      {words: ws([['en', wf(194)], ['tu', wf(195)], ['tienda', wf(196)]]), from: wf(194), to: wf(197)},
      {words: ws([['el', wf(197)], ['criterio', wf(198), true]]), from: wf(197), to: wf(199), size: 160},
      {words: ws([['que', wf(199)], ['necesitas', wf(200)]]), from: wf(199), to: wf(201)},
      {words: ws([['para', wf(201)], ['hacer', wf(202)]]), from: wf(201), to: wf(203)},
      {words: ws([['este', wf(203)], ['tipo', wf(204)], ['de', wf(205)], ['ads.', wf(206)]]), from: wf(203), to: 1585, exit: 'cut'},
    ]}
  />
);

import React from 'react';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 14 · CTA honesto (1786–1991) y 15 · Salida (1991–2050) ─────────────
// 14: plano frontal; el texto va en la capucha, entre la barbilla (≈620) y los ojos del
// estampado (≈900), sin tocar la cara del azul (x≥800) ni la mano que señala abajo.
// «pincha abajo» baja desde arriba, como el gesto. Desde «Veremos» (78,38 s), tramo sobrio:
// sin acentos ni efectos, solo la frase. «Así» empieza 2 f antes del corte: entra con él.
// 15: tinta marino sobre el mostrador crema, delante de la máquina; termina en «ads.».
export const Scene14: React.FC = () => (
  <BigLines
    x={505}
    y={850}
    maxWidth={540}
    maxSize={112}
    chunks={[
      {words: ws([['Así', Math.max(wf(238), 1786)], ['que', wf(239)], ['si', wf(240)]]), from: 1786, to: wf(241)},
      {words: ws([['la', wf(241)], ['quieres:', wf(242)]]), from: wf(241), to: wf(243)},
      {words: ws([['pincha', wf(243)], ['abajo', wf(244), true]]), from: wf(243), to: wf(245), enter: 'down'},
      {words: ws([['y', wf(245)], ['reserva', wf(246)]]), from: wf(245), to: wf(247)},
      {words: ws([['una', wf(247)], ['llamada', wf(248), true]]), from: wf(247), to: wf(249)},
      {words: ws([['con', wf(249)], ['nosotros.', wf(250)]]), from: wf(249), to: wf(251)},
      {words: ws([['Veremos', wf(251)], ['si', wf(252)], ['tiene', wf(253)]]), from: wf(251), to: wf(254)},
      {words: ws([['encaje', wf(254)], ['para', wf(255)], ['ti;', wf(256)]]), from: wf(254), to: wf(257)},
      {words: ws([['si', wf(257)], ['lo', wf(258)], ['tiene,', wf(259)]]), from: wf(257), to: wf(260)},
      {words: ws([['te', wf(260)], ['lo', wf(261)], ['diremos', wf(262)]]), from: wf(260), to: wf(263)},
      {words: ws([['y', wf(263)], ['si', wf(264)], ['no,', wf(265)]]), from: wf(263), to: wf(266)},
      {words: ws([['también.', wf(266)]]), from: wf(266), to: 1991, exit: 'cut'},
    ]}
  />
);

export const Scene15: React.FC = () => (
  <BigLines
    x={540}
    y={1330}
    maxWidth={820}
    maxSize={124}
    chunks={[
      {words: ws([['Me', wf(267)], ['voy,', wf(268)]]), from: wf(267), to: wf(269), ink: 'halo'},
      {words: ws([['que', wf(269)], ['quiero', wf(270)], ['seguir', wf(271)]]), from: wf(269), to: wf(272), ink: 'halo'},
      {words: ws([['produciendo', wf(272)], ['ads.', wf(273), true]]), from: wf(272), to: 2050, ink: 'halo', exit: 'cut'},
    ]}
  />
);

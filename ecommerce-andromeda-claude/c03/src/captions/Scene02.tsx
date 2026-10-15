import {useT} from '../lib/time';
import React from 'react';

import card from '../data/card-track.json';
import {clamp, lerp, outCubic} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, typeStyle} from '../lib/type';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 02 · Ticket: ángulo y semanas (350–444) ─────────────
// 02a · Selfie: no hay franja libre (cara, tarjeta, estampado). La petición se imprime en
//       el margen blanco de la tarjeta («la pieza») con la tinta azul de la persiana, y
//       viaja con ella durante la panorámica (seguimiento encadenado de la tarjeta).
// 02b · Máquina: «y necesitas / semanas» grande y centrado DETRÁS del ticket: el papel
//       cae por delante y se ve entero (matte por luminancia del papel y la tarjeta).
// 02c · Caída: el papel ocupa el centro; «para ver / el fruto / de eso» en la zona libre
//       de la izquierda, dentro de márgenes, también por detrás del borde del papel.

const ANCHOR = {x: 486, y: 848}; // margen superior de la tarjeta en el maestro 356, lejos del borde
// La tarjeta gira en la panorámica (borde superior ≈4° a f374, medido sobre fotogramas).
const cardRot = (t: number) => (t <= 358 ? 0 : t <= 374 ? 4.2 * ((t - 358) / 16) : 4.2 + 0.2 * (t - 374));
const cardAt = (t: number): [number, number] => {
  const frames = card.frames as Record<string, number[]>;
  const a = Math.floor(t);
  const k0 = frames[String(Math.max(350, Math.min(386, a)))];
  const k1 = frames[String(Math.max(350, Math.min(386, a + 1)))];
  const f = t - a;
  return [lerp(k0[0], k1[0], f), lerp(k0[1], k1[1], f)];
};

// Cada palabra conserva su instante hablado (vínculo verificable), aunque la impresión
// aparezca como unidad completa: la tarjeta sale de cuadro antes de «ángulo».
type PrintChunk = {from: number; to: number; words: {text: string; at: number}[]};

const CardPrint: React.FC = () => {
  const frame = useT();
  const chunks: PrintChunk[] = [
    {from: wf(43), to: wf(45), words: [{text: 'Quieres', at: wf(43)}, {text: 'testear', at: wf(44)}]},
    {from: wf(45), to: 386, words: [{text: 'un', at: wf(45)}, {text: 'nuevo', at: wf(46)}, {text: 'ángulo', at: wf(47)}]},
  ];
  const c = chunks.find((ch) => frame >= ch.from && frame < ch.to);
  if (!c) return null;
  const moving = (t: number) => t < c.from + 4 || (t > 357 && t < 387);
  const render = (t: number) => {
    const [dx, dy] = cardAt(t);
    const age = t - c.from;
    const sc = 1 + (1 - outCubic(clamp(age / 3))) * 0.16;
    return (
      <div
        style={{
          position: 'absolute',
          left: ANCHOR.x + dx,
          top: ANCHOR.y + dy,
          transform: `translate(-50%, -84%) rotate(${cardRot(t)}deg) scale(${sc})`,
          display: 'flex',
          alignItems: 'baseline',
          columnGap: '0.22em',
          whiteSpace: 'nowrap',
          opacity: clamp(age / 1 + 0.5) * 0.95,
          fontSize: 68,
        }}
      >
        {c.words.map((w, k) => (
          <span
            key={k}
            style={{
              ...typeStyle({size: 68, weight: 800, tracking: -0.035, color: INK.azul, shadowKind: 'none'}),
              display: 'inline-block',
              transformOrigin: '0% 80%',
            }}
          >
            {w.text}
          </span>
        ))}
      </div>
    );
  };
  return <Shutter render={render} moving={moving} style={{mixBlendMode: 'multiply'}} />;
};

const PAPER = {dir: 'paper-holdout', sceneFrom: 350, srcIn: 12, first: 48, count: 64};

export const Scene02: React.FC = () => (
  <>
    <CardPrint />
    <BigLines
      x={540}
      y={986}
      maxWidth={860}
      maxSize={180}
      behind={PAPER}
      chunks={[
        {words: ws([['y', wf(48)], ['necesitas', wf(49)]]), from: wf(48), to: wf(50), size: 124},
        {words: ws([['semanas', wf(50), true]]), from: wf(50), to: wf(51)},
      ]}
    />
    <BigLines
      x={300}
      y={906}
      maxWidth={380}
      maxSize={112}
      behind={PAPER}
      chunks={[
        {words: ws([['para', wf(51)], ['ver', wf(52)]]), from: wf(51), to: wf(53)},
        {words: ws([['el', wf(53)], ['fruto', wf(54), true]]), from: wf(53), to: wf(55)},
        {words: ws([['de', wf(55)], ['eso', wf(56)]]), from: wf(55), to: 444, exit: 'fade'},
      ]}
    />
  </>
);

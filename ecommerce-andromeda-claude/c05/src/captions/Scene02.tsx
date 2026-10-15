import {useT} from '../lib/time';
import React from 'react';

import edge from '../data/card-edge.json';
import {clamp, lerp, outCubic} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {typeStyle} from '../lib/type';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 02 · Ticket: ángulo y semanas (350–444) ─────────────
// 02a · Selfie: no hay franja libre (cara, tarjeta, estampado). La petición se imprime en
//       el margen blanco de la tarjeta («la pieza») con tinta azul, anclada a su canto.
// 02b · Máquina: «y necesitas / semanas» grande y centrado DETRÁS del ticket: el papel
//       cae por delante y se ve entero (matte por luminancia del papel y la tarjeta).
// 02c · Caída: el papel ocupa el centro; «para ver / el fruto / de eso» en la zona libre
//       de la izquierda, dentro de márgenes, también por detrás del borde del papel.

// C05 · Ale: «lo de nuevo ángulo… puede quedar más integrado porque se ve un poco cutre».
// La impresión ya no flota con un desplazamiento aproximado: va anclada al canto superior real
// de la tarjeta (recta ajustada al borde visible por fotograma, `card-edge.json`), con su mismo
// ángulo (≈6° → 4°), recortada dentro de la tarjeta y revelada de izquierda a derecha como una
// impresora. Tinta azul impresa (multiplicar, ligeramente blanda), nunca fuera del papel.
const CARD_W = edge.width; // anchura de la tarjeta en el maestro (≈742 px, constante medida)
const BAND_H = 170; // franja blanca superior donde va el texto
const edgeAt = (t: number): [number, number, number] => {
  const frames = edge.frames as Record<string, number[]>;
  const a = Math.floor(t);
  const k0 = frames[String(Math.max(350, Math.min(386, a)))];
  const k1 = frames[String(Math.max(350, Math.min(386, a + 1)))];
  const f = t - a;
  return [lerp(k0[0], k1[0], f), lerp(k0[1], k1[1], f), lerp(k0[2], k1[2], f)];
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
  const moving = (t: number) => t < c.from + 5 || (t > 357 && t < 387);
  const render = (t: number) => {
    const [rx, ry, deg] = edgeAt(t);
    const rad = (deg * Math.PI) / 180;
    // Esquina superior izquierda (virtual si ya está fuera de cuadro): la tarjeta mide CARD_W.
    const lx = rx - CARD_W * Math.cos(rad);
    const ly = ry - CARD_W * Math.sin(rad);
    const wipe = outCubic(clamp((t - c.from) / 5));
    return (
      <div
        style={{
          position: 'absolute',
          left: lx,
          top: ly,
          width: CARD_W,
          height: BAND_H,
          transformOrigin: '0 0',
          transform: `rotate(${deg}deg)`,
          overflow: 'hidden',
          clipPath: `inset(0 ${(1 - wipe) * 100}% 0 0)`,
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: CARD_W / 2,
            top: 92,
            transform: 'translate(-50%, -84%)',
            display: 'flex',
            alignItems: 'baseline',
            columnGap: '0.22em',
            whiteSpace: 'nowrap',
            fontSize: 58,
            filter: 'blur(0.45px)',
          }}
        >
          {c.words.map((w, k) => (
            <span key={k} style={{...typeStyle({size: 58, weight: 780, tracking: -0.03, color: '#2A4BD6', shadowKind: 'none'}), display: 'inline-block', opacity: 0.94}}>
              {w.text}
            </span>
          ))}
        </div>
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

import {useT} from '../lib/time';
import React from 'react';

import track from '../data/shutter-track.json';
import {clamp, inOutCubic, lerp, outCubic, outQuart, settle} from '../lib/anim';
import {quadMatrix, Pt} from '../lib/homography';
import {camPt} from '../fx/camera';
import {useCamAt} from '../fx/plan';
import {Shutter} from '../lib/Shutter';
import {INK, TypeSpec, typeStyle} from '../lib/type';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 01 · Ventanilla, persiana, banco y entrega (130–350) ─────────────

const RAIL: TypeSpec = {size: 62, weight: 680, tracking: -0.018, shadowKind: 'deep'};
const HERO: TypeSpec = {size: 170, weight: 840, tracking: -0.045, color: INK.white, shadowKind: 'deep'};

// 01A · Ventanilla: frases grandes centradas bajo las manos que entregan la carpeta
// (mostrador, y≈1030–1105); la empleada que baja la persiana queda libre.
const Window: React.FC = () => (
  <BigLines
    x={540}
    y={1105}
    maxWidth={860}
    maxSize={138}
    chunks={[
      {words: ws([['Y', wf(16)], ['sabes', wf(17)], ['que', wf(18)]]), from: wf(16), to: wf(19)},
      {words: ws([['de', wf(19)], ['la', wf(20)], ['forma', wf(21)]]), from: wf(19), to: wf(22)},
      {words: ws([['tradicional', wf(22), true]]), from: wf(22), to: wf(23)},
    ]}
  />
);

// 01B · Cartel impreso en la persiana cerrada, en su perspectiva y con su panorámica.
// Plano de 1000×700 px locales sobre el cuadrilátero medido en el fotograma fuente 70.
const PLANE_W = 1000;
const PLANE_H = 700;
const QUAD: [Pt, Pt, Pt, Pt] = [
  [600, 350],
  [1050, 239],
  [1050, 705],
  [600, 690],
];
const trackAt = (master: number): [number, number] => {
  const src = master - 130;
  const frames = track.frames as Record<string, number[]>;
  const a = Math.floor(src);
  const k0 = frames[String(Math.max(50, Math.min(106, a)))];
  const k1 = frames[String(Math.max(50, Math.min(106, a + 1)))];
  const f = src - a;
  return [lerp(k0[0], k1[0], f), lerp(k0[1], k1[1], f)];
};

type PrintLine = {words: {text: string; at: number}[]; y: number; size: number; weight: number; width?: number; heavy?: boolean};

const ShutterSign: React.FC = () => {
  const frame = useT();
  const camAt = useCamAt();
  const from = wf(23);
  const to = 237;
  if (frame < from || frame >= to) return null;
  // Bloque centrado a la izquierda del plano (x local 430) para que la panorámica
  // (+70 px al final) no lo saque de cuadro. Espaciado de palabra uniforme por línea.
  const lines: PrintLine[] = [
    {y: 150, size: 112, weight: 760, words: [{text: 'es', at: wf(23)}, {text: 'la', at: wf(24)}, {text: 'misma', at: wf(25)}]},
    {y: 452, size: 292, weight: 900, width: 72, heavy: true, words: [{text: 'MIERDA', at: wf(26)}]},
    {y: 612, size: 112, weight: 760, words: [{text: 'de', at: wf(27)}, {text: 'siempre', at: wf(28)}]},
  ];
  const all = lines.flatMap((l) => l.words.map((w) => ({...w, heavy: l.heavy})));
  const moving = (t: number) => all.some((w) => t >= w.at - 0.5 && t < w.at + (w.heavy ? 9 : 4));
  const render = (t: number) => {
    const [dx, dy] = trackAt(t);
    const c = camAt(t); // C06: el cartel va pegado a la persiana, también cuando la cámara golpea
    const q = QUAD.map(([x, y]) => camPt(c, x + dx, y + dy) as Pt) as [Pt, Pt, Pt, Pt];
    return (
      <div style={{position: 'absolute', left: 0, top: 0, width: PLANE_W, height: PLANE_H, transformOrigin: '0 0', transform: quadMatrix(PLANE_W, PLANE_H, q)}}>
        {lines.map((ln, li) => (
          <div key={li} style={{position: 'absolute', left: 430, top: ln.y, transform: 'translate(-50%, -84%)', display: 'flex', alignItems: 'baseline', columnGap: '0.24em', whiteSpace: 'nowrap', fontSize: ln.size}}>
            {ln.words.map((w, k) => {
              const age = t - w.at;
              const sc = ln.heavy ? 1 + (1 - settle(0.85, 5.5)(clamp(age / 9))) * 0.42 : 1 + (1 - outCubic(clamp(age / 3))) * 0.2;
              return (
                <span
                  key={k}
                  style={{
                    ...typeStyle({size: ln.size, weight: ln.weight, width: ln.width ?? 100, tracking: ln.heavy ? -0.01 : -0.02, color: INK.azul, shadowKind: 'none'}),
                    display: 'inline-block',
                    transform: `scale(${age < 0 ? 1 : sc})`,
                    transformOrigin: '50% 70%',
                    opacity: age < 0 ? 0 : clamp(age / 1 + 0.5) * 0.94,
                  }}
                >
                  {w.text}
                </span>
              );
            })}
          </div>
        ))}
      </div>
    );
  };
  return <Shutter render={render} moving={moving} style={{mixBlendMode: 'multiply'}} />;
};

// 01C · Banco: «días» → «y días» → «para que», grandes y centrados sobre sus cabezas.
// El segundo «días» se vence (6°) cuando él se desploma en el hombro del azul.
const Bench: React.FC = () => {
  const sag = (t: number) => inOutCubic(clamp((t - wf(31)) / 12));
  return (
    <BigLines
      x={540}
      y={592}
      maxWidth={860}
      maxSize={190}
      wordMotion={(w, t) => (w.text === 'días' && w.at === wf(31) ? {rot: 6 * sag(t), y: 10 * sag(t), moving: t > wf(31) && t < wf(31) + 13} : undefined)}
      chunks={[
        {words: ws([['días', wf(29)]]), from: wf(29), to: wf(30)},
        {words: ws([['y', wf(30)], ['días', wf(31), true]]), from: wf(30), to: wf(32)},
        {words: ws([['para', wf(32)], ['que', wf(33)]]), from: wf(32), to: 282, size: 130, exit: 'cut'},
      ]}
    />
  );
};

// 01D · Mostrador: franja del cuello y los cordones, entre caras (≤800) y estampado (≥1000).
const Counter: React.FC = () => (
  <BigLines
    x={540}
    y={936}
    maxWidth={860}
    maxSize={120}
    chunks={[
      {words: ws([['el', wf(34)], ['editor', wf(35)]]), from: wf(34), to: wf(36)},
      {words: ws([['o', wf(36)], ['una', wf(37)], ['agencia', wf(38)]]), from: wf(36), to: wf(39)},
      {words: ws([['te', wf(39)], ['entregue', wf(40)]]), from: wf(39), to: wf(41)},
      {words: ws([['las', wf(41)], ['piezas.', wf(42), true]]), from: wf(41), to: 350, exit: 'cut'},
    ]}
  />
);

export const Scene01: React.FC = () => (
  <>
    <Window />
    <ShutterSign />
    <Bench />
    <Counter />
  </>
);

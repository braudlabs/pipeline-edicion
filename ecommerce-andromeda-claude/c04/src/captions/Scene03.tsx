import {useT} from '../lib/time';
import React from 'react';

import {clamp, hash, outCubic, settle} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, TypeSpec, typeStyle} from '../lib/type';
import {wf} from '../lib/words';
import {BigLines, ws} from './Big';

// ───────────── 03 · Las pantallas se apagan (450–552) y 03b · otra puta vez (552–610) ─────────────

const RAIL: TypeSpec = {size: 58, weight: 690, tracking: -0.018, shadowKind: 'deep'};
const HERO: TypeSpec = {size: 112, weight: 880, tracking: -0.04, color: INK.sky, shadowKind: 'deep'};

// Apagados medidos en el bruto: maestro 486, 497 y 537 (último, sobre «antiguos»).
const OFF_LAST = 537;

/** Estado «sin señal» que copia el último apagado: parpadeo de 3 f y queda gris. */
const powerOffAt = (at: number) => (frame: number): React.CSSProperties | undefined => {
  if (frame < at) return undefined;
  const k = Math.floor(frame - at + 1e-6);
  const flick = [0.15, 1, 0.05, 0.7, 0.3][k] ?? 0.34;
  return {opacity: flick, filter: k >= 4 ? 'grayscale(1) brightness(0.72)' : undefined};
};

// Franja sobre el canto de las pantallas (y≈680–752): libre de caras, de ancho completo.
// «caído» cae dentro de la línea con gravedad y rebota; la frase se apaga como las
// pantallas cuando ya se ha podido leer «antiguos».
const G = 9; // px/f²
const DROP = 150;
const tFall = Math.sqrt((2 * DROP) / G);
const dropY = (t: number, at: number) => {
  const a = t - at;
  if (a < 0) return -DROP;
  if (a < tFall) return -DROP + 0.5 * G * a * a;
  const b = a - tFall;
  const v = G * tFall * 0.24;
  return -Math.max(0, v * b - 0.5 * G * b * b);
};

const Band: React.FC = () => (
  <BigLines
    x={540}
    y={752}
    maxWidth={860}
    maxSize={122}
    styleAt={(f) => (f >= 527 ? powerOffAt(547)(f) : undefined)}
    wordMotion={(w, t) => (w.text === 'caído' ? {y: dropY(t, w.at), moving: t >= w.at - 0.5 && t < w.at + tFall + 6} : undefined)}
    chunks={[
      {words: ws([['y', wf(57)], ['durante', wf(58)]]), from: wf(57), to: wf(59)},
      {words: ws([['todo', wf(59)], ['ese', wf(60)], ['proceso', wf(61)]]), from: wf(59), to: wf(62)},
      {words: ws([['ya', wf(62)], ['se', wf(63)], ['te', wf(64)], ['han', wf(65)]]), from: wf(62), to: wf(66)},
      {words: [{text: 'caído', at: wf(66), key: true, noRise: true}], from: wf(66), to: wf(67), exit: 'cut', size: 150},
      {words: ws([['los', wf(67)], ['ads', wf(68)], ['antiguos', wf(69), true]]), from: wf(67), to: 552, exit: 'cut'},
    ]}
  />
);

export const Scene03: React.FC = () => <Band />;

// 03b · «y venga a repetir» y remate condensado en columna izquierda, libre de caras y
// de la bobina. Tras «vez.» el bloque se queda quieto: la mirada a cámara remata.
const PUNCH: TypeSpec = {size: 178, weight: 900, width: 62, tracking: -0.005, color: INK.white, shadowKind: 'deep', lineHeight: 0.86};

const Slam: React.FC<{words: {text: string; at: number; y: number}[]; x: number; to: number}> = ({words, x, to}) => {
  const frame = useT();
  if (frame < words[0].at || frame >= to) return null;
  const moving = (t: number) => words.some((w) => t >= w.at - 0.5 && t < w.at + 6);
  const render = (t: number) => (
    <>
      {words.map((w, k) => {
        const a = t - w.at;
        if (a < 0) return null;
        const e = outCubic(clamp(a / 3));
        const sc = 1.32 - 0.32 * e;
        // micro temblor solo en «PUTA», 3 f, determinista
        const shake = w.text === 'PUTA' && a < 4 ? (hash(Math.floor(t) * 3.1) - 0.5) * 10 : 0;
        return (
          <div
            key={k}
            style={{
              position: 'absolute',
              left: x + shake,
              top: w.y,
              transformOrigin: '0% 70%',
              transform: `translate(0, -84%) scale(${sc})`,
              opacity: clamp(a / 1 + 0.4),
              ...typeStyle(PUNCH),
            }}
          >
            {w.text}
          </div>
        );
      })}
    </>
  );
  return <Shutter render={render} moving={moving} />;
};

export const Scene03b: React.FC = () => (
  <>
    <BigLines
      x={540}
      y={452}
      maxWidth={860}
      maxSize={132}
      chunks={[
        {words: ws([['y', wf(70)], ['venga', wf(71)], ['a', wf(72)]]), from: wf(70), to: wf(73)},
        {words: ws([['repetir', wf(73), true]]), from: wf(73), to: wf(74)},
      ]}
    />
    <Slam
      x={66}
      to={610}
      words={[
        {text: 'OTRA', at: wf(74), y: 676},
        {text: 'PUTA', at: wf(75), y: 830},
        {text: 'VEZ.', at: wf(76), y: 984},
      ]}
    />
  </>
);

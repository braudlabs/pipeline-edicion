import React from 'react';
import {useCurrentFrame} from 'remotion';
import {clamp, hash, outCubic, settle} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, TypeSpec, typeStyle} from '../lib/type';
import {wf} from '../lib/words';
import {line, Stack} from './Stack';

// ───────────── 03 · Las pantallas se apagan (450–552) y 03b · otra puta vez (552–610) ─────────────

const RAIL: TypeSpec = {size: 58, weight: 690, tracking: -0.018, shadowKind: 'deep'};
const HERO: TypeSpec = {size: 112, weight: 880, tracking: -0.04, color: INK.sky, shadowKind: 'deep'};

// Apagados medidos en el bruto: maestro 486, 497 y 537 (último, sobre «antiguos»).
const OFF_LAST = 537;

/** Estado «sin señal» que copia el último apagado: parpadeo de 3 f y queda gris. */
const powerOffAt = (at: number) => (frame: number): React.CSSProperties | undefined => {
  if (frame < at) return undefined;
  const k = frame - at;
  const flick = [0.15, 1, 0.05, 0.7, 0.3][k] ?? 0.34;
  return {opacity: flick, filter: k >= 4 ? 'grayscale(1) brightness(0.72)' : undefined};
};

// Columna estrecha entre las dos cabezas (x≈320–590): lista vertical de palabras.
const Column: React.FC = () => (
  <>
    <Stack
      from={wf(57)}
      to={wf(62)}
      x={336}
      spec={RAIL}
      exit="lift"
      exitFrames={3}
      lines={[line(392, [['y', wf(57)], ['durante', wf(58)]]), line(460, [['todo', wf(59)], ['ese', wf(60)]]), line(528, [['proceso', wf(61)]])]}
    />
    <Stack from={wf(62)} to={wf(67)} x={336} spec={RAIL} exit="fade" exitFrames={3} lines={[line(392, [['ya', wf(62)], ['se', wf(63)], ['te', wf(64)], ['han', wf(65)]])]} />
    <Stack
      from={wf(67)}
      to={552}
      x={336}
      spec={RAIL}
      styleAt={powerOffAt(547)}
      lines={[line(392, [['los', wf(67)], ['ads', wf(68)]]), line(462, [['antiguos', wf(69)]])]}
    />
  </>
);

/** «CAÍDO» cae con gravedad sobre el canto de las pantallas, rebota y se queda torcido. */
const Caido: React.FC = () => {
  const frame = useCurrentFrame();
  const at = wf(66);
  const to = 552;
  if (frame < at || frame >= to) return null;
  const y0 = 462; // arranca bajo «ya se te han», dentro del hueco entre las caras
  const yRest = 760; // canto superior de las pantallas, maestro 450–552
  const g = 9; // px / f²: cae en ~8 f y aterriza al acabar «caído»
  const tFall = Math.sqrt((2 * (yRest - y0)) / g);
  const pos = (t: number) => {
    const a = t - at;
    if (a < 0) return {y: y0, rot: 0, sq: 1};
    if (a < tFall) return {y: y0 + 0.5 * g * a * a, rot: -2 * (a / tFall), sq: 1};
    const b = a - tFall;
    const v = g * tFall * 0.26; // rebote con restitución baja
    const hop = Math.max(0, v * b - 0.5 * g * b * b);
    const landed = b > (2 * v) / g;
    const rot = landed ? -6 * settle(0.6, 7)(clamp((b - (2 * v) / g) / 8)) - 0 : -2 - 4 * clamp(b / ((2 * v) / g));
    const sq = landed ? 1 : 1;
    return {y: yRest - hop, rot, sq: b < 1.2 ? 0.86 : sq};
  };
  const moving = (t: number) => t >= at - 0.5 && t < at + tFall + 16;
  const off = powerOffAt(OFF_LAST)(frame);
  const render = (t: number) => {
    const p = pos(t);
    return (
      <div
        style={{
          position: 'absolute',
          left: 466,
          top: p.y,
          transformOrigin: '50% 100%',
          transform: `translate(-50%, -84%) rotate(${p.rot}deg) scaleY(${p.sq}) scaleX(${2 - p.sq})`,
          ...typeStyle({...HERO, size: 90}),
          ...off,
        }}
      >
        CAÍDO
      </div>
    );
  };
  return <Shutter render={render} moving={moving} />;
};

export const Scene03: React.FC = () => (
  <>
    <Column />
    <Caido />
  </>
);

// 03b · «y venga a repetir» y remate condensado en columna izquierda, libre de caras y
// de la bobina. Tras «vez.» el bloque se queda quieto: la mirada a cámara remata.
const PUNCH: TypeSpec = {size: 178, weight: 900, width: 62, tracking: -0.005, color: INK.white, shadowKind: 'deep', lineHeight: 0.86};

const Slam: React.FC<{words: {text: string; at: number; y: number}[]; x: number; to: number}> = ({words, x, to}) => {
  const frame = useCurrentFrame();
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
    <Stack
      from={wf(70)}
      to={wf(74)}
      x={72}
      spec={{...RAIL, size: 62}}
      exit="lift"
      exitFrames={3}
      lines={[line(520, [['y', wf(70)], ['venga', wf(71)], ['a', wf(72)]]), line(598, [['repetir', wf(73)]])]}
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

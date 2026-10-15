import React from 'react';
import {useCurrentFrame} from 'remotion';
import {clamp, outCubic, settle} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, TypeSpec, typeStyle} from '../lib/type';
import {wf} from '../lib/words';
import {line, Stack} from './Stack';

// ───────────── 05 · Presentación de la máquina (782–840) y 06 PROVISIONAL (840–920) ─────────────

const RAIL: TypeSpec = {size: 62, weight: 680, tracking: -0.018, shadowKind: 'deep'};
const HERO: TypeSpec = {size: 104, weight: 860, tracking: -0.04, color: INK.sky, shadowKind: 'deep'};

// Columna superior izquierda, sobre la pared: libre de su cara (x≥560) y de la pantalla
// negra (y≥720). La pantalla se deja vacía: define el hardware de las tomas siguientes.
export const Scene05: React.FC = () => (
  <>
    <Stack
      from={wf(102)}
      to={wf(106)}
      x={72}
      spec={RAIL}
      exit="lift"
      exitFrames={3}
      lines={[line(468, [['Instalaremos', wf(102)]]), line(546, [['en', wf(103)], ['tu', wf(104)], ['tienda', wf(105)]])]}
    />
    <Stack
      from={wf(106)}
      to={840}
      x={72}
      spec={RAIL}
      lines={[line(452, [['esta', wf(106)]]), line(586, [['maquinita', wf(107), {spec: HERO, enter: 'drop', settleAmp: 1}]])]}
    />
  </>
);

/** «5» se posa con peso (el dashboard definitivo enseñará las cinco versiones). */
const Five: React.FC<{at: number; to: number; x: number; y: number}> = ({at, to, x, y}) => {
  const frame = useCurrentFrame();
  if (frame < at || frame >= to) return null;
  const moving = (t: number) => t >= at - 0.5 && t < at + 10;
  const render = (t: number) => {
    const a = t - at;
    const s = settle(0.9, 6)(clamp(a / 10));
    const sc = 1.45 - 0.45 * s;
    return (
      <div style={{position: 'absolute', left: x, top: y, transformOrigin: '30% 80%', transform: `translate(0, -84%) scale(${sc})`, opacity: clamp(a / 1 + 0.4), ...typeStyle({size: 250, weight: 900, tracking: -0.06, color: INK.sky, shadowKind: 'deep'})}}>
        5
      </div>
    );
  };
  return <Shutter render={render} moving={moving} />;
};

export const Scene06: React.FC = () => (
  <>
    <Stack from={wf(108)} to={wf(112)} x={72} spec={{...RAIL, size: 54}} exit="fade" exitFrames={2} lines={[line(300, [['le', wf(108)], ['pedirás', wf(109)]])]} />
    <Five at={wf(110)} to={wf(116)} x={64} y={540} />
    <Stack from={wf(111)} to={wf(116)} x={246} spec={{...HERO, size: 112, color: INK.white}} exit="fade" exitFrames={3} lines={[line(540, [['ads', wf(111), {enter: 'left'}]])]} />
    <Stack
      from={wf(112)}
      to={wf(116)}
      x={72}
      spec={{...RAIL, size: 50, weight: 620}}
      exit="fade"
      exitFrames={3}
      lines={[line(300, [['para', wf(112)], ['un', wf(113)], ['concepto', wf(114)], ['nuevo', wf(115)]])]}
    />
    <Stack
      from={wf(116)}
      to={920}
      x={72}
      spec={RAIL}
      lines={[line(400, [['te', wf(116)], ['los', wf(117)]]), line(540, [['dará.', wf(118), {spec: {...HERO, size: 140}, enter: 'pop', settleAmp: 1}]])]}
    />
  </>
);

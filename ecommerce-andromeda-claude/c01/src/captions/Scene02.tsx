import React from 'react';
import {useCurrentFrame} from 'remotion';
import {clamp, inOutCubic, outCubic, outQuart} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, TypeSpec, typeStyle} from '../lib/type';
import {wf} from '../lib/words';
import {line, Stack} from './Stack';

// ───────────── 02 · Ticket: ángulo y semanas (350–450) ─────────────
// El plano barre de la cara+tarjeta a la máquina y baja con el papel. La única franja
// estable es una columna derecha (x≈800–1044, y≈840–1060): hombro del azul → frontal de
// la máquina (entre ranura y botón) → pared. Las tres frases comparten ese ancla.
// Libres: cara, tarjeta (la pieza), estampado, mano que pulsa, ranura y papel.

const RAIL: TypeSpec = {size: 58, weight: 690, tracking: -0.018, shadowKind: 'deep'};
const KEY: TypeSpec = {size: 76, weight: 860, tracking: -0.04, color: INK.sky, shadowKind: 'deep'};
const X = 1044;

/** «ángulo» se inclina sobre su extremo izquierdo y un arco de transportador mide el giro. */
const Angulo: React.FC<{right: number; y: number; at: number; to: number}> = ({right, y, at, to}) => {
  const frame = useCurrentFrame();
  if (frame < at || frame >= to) return null;
  const E = 5;
  const W = 262; // ancho de tinta aproximado de «ángulo» a 76 px
  const x = right - W;
  const tilt = (t: number) => -13 * inOutCubic(clamp((t - at - 3) / 8));
  const moving = (t: number) => t >= at - 0.5 && t < at + 12;
  const render = (t: number) => {
    const age = t - at;
    const e = outQuart(clamp(age / E));
    const deg = tilt(t);
    const arcR = 118;
    const rad = (Math.abs(deg) * Math.PI) / 180;
    const ex = arcR * Math.cos(rad);
    const ey = -arcR * Math.sin(rad);
    const arcOp = clamp((age - 3) / 3);
    return (
      <div style={{position: 'absolute', left: x, top: y}}>
        <svg width={200} height={90} style={{position: 'absolute', left: -4, top: -86, overflow: 'visible', opacity: arcOp, filter: 'drop-shadow(0 2px 4px rgba(6,16,40,0.45))'}}>
          <path d={`M ${4 + arcR} 86 A ${arcR} ${arcR} 0 0 0 ${4 + ex} ${86 + ey}`} fill="none" stroke={INK.sky} strokeWidth={3} strokeLinecap="round" />
          <line x1={4} y1={86} x2={4 + arcR + 18} y2={86} stroke="rgba(255,255,255,0.75)" strokeWidth={2} strokeDasharray="4 6" />
        </svg>
        <div
          style={{
            ...typeStyle(KEY),
            position: 'absolute',
            left: 0,
            top: 0,
            transformOrigin: '0% 84%',
            transform: `translate(0, -84%) translateY(${(1 - e) * 0.3 * KEY.size}px) rotate(${deg}deg)`,
            opacity: age < 0 ? 0 : clamp(age / 1.5 + 0.34),
          }}
        >
          ángulo
        </div>
      </div>
    );
  };
  return <Shutter render={render} moving={moving} />;
};

/** Barra de progreso que casi no avanza: «semanas» en lenguaje de interfaz BRAUD. */
const Wait: React.FC<{right: number; y: number; w: number; from: number; to: number}> = ({right, y, w, from, to}) => {
  const frame = useCurrentFrame();
  if (frame < from || frame >= to) return null;
  const grow = outCubic(clamp((frame - from) / 6));
  const crawl = 0.035 + 0.025 * clamp((frame - from - 6) / 30);
  const pulse = 0.55 + 0.45 * Math.abs(Math.sin((frame - from) * 0.19));
  const out = clamp((to - frame) / 3);
  return (
    <div style={{position: 'absolute', left: right - w, top: y, width: w, height: 12, opacity: out, transformOrigin: '100% 50%', transform: `scaleX(${grow})`}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: 6, background: 'rgba(255,255,255,0.6)', boxShadow: '0 3px 14px rgba(6,16,40,0.4)'}} />
      <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${crawl * 100}%`, borderRadius: 6, background: INK.sky}} />
      <div style={{position: 'absolute', left: `${crawl * 100}%`, top: 2, bottom: 2, width: 24, marginLeft: -4, borderRadius: 5, background: `rgba(169,205,255,${0.5 * pulse})`}} />
    </div>
  );
};

export const Scene02: React.FC = () => (
  <>
    <Stack from={wf(43)} to={wf(45)} x={X} align="right" spec={RAIL} exit="lift" exitFrames={3} lines={[line(900, [['Quieres', wf(43)]]), line(972, [['testear', wf(44)]])]} />
    <Stack from={wf(45)} to={wf(48)} x={X} align="right" spec={RAIL} exit="fade" exitFrames={2} lines={[line(900, [['un', wf(45)], ['nuevo', wf(46)]])]} />
    <Angulo right={X} y={996} at={wf(47)} to={wf(48)} />
    <Stack
      from={wf(48)}
      to={wf(51)}
      x={X}
      align="right"
      spec={RAIL}
      exit="fade"
      exitFrames={3}
      lines={[line(900, [['y', wf(48)], ['necesitas', wf(49)]]), line(996, [['semanas', wf(50), {spec: KEY, settleAmp: 1}]])]}
    />
    <Wait right={X} y={1022} w={276} from={wf(50) + 2} to={wf(51)} />
    <Stack
      from={wf(51)}
      to={444}
      x={X}
      align="right"
      spec={RAIL}
      exit="fade"
      exitFrames={3}
      lines={[line(900, [['para', wf(51)], ['ver', wf(52)]]), line(972, [['el', wf(53)], ['fruto', wf(54)]]), line(1044, [['de', wf(55)], ['eso', wf(56)]])]}
    />
  </>
);

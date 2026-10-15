import React from 'react';
import {useCurrentFrame} from 'remotion';
import curve from '../data/v8-selector-width.json';
import {clamp, FPS, lerp, outCubic, outQuart} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, TypeSpec, typeStyle} from '../lib/type';
import {wf} from '../lib/words';
import {line, Stack} from './Stack';

// ───────────── 04 · Sudadera y giro a la solución (610–782) ─────────────
// Relación «tu problema → la solución» con la ventana de selección V8 del motor
// (separación de tiradores medida, f230–300 a 59,94 fps). Gag de la sudadera (f691–739):
// blanco y negro y sin subtítulos por instrucción de Ale («más gag, pon blanco y negro,
// sin subtítulos»); el color vuelve con «Vengo a hablarte».

const RAIL: TypeSpec = {size: 60, weight: 680, tracking: -0.018, shadowKind: 'deep'};
const TERM: TypeSpec = {size: 84, weight: 780, tracking: -0.028, shadowKind: 'deep'};
const CX = 540;
const BOX_Y = 940; // centro vertical de la ventana (entre barbilla y estampado)

const SRC_FPS = curve.sourceFps;
const widthAt = (sourceFrame: number) => {
  if (sourceFrame <= 230 || sourceFrame >= 300) return 1;
  const i = Math.floor(sourceFrame) - 230;
  const p = sourceFrame - Math.floor(sourceFrame);
  return lerp(curve.width[i], curve.width[i + 1], p);
};

type Sel = {from: number; to: number; select?: number; closeStart?: number; oldText: string; newText?: string; newAt?: number[]; fullW: number};

/** Ventana de selección con tiradores: el texto se recorta (clipWidth), no se escala. */
const Selection: React.FC<Sel> = (s) => {
  const frame = useCurrentFrame();
  if (frame < s.from || frame >= s.to) return null;
  const H = TERM.size * 1.16;
  const knob = 10;
  const srcAt = (t: number) => (s.closeStart === undefined ? 0 : 230 + ((t - s.closeStart) / FPS) * SRC_FPS);
  const showNew = s.closeStart !== undefined && srcAt(frame) >= 258; // decisión discreta por fotograma presentado
  const moving = (t: number) =>
    (s.select !== undefined && t >= s.select - 0.5 && t < s.select + 7) || (s.closeStart !== undefined && srcAt(t) > 229 && srcAt(t) < 301) || t < s.from + 4;
  const render = (t: number) => {
    let w = s.fullW;
    let anchorLeft = false;
    if (s.select !== undefined) {
      // selección arrastrada de izquierda a derecha (diseñada, 6 f)
      const e = outCubic(clamp((t - s.select) / 6));
      w = s.fullW * e;
      anchorLeft = true;
    }
    if (s.closeStart !== undefined) w = s.fullW * widthAt(srcAt(t));
    const left = anchorLeft ? CX - s.fullW / 2 : CX - w / 2;
    const appear = outQuart(clamp((t - s.from) / 4));
    const out = clamp((s.to - t) / 3);
    const textNow = showNew ? s.newText ?? s.oldText : s.oldText;
    const words = textNow.split(' ');
    const newAt = s.newAt ?? [];
    return (
      <div style={{position: 'absolute', inset: 0, opacity: appear * out}}>
        <div style={{position: 'absolute', left, top: BOX_Y - H / 2, width: Math.max(2, w), height: H, background: 'rgba(169,205,255,0.30)', borderRadius: 3}} />
        <div style={{position: 'absolute', left, top: BOX_Y - H / 2 - 30, width: Math.max(2, w), height: H + 60, overflow: 'hidden'}}>
          <div style={{position: 'absolute', left: CX - left - s.fullW / 2, top: 30, width: s.fullW, height: H, display: 'flex', justifyContent: 'center', alignItems: 'center', columnGap: '0.24em', fontSize: TERM.size}}>
            {words.map((wd, k) => {
              const at = showNew ? newAt[k] ?? 0 : -1e9;
              const age = t - at;
              const e = outQuart(clamp(age / 5));
              return (
                <span key={k} style={{...typeStyle({...TERM, color: showNew ? INK.white : 'rgba(255,255,255,0.96)'}), display: 'inline-block', opacity: age < 0 ? 0 : clamp(age / 1.5 + 0.34), transform: `translateY(${(1 - e) * 0.26 * TERM.size}px)`}}>
                  {wd}
                </span>
              );
            })}
          </div>
        </div>
        {/* tiradores estilo selección de texto */}
        <div style={{position: 'absolute', left: left - 2, top: BOX_Y - H / 2 - knob * 1.6, width: 4, height: H + knob * 1.6, background: INK.sky, borderRadius: 2}} />
        <div style={{position: 'absolute', left: left - knob, top: BOX_Y - H / 2 - knob * 3.2, width: knob * 2, height: knob * 2, borderRadius: knob, background: INK.sky}} />
        <div style={{position: 'absolute', left: left + w - 2, top: BOX_Y - H / 2, width: 4, height: H + knob * 1.6, background: INK.sky, borderRadius: 2}} />
        <div style={{position: 'absolute', left: left + w - knob, top: BOX_Y + H / 2 + knob * 1.2, width: knob * 2, height: knob * 2, borderRadius: knob, background: INK.sky}} />
      </div>
    );
  };
  return <Shutter render={render} moving={moving} style={{filter: 'drop-shadow(0 4px 14px rgba(6,16,40,0.35))'}} />;
};

/** Aparte vertical descartado tras la instrucción de Ale (sin subtítulos en el gag). Se conserva como estudio. */
export const AsideDescartado: React.FC = () => {
  const frame = useCurrentFrame();
  const from = wf(89);
  const to = 729;
  if (frame < from || frame >= to) return null;
  const words: [string, number][] = [
    ['y', wf(89)],
    ['con', wf(90)],
    ['la', wf(91)],
    ['sudadera', wf(92)],
    ['de', wf(93)],
    ['este', wf(94)],
    ['tío.', wf(95)],
  ];
  const moving = (t: number) => words.some(([, at]) => t >= at - 0.5 && t < at + 5) || t >= to - 3.5;
  const render = (t: number) => {
    const out = clamp((to - t) / 3);
    return (
      <div style={{position: 'absolute', left: 96, top: 1330, transformOrigin: '0 0', transform: 'rotate(-90deg)', display: 'flex', columnGap: '0.26em', alignItems: 'baseline', opacity: out}}>
        {words.map(([w, at], k) => {
          const age = t - at;
          const e = outQuart(clamp(age / 5));
          const key = w === 'tío.';
          return (
            <span
              key={k}
              style={{
                ...typeStyle({...RAIL, size: 58, weight: key ? 820 : 640, color: key ? INK.sky : INK.white}),
                display: 'inline-block',
                opacity: age < 0 ? 0 : clamp(age / 1.5 + 0.34),
                transform: `translateX(${-(1 - e) * 26}px)`,
              }}
            >
              {w}
            </span>
          );
        })}
      </div>
    );
  };
  return <Shutter render={render} moving={moving} />;
};

const CLOSE = wf(100) - Math.round(((266 - 230) / SRC_FPS) * FPS); // la ventana cierra 0,6 s antes de «la»

export const Scene04: React.FC = () => (
  <>
    <Stack from={wf(77)} to={wf(84)} x={CX} align="center" spec={RAIL} exit="fade" exitFrames={3} lines={[line(852, [['No', wf(77)], ['vengo', wf(78)], ['a', wf(79)], ['hablarte', wf(80)], ['de', wf(81)]])]} />
    <Selection from={wf(82)} to={wf(84)} select={wf(83)} oldText="tu problema" fullW={560} />
    <Stack
      from={wf(84)}
      to={679}
      x={CX}
      align="center"
      spec={RAIL}
      exit="fade"
      exitFrames={3}
      lines={[line(900, [['ya', wf(84)], ['tienes', wf(85)], ['suficiente', wf(86)]]), line(976, [['con', wf(87)], ['eso', wf(88)]])]}
    />
    <Stack from={wf(96)} to={wf(100)} x={CX} align="center" spec={{...RAIL, size: 54, weight: 620}} exit="fade" exitFrames={2} lines={[line(846, [['Vengo', wf(96)], ['a', wf(97)], ['hablarte', wf(98)], ['de', wf(99)]])]} />
    <Selection from={wf(96)} to={782} closeStart={CLOSE} oldText="tu problema" newText="la solución" newAt={[wf(100), wf(101)]} fullW={560} />
  </>
);

import React from 'react';
import {useCurrentFrame} from 'remotion';
import {clamp, inCubic, outCubic, outQuart, settle} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {TypeSpec, typeStyle} from '../lib/type';

export type SWord = {text: string; at: number; spec?: Partial<TypeSpec>; font?: string; enter?: Enter; settleAmp?: number};
export type SLine = {words: SWord[]; y: number; x?: number; align?: 'left' | 'center' | 'right'; spec?: Partial<TypeSpec>; gap?: number};
type Enter = 'rise' | 'drop' | 'left' | 'right' | 'pop' | 'stamp' | 'fade' | 'none';
type Exit = 'cut' | 'fade' | 'lift' | 'sink' | 'left' | 'right';

export type StackProps = {
  lines: SLine[];
  from: number;
  to: number;
  x: number;
  align?: 'left' | 'center' | 'right';
  spec: TypeSpec;
  enter?: Enter;
  enterFrames?: number;
  exit?: Exit;
  exitFrames?: number;
  /** Transformación del bloque completo en el tiempo t (fotogramas). */
  block?: (t: number) => {x?: number; y?: number; rot?: number; scale?: number; opacity?: number; origin?: string};
  blockMoving?: (t: number) => boolean;
  /** Estado discreto por fotograma presentado (p. ej. apagado), no por submuestra. */
  styleAt?: (frame: number) => React.CSSProperties | undefined;
};

/**
 * Bloque de líneas con anclas fijas: cada línea tiene su línea base, cada palabra su
 * instante. La geometría completa se reserva desde el primer fotograma (las palabras
 * nuevas no recentran las anteriores). Entradas por un eje, obturador en movimiento.
 */
export const Stack: React.FC<StackProps> = (p) => {
  const frame = useCurrentFrame();
  if (frame < p.from || frame >= p.to) return null;
  const E = p.enterFrames ?? 5;
  const exitFrames = p.exit && p.exit !== 'cut' ? (p.exitFrames ?? 4) : 0;
  const exitStart = p.to - exitFrames;
  const all = p.lines.flatMap((l) => l.words);
  const moving = (t: number) =>
    all.some((w) => t >= w.at - 0.5 && t < w.at + E + (w.settleAmp ? 7 : 0)) ||
    (exitFrames > 0 && t >= exitStart - 0.5) ||
    (p.blockMoving ? p.blockMoving(t) : false);
  const discrete = p.styleAt?.(frame);

  const render = (t: number) => {
    const ex = exitFrames ? clamp((t - exitStart) / exitFrames) : 0;
    const exE = inCubic(ex);
    const b = p.block?.(t) ?? {};
    let ox = 0;
    let oy = 0;
    if (p.exit === 'lift') oy = -exE * 0.4 * p.spec.size;
    if (p.exit === 'sink') oy = exE * 0.5 * p.spec.size;
    if (p.exit === 'left') ox = -exE * 0.8 * p.spec.size;
    if (p.exit === 'right') ox = exE * 0.8 * p.spec.size;
    const exitOp = p.exit === 'fade' || p.exit === 'lift' || p.exit === 'sink' || p.exit === 'left' || p.exit === 'right' ? 1 - ex : 1;
    return (
      <div
        style={{
          position: 'absolute',
          inset: 0,
          transform: `translate(${(b.x ?? 0) + ox}px, ${(b.y ?? 0) + oy}px) rotate(${b.rot ?? 0}deg) scale(${b.scale ?? 1})`,
          transformOrigin: b.origin ?? `${p.x}px ${p.lines[0]?.y ?? 0}px`,
          opacity: exitOp * (b.opacity ?? 1),
          ...discrete,
        }}
      >
        {p.lines.map((ln, li) => {
          const align = ln.align ?? p.align ?? 'left';
          const lx = ln.x ?? p.x;
          const anchor = align === 'left' ? '0' : align === 'right' ? '-100%' : '-50%';
          const lspec = {...p.spec, ...ln.spec};
          return (
            <div
              key={li}
              style={{
                position: 'absolute',
                left: lx,
                top: ln.y,
                transform: `translate(${anchor}, -84%)`,
                display: 'flex',
                alignItems: 'baseline',
                columnGap: `${ln.gap ?? 0.24}em`,
                fontSize: lspec.size,
                whiteSpace: 'nowrap',
              }}
            >
              {ln.words.map((w, k) => {
                const spec = {...lspec, ...w.spec};
                const age = t - w.at;
                const kind = w.enter ?? p.enter ?? 'rise';
                const e = outQuart(clamp(age / E));
                const s = w.settleAmp ? settle(1.0, 6)(clamp(age / (E + 7))) : e;
                let tx = 0;
                let ty = 0;
                let sc = 1;
                let op = age < 0 ? 0 : clamp(age / 1.5 + 0.34);
                if (kind === 'rise') ty = (1 - s) * 0.34 * spec.size;
                if (kind === 'drop') ty = -(1 - s) * 0.34 * spec.size;
                if (kind === 'left') tx = -(1 - s) * 0.55 * spec.size;
                if (kind === 'right') tx = (1 - s) * 0.55 * spec.size;
                if (kind === 'pop') sc = 0.62 + 0.38 * s;
                if (kind === 'stamp') {
                  sc = 1 + (1 - outCubic(clamp(age / 3))) * 0.22;
                  op = age < 0 ? 0 : clamp(age / 1 + 0.5);
                }
                if (kind === 'fade') op = age < 0 ? 0 : outCubic(clamp(age / 6));
                if (kind === 'none') op = age < 0 ? 0 : 1;
                return (
                  <span
                    key={k}
                    style={{
                      ...typeStyle(spec),
                      ...(w.font ? {fontFamily: w.font} : {}),
                      display: 'inline-block',
                      opacity: op,
                      transform: `translate(${tx}px, ${ty}px) scale(${sc})`,
                      transformOrigin: '50% 75%',
                    }}
                  >
                    {w.text}
                  </span>
                );
              })}
            </div>
          );
        })}
      </div>
    );
  };
  return <Shutter render={render} moving={moving} />;
};

/** Utilidad: línea de palabras con sus instantes. */
export const line = (y: number, words: [string, number, Partial<SWord>?][], extra: Partial<SLine> = {}): SLine => ({
  y,
  words: words.map(([text, at, o]) => ({text, at, ...o})),
  ...extra,
});

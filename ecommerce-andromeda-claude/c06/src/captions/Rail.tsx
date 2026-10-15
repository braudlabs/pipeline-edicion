import {useT} from '../lib/time';
import React from 'react';

import {clamp, outCubic, outQuart, settle} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, TypeSpec, typeStyle} from '../lib/type';

export type RailWord = {text: string; at: number; key?: boolean; spec?: Partial<TypeSpec>};

export type RailProps = {
  words: RailWord[];
  from: number; // primer fotograma visible (normalmente el de la primera palabra)
  to: number; // fotograma exclusivo de salida
  x: number;
  y: number; // línea base aproximada del bloque (borde inferior de la caja)
  align?: 'center' | 'left' | 'right';
  spec: TypeSpec;
  keySpec?: Partial<TypeSpec>;
  enter?: 'rise' | 'left' | 'right' | 'pop' | 'none';
  exit?: 'cut' | 'fall' | 'lift' | 'fade';
  exitFrames?: number;
  gap?: number; // em
  maxWidth?: number; // si se define, permite varias líneas con ancla estable
  lineGap?: number;
};

const ENTER = 5;

/**
 * Rail de lectura: la geometría de la frase completa se reserva desde el primer
 * fotograma; cada palabra aparece con su sonido sin recentrar las anteriores.
 * Entrada por un eje (preferencia de Ale), obturador solo durante el movimiento.
 */
export const Rail: React.FC<RailProps> = (p) => {
  const frame = useT();
  if (frame < p.from || frame >= p.to) return null;
  const enter = p.enter ?? 'rise';
  const exitFrames = p.exitFrames ?? 4;
  const exitStart = p.to - exitFrames;
  const moving = (t: number) =>
    p.words.some((w) => t >= w.at - 0.5 && t < w.at + ENTER + (w.key ? 6 : 0)) || (p.exit !== 'cut' && t >= exitStart - 0.5);

  const render = (t: number) => {
    const ex = p.exit && p.exit !== 'cut' ? clamp((t - exitStart) / exitFrames) : 0;
    const exE = outCubic(ex);
    const exitTransform =
      p.exit === 'fall' ? `translateY(${exE * 0.45 * p.spec.size}px)` : p.exit === 'lift' ? `translateY(${-exE * 0.35 * p.spec.size}px)` : '';
    const exitOpacity = p.exit === 'cut' ? 1 : 1 - ex;
    const anchor = p.align === 'left' ? '0' : p.align === 'right' ? '-100%' : '-50%';
    return (
      <div
        style={{
          position: 'absolute',
          left: p.x,
          top: p.y,
          transform: `translate(${anchor}, -100%) ${exitTransform}`,
          opacity: exitOpacity,
          display: 'flex',
          flexWrap: p.maxWidth ? 'wrap' : 'nowrap',
          maxWidth: p.maxWidth,
          justifyContent: p.align === 'left' ? 'flex-start' : p.align === 'right' ? 'flex-end' : 'center',
          alignItems: 'baseline',
          columnGap: `${p.gap ?? 0.24}em`,
          rowGap: p.lineGap ?? 0,
          fontSize: p.spec.size,
        }}
      >
        {p.words.map((w, k) => {
          const age = t - w.at;
          const visible = age >= 0;
          const e = outQuart(clamp(age / ENTER));
          const spec = {...p.spec, ...(w.key ? p.keySpec : {}), ...w.spec};
          let tx = 0;
          let ty = 0;
          let sc = 1;
          if (enter === 'rise') ty = (1 - e) * 0.32 * spec.size;
          if (enter === 'left') tx = -(1 - e) * 0.5 * spec.size;
          if (enter === 'right') tx = (1 - e) * 0.5 * spec.size;
          if (enter === 'pop') sc = 0.7 + 0.3 * e;
          if (w.key) sc *= 0.86 + 0.14 * settle(1.0, 6)(clamp(age / (ENTER + 6)));
          const op = visible ? clamp(age / 1.5 + 0.34) : 0;
          return (
            <span
              key={k}
              style={{
                ...typeStyle(spec),
                display: 'inline-block',
                opacity: op,
                transform: `translate(${tx}px, ${ty}px) scale(${sc})`,
                transformOrigin: '50% 80%',
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    );
  };
  return <Shutter render={render} moving={moving} />;
};

export const railWords = (items: [string, number, boolean?][]): RailWord[] =>
  items.map(([text, at, key]) => ({text, at, key: !!key}));

export const keyColor = {color: INK.sky};

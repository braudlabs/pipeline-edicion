import {useT} from '../lib/time';
import React from 'react';

import {clamp, FPS, inCubic, noise1, outCubic, outQuart, settle} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, typeStyle, TypeSpec} from '../lib/type';
import {HOOK_WORDS, wf} from '../lib/words';
import {Behind} from './Masked';
import {Rail} from './Rail';

// ───────────────────────── Hook · 0–130 ─────────────────────────
// El azul (Andrómeda) susurra; el protagonista mira con miedo. El acercamiento final al
// miedo (f116–124) pertenece a la imagen: el texto sale antes de que llegue.

const HOOK = {sceneFrom: 0, count: 130, dir: 'hook-holdout'};

type BandWord = {text: string; at: number; key?: boolean};
type BandGroup = {words: BandWord[]; from: number; to: number; size: number; width?: number};

/** Línea grande detrás de las cabezas: relleno ocluido + contorno delante. */
const BandLine: React.FC<{g: BandGroup; baseline: number; color?: string; keyColor?: string; outline?: number; strokeColor?: string; fillShadow?: boolean}> = ({
  g,
  baseline,
  color = INK.white,
  keyColor = INK.sky,
  outline = 0.55,
  strokeColor = 'rgba(255,255,255,0.95)',
  fillShadow = false,
}) => {
  const frame = useT();
  if (frame < g.from || frame >= g.to) return null;
  const E = 6;
  const exitFrames = 3;
  const moving = (t: number) => g.words.some((w) => t >= w.at - 0.5 && t < w.at + E) || t >= g.to - exitFrames - 0.5;
  const spec: TypeSpec = {size: g.size, weight: 820, width: g.width ?? 100, tracking: -0.045, shadowKind: 'none', lineHeight: 0.9};
  const line = (t: number, mode: 'fill' | 'stroke') => {
    const ex = clamp((t - (g.to - exitFrames)) / exitFrames);
    return (
      <div
        style={{
          position: 'absolute',
          left: 540,
          top: baseline,
          transform: `translate(-50%, -100%) translateY(${inCubic(ex) * 0.55 * g.size}px)`,
          display: 'flex',
          alignItems: 'baseline',
          columnGap: '0.22em',
          fontSize: g.size,
        }}
      >
        {g.words.map((w, k) => {
          const age = t - w.at;
          const e = outQuart(clamp(age / E));
          const s = settle(0.9, 6.5)(clamp(age / (E + 5)));
          const fill = w.key ? keyColor : color;
          return (
            <span
              key={k}
              style={{
                ...typeStyle({...spec, color: mode === 'fill' ? fill : 'transparent', shadowKind: mode === 'fill' && fillShadow ? 'soft' : 'none'}),
                display: 'inline-block',
                opacity: age < 0 ? 0 : mode === 'stroke' ? outline * e * e * (1 - ex) : 1,
                WebkitTextStroke: mode === 'stroke' ? `${Math.max(1.6, g.size / 62)}px ${strokeColor}` : undefined,
                transform: `translateY(${(1 - (age < E ? e : s)) * 0.62 * g.size}px)`,
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    );
  };
  return (
    <>
      <Behind dir={HOOK.dir} sceneFrom={HOOK.sceneFrom} count={HOOK.count}>
        <Shutter render={(t) => line(t, 'fill')} moving={moving} />
      </Behind>
      <Shutter render={(t) => line(t, 'stroke')} moving={moving} />
    </>
  );
};

/** Segunda voz: el susurro nativo del azul, pequeño, en azul claro, pegado a él. */
export const Whisper: React.FC<{x: number; y: number; size?: number; lines: {text: string; at: number}[][]; from: number; to: number}> = ({
  x,
  y,
  size = 46,
  lines,
  from,
  to,
}) => {
  const frame = useT();
  if (frame < from || frame >= to) return null;
  const fadeOut = clamp((to - frame) / 4);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: 'translateY(-100%)', opacity: fadeOut}}>
      {lines.map((ln, li) => (
        <div key={li} style={{display: 'flex', columnGap: '0.28em', lineHeight: 1.02}}>
          {ln.map((w, k) => {
            const age = frame - w.at;
            if (age < 0) return <span key={k} style={{...typeStyle({size, weight: 560, color: INK.sky}), opacity: 0}}>{w.text}</span>;
            const e = outCubic(clamp(age / 6));
            return (
              <span key={k} style={{display: 'inline-flex'}}>
                {Array.from(w.text).map((ch, ci) => {
                  const j = noise1(frame * 0.55 + ci * 1.7 + li * 9 + k * 3, 3);
                  return (
                    <span
                      key={ci}
                      style={{
                        ...typeStyle({size, weight: 560, tracking: 0.01 + (1 - e) * 0.12, color: INK.sky, shadowKind: 'tight'}),
                        display: 'inline-block',
                        opacity: e * (0.86 + 0.14 * noise1(frame * 0.8 + ci, 7)),
                        transform: `translate(${(1 - e) * -10}px, ${j * 1.6}px)`,
                        filter: e < 1 ? `blur(${(1 - e) * 3}px)` : undefined,
                      }}
                    >
                      {ch}
                    </span>
                  );
                })}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};

const hf = (k: number) => Math.floor(HOOK_WORDS[k].start * FPS + 1e-6);

const whisperA = () => (
  <>
    <Whisper
      x={58}
      y={1004}
      from={hf(0)}
      to={84}
      lines={[[{text: 'más', at: hf(0)}], [{text: 'anuncios.', at: hf(1)}]]}
    />
    <Whisper x={58} y={1004} from={hf(2)} to={130} size={58} lines={[[{text: 'más.', at: hf(2)}]]} />
  </>
);

// Variante A · banda alta detrás de las cabezas (lectura V5), frase a frase.
export const HookA: React.FC = () => {
  const groups: BandGroup[] = [
    {words: [{text: 'Si', at: wf(0)}, {text: 'eres', at: wf(1)}, {text: 'dueño', at: wf(2)}], from: wf(0), to: wf(3), size: 136},
    {words: [{text: 'de', at: wf(3)}, {text: 'un', at: wf(4)}, {text: 'ecommerce', at: wf(5), key: true}], from: wf(3), to: wf(6), size: 120},
    {words: [{text: 'ya', at: wf(6)}, {text: 'sabes', at: wf(7)}, {text: 'que', at: wf(8)}, {text: 'con', at: wf(9)}], from: wf(6), to: wf(10), size: 112},
    {words: [{text: 'Andrómeda', at: wf(10), key: true}], from: wf(10), to: wf(11), size: 190},
    {words: [{text: 'necesitas', at: wf(11)}], from: wf(11), to: wf(12), size: 176},
    {words: [{text: 'anuncios', at: wf(12)}, {text: 'nuevos', at: wf(13)}], from: wf(12), to: wf(14), size: 118},
    {words: [{text: 'cada', at: wf(14)}, {text: 'semana', at: wf(15), key: true}], from: wf(14), to: 121, size: 150},
  ];
  return (
    <>
      {groups.map((g, i) => (
        <BandLine key={i} g={g} baseline={492} />
      ))}
      {whisperA()}
    </>
  );
};

// Variante B · rail en la franja del pecho + «Andrómeda» como único héroe ocluido.
export const HookB: React.FC = () => {
  const rail: TypeSpec = {size: 62, weight: 680, tracking: -0.02, shadowKind: 'soft'};
  const R = (words: [string, number, boolean?][], from: number, to: number, spec = rail) => (
    <Rail
      words={words.map(([text, at, key]) => ({text, at, key: !!key}))}
      from={from}
      to={to}
      x={540}
      y={1052}
      spec={spec}
      keySpec={{color: INK.sky}}
      exit="cut"
    />
  );
  const andro: BandGroup = {words: [{text: 'Andrómeda', at: wf(10), key: true}], from: wf(10), to: wf(12), size: 200};
  return (
    <>
      {R([['Si', wf(0)], ['eres', wf(1)], ['dueño', wf(2)]], wf(0), wf(3))}
      {R([['de', wf(3)], ['un', wf(4)], ['ecommerce', wf(5), true]], wf(3), wf(6))}
      {R([['ya', wf(6)], ['sabes', wf(7)], ['que', wf(8)], ['con', wf(9)]], wf(6), wf(10))}
      <BandLine g={andro} baseline={492} />
      {R([['necesitas', wf(11)], ['anuncios', wf(12)], ['nuevos', wf(13)]], wf(11), wf(14))}
      {R([['cada', wf(14)], ['semana', wf(15), true]], wf(14), 121, {...rail, size: 96, weight: 800, tracking: -0.035})}
      {whisperA()}
    </>
  );
};

// Variante A2 · misma banda, relleno azul BRAUD detrás y contorno blanco delante.
export const HookA2: React.FC = () => {
  const groups: BandGroup[] = [
    {words: [{text: 'Si', at: wf(0)}, {text: 'eres', at: wf(1)}, {text: 'dueño', at: wf(2)}], from: wf(0), to: wf(3), size: 150},
    {words: [{text: 'de', at: wf(3)}, {text: 'un', at: wf(4)}, {text: 'ecommerce', at: wf(5), key: true}], from: wf(3), to: wf(6), size: 124},
    {words: [{text: 'ya', at: wf(6)}, {text: 'sabes', at: wf(7)}, {text: 'que', at: wf(8)}, {text: 'con', at: wf(9)}], from: wf(6), to: wf(10), size: 120},
    {words: [{text: 'Andrómeda', at: wf(10), key: true}], from: wf(10), to: wf(11), size: 196},
    {words: [{text: 'necesitas', at: wf(11)}], from: wf(11), to: wf(12), size: 190},
    {words: [{text: 'anuncios', at: wf(12)}, {text: 'nuevos', at: wf(13)}], from: wf(12), to: wf(14), size: 124},
    {words: [{text: 'cada', at: wf(14)}, {text: 'semana', at: wf(15), key: true}], from: wf(14), to: 121, size: 158},
  ];
  return (
    <>
      {groups.map((g, i) => (
        <BandLine key={i} g={g} baseline={468} color={INK.azul} keyColor={INK.azulDeep} outline={0.95} fillShadow />
      ))}
      {whisperA()}
    </>
  );
};

// ───────── Hook definitivo C01 ─────────
// Banda detrás de las cabezas (A2) con jerarquía contexto pequeño / héroe grande, que
// alterna construcciones: línea, contexto+héroe, línea, nombre, contexto+héroe, remate.
// El remate «cada semana» no sale: el acercamiento de la imagen lo tapa por oclusión.
const Context: React.FC<{words: BandWord[]; from: number; to: number; y: number; size?: number}> = ({words, from, to, y, size = 60}) => {
  const frame = useT();
  if (frame < from || frame >= to) return null;
  const E = 5;
  const exitFrames = 3;
  const moving = (t: number) => words.some((w) => t >= w.at - 0.5 && t < w.at + E) || t >= to - exitFrames - 0.5;
  const render = (t: number) => {
    const ex = clamp((t - (to - exitFrames)) / exitFrames);
    return (
      <div style={{position: 'absolute', left: 540, top: y, transform: `translate(-50%, -84%) translateY(${-inCubic(ex) * 0.4 * size}px)`, opacity: 1 - ex, display: 'flex', columnGap: '0.24em', fontSize: size}}>
        {words.map((w, k) => {
          const age = t - w.at;
          const e = outQuart(clamp(age / E));
          return (
            <span key={k} style={{...typeStyle({size, weight: 660, tracking: -0.015, shadowKind: 'deep'}), display: 'inline-block', opacity: age < 0 ? 0 : clamp(age / 1.5 + 0.34), transform: `translateY(${-(1 - e) * 0.3 * size}px)`}}>
              {w.text}
            </span>
          );
        })}
      </div>
    );
  };
  return <Shutter render={render} moving={moving} />;
};

export const HookFinal: React.FC = () => {
  const blue = {color: INK.azul, keyColor: INK.azul, outline: 0.95, fillShadow: true};
  const groups: (BandGroup & {baseline: number})[] = [
    {words: [{text: 'Si', at: wf(0)}, {text: 'eres', at: wf(1)}, {text: 'dueño', at: wf(2)}], from: wf(0), to: wf(3), size: 150, baseline: 446},
    {words: [{text: 'ecommerce', at: wf(5)}], from: wf(3), to: wf(6), size: 178, baseline: 450},
    {words: [{text: 'ya', at: wf(6)}, {text: 'sabes', at: wf(7)}, {text: 'que', at: wf(8)}, {text: 'con', at: wf(9)}], from: wf(6), to: wf(10), size: 122, baseline: 440},
    {words: [{text: 'Andrómeda', at: wf(10)}], from: wf(10), to: wf(11), size: 208, baseline: 456},
    {words: [{text: 'nuevos', at: wf(13)}], from: wf(11), to: wf(14), size: 214, baseline: 456},
    {words: [{text: 'cada', at: wf(14)}, {text: 'semana', at: wf(15)}], from: wf(14), to: 130, size: 156, baseline: 446},
  ];
  return (
    <>
      {groups.map((g, i) => (
        <BandLine key={i} g={g} baseline={g.baseline} {...blue} />
      ))}
      <Context words={[{text: 'de', at: wf(3)}, {text: 'un', at: wf(4)}]} from={wf(3)} to={wf(6)} y={262} />
      <Context words={[{text: 'necesitas', at: wf(11)}, {text: 'anuncios', at: wf(12)}]} from={wf(11)} to={wf(14)} y={262} />
      <Whisper x={58} y={1004} from={hf(0)} to={84} size={50} lines={[[{text: 'más', at: hf(0)}], [{text: 'anuncios.', at: hf(1)}]]} />
      <Whisper x={58} y={1004} from={hf(2)} to={130} size={66} lines={[[{text: 'más.', at: hf(2)}]]} />
    </>
  );
};

export const HookVariant: React.FC<{variant: string}> = ({variant}) =>
  variant === 'B' ? <HookB /> : variant === 'A2' ? <HookA2 /> : variant === 'F' ? <HookFinal /> : <HookA />;

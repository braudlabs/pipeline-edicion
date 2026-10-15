import React from 'react';
import {Audio, Sequence, interpolate, staticFile} from 'remotion';
import {FPS, at, endOf, f} from './lib/motion';

// Voz (1,08×, «publicar» corregido) + pista de música montada por tools/sound.py (frenazo de cinta,
// tramo filtrado, compás en «Esto es BRAUD Studio», ducking) + efectos sintetizados (sfx-*) y los de
// El Sistema (click, typing). Licencia de la tech house por confirmar antes de la versión final.
type Fx = {file: string; t: number; vol?: number; dur?: number};
const A = (b: number, w: string, n = 0) => at(b, w, n);

export const effects = (): Fx[] => {
  const typing0 = A(4, 'cuentas') - 0.05, typing1 = A(4, 'Escrita') - 0.1;
  const sent = A(4, 'ChatGPT') + 0.06;
  return [
    // bloque 1
    {file: 'sfx-impact', t: 0.0, vol: 0.45}, {file: 'sfx-whoosh-long', t: 0.0, vol: 0.35},
    {file: 'sfx-shimmer', t: A(1, 'Andrómeda') + 0.05, vol: 0.3},
    {file: 'sfx-whoosh-fast', t: A(1, 'Meta') - 0.16, vol: 0.4}, {file: 'sfx-thump', t: A(1, 'Meta'), vol: 0.55},
    {file: 'sfx-tick', t: A(1, 'pide') + 0.04, vol: 0.4}, {file: 'sfx-pop', t: A(1, 'creatividad'), vol: 0.45}, {file: 'sfx-pop', t: A(1, 'nueva'), vol: 0.45},
    {file: 'sfx-blips', t: A(1, 'cada'), vol: 0.4}, {file: 'sfx-blips', t: A(1, 'cada') + 0.45, vol: 0.45},
    {file: 'sfx-thump', t: A(1, 'semana'), vol: 0.6},
    {file: 'sfx-whoosh-down', t: 3.9, vol: 0.45},
    {file: 'sfx-clock', t: 4.45, vol: 0.5}, {file: 'sfx-clock', t: 5.05, vol: 0.5}, {file: 'sfx-clock', t: 5.65, vol: 0.5},
    {file: 'sfx-impact', t: 6.2, vol: 0.6}, {file: 'sfx-whoosh-fast', t: 6.12, vol: 0.45},
    {file: 'sfx-whoosh-long', t: 6.35, vol: 0.3},
    {file: 'sfx-blips', t: A(1, 'parecen'), vol: 0.4},
    {file: 'sfx-thump', t: A(1, 'más'), vol: 0.5},
    {file: 'sfx-riser', t: 9.22 - 2.8, vol: 0.5},
    // bloque 2
    {file: 'sfx-impact', t: 9.22, vol: 0.75}, {file: 'sfx-whoosh-down', t: 9.2, vol: 0.4},
    {file: 'sfx-whoosh-fast', t: endOf(2, 'Studio') - 0.05, vol: 0.45},
    {file: 'sfx-whoosh-long', t: A(2, 'cerebro') + 0.02, vol: 0.35},
    {file: 'sfx-shimmer', t: A(2, 'idea'), vol: 0.45}, {file: 'sfx-pop', t: A(2, 'idea') + 0.02, vol: 0.5},
    {file: 'sfx-whoosh-fast', t: A(2, 'convierte') - 0.05, vol: 0.45},
    ...[0, 1, 2, 3, 4].map((i) => ({file: 'sfx-tick', t: A(2, 'convierte') + 0.05 + i * 0.07, vol: 0.35})),
    {file: 'sfx-thump', t: A(2, 'listo'), vol: 0.45},
    {file: 'sfx-pop', t: A(2, 'publicar'), vol: 0.55}, {file: 'sfx-shimmer', t: A(2, 'publicar') + 0.03, vol: 0.35},
    // bloque 3
    {file: 'sfx-whoosh-long', t: A(3, 'Así') - 0.1, vol: 0.55}, {file: 'sfx-impact', t: A(3, 'Así') + 0.32, vol: 0.5},
    // bloque 4
    {file: 'typing', t: typing0, vol: 0.45, dur: typing1 - typing0},
    {file: 'click-soft', t: A(4, 'voz') - 0.12, vol: 0.55}, {file: 'sfx-shimmer', t: A(4, 'voz') - 0.08, vol: 0.2},
    {file: 'click-soft', t: sent, vol: 0.6}, {file: 'sfx-whoosh-fast', t: sent + 0.02, vol: 0.5}, {file: 'sfx-pop', t: sent + 0.38, vol: 0.4},
    // bloque 5
    {file: 'sfx-whoosh-fast', t: A(5, 'marca') - 0.12, vol: 0.4}, {file: 'sfx-whoosh-fast', t: A(5, 'productos') - 0.08, vol: 0.4},
    {file: 'sfx-whoosh-fast', t: A(5, 'quién') - 0.12, vol: 0.4}, {file: 'sfx-whoosh-fast', t: A(5, 'quién') + 0.32, vol: 0.35},
    {file: 'sfx-whoosh-long', t: A(5, 'No') - 0.05, vol: 0.45}, {file: 'sfx-impact', t: A(5, 'cero') + 0.3, vol: 0.55},
    {file: 'sfx-shimmer', t: A(5, 'cero') + 0.32, vol: 0.35},
    {file: 'sfx-blips', t: A(5, 'Empieza'), vol: 0.35},
  ];
};

export const Sound: React.FC<{duration: number}> = ({duration}) => {
  const end = f(duration);
  return (
    <>
      <Audio src={staticFile('audio/locucion.wav')} volume={1} />
      <Audio src={staticFile('audio/music-stem.wav')}
        volume={(fr) => 0.7 * interpolate(fr, [end - f(0.8), end], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} /> {/* −3 dB más (V03) */}
      {effects().filter((x) => x.t < duration).map((x, i) => (
        <Sequence key={i} from={Math.max(0, Math.round(x.t * FPS))} durationInFrames={x.dur ? Math.round(x.dur * FPS) : undefined}>
          <Audio src={staticFile(`audio/${x.file}.${x.file.startsWith('sfx-') ? 'wav' : 'mp3'}`)} volume={x.vol ?? 0.4} />
        </Sequence>
      ))}
    </>
  );
};

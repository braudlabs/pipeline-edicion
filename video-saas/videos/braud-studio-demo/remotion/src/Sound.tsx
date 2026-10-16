import React from 'react';
import {Audio, Sequence, interpolate, staticFile} from 'remotion';
import {FPS, at, endOf, f} from './lib/motion';

// Voz (1,08×, «publicar» corregido) + pista de música montada por tools/sound.py (frenazo de cinta,
// tramo filtrado, compás en «Esto es BRAUD Studio», ducking) + efectos sintetizados (sfx-*) y los de
// El Sistema (click, typing). Licencia de la tech house por confirmar antes de la versión final.
type Fx = {file: string; t: number; vol?: number; dur?: number};
const A = (b: number, w: string, n = 0) => at(b, w, n);

export const effects = (): Fx[] => {
  // V04: sonido sobrio. Whoosh suave en cada movimiento, ticks en el tramo lento, clics y tecleo
  // reales y un único golpe cuando aparece Studio.
  const typing0 = A(4, 'cuentas') - 0.05, typing1 = A(4, 'Escrita') - 0.15;
  const sent = A(4, 'ChatGPT') + 0.06;
  return [
    {file: 'sfx-whoosh-fast', t: 0.8, vol: 0.18},
    {file: 'sfx-whoosh-long', t: A(1, 'cada') - 0.1, vol: 0.28},
    {file: 'sfx-whoosh-down', t: 3.85, vol: 0.28},
    {file: 'sfx-clock', t: 4.45, vol: 0.32}, {file: 'sfx-clock', t: 5.05, vol: 0.32}, {file: 'sfx-clock', t: 5.65, vol: 0.32},
    {file: 'sfx-whoosh-fast', t: 6.12, vol: 0.3},
    {file: 'sfx-tick', t: A(1, 'parecen'), vol: 0.22},
    {file: 'sfx-whoosh-long', t: 8.55, vol: 0.26},
    {file: 'sfx-impact', t: 9.22, vol: 0.32},
    {file: 'click-soft', t: A(2, 'idea') + 0.02, vol: 0.45},
    {file: 'sfx-whoosh-fast', t: A(2, 'convierte') + 0.1, vol: 0.28},
    {file: 'sfx-whoosh-long', t: A(3, 'Así') - 0.2, vol: 0.3},
    {file: 'sfx-whoosh-fast', t: A(3, 'Así') + 0.66, vol: 0.26},
    {file: 'typing', t: typing0, vol: 0.4, dur: typing1 - typing0},
    {file: 'click-soft', t: A(4, 'voz') - 0.12, vol: 0.5}, {file: 'click-soft', t: A(4, 'Como') + 0.02, vol: 0.42}, // «Dictar» y «Terminar»
    {file: 'click-soft', t: sent, vol: 0.55}, {file: 'sfx-whoosh-fast', t: sent + 0.05, vol: 0.24},
    {file: 'sfx-whoosh-fast', t: A(5, 'productos') - 0.12, vol: 0.2}, {file: 'sfx-whoosh-fast', t: A(5, 'quién') - 0.12, vol: 0.2},
    {file: 'sfx-whoosh-long', t: A(5, 'No') - 0.05, vol: 0.24},
    {file: 'sfx-tick', t: A(5, 'Empieza', 1) + 0.06, vol: 0.16},
    // V05 · bloques 6–13: un whoosh suave por cambio de módulo, clics reales y un golpe en «Pero aquí no se acaba».
    {file: 'sfx-whoosh-fast', t: A(6, 'Aterriza') + 0.1, vol: 0.2}, {file: 'sfx-whoosh-fast', t: A(6, 'Y', 1) + 0.1, vol: 0.18},
    {file: 'sfx-whoosh-fast', t: A(7, 'Escribe'), vol: 0.2}, {file: 'sfx-whoosh-fast', t: A(7, 'Y') + 0.08, vol: 0.18},
    {file: 'sfx-whoosh-long', t: A(7, 'te') - 0.05, vol: 0.2},
    {file: 'sfx-whoosh-fast', t: A(8, 'Propone') + 0.05, vol: 0.2}, {file: 'sfx-whoosh-fast', t: A(8, 'mantiene'), vol: 0.18},
    {file: 'sfx-whoosh-fast', t: A(9, 'Convierte'), vol: 0.2}, {file: 'sfx-whoosh-fast', t: A(9, 'Escribe'), vol: 0.18},
    {file: 'typing', t: A(9, 'Escribe') + 0.05, vol: 0.28, dur: 0.85},
    {file: 'click-soft', t: A(9, 'te') - 0.06, vol: 0.45}, {file: 'click-soft', t: A(9, 'y'), vol: 0.5},
    {file: 'sfx-whoosh-long', t: A(10, 'Y', 0) - 0.1, vol: 0.26},
    {file: 'sfx-whoosh-fast', t: A(10, 'Con', 0), vol: 0.22}, {file: 'sfx-whoosh-fast', t: A(10, 'escena'), vol: 0.2},
    {file: 'sfx-whoosh-fast', t: A(10, 'plano'), vol: 0.2}, {file: 'sfx-whoosh-fast', t: A(10, 'con', 1), vol: 0.2},
    {file: 'sfx-whoosh-long', t: A(10, 'Tus') - 0.05, vol: 0.22}, {file: 'sfx-tick', t: A(10, 'más', 0) - 0.05, vol: 0.16},
    {file: 'sfx-whoosh-fast', t: A(10, 'Y', 2), vol: 0.2},
    {file: 'sfx-whoosh-fast', t: A(11, 'Te'), vol: 0.2}, {file: 'sfx-whoosh-fast', t: A(11, 'Y') + 0.05, vol: 0.2},
    {file: 'sfx-whoosh-fast', t: A(11, 'Listo') - 0.05, vol: 0.2}, {file: 'sfx-whoosh-fast', t: A(12, 'Tú') + 0.08, vol: 0.18},
    {file: 'click-soft', t: A(12, 'sí') - 0.16, vol: 0.55},
    {file: 'sfx-impact', t: A(13, 'Pero') - 0.02, vol: 0.3},
    // V06 · bloques 14–21
    {file: 'sfx-whoosh-fast', t: A(14, 'agente') + 0.1, vol: 0.2}, {file: 'sfx-whoosh-long', t: A(14, 'Lee') - 0.05, vol: 0.16},
    {file: 'sfx-whoosh-fast', t: A(14, 'interpreta') - 0.1, vol: 0.2}, {file: 'sfx-whoosh-fast', t: A(15, 'Este') - 0.15, vol: 0.2},
    {file: 'click-soft', t: A(16, 'botón') - 0.02, vol: 0.55}, {file: 'sfx-whoosh-fast', t: A(16, 'Y') + 0.02, vol: 0.18},
    {file: 'sfx-whoosh-fast', t: A(16, 'sube') - 0.12, vol: 0.2}, {file: 'sfx-tick', t: A(16, 'cuenta'), vol: 0.16},
    {file: 'sfx-whoosh-long', t: A(17, 'Datos') - 0.1, vol: 0.24}, {file: 'sfx-tick', t: A(17, 'Hipótesis'), vol: 0.14},
    {file: 'sfx-tick', t: A(17, 'Siguiente'), vol: 0.14},
    {file: 'sfx-whoosh-fast', t: A(18, 'Todo'), vol: 0.2}, {file: 'sfx-whoosh-fast', t: A(18, 'personajes') - 0.15, vol: 0.16},
    {file: 'sfx-whoosh-fast', t: A(18, 'clips') - 0.15, vol: 0.16}, {file: 'sfx-whoosh-fast', t: A(18, 'aprendido') - 0.1, vol: 0.16},
    {file: 'sfx-whoosh-long', t: A(18, 'Founders') - 0.1, vol: 0.2},
    {file: 'sfx-whoosh-long', t: A(19, 'Tú') - 0.1, vol: 0.22}, {file: 'sfx-whoosh-fast', t: A(20, 'No') - 0.05, vol: 0.2},
    {file: 'sfx-impact', t: A(21, 'BRAUD') - 0.02, vol: 0.32},
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

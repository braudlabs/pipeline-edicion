import React from 'react';
import {useCurrentFrame} from 'remotion';
import {FPS} from './motion';

/**
 * Motion blur de obturador (no gaussiano), adaptado del de Andrómeda C03: repite la capa en
 * `samples` instantes dentro del ángulo de obturación y acumula con plus-lighter.
 * Si la capa no se mueve en ese intervalo, se dibuja una sola vez.
 * `render(t)` recibe el tiempo en segundos de la submuestra.
 */
export const Shutter: React.FC<{
  render: (t: number) => React.ReactNode;
  moving: (t: number) => boolean;
  samples?: number;
  angle?: number;
}> = ({render, moving, samples = 8, angle = 180}) => {
  const t = useCurrentFrame() / FPS;
  const span = angle / 360 / FPS;
  const n = Number(process.env.REMOTION_SAMPLES ?? samples);
  if (n <= 1 || !moving(t)) return <div style={{position: 'absolute', inset: 0}}>{render(t)}</div>;
  return (
    <div style={{position: 'absolute', inset: 0, isolation: 'isolate'}}>
      {Array.from({length: n}, (_, k) => (
        <div key={k} style={{position: 'absolute', inset: 0, opacity: 1 / n, mixBlendMode: 'plus-lighter'}}>
          {render(t + ((k + 0.5) / n - 0.5) * span)}
        </div>
      ))}
    </div>
  );
};

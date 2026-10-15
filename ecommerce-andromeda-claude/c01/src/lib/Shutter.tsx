import React from 'react';
import {useCurrentFrame} from 'remotion';

/**
 * Obturador temporal (no desenfoque gaussiano): repite la capa en `samples` instantes
 * repartidos en el ángulo de obturación y acumula con plus-lighter dentro de un grupo
 * aislado. Si la capa no se mueve en el intervalo, se dibuja una sola vez.
 *
 * `render(t)` recibe el tiempo (fotogramas fraccionarios) de la submuestra y debe
 * devolver la geometría de ese instante. El contenido discreto (qué texto se lee) se
 * decide fuera con el fotograma presentado, para no mezclar cadenas entre muestras.
 */
export const Shutter: React.FC<{
  render: (t: number) => React.ReactNode;
  moving: (t: number) => boolean;
  samples?: number;
  angle?: number; // grados; 180 = medio fotograma
  style?: React.CSSProperties;
}> = ({render, moving, samples = 8, angle = 180, style}) => {
  const frame = useCurrentFrame();
  const span = angle / 360;
  const blur = moving(frame) || moving(frame - span / 2) || moving(frame + span / 2);
  if (!blur) return <div style={{position: 'absolute', inset: 0, ...style}}>{render(frame)}</div>;
  const items = Array.from({length: samples}, (_, k) => frame + ((k + 0.5) / samples - 0.5) * span);
  return (
    <div style={{position: 'absolute', inset: 0, isolation: 'isolate', ...style}}>
      {items.map((t, k) => (
        <div key={k} style={{position: 'absolute', inset: 0, opacity: 1 / samples, mixBlendMode: 'plus-lighter'}}>
          {render(t)}
        </div>
      ))}
    </div>
  );
};

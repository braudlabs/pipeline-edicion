import {useT} from '../lib/time';
import React from 'react';

import {clamp, outQuart} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {SF} from '../lib/Fonts';
import {SAFE, widthAt100} from './Big';

// ───────── Etiqueta de handle (solo en 10 · fundadores) ─────────
// Pastilla pequeña tipo etiqueta de perfil, distinta de los subtítulos: el narrador no dice
// el handle. Entra en 5 fotogramas por un solo eje (desde la izquierda), se sostiene más de
// 1 s y sale con un fundido corto. Nunca sobre la cara.
const IN = 5;
const OUT = 4;

export const Tag: React.FC<{text: string; x: number; y: number; from: number; to: number}> = ({text, x, y, from, to}) => {
  const frame = useT();
  if (frame < from || frame >= to) return null;
  // Margen seguro de Meta: la pastilla entera (texto + relleno) dentro de x≈100–980.
  const half = (widthAt100(text, 620, -0.01) * 38) / 100 / 2 + 22;
  const cx = Math.min(SAFE.right - half, Math.max(SAFE.left + half, x));
  const moving = (t: number) => t >= from - 0.5 && t < from + IN + 0.5;
  const render = (t: number) => {
    const e = outQuart(clamp((t - from) / IN));
    const out = clamp((t - (to - OUT)) / OUT);
    return (
      <div
        style={{
          position: 'absolute',
          left: cx,
          top: y,
          transform: `translate(-50%, -50%) translateX(${(1 - e) * -26}px)`,
          opacity: e * (1 - out),
          padding: '9px 22px 11px',
          borderRadius: 999,
          background: 'rgba(8,18,44,0.58)',
          boxShadow: '0 4px 18px rgba(6,16,40,0.28)',
          fontFamily: SF,
          fontSize: 38,
          fontWeight: 620,
          letterSpacing: '-0.01em',
          color: '#FFFFFF',
          whiteSpace: 'nowrap',
          lineHeight: 1,
        }}
      >
        {text}
      </div>
    );
  };
  return <Shutter render={render} moving={moving} />;
};

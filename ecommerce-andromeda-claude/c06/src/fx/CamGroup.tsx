import React from 'react';
import {useCurrentFrame} from 'remotion';
import {hash} from '../lib/anim';
import {useScale, useT} from '../lib/time';
import {Cam, camCss, camDelta} from './camera';
import {GLITCHES, useCamAt, useVariant, whipAt} from './plan';

// ───────── Grupo de cámara ─────────
// Metraje + efectos anclados al metraje se mueven juntos (mismo contexto de apilado, así que
// sus modos de fusión siguen mezclándose con el vídeo). Si la cámara se mueve deprisa dentro
// del obturador (180° del fotograma de salida), el grupo se dibuja en 8 submuestras
// acumuladas: desenfoque de movimiento real, no gaussiano. El barrido añade desenfoque
// horizontal (filtro SVG) y el fallo «meta» repite el grupo en franjas desplazadas.

const Layer: React.FC<{cam: Cam; children: React.ReactNode; style?: React.CSSProperties}> = ({cam, children, style}) => (
  <div style={{position: 'absolute', inset: 0, transformOrigin: '0 0', transform: camCss(cam), ...style}}>{children}</div>
);

export const CamGroup: React.FC<{children: () => React.ReactNode}> = ({children}) => {
  const t = useT();
  const span = 0.5 / useScale();
  const camAt = useCamAt();
  const v = useVariant();
  const id = useCurrentFrame();
  const c = camAt(t);
  const moving = camDelta(camAt(t - span / 2), camAt(t + span / 2)) > 1.5;

  let body: React.ReactNode;
  if (moving) {
    const N = 8;
    body = (
      <div style={{position: 'absolute', inset: 0, isolation: 'isolate'}}>
        {Array.from({length: N}, (_, k) => (
          <div key={k} style={{position: 'absolute', inset: 0, opacity: 1 / N, mixBlendMode: 'plus-lighter'}}>
            <Layer cam={camAt(t + ((k + 0.5) / N - 0.5) * span)}>{children()}</Layer>
          </div>
        ))}
      </div>
    );
  } else {
    body = <Layer cam={c}>{children()}</Layer>;
  }

  // Fallo «meta»: 4 franjas del mismo grupo desplazadas en x, con un velo azul claro.
  const g = GLITCHES.find((e) => t >= e.at && t < e.at + e.frames);
  const glitch = g
    ? [0, 1, 2, 3].map((k) => {
        const n = Math.floor(t) * 7 + k;
        // Franjas solo por encima de la pantalla de la maquinita (y < 900 en el plano 13).
        const y0 = Math.round(150 + hash(n) * 560);
        const h = Math.round(40 + hash(n + 3) * 150);
        const dx = Math.round((hash(n + 5) - 0.5) * 140);
        return (
          <div key={`g${k}`} style={{position: 'absolute', inset: 0, clipPath: `inset(${y0}px 0 ${Math.max(0, 1920 - y0 - h)}px 0)`, transform: `translateX(${dx}px)`}}>
            <Layer cam={c}>{children()}</Layer>
            <div style={{position: 'absolute', inset: 0, background: 'rgba(169,205,255,0.22)', mixBlendMode: 'screen'}} />
          </div>
        );
      })
    : null;

  const wb = whipAt(v, t);
  if (wb > 0.5) {
    const fid = `whip-${id}`;
    return (
      <>
        <svg width={0} height={0} style={{position: 'absolute'}}>
          <filter id={fid} x="-5%" y="0" width="110%" height="100%" colorInterpolationFilters="sRGB">
            <feGaussianBlur stdDeviation={`${wb} 0`} edgeMode="duplicate" />
          </filter>
        </svg>
        <div style={{position: 'absolute', inset: 0, filter: `url(#${fid})`}}>
          {body}
          {glitch}
        </div>
      </>
    );
  }
  return (
    <>
      {body}
      {glitch}
    </>
  );
};

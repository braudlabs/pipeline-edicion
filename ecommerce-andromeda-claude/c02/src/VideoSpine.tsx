import React from 'react';
import {OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import timeline from './data/timeline.json';

// Montaje bloqueado: orden, IN/OUT exclusivos y offset del ticket (0,5 s = 12 f) del CSV.
// Vídeo mudo: el audio nativo va por pistas separadas (AudioTracks) para no duplicar voces.
// Gag de la sudadera en blanco y negro (Ale): desde «y con la sudadera» (f691) hasta
// «Vengo a hablarte» (f739, exclusivo). Corte seco de color, sin rampa.
export const BW_GAG: [number, number] = [691, 739];

export const VideoSpine: React.FC = () => {
  const frame = useCurrentFrame();
  const bw = frame >= BW_GAG[0] && frame < BW_GAG[1];
  return (
  <div style={{position: 'absolute', inset: 0, filter: bw ? 'grayscale(1) contrast(1.08) brightness(1.02)' : undefined}}>
    {timeline.scenes.map((s) => (
      <Sequence key={s.id} name={`${s.id} · ${s.status}`} from={s.from} durationInFrames={s.dur} layout="none">
        <OffthreadVideo
          src={staticFile(s.asset)}
          trimBefore={s.srcIn}
          muted
          style={{position: 'absolute', inset: 0, width: 1080, height: 1920, objectFit: 'cover'}}
        />
      </Sequence>
    ))}
  </div>
  );
};

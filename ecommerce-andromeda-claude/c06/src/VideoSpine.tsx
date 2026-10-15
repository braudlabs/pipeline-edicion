import React from 'react';
import {OffthreadVideo, Sequence, staticFile} from 'remotion';
import {useScale, useT} from './lib/time';
import timeline from './data/timeline.json';

// Montaje bloqueado: orden, IN/OUT exclusivos y offset del ticket (0,5 s = 12 f) del CSV.
// Vídeo mudo: el audio nativo va por pistas separadas (AudioTracks) para no duplicar voces.
// Gag de la sudadera en blanco y negro (Ale): desde «y con la sudadera» (f691) hasta
// «Vengo a hablarte» (f739, exclusivo). Corte seco de color, sin rampa.
export const BW_GAG: [number, number] = [691, 739];

export const VideoSpine: React.FC<{filter?: string; clip?: string}> = ({filter, clip}) => {
  const frame = useT();
  const k = useScale();
  const bw = frame >= BW_GAG[0] && frame < BW_GAG[1];
  return (
  <div style={{position: 'absolute', inset: 0, clipPath: clip, filter: [bw ? 'grayscale(1) contrast(1.08) brightness(1.02)' : '', filter ?? ''].join(' ').trim() || undefined}}>
    {timeline.scenes.map((s) => {
      // Escala 1 y 6 son exactas. A 60 fps (×2,5) los cortes de fotograma impar caen en medio
      // fotograma: se redondea el inicio y el final de cada plano, así que siguen contiguos.
      const from = Math.round(s.from * k);
      const end = Math.round((s.from + s.dur) * k);
      return (
        <Sequence key={s.id} name={`${s.id} · ${s.status}`} from={from} durationInFrames={end - from} layout="none">
          <OffthreadVideo
            src={staticFile(s.asset)}
            trimBefore={Math.round(s.srcIn * k)}
            muted
            style={{position: 'absolute', inset: 0, width: 1080, height: 1920, objectFit: 'cover'}}
          />
        </Sequence>
      );
    })}
  </div>
  );
};

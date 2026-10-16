import React from 'react';
import {OffthreadVideo, Sequence, staticFile} from 'remotion';
import {FPS} from './lib/motion';

/**
 * Clip real que empieza a reproducirse cuando entra en cuadro (t0, en segundos de la película).
 * Sin la Sequence, un OffthreadVideo usa el fotograma absoluto: un clip de 7 s que aparece en el
 * segundo 44 se quedaría congelado en su último fotograma.
 * `crop` amplía el plano z veces anclado en (fx, fy) ∈ [0, 1]: así los planos del anuncio de la
 * maquinita se encuadran hacia la máquina y dejan fuera la sudadera vetada.
 */
export type ClipCrop = {z: number; fx: number; fy: number};
export const Clip: React.FC<{id: string; t0: number; offset?: number; rate?: number; crop?: ClipCrop; style?: React.CSSProperties}> = (
  {id, t0, offset = 0, rate = 1, crop, style}) => {
  const z = crop?.z ?? 1, fx = crop?.fx ?? 0.5, fy = crop?.fy ?? 0.5;
  return (
    <Sequence from={Math.round(t0 * FPS)} layout="none">
      <OffthreadVideo src={staticFile(`proxies/${id}.mp4`)} muted playbackRate={rate} startFrom={Math.round(offset * FPS)}
        style={{position: 'absolute', left: `${-(z - 1) * fx * 100}%`, top: `${-(z - 1) * fy * 100}%`, width: `${z * 100}%`, height: `${z * 100}%`,
          objectFit: 'cover', ...style}} />
    </Sequence>
  );
};

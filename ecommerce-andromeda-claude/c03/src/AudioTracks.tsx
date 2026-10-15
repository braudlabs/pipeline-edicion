import React from 'react';
import {Audio, Sequence, staticFile} from 'remotion';
import {useScale} from './lib/time';
import audio from './data/audio.json';

export const AudioTracks: React.FC<{only?: string[]}> = ({only}) => {
  const k = useScale();
  return (
  <>
    {audio.tracks
      .filter((t) => t.src && t.enabled !== false && (!only || only.includes(t.id)))
      .map((t) => (
        <Sequence key={t.id} name={`audio · ${t.id}`} from={t.from * k} layout="none">
          <Audio src={staticFile(t.src as string)} volume={t.gain} />
        </Sequence>
      ))}
  </>
  );
};

import React from 'react';
import {Audio, Sequence, staticFile} from 'remotion';
import audio from './data/audio.json';

export const AudioTracks: React.FC<{only?: string[]}> = ({only}) => (
  <>
    {audio.tracks
      .filter((t) => t.src && t.enabled !== false && (!only || only.includes(t.id)))
      .map((t) => (
        <Sequence key={t.id} name={`audio · ${t.id}`} from={t.from} layout="none">
          <Audio src={staticFile(t.src as string)} volume={t.gain} />
        </Sequence>
      ))}
  </>
);

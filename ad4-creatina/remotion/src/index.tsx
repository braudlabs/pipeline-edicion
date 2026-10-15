import React from 'react';
import {AbsoluteFill, Composition, OffthreadVideo, Sequence, registerRoot, staticFile} from 'remotion';
import t from './timeline.json';

/* Montaje base: solo imagen. La voz va en la mezcla aparte y los gráficos en AE. */
const Montaje: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: '#000'}}>
    {t.video.map((s, i) => (
      <Sequence key={i} from={s.from} durationInFrames={s.duration}>
        <OffthreadVideo
          src={staticFile(s.src)}
          trimBefore={s.sourceFrame}
          muted
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      </Sequence>
    ))}
  </AbsoluteFill>
);

registerRoot(() => (
  <Composition id="Montaje-Creatina" component={Montaje}
    width={1080} height={1920} fps={t.fps} durationInFrames={t.duration} />
));

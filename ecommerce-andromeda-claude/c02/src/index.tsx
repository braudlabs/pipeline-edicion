import React from 'react';
import {AbsoluteFill, Composition, registerRoot} from 'remotion';
import {AudioTracks} from './AudioTracks';
import {HookVariant} from './captions/Hook';
import {Film} from './Film';
import {Fonts} from './lib/Fonts';
import {VideoSpine} from './VideoSpine';

// Estudio de alternativas del bloque protagonista (hook). Solo fotogramas de diseño.
const HookStudy: React.FC<{variant: string}> = ({variant}) => (
  <AbsoluteFill style={{background: '#14262e'}}>
    <Fonts />
    <VideoSpine />
    <HookVariant variant={variant} />
    <AudioTracks only={['narrador', 'hook-nativo']} />
  </AbsoluteFill>
);

registerRoot(() => (
  <>
    <Composition id="AndromedaC02" component={Film} durationInFrames={920} fps={24} width={1080} height={1920} />
    <Composition id="HookStudy" component={HookStudy} defaultProps={{variant: 'A'}} durationInFrames={130} fps={24} width={1080} height={1920} />
  </>
));

import React from 'react';
import {AbsoluteFill, Composition, registerRoot, useCurrentFrame} from 'remotion';
import {Chapters} from './Chapters';
import {Sound} from './Sound';
import {Stage} from './Stage';
import {FontsGate} from './lib/Fonts';
import {FPS, H, W} from './lib/motion';
import {IDEA_END, Idea} from './scenes/Idea';
import {Opening} from './scenes/Opening';
import {Process} from './scenes/Process';
import {Quality} from './scenes/Quality';
import {Edit} from './scenes/Edit';
import {Meta} from './scenes/Meta';
import {FILM_END, Outro} from './scenes/Outro';

// Demo SaaS de BRAUD Studio · 1920×1080 a 60 fps, con el sistema visual del Avance 04
// (la landing de BRAUD tras «se ve muy IA, hazlo más pro»; Ale: «este estilo mucho mejor»).
// Avance 05: bloques 1–13. Avance 06: la película entera con el caso de la maquinita (Andrómeda).
const AVANCE05_END = 83.95;

const Film: React.FC<{duration: number}> = ({duration}) => {
  const t = useCurrentFrame() / FPS;
  return (
    <FontsGate>
      <Stage>
        <Opening t={t} />
        <Idea t={t} />
        <Process t={t} />
        <Quality t={t} />
        <Edit t={t} />
        <Meta t={t} />
        <Outro t={t} />
        <Chapters t={t} />
      </Stage>
      <AbsoluteFill style={{pointerEvents: 'none'}} />
      <Sound duration={duration} />
    </FontsGate>
  );
};

registerRoot(() => (
  <>
    <Composition id="Avance04" component={Film} defaultProps={{duration: IDEA_END}} durationInFrames={Math.round(IDEA_END * FPS)} fps={FPS} width={W} height={H} />
    <Composition id="Avance05" component={Film} defaultProps={{duration: AVANCE05_END}} durationInFrames={Math.round(AVANCE05_END * FPS)} fps={FPS} width={W} height={H} />
    <Composition id="Avance06" component={Film} defaultProps={{duration: FILM_END}} durationInFrames={Math.round(FILM_END * FPS)} fps={FPS} width={W} height={H} />
  </>
));

import React from 'react';
import {AbsoluteFill, Composition, registerRoot, useCurrentFrame} from 'remotion';
import {Sound} from './Sound';
import {Stage} from './Stage';
import {FontsGate} from './lib/Fonts';
import {FPS, H, W} from './lib/motion';
import {IDEA_END, Idea} from './scenes/Idea';
import {Opening} from './scenes/Opening';

// Demo SaaS de BRAUD Studio · 1920×1080 a 60 fps. Avance 04 (bloques 1–5): sistema visual de la landing de BRAUD tras «se ve muy IA, hazlo más pro».
const Film: React.FC<{duration: number}> = ({duration}) => {
  const t = useCurrentFrame() / FPS;
  return (
    <FontsGate>
      <Stage>
        <Opening t={t} />
        <Idea t={t} />
      </Stage>
      <AbsoluteFill style={{pointerEvents: 'none'}} />
      <Sound duration={duration} />
    </FontsGate>
  );
};

registerRoot(() => (
  <>
    <Composition id="Avance04" component={Film} defaultProps={{duration: IDEA_END}} durationInFrames={Math.round(IDEA_END * FPS)} fps={FPS} width={W} height={H} />
  </>
));

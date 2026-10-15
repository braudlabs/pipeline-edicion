import React from 'react';
import {AbsoluteFill} from 'remotion';
import {AudioTracks} from './AudioTracks';
import {HookA} from './captions/Hook';
import {Scene01} from './captions/Scene01';
import {Scene02} from './captions/Scene02';
import {Scene03, Scene03b} from './captions/Scene03';
import {Scene04} from './captions/Scene04';
import {Scene05} from './captions/Scene05';
import {Scene06} from './captions/Scene06';
import {Scene07} from './captions/Scene07';
import {Scene08} from './captions/Scene08';
import {Scene09} from './captions/Scene09';
import {Scene10} from './captions/Scene10';
import {Scene11} from './captions/Scene11';
import {Scene12} from './captions/Scene12';
import {Scene13} from './captions/Scene13';
import {Scene14, Scene15} from './captions/Scene14';
import {CamGroup} from './fx/CamGroup';
import {Footage, FootageFx, ScreenFx} from './fx/Moments';
import {Variant, VariantId} from './fx/plan';
import {FontsGate} from './lib/Fonts';

// C06 · Ecommerce Andrómeda (Claude). Sobre C05 (feedback de C04 aplicado), Ale pidió «otra
// versión con más efectos aún, un upgrade infernal». Montaje, audio, música y rótulos son los
// de C05; C06 añade la cámara digital (fx/plan.ts) y la capa de efectos (fx/Moments.tsx).
// Capas: cámara { metraje + efectos anclados al metraje } → efectos de pantalla → rótulos.
// Los rótulos libres no se mueven con la cámara (margen seguro de Meta); los anclados al
// metraje (persiana, tarjeta) y las máscaras de los textos detrás del sujeto sí la siguen.
export const Film: React.FC<{audit?: boolean; variant?: VariantId}> = ({audit, variant = 'A'}) => (
  <Variant.Provider value={variant}>
    <AbsoluteFill style={{background: audit ? '#000' : '#14262e'}}>
      {/* audit: solo rótulos sobre negro, para medir sus márgenes reales (study/audit-margins.json) */}
      {audit ? null : (
        <CamGroup>
          {() => (
            <>
              <Footage />
              <FootageFx />
            </>
          )}
        </CamGroup>
      )}
      {audit ? null : <ScreenFx />}
      <FontsGate>
        <HookA />
        <Scene01 />
        <Scene02 />
        <Scene03 />
        <Scene03b />
        <Scene04 />
        <Scene05 />
        <Scene06 />
        <Scene07 />
        <Scene08 />
        <Scene09 />
        <Scene10 />
        <Scene11 />
        <Scene12 />
        <Scene13 />
        <Scene14 />
        <Scene15 />
      </FontsGate>
      {audit ? null : <AudioTracks />}
    </AbsoluteFill>
  </Variant.Provider>
);

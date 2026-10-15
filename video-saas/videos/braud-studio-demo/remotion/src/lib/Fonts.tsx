import React, {useEffect, useState} from 'react';
import {cancelRender, continueRender, delayRender, staticFile} from 'remotion';

// SF Pro (decisión de Ale) para titulares y SF Mono para las etiquetas, como en la landing de BRAUD.
export const SF = "'SFV', 'SFD', -apple-system, sans-serif";
export const MONO = "'SFM', ui-monospace, Menlo, monospace";
// La interfaz de Studio usa -apple-system: en este Mac es la misma SF Pro.
export const UI_FONT = "-apple-system, system-ui, 'Segoe UI', sans-serif";

export const FontsGate: React.FC<{children: React.ReactNode}> = ({children}) => {
  const [ready, setReady] = useState(false);
  const [handle] = useState(() => delayRender('Fuentes SF Pro'));
  useEffect(() => {
    const faces = [
      new FontFace('SFV', `url("${staticFile('fonts/SFNS.ttf')}")`, {weight: '1 1000', stretch: '30% 150%'}),
      new FontFace('SFD', `url("${staticFile('fonts/SFProDisplay-Bold.otf')}")`, {weight: '700'}),
      new FontFace('SFD', `url("${staticFile('fonts/SFProDisplay-Regular.otf')}")`, {weight: '400'}),
      new FontFace('SFM', `url("${staticFile('fonts/SFNSMono.ttf')}")`, {weight: '1 1000'}),
    ];
    Promise.all(faces.map((x) => x.load()))
      .then((loaded) => {
        loaded.forEach((x) => document.fonts.add(x));
        return document.fonts.ready;
      })
      .then(() => {
        setReady(true);
        continueRender(handle);
      })
      .catch((e) => cancelRender(e));
  }, [handle]);
  return ready ? <>{children}</> : null;
};

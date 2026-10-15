import React, {useEffect, useState} from 'react';
import {cancelRender, continueRender, delayRender, staticFile} from 'remotion';

// SF Pro variable del sistema (ejes wght 1–1000, wdth 30–150, opsz 17–96) y SF Pro
// Display estática como respaldo. Decisión de Ale: SF Pro se mantiene.
export const SF = "'SFV', 'SFD', -apple-system, sans-serif";
/** Serif de Apple, solo para «tradicional» (contraste semántico propuesto, no preferencia de Ale). */
export const NY = "'NYV', 'SFV', serif";

/**
 * Carga las fuentes y solo entonces monta los hijos: las líneas que se ajustan al ancho
 * miden con la fuente real (nunca con la de respaldo).
 */
export const FontsGate: React.FC<{children: React.ReactNode}> = ({children}) => {
  const [ready, setReady] = useState(false);
  return (
    <>
      <Fonts onReady={() => setReady(true)} />
      {ready ? children : null}
    </>
  );
};

export const Fonts: React.FC<{onReady?: () => void}> = ({onReady}) => {
  const [handle] = useState(() => delayRender('Fuentes SF Pro'));
  useEffect(() => {
    const faces = [
      new FontFace('SFV', `url("${staticFile('assets/fonts/SFNS.ttf')}")`, {weight: '1 1000', stretch: '30% 150%'}),
      new FontFace('NYV', `url("${staticFile('assets/fonts/NewYork.ttf')}")`, {weight: '1 1000'}),
      new FontFace('SFD', `url("${staticFile('assets/fonts/SFProDisplay-Bold.otf')}")`, {weight: '700'}),
      new FontFace('SFD', `url("${staticFile('assets/fonts/SFProDisplay-Regular.otf')}")`, {weight: '400'}),
    ];
    Promise.all(faces.map((f) => f.load()))
      .then((loaded) => {
        loaded.forEach((f) => document.fonts.add(f));
        return document.fonts.ready;
      })
      .then(() => {
        onReady?.();
        continueRender(handle);
      })
      .catch((e) => cancelRender(e));
  }, [handle]);
  return null;
};

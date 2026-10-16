import React from 'react';
import {Progress} from './system';
import {prog, ease} from './lib/motion';

// Barra de proceso global (V05): un tramo por paso, sincronizado con la voz. Se oculta en el
// escaparate de calidad (bloque 10) y en «Pero aquí no se acaba», y vuelve para Meta.
// Pasos: 0 Idea · 1 Marca · 2 Intención · 3 Guion · 4 Casting · 5 Escenas · 6 Montaje · 7 Meta
const SPANS: [number, number, number][] = [
  [0, 16.86, 21.8], [1, 21.8, 30.45], [2, 30.45, 36.75], [3, 36.75, 42.5], [4, 42.5, 46.5],
  [5, 46.5, 72.9], [6, 72.9, 82.4], [7, 84.0, 104.5],
];
const VISIBLE: [number, number][] = [[16.21, 51.95], [72.95, 82.45], [84.1, 104.45]];

export const Chapters: React.FC<{t: number}> = ({t}) => {
  const span = SPANS.find(([, a, b]) => t >= a && t < b) ?? (t < SPANS[0][1] ? SPANS[0] : SPANS[SPANS.length - 1]);
  const [step, a, b] = span;
  const k = prog(t, a, b, ease.linear);
  return (
    <>
      {VISIBLE.map(([t0, out]) => <Progress key={t0} t={t} t0={t0} out={out} step={step} stepK={k} />)}
    </>
  );
};

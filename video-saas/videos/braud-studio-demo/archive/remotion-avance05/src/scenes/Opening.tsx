import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile} from 'remotion';
import {COLORS} from '../Stage';
import {Headline, Mono, Pill, cardStyle} from '../system';
import {UI_H, UI_W} from '../UIPlane';
import {at, clamp, ease, mix, prog} from '../lib/motion';

// Bloque 1 · V04 (tras «se ve muy IA, hazlo más pro»): el hero de la landing de BRAUD.
// Titular en degradado sobre un carrusel de anuncios reales hechos con el sistema (Creatina, Sérum,
// Moda, PapiCat). El carrusel acelera con «cada semana», se para con «ritmo de mes» y, con «se parecen»,
// todas las tarjetas acaban siendo la misma. Nada dibujado, nada que brille.

const T = {
  desde: at(1, 'Desde'), meta: at(1, 'Meta'), nueva: at(1, 'nueva'), cada: at(1, 'cada'),
  tu: at(1, 'Tu'), ritmo: at(1, 'ritmo'), y: at(1, 'Y'), anuncios: at(1, 'anuncios'), parecen: at(1, 'parecen'),
};
export const OPENING_END = 9.22; // «Esto es BRAUD Studio»
const ENTER = 0.02, FAST0 = T.cada - 0.08, FAST1 = 3.3, STOP = 4.0, BACK = 6.2, COLLAPSE = 8.62;

const CARDS = ['CR-A', 'SERUM-ad', 'MO-1', 'PAPICAT-ad', 'SE-1', 'MO-3', 'CR-M1', 'MO-5', 'CR-final', 'SE-2', 'MO-2', 'CR-C'];
const CW = 230, CH = Math.round(CW * 16 / 9), GAP = 26, STEP = CW + GAP, LOOP = CARDS.length * STEP, CY = 770;

// Velocidad del carrusel (px/s) e integración determinista de su desplazamiento.
const speed = (t: number) => {
  if (t < ENTER) return 0;
  if (t < FAST0) return 70;
  if (t < FAST0 + 0.4) return mix(70, 1150, ease.in(clamp((t - FAST0) / 0.4)));
  if (t < FAST1) return 1150;
  if (t < STOP) return mix(1150, 0, ease.out(clamp((t - FAST1) / (STOP - FAST1))));
  if (t < BACK) return 6;
  if (t < BACK + 0.3) return mix(6, 300, ease.out(clamp((t - BACK) / 0.3)));
  return 300;
};
const offset = (t: number) => {
  let x = 0;
  for (let s = ENTER; s < t; s += 1 / 120) x += speed(s) / 120;
  return x;
};
const X_FAST0 = offset(FAST0);
const heroIndex = (() => { // la tarjeta que queda en el centro al pararse
  const x = offset(STOP);
  let best = 0, bd = 1e9;
  CARDS.forEach((_, i) => {
    const cx = ((((i * STEP - x) % LOOP) + LOOP) % LOOP) - LOOP / 2 + 960 + STEP / 2;
    if (Math.abs(cx - 960) < bd) { bd = Math.abs(cx - 960); best = i; }
  });
  return best;
})();

const Carousel: React.FC<{t: number}> = ({t}) => {
  if (t < ENTER - 0.05 || t > OPENING_END) return null;
  const x = offset(t);
  const slow = prog(t, STOP - 0.35, STOP + 0.2) * (1 - prog(t, BACK - 0.1, BACK + 0.2));
  const coll = prog(t, COLLAPSE, OPENING_END - 0.06, ease.in);
  return (
    <div style={{position: 'absolute', inset: 0, WebkitMaskImage: 'linear-gradient(90deg, transparent 0%, #000 14%, #000 86%, transparent 100%)'}}>
      {CARDS.map((id, i) => {
        const cx = ((((i * STEP - x) % LOOP) + LOOP) % LOOP) - LOOP / 2 + 960 + STEP / 2;
        if (cx < -CW || cx > 1920 + CW) return null;
        // entrada desde el primer fotograma (Avance 03 → 04: el primer segundo no puede ser negro)
        const k = prog(t, ENTER + Math.abs(cx - 960) / 3000, ENTER + 0.45 + Math.abs(cx - 960) / 3000, ease.out);
        const isHero = i === heroIndex;
        const clone = clamp((t - (T.parecen - 0.05)) * 2.4 - Math.abs(cx - 960) / 650);
        const fx = mix(cx, 960, coll), sc = mix(isHero ? 1 + 0.06 * slow : 1, 0.55, coll);
        const op = k * (isHero ? 1 : 1 - 0.65 * slow) * (1 - coll);
        return (
          <div key={id} style={{...cardStyle(CW, CH), position: 'absolute', left: fx - CW / 2, top: CY - CH / 2 + (1 - k) * 60, opacity: op, transform: `scale(${sc})`}}>
            <OffthreadVideo src={staticFile(`proxies/${id}.mp4`)} muted playbackRate={t > STOP && t < BACK ? 0.25 : 1}
              style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}} />
            {clone > 0 ? <Img src={staticFile('stills/same.jpg')} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', opacity: clone,
              filter: 'grayscale(1) brightness(0.75)'}} /> : null}
            {isHero && slow > 0 ? (
              <div style={{position: 'absolute', left: 16, right: 16, bottom: 16, height: 3, borderRadius: 2, background: 'rgba(255,255,255,0.25)', opacity: slow}}>
                <div style={{width: `${mix(3, 14, clamp((t - STOP) / (BACK - STOP)))}%`, height: '100%', borderRadius: 2, background: COLORS.ink}} />
              </div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
};

/** La tarjeta central se convierte en la ventana de Studio (objeto que conecta con el bloque 2). */
const ToStudio: React.FC<{t: number}> = ({t}) => {
  if (t < COLLAPSE + 0.2 || t > OPENING_END + 0.02) return null;
  const k = prog(t, COLLAPSE + 0.2, OPENING_END, ease.inOut);
  const w = mix(CW * 0.55, UI_W * 0.82, k), h = mix(CH * 0.55, UI_H * 0.82, k);
  return (
    <div style={{position: 'absolute', left: 960 - w / 2, top: mix(CY, 560, k) - h / 2, width: w, height: h, borderRadius: mix(20, 21, k), overflow: 'hidden',
      boxShadow: '0 40px 120px rgba(0,0,0,0.7), inset 0 0 0 1px rgba(255,255,255,0.1)', opacity: prog(t, COLLAPSE + 0.2, COLLAPSE + 0.35)}}>
      <Img src={staticFile('snaps/home.png')} style={{width: '100%', height: '100%', objectFit: 'cover', opacity: k}} />
    </div>
  );
};

export const Opening: React.FC<{t: number}> = ({t}) => {
  if (t > OPENING_END + 0.02) return null;
  const weeks = t > FAST0 && t < STOP ? Math.max(1, Math.min(52, 1 + Math.floor((offset(t) - X_FAST0) / STEP))) : 1;
  return (
    <AbsoluteFill>
      <Carousel t={t} />
      <ToStudio t={t} />
      <Pill t={t} t0={T.desde} out={STOP - 0.15} parts={['Meta Ads', 'Andrómeda']} y={148} />
      <Headline t={t} out={STOP - 0.15} y={335} size={112} lines={[{text: 'Meta pide creatividad', t: T.meta}, {text: 'nueva cada semana.', t: T.nueva + 0.1}]} />
      <Mono t={t} t0={FAST0} out={STOP - 0.15} y={498} text={`Semana ${String(weeks).padStart(2, '0')}`} color={COLORS.gray} />
      <Pill t={t} t0={T.tu} out={BACK - 0.12} parts={['Tu producción']} y={148} />
      <Headline t={t} out={BACK - 0.12} y={335} size={112} gray={0.3} lines={[{text: 'Tu producción,', t: T.tu + 0.02}, {text: 'a ritmo de mes.', t: T.ritmo - 0.15}]} />
      <Pill t={t} t0={T.y} out={COLLAPSE - 0.05} parts={['Tu sector']} y={148} />
      <Headline t={t} out={COLLAPSE - 0.05} y={335} size={112} lines={[{text: 'Los de tu sector', t: T.anuncios}, {text: 'se parecen cada vez más.', t: T.parecen - 0.1}]} />
    </AbsoluteFill>
  );
};
